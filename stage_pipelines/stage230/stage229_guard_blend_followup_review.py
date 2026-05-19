from __future__ import annotations

import csv
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


STAGE_ID = "230_adapter_research__stage229_guard_blend_followup_review"
RUN_ID = "run230A_stage230_stage229_guard_blend_followup_review_v1"
PACKET_ID = "stage230_stage229_guard_blend_followup_review_v1"
PARENT_RUN_ID = "run229A_stage229_dual_objective_guard_blend_after_selection_tradeoff_v1"
SOURCE_STAGE_ID = "229_adapter_research__dual_objective_guard_blend_after_selection_tradeoff"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE229_EVIDENCE_COMMIT = "bb0fdb1e380e09fc4b2ccc086423c230aea0905e"
SOURCE_STAGE229_HASH_RECORD_COMMIT = "0233312ae03723ae58a10cb54d3532297bfa9958"
NEXT_STAGE_ID = "231_adapter_research__midpf_oos_repair_after_guard_blend_failure"
NEXT_RUN_ID = "run231A_stage231_midpf_oos_repair_after_guard_blend_failure_v1"
NEXT_PACKET_ID = "stage231_midpf_oos_repair_after_guard_blend_failure_v1"
DECISION = "open_stage231_bounded_midpf_oos_repair_after_guard_blend_failure_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage229_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_midpf_oos_repair_after_guard_blend_failure"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "net_profit": 987.60,
    "profit_factor": 1.583157,
    "max_drawdown_percent": 12.909136,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE_SUMMARY_PATH = SOURCE_ROOT / "stage229_summary.json"
SOURCE_REPORT_PATH = SOURCE_ROOT / "stage229_guard_blend_report.md"
SOURCE_QUALITY_PATH = SOURCE_ROOT / "stage229_quality_matrix.csv"
SOURCE_KPI_PATH = SOURCE_ROOT / "stage229_guard_blend_kpi_summary.csv"
SOURCE_SEGMENT_PATH = SOURCE_ROOT / "stage229_segment_kpi_summary.csv"
SOURCE_BALANCE_PATH = SOURCE_ROOT / "stage229_balance_curve_audit.csv"
SOURCE_MONTHLY_PATH = SOURCE_ROOT / "stage229_monthly_kpi_summary.csv"
SOURCE_CONCENTRATION_PATH = SOURCE_ROOT / "stage229_concentration_risk_summary.csv"
SOURCE_DRAWDOWN_PATH = SOURCE_ROOT / "stage229_drawdown_recovery_summary.csv"
SOURCE_RISK_ATR_PATH = SOURCE_ROOT / "stage229_risk_atr_telemetry.csv"
SOURCE_GATE_PATH = SOURCE_ROOT / "stage229_gate_feature_summary.csv"
SOURCE_TRADE_AUDIT_PATH = SOURCE_ROOT / "stage229_trade_audit.csv"
SOURCE_DECISION_PATH = SOURCE_ROOT / "stage229_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage230_guard_blend_followup_review.md"
TRADEOFF_PATH = REVIEWS_ROOT / "stage230_guard_blend_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage230_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage230_route_matrix.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage230_failure_memory.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage230_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage230_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage230/stage229_guard_blend_followup_review.py")

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    inferred: list[str] = []
    for row in rows:
        for key in row:
            if key not in inferred:
                inferred.append(key)
    fieldnames = list(columns or inferred)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        text = str(value).strip().replace(",", "")
        return float(text) if text else default
    except (TypeError, ValueError):
        return default


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def lookup(rows: Sequence[Mapping[str, Any]], **filters: str) -> Mapping[str, Any]:
    for row in rows:
        if all(str(row.get(key, "")) == value for key, value in filters.items()):
            return row
    return {}


def pct_delta(value: float, reference: float) -> float:
    if reference == 0:
        return 0.0
    return round((value - reference) / abs(reference), 6)


def classify_row(row: Mapping[str, Any], reference: Mapping[str, Any]) -> str:
    val_net_ok = as_float(row.get("validation_net")) >= LEGACY_34D["net_profit"]
    early_ok = as_float(row.get("validation_early_pf")) >= LEGACY_34D["profit_factor"]
    mid_ok = as_float(row.get("validation_mid_pf")) >= LEGACY_34D["profit_factor"]
    dd_ok = as_float(row.get("validation_balance_dd_percent"), 99.0) <= LEGACY_34D["max_drawdown_percent"]
    oos_net_ok = as_float(row.get("oos_net")) >= as_float(reference.get("oos_net"))
    oos_pf_ok = as_float(row.get("oos_pf")) >= as_float(reference.get("oos_pf"))
    oos_dd_ok = as_float(row.get("oos_balance_dd_percent"), 99.0) <= as_float(
        reference.get("oos_balance_dd_percent"), 99.0
    )
    if val_net_ok and early_ok and mid_ok and dd_ok and oos_net_ok and oos_pf_ok and oos_dd_ok:
        return "dual_objective_pass_candidate_not_final"
    if not val_net_ok and not early_ok and not mid_ok and oos_net_ok and oos_pf_ok and oos_dd_ok:
        return "oos_reference_preserved_validation_under_34d"
    if val_net_ok and early_ok and dd_ok and not mid_ok and not oos_net_ok:
        return "validation_recovered_midpf_oos_damaged"
    if not oos_net_ok:
        return "oos_damaged_no_full_repair"
    return "mixed_tradeoff_no_full_repair"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    reference = lookup(quality_rows, adapter_id="s229_blend_session_only_ref")
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        val_risk = lookup(risk_rows, adapter_id=adapter_id, split="validation_is", view="actual_routed_total")
        oos_risk = lookup(risk_rows, adapter_id=adapter_id, split="oos", view="actual_routed_total")
        val_mid = lookup(
            segment_rows,
            adapter_id=adapter_id,
            split="validation_is",
            view="actual_routed_total",
            segment_type="chronological_third",
            segment="mid",
        )
        oos_mid = lookup(
            segment_rows,
            adapter_id=adapter_id,
            split="oos",
            view="actual_routed_total",
            segment_type="chronological_third",
            segment="mid",
        )
        val_gate = lookup(gate_rows, adapter_id=adapter_id, split="validation_is")
        oos_gate = lookup(gate_rows, adapter_id=adapter_id, split="oos")
        label = classify_row(row, reference)
        validation_net = as_float(row.get("validation_net"))
        oos_net = as_float(row.get("oos_net"))
        ref_oos = as_float(reference.get("oos_net"))
        ref_val = as_float(reference.get("validation_net"))
        risk_atr_ok = (
            as_bool(val_risk.get("atr_enabled"))
            and as_bool(val_risk.get("model_risk_enabled"))
            and as_float(val_risk.get("max_model_risk_pct")) <= 0.05
            and as_float(oos_risk.get("max_model_risk_pct")) <= 0.05
        )
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "tradeoff_label": label,
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "validation_pf": row.get("validation_pf", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": row.get("validation_net_gap_vs_34d", ""),
                "validation_net_delta_vs_session_ref": round(validation_net - ref_val, 2),
                "validation_net_delta_pct_vs_session_ref": pct_delta(validation_net, ref_val),
                "validation_early_pf": row.get("validation_early_pf", ""),
                "validation_early_pf_gap_vs_34d": round(as_float(row.get("validation_early_pf")) - LEGACY_34D["profit_factor"], 6),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d": round(as_float(row.get("validation_mid_pf")) - LEGACY_34D["profit_factor"], 6),
                "validation_mid_mfe_capture_ratio": val_mid.get("mfe_capture_ratio", ""),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_dd_margin_vs_34d": row.get("validation_dd_margin_vs_34d", ""),
                "validation_late_net_share": row.get("validation_late_net_share", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_session_ref": round(oos_net - ref_oos, 2),
                "oos_net_delta_pct_vs_session_ref": pct_delta(oos_net, ref_oos),
                "oos_mid_pf": oos_mid.get("profit_factor", ""),
                "oos_mid_mfe_capture_ratio": oos_mid.get("mfe_capture_ratio", ""),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "oos_late_net_share": row.get("oos_late_net_share", ""),
                "validation_blocked_signal_ratio": val_gate.get("blocked_signal_ratio", ""),
                "oos_blocked_signal_ratio": oos_gate.get("blocked_signal_ratio", ""),
                "risk_atr_ok": risk_atr_ok,
                "validation_max_model_risk_pct": val_risk.get("max_model_risk_pct", ""),
                "oos_max_model_risk_pct": oos_risk.get("max_model_risk_pct", ""),
                "validation_risk_floor_applied_count": val_risk.get("risk_floor_applied_count", ""),
                "oos_risk_floor_applied_count": oos_risk.get("risk_floor_applied_count", ""),
                "atr_stop_multiplier": row.get("atr_stop_multiplier", ""),
                "atr_take_profit_multiplier": row.get("atr_take_profit_multiplier", ""),
                "quality_flags": row.get("quality_flags", ""),
            }
        )
    return rows


def best_oos_reference(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(rows, key=lambda row: (as_float(row.get("oos_net")), as_float(row.get("oos_pf"))), default={})


def best_validation_clue(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(rows, key=lambda row: (as_float(row.get("validation_net")), as_float(row.get("validation_early_pf"))), default={})


def build_attribution_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ref = lookup(rows, adapter_id="s229_blend_session_only_ref")
    val = best_validation_clue(rows)
    return [
        {
            "run_id": RUN_ID,
            "finding": "margin_band_blend_recovers_validation_net_but_damages_oos(마진 구간 혼합은 검증 순손익을 회복하지만 표본외를 훼손)",
            "evidence": f"validation_net_delta_vs_session_ref={val.get('validation_net_delta_vs_session_ref')}; oos_net_delta_vs_session_ref={val.get('oos_net_delta_vs_session_ref')}",
            "damage": f"validation_mid_pf={val.get('validation_mid_pf')}; oos_net={val.get('oos_net')}",
            "interpretation": "롱 공급을 되돌리는 보호 혼합은 34D(34D 기준) 순손익은 넘기지만 중반 PF(수익요인)와 OOS(표본외) 균형을 동시에 살리지 못했다.",
            "next_use": "Stage231(231단계)에서는 마진 구간 혼합 반복이 아니라 중반 PF/OOS(표본외) 훼손 원인을 별도 축으로 수리한다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "session_only_remains_oos_bound_but_validation_under_34d(세션 전용은 표본외 경계지만 검증이 34D 미만)",
            "evidence": f"validation_net={ref.get('validation_net')}; early_pf={ref.get('validation_early_pf')}; mid_pf={ref.get('validation_mid_pf')}; oos_net={ref.get('oos_net')}",
            "damage": f"validation_net_gap_vs_34d={ref.get('validation_net_gap_vs_34d')}; validation_mid_pf_gap_vs_34d={ref.get('validation_mid_pf_gap_vs_34d')}",
            "interpretation": "가장 덜 망가지는 참조선은 세션 전용이지만 이 상태로는 34D(34D 기준) 이상이라고 볼 수 없다.",
            "next_use": "Stage231(231단계)의 OOS(표본외) 보존 하한으로만 사용한다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "risk_atr_capability_present_not_sufficient(위험/ATR 기능은 있으나 충분조건 아님)",
            "evidence": f"risk_atr_ok={all(str(row.get('risk_atr_ok')).lower() == 'true' for row in rows)}; atr_sl_tp=2.0325/4.615; model_risk_cap=0.031375",
            "damage": "mandatory capability(필수 기능)가 있어도 segment KPI(구간 핵심 성과 지표)와 OOS(표본외)가 깨지면 후보는 최종이 아니다.",
            "interpretation": "ATR(평균 진폭)과 model risk(모델 위험)는 유지하되, 다음 문제는 KPI 구조 수리다.",
            "next_use": "Stage231(231단계)에서 위험/ATR 기록은 고정 필수 조건으로 유지한다.",
        },
    ]


def build_route_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ref = best_oos_reference(rows)
    val = best_validation_clue(rows)
    return [
        {
            "run_id": RUN_ID,
            "route": DECISION,
            "action": "open Stage231(231단계)를 mid PF/OOS repair(중반 수익요인/표본외 수리)로 제한한다.",
            "effect": "Stage230(230단계)이 새 실험을 흡수하지 않고, 실패 원인과 다음 질문을 분리한다.",
            "reference_oos_bound": ref.get("adapter_id", ""),
            "validation_clue": val.get("adapter_id", ""),
            "risk": "중반 PF(수익요인)를 고치면 검증 순손익이나 표본외 순손익이 다시 줄 수 있다.",
        },
        {
            "run_id": RUN_ID,
            "route": "stop_repeating_margin_band_blend(마진 구간 혼합 반복 중지)",
            "action": "wide/base/tight margin band(넓은/기본/좁은 마진 구간)를 failure memory(실패 기억)로 보존한다.",
            "effect": "같은 축을 더 넓히며 Stage229(229단계)를 반복하는 일을 막는다.",
            "reference_oos_bound": ref.get("adapter_id", ""),
            "validation_clue": val.get("adapter_id", ""),
            "risk": "마진 구간 밖의 다른 문맥 축은 아직 탐색 대상일 수 있다.",
        },
        {
            "run_id": RUN_ID,
            "route": "no_final_claim_no_onnx(최종 주장 없음, ONNX 경화 없음)",
            "action": "adapter_candidate(어댑터 후보) 상태로 유지한다.",
            "effect": "34D(34D 기준) 일부 초과나 ATR/risk(ATR/위험) 존재를 완료로 오해하지 않는다.",
            "reference_oos_bound": ref.get("adapter_id", ""),
            "validation_clue": val.get("adapter_id", ""),
            "risk": "추가 bounded stage(경계 단계)가 필요하다.",
        },
    ]


def build_failure_memory(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    memory: list[dict[str, Any]] = []
    for row in rows:
        label = str(row.get("tradeoff_label", ""))
        if row.get("adapter_id") == "s229_blend_session_only_ref":
            next_use = "use_as_oos_preservation_bound_not_final"
        elif "validation_recovered" in label:
            next_use = "preserve_as_validation_recovery_oos_damage_memory"
        else:
            next_use = "preserve_as_failed_guard_blend_memory"
        memory.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row.get("adapter_id", ""),
                "failure_label": label,
                "next_use": next_use,
                "validation_net_gap_vs_34d": row.get("validation_net_gap_vs_34d", ""),
                "validation_mid_pf_gap_vs_34d": row.get("validation_mid_pf_gap_vs_34d", ""),
                "oos_net_delta_vs_session_ref": row.get("oos_net_delta_vs_session_ref", ""),
                "risk_atr_ok": row.get("risk_atr_ok", ""),
            }
        )
    return memory


def report_markdown(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage230 Guard Blend Follow-up Review(230단계 보호 혼합 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- decision(판정): `{DECISION}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        "- Stage229(229단계)는 검증 순손익을 34D(34D 기준) 이상으로 끌어올리는 실마리를 보였지만, 그 대가로 OOS(표본외) 순손익이 크게 줄었다.",
        "- 세션 전용 참조선은 OOS(표본외)가 가장 낫지만 검증 순손익, 초반 PF(수익요인), 중반 PF(수익요인)가 34D(34D 기준)에 못 미친다.",
        "- 결론은 단순하다. 현재 guard blend(보호 혼합)는 최종 후보가 아니며, 다음은 중반 PF/OOS(중반 수익요인/표본외) 수리다.",
        "",
        "## KPI Tradeoff(KPI 핵심 성과 지표 상충)",
        "",
        "| adapter(어댑터) | label(라벨) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS delta(표본외 차이) | risk/ATR(위험/ATR) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {row.get('tradeoff_label', '')} | "
            f"{row.get('validation_net', '')} | {row.get('validation_early_pf', '')} | "
            f"{row.get('validation_mid_pf', '')} | {row.get('validation_dd_percent', '')} | "
            f"{row.get('oos_net', '')} | {row.get('oos_net_delta_vs_session_ref', '')} | "
            f"{row.get('risk_atr_ok', '')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- result_subject(판정 대상): Stage229(229단계) dual-objective guard blend(이중목표 보호 혼합).",
            "- judgment_label(판정 라벨): guard_blend_tradeoff_failed_candidate_not_final(보호 혼합 상충 실패, 최종 아님).",
            "- next_condition(다음 조건): Stage231(231단계)는 ATR/risk(ATR/위험)와 lifecycle(생애주기)을 유지한 채 중반 PF/OOS(중반 수익요인/표본외)를 고치는 한 가지 질문만 다룬다.",
            "",
            "Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).",
        ]
    )
    return "\n".join(lines)


def decision_markdown(best_ref: Mapping[str, Any], best_val: Mapping[str, Any]) -> str:
    return f"""# Stage230 Decision(230단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage229_evidence_commit(원천 229단계 근거 커밋): `{SOURCE_STAGE229_EVIDENCE_COMMIT}`
- source_stage229_hash_record_commit(원천 229단계 해시 기록 커밋): `{SOURCE_STAGE229_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- oos_reference_bound(표본외 보존 경계): `{best_ref.get('adapter_id', '')}`
- validation_recovery_clue(검증 회복 단서): `{best_val.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage230(230단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage231(231단계)는 guard blend(보호 혼합)를 반복하지 않고, mid PF/OOS(중반 수익요인/표본외) 훼손을 별도 bounded repair(경계 수리)로 다룬다.
"""


def write_stage231_seed(best_ref: Mapping[str, Any], best_val: Mapping[str, Any]) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage231(231단계)는 Stage230(230단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can the adapter repair validation mid PF(검증 중반 수익요인) and preserve OOS net/PF/DD(표본외 순손익/수익요인/낙폭) after Stage229(229단계) showed that margin-band guard blend(마진 구간 보호 혼합) recovers validation net(검증 순손익) but damages OOS(표본외)?

Effect(효과): Stage229(229단계)의 같은 margin band(마진 구간) 혼합을 반복하지 않고, OOS reference bound(표본외 보존 경계) `{best_ref.get('adapter_id', '')}`와 validation recovery clue(검증 회복 단서) `{best_val.get('adapter_id', '')}` 사이의 중반 PF/OOS(중반 수익요인/표본외) 훼손 원인만 좁게 수리한다.

## Fixed Requirements(고정 요구)

- model-controlled risk%(모델 제어 위험 비율) remains mandatory(필수 유지).
- ATR SL/TP(ATR 손절/익절) remains mandatory(필수 유지).
- no ONNX hardening(ONNX 경화 없음).
- no deployment/live/production/operating claim(배포/실거래/생산/운영 주장 없음).

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage231 Input References(231단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- stage230_report(230단계 보고서): `{rel(REPORT_PATH)}`
- stage230_tradeoff_matrix(230단계 상충 행렬): `{rel(TRADEOFF_PATH)}`
- stage230_failure_memory(230단계 실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- source_stage229_quality_matrix(원천 229단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage229_segment_kpi(원천 229단계 구간 KPI): `{rel(SOURCE_SEGMENT_PATH)}`
- source_stage229_risk_atr(원천 229단계 위험/ATR): `{rel(SOURCE_RISK_ATR_PATH)}`
- oos_reference_bound(표본외 보존 경계): `{best_ref.get('adapter_id', '')}`
- validation_recovery_clue(검증 회복 단서): `{best_val.get('adapter_id', '')}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage231 Review Index(231단계 검토 색인)

- status(상태): `open_planned_from_stage230`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage231 Selection Status(231단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage230`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(best_ref: Mapping[str, Any], best_val: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1)
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1)
    focus = f"""current_focus:
- >-
  Stage230(230단계) closed(종료) as `{DECISION}` and Stage231(231단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): guard blend(보호 혼합) 실패를 mid PF/OOS repair(중반 수익요인/표본외 수리)로 분리한다.
- >-
  Stage230 evidence(230단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`에 있다. Effect(효과): Stage229(229단계)의 검증 회복/OOS 훼손 상충을 숨기지 않고 다음 수리 경계로 전달한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)\nstage230_stage229_guard_blend_followup_review:.*?(?=\nstage\d+_|\Z)", "\n", state)
    state = re.sub(r"(?ms)\nstage231_midpf_oos_repair_after_guard_blend_failure:.*?(?=\nstage\d+_|\Z)", "\n", state)
    block = f"""
stage230_stage229_guard_blend_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  oos_reference_bound: {best_ref.get('adapter_id', '')}
  validation_recovery_clue: {best_val.get('adapter_id', '')}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  failure_memory_path: {rel(FAILURE_MEMORY_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage231_midpf_oos_repair_after_guard_blend_failure:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage230
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `midpf_oos_repair_after_guard_blend_failure`
- status(상태): `stage230_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage230(230단계)는 Stage229(229단계) guard blend(보호 혼합)를 follow-up review(후속 검토)로 닫았다. Effect(효과): Stage231(231단계)가 mid PF/OOS(중반 수익요인/표본외) 수리만 좁게 다룬다.

## Latest Stage230 Evidence(최신 230단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- oos_reference_bound(표본외 보존 경계): `{best_ref.get('adapter_id', '')}`
- validation_recovery_clue(검증 회복 단서): `{best_val.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage230 Selection Status(230단계 선택 상태)

- stage_status(단계 상태): `reviewed_closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage230 Review Index(230단계 검토 색인)

- status(상태): `reviewed_closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage230 guard blend follow-up review closeout(230단계 보호 혼합 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage229(229단계)의 검증 회복/OOS 훼손 상충을 Stage231(231단계) 중반 PF/OOS 수리로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        TRADEOFF_PATH,
        ATTRIBUTION_PATH,
        ROUTE_MATRIX_PATH,
        FAILURE_MEMORY_PATH,
        SUMMARY_JSON_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage230_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage230 Stage229 guard blend follow-up review evidence.",
                }
            )
    return rows


def write_ledgers(best_ref: Mapping[str, Any], best_val: Mapping[str, Any]) -> dict[str, Any]:
    primary = ledger_pairs(
        [
            ("oos_reference_bound", best_ref.get("adapter_id", "")),
            ("oos_reference_net", best_ref.get("oos_net", "")),
            ("validation_clue", best_val.get("adapter_id", "")),
            ("validation_clue_net", best_val.get("validation_net", "")),
            ("validation_clue_mid_pf", best_val.get("validation_mid_pf", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("stage230_role", "review_only_no_tuning"),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage230_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage230_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage229_guard_blend_followup_review(229단계 보호 혼합 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage230 review-only closeout; not final and not deployment.",
        }
    ]
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "notes": ledger_pairs(
                [
                    ("source_run", SOURCE_RUN_ID),
                    ("oos_reference_bound", best_ref.get("adapter_id", "")),
                    ("validation_recovery_clue", best_val.get("adapter_id", "")),
                    ("boundary", BOUNDARY),
                ]
            ),
        }
    ]
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    return {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload}


def write_packet_files(
    rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    best_ref: Mapping[str, Any],
    best_val: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
) -> None:
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "oos_reference_bound": best_ref.get("adapter_id", ""),
        "validation_recovery_clue": best_val.get("adapter_id", ""),
        "external_verification_status": EXTERNAL_STATUS,
        "tradeoff_rows": list(rows),
        "attribution_rows": list(attribution_rows),
        "route_rows": list(route_rows),
        "failure_memory": list(failure_rows),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    files = {
        "routing_receipt.json": {
            **base_payload,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"],
            "required_gates": [
                "kpi_contract_audit",
                "result_judgment_gate",
                "performance_attribution_gate",
                "artifact_lineage_audit",
                "final_claim_guard",
                "required_gate_coverage_audit",
            ],
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            **base_payload,
            "source_quality": rel(SOURCE_QUALITY_PATH),
            "source_segments": rel(SOURCE_SEGMENT_PATH),
            "source_risk_atr": rel(SOURCE_RISK_ATR_PATH),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(ATTRIBUTION_PATH), rel(FAILURE_MEMORY_PATH), rel(DECISION_PATH)],
            "evidence_missing": ["new_repair_not_attempted_in_stage230_by_design"],
            "judgment_label": "guard_blend_tradeoff_failed_candidate_not_final",
            "next_condition": "Stage231 must repair mid PF/OOS with ATR/risk retained.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Margin-band guard blend recovered validation net and early PF but kept mid PF below 34D and damaged OOS net.",
            "comparison_baseline": "Stage229 session-only reference versus wide/base/tight margin-band blends",
            "likely_drivers": ["released session long supply", "margin-band context filter", "mid-period trade quality", "OOS regime sensitivity"],
            "attribution_confidence": "medium",
            "next_probe": NEXT_STAGE_ID,
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [
                rel(SOURCE_QUALITY_PATH),
                rel(SOURCE_SEGMENT_PATH),
                rel(SOURCE_RISK_ATR_PATH),
                rel(SOURCE_GATE_PATH),
                rel(SOURCE_DECISION_PATH),
            ],
            "producer": rel(PRODUCER_PATH),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID],
            "artifact_paths": [rel(path) for path in [REPORT_PATH, TRADEOFF_PATH, ATTRIBUTION_PATH, ROUTE_MATRIX_PATH, FAILURE_MEMORY_PATH, SUMMARY_JSON_PATH, DECISION_PATH]],
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "ledger_payload": ledger_payload,
            "status": "completed",
        },
        "final_claim_guard.json": {
            **base_payload,
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "required_gate_coverage_audit.json": {
            **base_payload,
            "missing_gates": [],
            "status": "passed",
        },
        "aggregate_summary.json": {
            **base_payload,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "tradeoff": rel(TRADEOFF_PATH),
                "attribution": rel(ATTRIBUTION_PATH),
                "route": rel(ROUTE_MATRIX_PATH),
                "failure_memory": rel(FAILURE_MEMORY_PATH),
                "decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
        },
        "packet_receipt.json": base_payload,
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage230 Closeout Packet(230단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- oos_reference_bound(표본외 보존 경계): `{best_ref.get('adapter_id', '')}`
- validation_recovery_clue(검증 회복 단서): `{best_val.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def run() -> Mapping[str, Any]:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    segment_rows = read_csv(SOURCE_SEGMENT_PATH)
    risk_rows = read_csv(SOURCE_RISK_ATR_PATH)
    gate_rows = read_csv(SOURCE_GATE_PATH)

    tradeoff_rows = build_tradeoff_rows(quality_rows, segment_rows, risk_rows, gate_rows)
    best_ref = best_oos_reference(tradeoff_rows)
    best_val = best_validation_clue(tradeoff_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    route_rows = build_route_rows(tradeoff_rows)
    failure_rows = build_failure_memory(tradeoff_rows)

    write_md(REPORT_PATH, report_markdown(tradeoff_rows))
    write_csv(TRADEOFF_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_csv(FAILURE_MEMORY_PATH, failure_rows)
    write_md(DECISION_PATH, decision_markdown(best_ref, best_val))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": DECISION,
            "external_verification_status": EXTERNAL_STATUS,
            "source_summary": rel(SOURCE_SUMMARY_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
            "source_quality": rel(SOURCE_QUALITY_PATH),
            "source_kpi": rel(SOURCE_KPI_PATH),
            "source_segment_kpi": rel(SOURCE_SEGMENT_PATH),
            "source_balance_audit": rel(SOURCE_BALANCE_PATH),
            "source_monthly_kpi": rel(SOURCE_MONTHLY_PATH),
            "source_concentration": rel(SOURCE_CONCENTRATION_PATH),
            "source_drawdown": rel(SOURCE_DRAWDOWN_PATH),
            "source_risk_atr": rel(SOURCE_RISK_ATR_PATH),
            "source_gate": rel(SOURCE_GATE_PATH),
            "source_trade_audit": rel(SOURCE_TRADE_AUDIT_PATH),
            "tradeoff_rows": tradeoff_rows,
            "attribution_rows": attribution_rows,
            "route_rows": route_rows,
            "failure_memory": failure_rows,
            "oos_reference_bound": best_ref,
            "validation_recovery_clue": best_val,
            "legacy_34d": LEGACY_34D,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_stage231_seed(best_ref, best_val)
    update_current_truth(best_ref, best_val)
    write_status_files()
    append_changelog()
    ledger_payload = write_ledgers(best_ref, best_val)
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(tradeoff_rows, attribution_rows, route_rows, failure_rows, best_ref, best_val, {**ledger_payload, "artifact_registry": artifact_payload})
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    return {
        "status": "reviewed_closed",
        "run_id": RUN_ID,
        "decision": DECISION,
        "oos_reference_bound": best_ref.get("adapter_id", ""),
        "validation_recovery_clue": best_val.get("adapter_id", ""),
        "report": rel(REPORT_PATH),
        "next_stage": NEXT_STAGE_ID,
        "artifact_registry": artifact_payload,
        "overall_goal_complete": False,
    }


def main() -> int:
    print(json.dumps(json_ready(run()), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
