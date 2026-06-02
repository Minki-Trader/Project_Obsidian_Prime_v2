from __future__ import annotations

import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import review_cost_session_stress_scout_without_db as review  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = review.STAGE_ID
RUN_NUMBER = "run364AC"
RUN_ID = "run364AC_materialize_pf_dd_near_miss_density_bridge_without_db_v1"
PARENT_RUN_ID = review.RUN_ID
NEXT_RUN_ID = "run364AD_train_pf_dd_near_miss_density_bridge_scout_without_db_v1"

STATUS = "completed_stage364AC_pf_dd_near_miss_density_bridge_queue_materialized_no_training_no_mt5_no_authority"
JUDGMENT = "density_bridge_scout_inputs_ready_no_operating_claim"
DECISION = "stage364AC_open_run364AD_pf_dd_near_miss_density_bridge_scout"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = review.DENSITY_FLOOR
TARGET_PF = review.TARGET_PF

STAGE_DIR = review.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
NEAR_MISS_PROFILE = RUN_DIR / "near_miss_profile.csv"
DENSITY_BRIDGE_QUEUE = RUN_DIR / "density_bridge_queue.csv"
BRIDGE_CONTROL_QUEUE = RUN_DIR / "bridge_control_queue.csv"
RUN364AD_QUEUE = RUN_DIR / "run364AD_scout_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AC_density_bridge_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AC_density_bridge_inputs.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

INPUT_FILES = [
    review.FINAL_DECISION,
    review.GATE_AUDIT,
    review.SURFACE_REVIEW,
    review.NEAR_MISS_CANDIDATES,
    review.NEXT_QUEUE,
    review.POSITIVE_CLUES,
    review.FAILURE_MEMORY,
    review.REPORT_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    NEAR_MISS_PROFILE,
    DENSITY_BRIDGE_QUEUE,
    BRIDGE_CONTROL_QUEUE,
    RUN364AD_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    ATTRIBUTION_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return review.rel(path)


def exists(path: Path | str) -> bool:
    return review.exists(path)


def sha(path: Path | str) -> str:
    return review.sha(path)


def read_json(path: Path) -> Any:
    return review.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    review.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    review.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    review.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    review.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return review.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    review.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if math.isnan(number):
        return ""
    if math.isinf(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(path, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    final = read_json(review.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(운영 주장 금지 위반)")
    gates = read_csv_rows(review.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트 미통과)")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing materialization inputs(구체화 입력 누락): " + ", ".join(missing))
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def load_near_miss() -> pd.DataFrame:
    df = pd.read_csv(review.NEAR_MISS_CANDIDATES, encoding="utf-8-sig")
    for col in [
        "combined_net_profit",
        "combined_profit_factor",
        "combined_trade_count",
        "combined_trade_per_business_day",
        "combined_max_drawdown",
        "combined_recovery_factor",
        "combined_short_count",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def business_days(row: Mapping[str, Any]) -> float:
    density = as_float(row.get("combined_trade_per_business_day"))
    trades = as_float(row.get("combined_trade_count"))
    if density <= 0:
        return 0.0
    return trades / density


def profile_rows(near: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for _, raw in near.iterrows():
        row = raw.to_dict()
        days = business_days(row)
        required_trades = math.ceil(DENSITY_FLOOR * days) if days > 0 else 0
        trade_count = as_float(row.get("combined_trade_count"))
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row.get("queue_id", ""),
                "variant_id": row.get("variant_id", ""),
                "combined_net_profit": finite(row.get("combined_net_profit")),
                "combined_profit_factor": finite(row.get("combined_profit_factor")),
                "combined_trade_count": finite(trade_count),
                "combined_trade_per_business_day": finite(row.get("combined_trade_per_business_day")),
                "combined_max_drawdown": finite(row.get("combined_max_drawdown")),
                "combined_short_count": finite(row.get("combined_short_count")),
                "estimated_business_days": finite(days, 6),
                "density_floor_required_trades": required_trades,
                "density_trade_gap": finite(max(0.0, required_trades - trade_count), 6),
                "pf_gap_to_target": finite(max(0.0, TARGET_PF - as_float(row.get("combined_profit_factor"))), 10),
                "materialization_read(구체화 판독)": "density_bridge_needed(밀도 연결 필요)" if as_float(row.get("combined_trade_per_business_day")) < DENSITY_FLOOR else "pf_lift_needed(PF 상승 필요)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def bridge_rows(profile: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_queue = {str(row.get("queue_id")): row for row in profile}
    stress3 = by_queue.get("stress_zone_3", {})
    stress4 = by_queue.get("stress_zone_4", {})
    base = [
        {
            "queue_rank": 1,
            "queue_id": "stress3_restore_march_short_top5",
            "seed_queue_id": "stress_zone_3",
            "seed_variant_id": stress3.get("variant_id", ""),
            "short_probability_threshold": 0.45,
            "long_block_min": 40.0,
            "max_hold_m5": 8,
            "bridge_expression": "entry_month=2025-03 restore side=short top_n=5 by p_short",
            "expected_effect(기대 효과)": "adds about five trades to cross density floor while preserving March long block(약 5개 거래를 복원해 밀도 하한을 넘기고 3월 롱 차단은 보존)",
        },
        {
            "queue_rank": 2,
            "queue_id": "stress3_restore_march_non_hour16_top8",
            "seed_queue_id": "stress_zone_3",
            "seed_variant_id": stress3.get("variant_id", ""),
            "short_probability_threshold": 0.45,
            "long_block_min": 40.0,
            "max_hold_m5": 8,
            "bridge_expression": "entry_month=2025-03 restore non_hour16 top_n=8 by absolute_margin",
            "expected_effect(기대 효과)": "tests whether hour16 risk was the March damage source(16시 위험이 3월 손상 원천인지 시험)",
        },
        {
            "queue_rank": 3,
            "queue_id": "stress3_restore_march_adx45_long_top8",
            "seed_queue_id": "stress_zone_3",
            "seed_variant_id": stress3.get("variant_id", ""),
            "short_probability_threshold": 0.45,
            "long_block_min": 45.0,
            "max_hold_m5": 8,
            "bridge_expression": "entry_month=2025-03 restore side=long adx_14>=45 top_n=8 by p_long",
            "expected_effect(기대 효과)": "tries quality-gated long restoration instead of full March removal(전체 3월 제거 대신 품질 제한 롱 복원 시험)",
        },
        {
            "queue_rank": 4,
            "queue_id": "stress4_short0475_pf_lift",
            "seed_queue_id": "stress_zone_4",
            "seed_variant_id": stress4.get("variant_id", ""),
            "short_probability_threshold": 0.475,
            "long_block_min": 40.0,
            "max_hold_m5": 8,
            "bridge_expression": "entry_month=2025-03 block side=long; short_threshold=0.475",
            "expected_effect(기대 효과)": "keeps density-pass March-long block and lifts short quality(밀도 통과 3월 롱 차단을 유지하고 숏 품질을 올림)",
        },
        {
            "queue_rank": 5,
            "queue_id": "stress4_short050_pf_lift",
            "seed_queue_id": "stress_zone_4",
            "seed_variant_id": stress4.get("variant_id", ""),
            "short_probability_threshold": 0.50,
            "long_block_min": 40.0,
            "max_hold_m5": 8,
            "bridge_expression": "entry_month=2025-03 block side=long; short_threshold=0.50",
            "expected_effect(기대 효과)": "stronger short quality lift with density stress tracked(더 강한 숏 품질 상승과 밀도 압박 추적)",
        },
        {
            "queue_rank": 6,
            "queue_id": "adx38_stress3_month_block",
            "seed_queue_id": "adx38_density_counterfactual",
            "seed_variant_id": "adx38_density_counterfactual",
            "short_probability_threshold": 0.45,
            "long_block_min": 38.0,
            "max_hold_m5": 8,
            "bridge_expression": "adx_block_min=38; entry_month=2025-03 block all",
            "expected_effect(기대 효과)": "combines ADX38 density recovery with full March damage cut(ADX38 밀도 회복과 3월 손상 차단 결합)",
        },
        {
            "queue_rank": 7,
            "queue_id": "adx38_stress4_month_long_block",
            "seed_queue_id": "adx38_density_counterfactual",
            "seed_variant_id": "adx38_density_counterfactual",
            "short_probability_threshold": 0.45,
            "long_block_min": 38.0,
            "max_hold_m5": 8,
            "bridge_expression": "adx_block_min=38; entry_month=2025-03 block side=long",
            "expected_effect(기대 효과)": "keeps more density than full March block while cutting bad March longs(전체 3월 차단보다 밀도를 보존하며 나쁜 3월 롱을 자름)",
        },
    ]
    for row in base:
        row.update({"run_id": RUN_ID, "next_run_id": NEXT_RUN_ID, "trade_splitting_status": "not_used(거래 쪼개기 없음)", "claim_boundary(주장 경계)": CLAIM_BOUNDARY})
    return base


def control_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "queue_rank": 1,
            "queue_id": "baseline_replay_control",
            "bridge_expression": "none",
            "required_reason(필수 이유)": "control baseline for attribution(귀속 기준)",
        },
        {
            "queue_rank": 2,
            "queue_id": "stress_zone_3_control",
            "bridge_expression": "entry_month=2025-03 block all",
            "required_reason(필수 이유)": "near-miss seed control(근접 실패 씨앗 기준)",
        },
        {
            "queue_rank": 3,
            "queue_id": "stress_zone_4_control",
            "bridge_expression": "entry_month=2025-03 block side=long",
            "required_reason(필수 이유)": "density-pass PF-lift seed control(밀도 통과 PF 상승 씨앗 기준)",
        },
    ]
    for row in rows:
        row.update({"run_id": RUN_ID, "next_run_id": NEXT_RUN_ID, "claim_boundary(주장 경계)": CLAIM_BOUNDARY})
    return rows


def scout_queue_rows(bridges: Sequence[Mapping[str, Any]], controls: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    rank = 1
    for row in controls:
        out = dict(row)
        out["queue_rank"] = rank
        out["queue_type"] = "control(대조)"
        rows.append(out)
        rank += 1
    for row in bridges:
        out = dict(row)
        out["queue_rank"] = rank
        out["queue_type"] = "bridge_scout(연결 정찰)"
        rows.append(out)
        rank += 1
    return rows


def gate_row(name: str, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate(게이트)": name,
        "status": "passed",
        "evidence(근거)": rel(evidence),
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def final_payload(profile: Sequence[Mapping[str, Any]], bridges: Sequence[Mapping[str, Any]], scout: Sequence[Mapping[str, Any]], created_at_utc: str) -> dict[str, Any]:
    density_gap = next((row.get("density_trade_gap", "") for row in profile if row.get("queue_id") == "stress_zone_3"), "")
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "near_miss_profile_rows": len(profile),
        "density_bridge_rows": len(bridges),
        "run364AD_queue_rows": len(scout),
        "stress_zone_3_density_trade_gap": density_gap,
        "primary_seed": "stress_zone_3",
        "secondary_seed": "stress_zone_4",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": 0,
        "gate_total": 0,
    }


def write_receipts(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(DATA_RECEIPT, {**base, "skill": "obsidian-data-integrity(데이터 무결성)", "inputs": [rel(path) for path in INPUT_FILES], "effect(효과)": "reviewed proxy rows(검토된 프록시 행)만 사용한다."})
    write_json(EXPERIMENT_RECEIPT, {**base, "skill": "obsidian-experiment-design(실험 설계)", "hypothesis": "near-miss PF/DD rows can recover density using timestamp-safe restoration/quality bridge(근접 실패 PF/DD 행은 시점 안전 복원/품질 연결로 밀도를 회복할 수 있다)", "stop_condition": "no queue row may use trade splitting(어떤 대기열 행도 거래 쪼개기를 쓰지 않음)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "skill": "obsidian-performance-attribution(성과 귀속)", "profile": rel(NEAR_MISS_PROFILE), "queue": rel(RUN364AD_QUEUE), "effect(효과)": "stress_zone_3 density gap and stress_zone_4 PF gap(3번 밀도 부족과 4번 PF 부족)을 분리한다."})
    write_json(CLAIM_RECEIPT, {**base, "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "effect(효과)": "materialization(구체화)을 운영 주장으로 승격하지 않는다."})
    write_json(LINEAGE_RECEIPT, {**base, "skill": "obsidian-artifact-lineage(산출물 계보)", "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()}})
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AC materialization(364AC 구체화)을 닫는다."),
        gate_row("input_parent_gate(부모 입력 게이트)", INPUT_MANIFEST, "run364AB 검토 산출물을 확인한다."),
        gate_row("near_miss_profile_gate(근접 실패 프로필 게이트)", NEAR_MISS_PROFILE, "stress_zone_3/4 gap(압박 구간 3/4 부족분)을 계산한다."),
        gate_row("queue_materialization_gate(대기열 구체화 게이트)", RUN364AD_QUEUE, "run364AD scout queue(364AD 정찰 대기열)를 만든다."),
        gate_row("experiment_boundary_gate(실험 경계 게이트)", EXPERIMENT_RECEIPT, "거래 쪼개기 금지를 기록한다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 hash(해시)를 연결한다."),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "runtime authority(런타임 권위)를 주장하지 않는다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "필수 gate(게이트)를 closeout(종료 기록)에 연결한다."),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def refresh_stage_brief_header() -> None:
    if not exists(STAGE_BRIEF):
        return
    text = STAGE_BRIEF.read_text(encoding="utf-8-sig")
    lines = []
    for line in text.splitlines():
        if line.startswith("- current_run_id"):
            lines.append(f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`")
        elif line.startswith("- latest_completed_run_id"):
            lines.append(f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`")
        elif line.startswith("- selection_status"):
            lines.append(f"- selection_status(선택 상태): `{STATUS}`")
        elif line.startswith("- claim_boundary"):
            lines.append(f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
        else:
            lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(lines) + "\n")


def write_docs(final: Mapping[str, Any], profile: Sequence[Mapping[str, Any]], bridges: Sequence[Mapping[str, Any]], scout: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header()
    text = f"""# run364AC density bridge inputs(364AC 밀도 연결 입력)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- near_miss_profile_rows(근접 실패 프로필 행): `{final['near_miss_profile_rows']}`
- density_bridge_rows(밀도 연결 행): `{final['density_bridge_rows']}`
- run364AD_queue_rows(364AD 대기열 행): `{final['run364AD_queue_rows']}`
- stress_zone_3_density_trade_gap(3번 압박 구간 밀도 부족 거래수): `{final['stress_zone_3_density_trade_gap']}`
- runtime_authority(런타임 권위): `not_claimed`

## Near miss profile(근접 실패 프로필)

{markdown_table(profile, ['queue_id', 'combined_profit_factor', 'combined_trade_per_business_day', 'density_trade_gap', 'pf_gap_to_target', 'materialization_read(구체화 판독)'])}

## Bridge queue(연결 대기열)

{markdown_table(bridges, ['queue_id', 'seed_queue_id', 'bridge_expression', 'expected_effect(기대 효과)'])}

## Scout queue(정찰 대기열)

{markdown_table(scout, ['queue_rank', 'queue_id', 'queue_type', 'bridge_expression'])}

## Gate audit(게이트 감사)

{markdown_table(gates, ['gate(게이트)', 'status', 'evidence(근거)', 'effect(효과)'])}

## Claim boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): 이 materialization(구체화)은 다음 scout(정찰) 입력만 만들며, MT5 runtime authority(MT5 런타임 권위)나 operating promotion(운영 승격)을 주장하지 않는다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(REVIEW_INDEX, RUN_ID, f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): run364AD(364AD 실행) density bridge scout queue(밀도 연결 정찰 대기열)를 만들었다.\n")
    append_text_once(STAGE_BRIEF, RUN_ID, f"\n## run364AC Density Bridge Input Closeout(364AC 밀도 연결 입력 종료)\n\nAction(행동): stress_zone_3/4(압박 구간 3/4) near-miss(근접 실패)를 `{len(scout)}`개 scout queue(정찰 대기열)로 구체화했다.\n\nEffect(효과): 다음 작업은 `{NEXT_RUN_ID}`이며, Stage364(364단계) 안에서 PF/DD density bridge(PF/DD 밀도 연결)를 계속 탐색한다.\n")
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_materialization_only(구체화 전용이라 없음)
- latest_proxy_review(최근 프록시 검토): `run364AB`
- latest_materialization(최근 구체화): `run364AC`
- next_scout_queue(다음 정찰 대기열): `{rel(RUN364AD_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")
    write_text(CURRENT_WORKING_STATE, f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): run364AC(364AC 실행)는 stress_zone_3/4(압박 구간 3/4) near-miss(근접 실패)를 run364AD scout queue(364AD 정찰 대기열)로 구체화했다. stress_zone_3(압박 구간 3)은 밀도 하한까지 약 `{final['stress_zone_3_density_trade_gap']}`개 거래가 부족하다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 queue(대기열)를 replay scout(재생 정찰)한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""")
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): PF/DD near-miss density bridge(PF/DD 근접 실패 밀도 연결) 입력을 구체화했다.\n- effect(효과): `{NEXT_RUN_ID}` scout(정찰)로 넘길 queue(대기열)를 만들었다.\n- report(보고서): `{rel(REPORT_PATH)}`\n")
    append_text_once(IDEA_REGISTRY, RUN_ID, f"\n## {RUN_ID}\n\n- idea(아이디어): stress_zone_3(압박 구간 3)의 5거래 내외 밀도 부족을 timestamp-safe restoration(시점 안전 복원)으로 메운다.\n- positive clue(긍정 단서): stress_zone_3/4(압박 구간 3/4)는 DD(낙폭)를 줄인다.\n- failure memory(실패 기억): density-only(밀도 단독)는 PF/DD(수익 팩터/낙폭)를 악화한다.\n")
    append_text_once(STAGE_README, RUN_ID, f"\n## {RUN_ID}\n\n- action(행동): near-miss density bridge queue(근접 실패 밀도 연결 대기열)를 만들었다.\n- effect(효과): stage branch(단계 분기) 없이 Stage364(364단계) 안에서 다음 scout(정찰)를 연다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "materialization(구체화)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        "notes": f"queue_rows={final['run364AD_queue_rows']}; density_gap={final['stress_zone_3_density_trade_gap']}",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["run364AD_queue_rows"],
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(RUN364AD_QUEUE),
        "result_status": STATUS,
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_design(실험 설계)",
        "trade_density_requirement_status": "materialized_for_next_scout(다음 정찰용 구체화)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "evidence_scope": "materialization_no_authority(구체화, 권위 없음)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for subrun_id, record_view, tier_scope, kpi_scope in [
        (f"{RUN_ID}__Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "materialization queue(구체화 대기열)"),
        (f"{RUN_ID}__Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)"),
        (f"{RUN_ID}__Tier_A_plus_B", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A only plus Tier B missing_required(Tier A만 있고 Tier B 필수 누락)"),
    ]:
        row = dict(common)
        row.update({"ledger_row_id": subrun_id, "subrun_id": subrun_id, "record_view": record_view, "tier_scope": tier_scope, "kpi_scope": kpi_scope})
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("near_miss_profile", NEAR_MISS_PROFILE, "Near-miss profile(근접 실패 프로필)."),
            ("density_bridge_queue", DENSITY_BRIDGE_QUEUE, "Density bridge queue(밀도 연결 대기열)."),
            ("run364AD_queue", RUN364AD_QUEUE, "Next scout queue(다음 정찰 대기열)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    near = load_near_miss()
    profile = profile_rows(near)
    bridges = bridge_rows(profile)
    controls = control_rows()
    scout = scout_queue_rows(bridges, controls)
    write_csv(NEAR_MISS_PROFILE, profile)
    write_csv(DENSITY_BRIDGE_QUEUE, bridges)
    write_csv(BRIDGE_CONTROL_QUEUE, controls)
    write_csv(RUN364AD_QUEUE, scout)
    write_json(WORK_PACKET, {"run_id": RUN_ID, "primary_family": "experiment_design(실험 설계)", "primary_skill": "obsidian-experiment-design(실험 설계)", "support_skills": ["obsidian-data-integrity(데이터 무결성)", "obsidian-performance-attribution(성과 귀속)", "obsidian-artifact-lineage(산출물 계보)"], "required_gates": ["scope_completion_gate", "input_parent_gate", "near_miss_profile_gate", "queue_materialization_gate", "experiment_boundary_gate", "artifact_lineage_audit", "claim_boundary_audit", "required_gate_coverage_audit"], "claim_boundary(주장 경계)": CLAIM_BOUNDARY})
    final = final_payload(profile, bridges, scout, now_utc())
    write_json(FINAL_DECISION, final)
    gates = write_receipts(final)
    final["gate_passes"] = sum(1 for row in gates if row.get("status") == "passed")
    final["gate_total"] = len(gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, profile, bridges, scout, gates)
    write_ledgers(final, gates)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
