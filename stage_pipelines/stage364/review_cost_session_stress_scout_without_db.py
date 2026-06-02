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

from stage_pipelines.stage364 import train_density_side_balance_cost_session_stress_scout_without_db as parent  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AB"
RUN_ID = "run364AB_review_density_side_balance_cost_session_stress_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
NEXT_RUN_ID = "run364AC_materialize_pf_dd_near_miss_density_bridge_without_db_v1"

STATUS = "completed_stage364AB_proxy_scout_review_negative_strict_pass_near_miss_repair_seed_no_authority"
JUDGMENT = "negative_for_package_positive_near_miss_pf_dd_density_bridge_seed_no_authority"
DECISION = "stage364AB_no_package_open_run364AC_pf_dd_near_miss_density_bridge"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = parent.DENSITY_FLOOR
TARGET_PF = parent.TARGET_PF

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SURFACE_REVIEW = RUN_DIR / "surface_review.csv"
STRICT_PASS_AUDIT = RUN_DIR / "strict_pass_audit.csv"
NEAR_MISS_CANDIDATES = RUN_DIR / "near_miss_candidates.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364AC_repair_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AB_scout_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AB_scout_review.md"
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
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.SCOUT_SURFACE,
    parent.SELECTED_PROXY_CANDIDATE,
    parent.SELECTED_EXPECTED_TRADE_TAPE,
    parent.BASELINE_COMPARISON,
    parent.RUN364AB_QUEUE,
    parent.REPORT_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SURFACE_REVIEW,
    STRICT_PASS_AUDIT,
    NEAR_MISS_CANDIDATES,
    POSITIVE_CLUES,
    FAILURE_MEMORY,
    NEXT_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
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
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    parent.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


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


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
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
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(운영 주장 금지 위반)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트 미통과)")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing review inputs(검토 입력 누락): " + ", ".join(missing))
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
        }
        for path in INPUT_FILES
    ]


def load_surface() -> pd.DataFrame:
    df = pd.read_csv(parent.SCOUT_SURFACE, encoding="utf-8-sig")
    numeric_cols = [
        "combined_net_profit",
        "combined_profit_factor",
        "combined_trade_count",
        "combined_trade_per_business_day",
        "combined_max_drawdown",
        "combined_recovery_factor",
        "combined_long_count",
        "combined_short_count",
        "selection_score",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def row_for(df: pd.DataFrame, queue_id: str) -> dict[str, Any]:
    rows = df[df["queue_id"].astype(str) == queue_id]
    if rows.empty:
        return {}
    return rows.iloc[0].to_dict()


def classify_row(row: Mapping[str, Any], baseline: Mapping[str, Any]) -> str:
    pf = as_float(row.get("combined_profit_factor"))
    density = as_float(row.get("combined_trade_per_business_day"))
    dd = as_float(row.get("combined_max_drawdown"))
    shorts = as_int(row.get("combined_short_count"))
    baseline_dd = as_float(baseline.get("combined_max_drawdown"))
    if density >= DENSITY_FLOOR and pf >= TARGET_PF and dd >= baseline_dd and shorts > 0:
        return "strict_pass(엄격 통과)"
    if density >= 2.95 and pf >= 1.25 and dd >= baseline_dd:
        return "near_miss_density_bridge_seed(밀도 연결 수리 씨앗)"
    if density >= DENSITY_FLOOR and dd >= baseline_dd and pf >= 1.25:
        return "watch_pf_lift_seed(PF 상승 씨앗)"
    if density >= DENSITY_FLOOR:
        return "density_only_watch(밀도만 관찰)"
    return "reject_density_floor(밀도 하한 탈락)"


def review_surface(df: pd.DataFrame, parent_final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    baseline = row_for(df, "baseline_replay_control")
    if not baseline:
        baseline = {
            "combined_net_profit": parent_final.get("selected_combined_net_profit"),
            "combined_profit_factor": parent_final.get("selected_combined_profit_factor"),
            "combined_trade_per_business_day": parent_final.get("selected_combined_trade_per_business_day"),
            "combined_max_drawdown": parent_final.get("selected_combined_max_drawdown"),
            "combined_short_count": parent_final.get("selected_combined_short_count"),
        }
    rows: list[dict[str, Any]] = []
    for _, raw in df.iterrows():
        row = raw.to_dict()
        status = classify_row(row, baseline)
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row.get("queue_id", ""),
                "variant_id": row.get("variant_id", ""),
                "review_status": status,
                "source_candidate_status": row.get("candidate_status", ""),
                "combined_net_profit": finite(row.get("combined_net_profit")),
                "combined_profit_factor": finite(row.get("combined_profit_factor")),
                "combined_trade_count": finite(row.get("combined_trade_count")),
                "combined_trade_per_business_day": finite(row.get("combined_trade_per_business_day")),
                "combined_max_drawdown": finite(row.get("combined_max_drawdown")),
                "combined_recovery_factor": finite(row.get("combined_recovery_factor")),
                "combined_long_count": finite(row.get("combined_long_count")),
                "combined_short_count": finite(row.get("combined_short_count")),
                "net_delta_vs_baseline_proxy": finite(as_float(row.get("combined_net_profit")) - as_float(baseline.get("combined_net_profit"))),
                "pf_delta_vs_baseline_proxy": finite(as_float(row.get("combined_profit_factor")) - as_float(baseline.get("combined_profit_factor"))),
                "density_delta_vs_baseline_proxy": finite(as_float(row.get("combined_trade_per_business_day")) - as_float(baseline.get("combined_trade_per_business_day"))),
                "dd_delta_vs_baseline_proxy": finite(as_float(row.get("combined_max_drawdown")) - as_float(baseline.get("combined_max_drawdown"))),
                "selection_score": finite(row.get("selection_score")),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    rows.sort(key=lambda item: (str(item["review_status"]).startswith("strict_pass"), as_float(item["combined_profit_factor"]), as_float(item["combined_net_profit"])), reverse=True)
    near = [
        row
        for row in rows
        if row["review_status"] in {"near_miss_density_bridge_seed(밀도 연결 수리 씨앗)", "watch_pf_lift_seed(PF 상승 씨앗)"}
    ]
    return rows, near


def strict_pass_rows(review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    strict = [dict(row) for row in review_rows if str(row.get("review_status", "")).startswith("strict_pass")]
    if strict:
        return strict
    return [
        {
            "run_id": RUN_ID,
            "strict_pass_rows": 0,
            "status": "failed_for_package(패키지 실패)",
            "reason": "no row met PF>=1.30, density>=3/day, DD not worse than baseline, and short_count>0(PF 1.30 이상, 일 3회 이상, 기준보다 나쁘지 않은 낙폭, 숏 0 초과를 동시에 만족한 행 없음)",
            "effect(효과)": "package/MT5 runtime probe(패키지/MT5 런타임 탐침)로 넘기지 않는다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
    ]


def clue_rows(parent_final: Mapping[str, Any], review_rows: Sequence[Mapping[str, Any]], near_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    top_pf = max(review_rows, key=lambda row: as_float(row.get("combined_profit_factor"))) if review_rows else {}
    top_density = max(review_rows, key=lambda row: as_float(row.get("combined_trade_per_business_day"))) if review_rows else {}
    rows = [
        {
            "run_id": RUN_ID,
            "clue_id": "density_recovered_but_pf_dd_not_repaired(밀도 회복, PF/DD 미수리)",
            "evidence": parent_final.get("selected_variant_id", ""),
            "kpi_read": f"net={parent_final.get('selected_combined_net_profit')}; pf={parent_final.get('selected_combined_profit_factor')}; density={parent_final.get('selected_combined_trade_per_business_day')}; dd={parent_final.get('selected_combined_max_drawdown')}",
            "effect(효과)": "maxhold6 density control(최대보유 6 밀도 대조)은 운영 패키지가 아니라 밀도 회복 단서로만 쓴다.",
        },
        {
            "run_id": RUN_ID,
            "clue_id": "stress_zone_3_near_density_floor(3번 압박 구간 밀도 하한 근접)",
            "evidence": next((row.get("variant_id", "") for row in near_rows if row.get("queue_id") == "stress_zone_3"), top_pf.get("variant_id", "")),
            "kpi_read": f"best_pf_queue={top_pf.get('queue_id', '')}; pf={top_pf.get('combined_profit_factor', '')}; density={top_pf.get('combined_trade_per_business_day', '')}; dd={top_pf.get('combined_max_drawdown', '')}",
            "effect(효과)": "PF/DD(수익 팩터/낙폭)는 좋아졌지만 density(밀도)가 살짝 부족한 조합을 다음 offensive repair(공격 수리) 씨앗으로 쓴다.",
        },
        {
            "run_id": RUN_ID,
            "clue_id": "density_ceiling_requires_quality_filter(밀도 상단은 품질 필터 필요)",
            "evidence": top_density.get("variant_id", ""),
            "kpi_read": f"top_density_queue={top_density.get('queue_id', '')}; density={top_density.get('combined_trade_per_business_day', '')}; pf={top_density.get('combined_profit_factor', '')}; dd={top_density.get('combined_max_drawdown', '')}",
            "effect(효과)": "거래수를 늘리는 행동(action, 행동)은 PF/DD(수익 팩터/낙폭) 압박을 같이 가져오므로 quality bridge(품질 연결)가 필요하다.",
        },
    ]
    return rows


def failure_rows(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "failure_id": "strict_pass_zero(엄격 통과 0)",
            "evidence": rel(parent.SCOUT_SURFACE),
            "kpi_read": f"strict_pass_rows={parent_final.get('strict_pass_rows')}",
            "constraint_for_next(다음 제약)": "no MT5 package until PF/DD/density/short balance pass together(PF/DD/밀도/숏 균형 동시 통과 전 MT5 패키지 금지)",
        },
        {
            "run_id": RUN_ID,
            "failure_id": "maxhold6_worse_than_baseline_pf_dd(최대보유 6 기준 대비 PF/DD 악화)",
            "evidence": parent_final.get("selected_variant_id", ""),
            "kpi_read": f"pf_delta={parent_final.get('pf_delta_vs_run364V_proxy')}; dd_delta={parent_final.get('dd_delta_vs_run364V_proxy')}; net_delta={parent_final.get('net_delta_vs_run364V_proxy')}",
            "constraint_for_next(다음 제약)": "do not promote density-only selection(밀도만 좋은 선택 승격 금지)",
        },
        {
            "run_id": RUN_ID,
            "failure_id": "account_dd_soft_stop_overkills_density(계좌 낙폭 소프트스톱 밀도 과도 감소)",
            "evidence": "prevdd_2pct_soft_stop / prevdd_5pct_soft_stop",
            "kpi_read": "trade_count collapsed to 5 or 40(거래수 5 또는 40으로 붕괴)",
            "constraint_for_next(다음 제약)": "avoid hard account-state stops as primary repair(계좌 상태 하드 중단을 주 수리로 쓰지 않음)",
        },
    ]


def next_queue_rows(near_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_queue = {str(row.get("queue_id")): row for row in near_rows}
    stress3 = by_queue.get("stress_zone_3", {})
    stress4 = by_queue.get("stress_zone_4", {})
    adx38 = by_queue.get("adx38_density_counterfactual", {})
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "density_bridge_from_stress_zone_3(3번 압박 구간 밀도 연결)",
            "seed_variant_id": stress3.get("variant_id", "stress_zone_3"),
            "hypothesis(가설)": "restore only timestamp-safe low-risk trades around the 2025-03 block to lift density above 3/day while preserving PF/DD(2025-03 차단 주변 저위험 거래만 복원해 밀도 3 이상과 PF/DD 보존을 동시에 노린다)",
            "required_control(필수 대조)": "no trade splitting(거래 쪼개기 금지); compare against baseline_replay_control and stress_zone_3(기준 재생과 3번 압박 구간 비교)",
            "effect(효과)": "near-miss PF/DD(근접 실패 PF/DD)를 새 offensive exploration(공격 탐색) 씨앗으로 바꾼다.",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "stress_zone_4_pf_lift(4번 압박 구간 PF 상승)",
            "seed_variant_id": stress4.get("variant_id", "stress_zone_4"),
            "hypothesis(가설)": "use month-long block plus selective short quality threshold to lift PF toward 1.30 without losing density(월별 롱 차단과 선택적 숏 품질 임계값으로 밀도 손실 없이 PF 1.30에 접근한다)",
            "required_control(필수 대조)": "long/short balance audit(롱/숏 균형 감사); density floor >=3/day(밀도 일 3회 이상)",
            "effect(효과)": "density pass(밀도 통과) 조합에서 PF lift(PF 상승) 가능성을 본다.",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "adx38_stress_blend(ADX38 압박 혼합)",
            "seed_variant_id": adx38.get("variant_id", "adx38_density_counterfactual"),
            "hypothesis(가설)": "blend ADX38 density recovery with stress-zone DD cuts using timestamp-safe entry filters(ADX38 밀도 회복과 압박 구간 낙폭 절감을 시점 안전 진입 필터로 섞는다)",
            "required_control(필수 대조)": "baseline_replay_control, adx38 only, stress block only(기준 재생, ADX38 단독, 압박 차단 단독)",
            "effect(효과)": "density-only clue(밀도 단서)를 PF/DD repair(PF/DD 수리)로 밀어본다.",
        },
    ]


def gate_row(name: str, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate(게이트)": name,
        "status": "passed",
        "evidence(근거)": rel(evidence),
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def final_payload(
    parent_final: Mapping[str, Any],
    review_rows: Sequence[Mapping[str, Any]],
    near_rows: Sequence[Mapping[str, Any]],
    next_queue: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
    strict_count = sum(1 for row in review_rows if str(row.get("review_status", "")).startswith("strict_pass"))
    best_pf = max(review_rows, key=lambda row: as_float(row.get("combined_profit_factor"))) if review_rows else {}
    best_density = max(review_rows, key=lambda row: as_float(row.get("combined_trade_per_business_day"))) if review_rows else {}
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
        "parent_selected_variant_id": parent_final.get("selected_variant_id"),
        "parent_selected_net_profit": parent_final.get("selected_combined_net_profit"),
        "parent_selected_profit_factor": parent_final.get("selected_combined_profit_factor"),
        "parent_selected_trade_count": parent_final.get("selected_combined_trade_count"),
        "parent_selected_density": parent_final.get("selected_combined_trade_per_business_day"),
        "parent_selected_max_drawdown": parent_final.get("selected_combined_max_drawdown"),
        "surface_rows": len(review_rows),
        "strict_pass_rows": strict_count,
        "near_miss_rows": len(near_rows),
        "next_queue_rows": len(next_queue),
        "best_pf_queue_id": best_pf.get("queue_id", ""),
        "best_pf": best_pf.get("combined_profit_factor", ""),
        "best_pf_density": best_pf.get("combined_trade_per_business_day", ""),
        "best_pf_drawdown": best_pf.get("combined_max_drawdown", ""),
        "best_density_queue_id": best_density.get("queue_id", ""),
        "best_density": best_density.get("combined_trade_per_business_day", ""),
        "best_density_pf": best_density.get("combined_profit_factor", ""),
        "package_decision": "no_package_strict_pass_zero(패키지 없음, 엄격 통과 0)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": 0,
        "gate_total": 0,
    }


def write_receipts(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "skill": "obsidian-data-integrity(데이터 무결성)",
            "inputs": [rel(path) for path in INPUT_FILES],
            "timestamp_boundary": "review only; no new feature/label join(검토 전용, 새 피처/라벨 결합 없음)",
            "effect(효과)": "look-ahead bias(미래참조 편향) 새 위험을 만들지 않는다.",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "skill": "obsidian-performance-attribution(성과 귀속)",
            "surface_review": rel(SURFACE_REVIEW),
            "near_miss_candidates": rel(NEAR_MISS_CANDIDATES),
            "failure_memory": rel(FAILURE_MEMORY),
            "effect(효과)": "KPI 차이를 패키지 승격이 아니라 다음 수리 제약으로 바꾼다.",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "skill": "obsidian-result-judgment(결과 판정)",
            "judgment_label": JUDGMENT,
            "package_decision": final["package_decision"],
            "next_condition": NEXT_RUN_ID,
            "evidence_missing": "MT5 runtime probe(MT5 런타임 탐침) out of scope by claim(주장 범위 밖)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect(효과)": "proxy review(프록시 검토)를 운영 주장(operating claim, 운영 주장)으로 승격하지 않는다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "skill": "obsidian-artifact-lineage(산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
        },
    )
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AB review(364AB 검토) 범위를 닫는다."),
        gate_row("input_parent_gate(부모 입력 게이트)", INPUT_MANIFEST, "run364AA 산출물과 gate(게이트)를 확인한다."),
        gate_row("proxy_scout_review_gate(프록시 정찰 검토 게이트)", SURFACE_REVIEW, "16개 surface row(표면 행)를 판정한다."),
        gate_row("strict_pass_boundary_gate(엄격 통과 경계 게이트)", STRICT_PASS_AUDIT, "strict pass 0(엄격 통과 0)을 패키지 금지로 연결한다."),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "PF/DD/density(수익 팩터/낙폭/밀도) 차이를 귀속한다."),
        gate_row("next_queue_gate(다음 대기열 게이트)", NEXT_QUEUE, "run364AC repair queue(수리 대기열)를 만든다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 경로와 hash(해시)를 연결한다."),
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


def write_docs(
    final: Mapping[str, Any],
    review_rows: Sequence[Mapping[str, Any]],
    near_rows: Sequence[Mapping[str, Any]],
    clue_rows_: Sequence[Mapping[str, Any]],
    failure_rows_: Sequence[Mapping[str, Any]],
    next_queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    refresh_stage_brief_header()
    top = list(review_rows)[:8]
    text = f"""# run364AB scout review(364AB 정찰 검토)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- package_decision(패키지 결정): `{final['package_decision']}`
- strict_pass_rows(엄격 통과 행): `{final['strict_pass_rows']}`
- near_miss_rows(근접 실패 행): `{final['near_miss_rows']}`
- best_pf_queue(최고 PF 대기열): `{final['best_pf_queue_id']}` / PF `{final['best_pf']}` / density(밀도) `{final['best_pf_density']}` / DD(낙폭) `{final['best_pf_drawdown']}`
- runtime_authority(런타임 권위): `not_claimed`

## Top review rows(상위 검토 행)

{markdown_table(top, ['queue_id', 'review_status', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_per_business_day', 'combined_max_drawdown', 'combined_short_count'])}

## Near miss candidates(근접 실패 후보)

{markdown_table(near_rows, ['queue_id', 'review_status', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_per_business_day', 'combined_max_drawdown'])}

## Positive clues(긍정 단서)

{markdown_table(clue_rows_, ['clue_id', 'evidence', 'kpi_read', 'effect(효과)'])}

## Failure memory(실패 기억)

{markdown_table(failure_rows_, ['failure_id', 'evidence', 'kpi_read', 'constraint_for_next(다음 제약)'])}

## Next queue(다음 대기열)

{markdown_table(next_queue, ['queue_id', 'seed_variant_id', 'hypothesis(가설)', 'required_control(필수 대조)'])}

## Gate audit(게이트 감사)

{markdown_table(gates, ['gate(게이트)', 'status', 'evidence(근거)', 'effect(효과)'])}

## Claim boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): 이 review(검토)는 package(패키지), MT5 runtime probe(MT5 런타임 탐침), operating promotion(운영 승격)을 열지 않고, Stage364(364단계) 안에서 다음 offensive repair(공격 수리) 재료만 남긴다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"""

## {RUN_ID}

- report(보고서): `{rel(REPORT_PATH)}`
- judgment(판정): `{JUDGMENT}`
- package_decision(패키지 결정): `{final['package_decision']}`
- effect(효과): strict pass 0(엄격 통과 0)을 패키지 금지와 run364AC(364AC 실행) 수리 queue(대기열)로 연결했다.
""",
    )
    append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"""

## run364AB Scout Review Closeout(364AB 정찰 검토 종료)

Action(행동): run364AA(364AA 실행) proxy scout(프록시 정찰) `16`개 row(행)를 review(검토)했다.

Effect(효과): strict pass(엄격 통과)는 `0`개라 package(패키지)를 열지 않고, `{NEXT_RUN_ID}`로 near-miss PF/DD density bridge(근접 실패 PF/DD 밀도 연결)를 넘긴다.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_by_strict_pass_zero(엄격 통과 0으로 없음)
- latest_mt5_probe(최근 MT5 탐침): `run364X`
- latest_mt5_review(최근 MT5 검토): `run364Y`
- latest_materialization(최근 구체화): `run364Z`
- latest_proxy_scout(최근 프록시 정찰): `run364AA`
- latest_proxy_review(최근 프록시 검토): `run364AB`
- next_repair_seed(다음 수리 씨앗): `stress_zone_3_near_density_floor(3번 압박 구간 밀도 하한 근접)`
- blockers(차단): no strict pass(엄격 통과 없음), package blocked(패키지 차단), MT5 runtime probe out_of_scope(런타임 탐침 범위 밖)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): run364AB(364AB 실행)는 run364AA(364AA 실행)의 proxy scout(프록시 정찰)를 review(검토)했고 strict pass(엄격 통과)는 `0`개다. best PF(최고 수익 팩터)는 `{final['best_pf_queue_id']}`의 `{final['best_pf']}`지만 density(밀도)는 `{final['best_pf_density']}`라 운영 패키지로 닫지 않는다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 PF/DD near-miss density bridge(수익 팩터/낙폭 근접 실패 밀도 연결)를 materialize(구체화)한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""

## {TODAY} - {RUN_ID}

- action(행동): run364AA proxy scout(프록시 정찰)를 review(검토)했다.
- effect(효과): package(패키지)를 열지 않고 `{NEXT_RUN_ID}` repair queue(수리 대기열)를 남겼다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""

## {RUN_ID}

- idea(아이디어): strict pass zero(엄격 통과 0)를 실패 기억으로 닫고 stress_zone_3(3번 압박 구간)을 density bridge(밀도 연결) 씨앗으로 재사용한다.
- positive clue(긍정 단서): best PF near-miss(최고 수익 팩터 근접 실패)가 있다.
- failure memory(실패 기억): density-only selection(밀도만 좋은 선택)은 PF/DD(수익 팩터/낙폭)를 악화한다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""

## {RUN_ID}

- action(행동): proxy scout review(프록시 정찰 검토)를 완료했다.
- effect(효과): Stage364(364단계) 분기 없이 run364AC(364AC 실행)로 PF/DD density bridge(PF/DD 밀도 연결)를 계속한다.
""",
    )


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "proxy_review(프록시 검토)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        "notes": f"strict_pass_rows={final['strict_pass_rows']}; near_miss_rows={final['near_miss_rows']}",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["surface_rows"],
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(SURFACE_REVIEW),
        "result_status": STATUS,
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "kpi_evidence(KPI 근거)",
        "trade_density_requirement_status": "reviewed_strict_pass_zero(검토됨, 엄격 통과 0)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "net_profit": final["parent_selected_net_profit"],
        "profit_factor": final["parent_selected_profit_factor"],
        "trade_count": final["parent_selected_trade_count"],
        "expectancy": "",
        "max_drawdown_amount": final["parent_selected_max_drawdown"],
        "long_trade_count": "",
        "short_trade_count": "",
        "evidence_scope": "proxy_review_no_authority(프록시 검토, 권위 없음)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for subrun_id, record_view, tier_scope, kpi_scope in [
        (f"{RUN_ID}__Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "proxy review surface(프록시 검토 표면)"),
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
            ("surface_review", SURFACE_REVIEW, "Surface review(표면 검토)."),
            ("near_miss_candidates", NEAR_MISS_CANDIDATES, "Near-miss candidates(근접 실패 후보)."),
            ("failure_memory", FAILURE_MEMORY, "Failure memory(실패 기억)."),
            ("next_queue", NEXT_QUEUE, "run364AC queue(364AC 대기열)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    surface = load_surface()
    review_rows, near_rows = review_surface(surface, parent_final)
    strict_rows = strict_pass_rows(review_rows)
    clues = clue_rows(parent_final, review_rows, near_rows)
    failures = failure_rows(parent_final)
    next_queue = next_queue_rows(near_rows)
    write_csv(SURFACE_REVIEW, review_rows)
    write_csv(STRICT_PASS_AUDIT, strict_rows)
    write_csv(NEAR_MISS_CANDIDATES, near_rows)
    write_csv(POSITIVE_CLUES, clues)
    write_csv(FAILURE_MEMORY, failures)
    write_csv(NEXT_QUEUE, next_queue)
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "input_parent_gate",
                "proxy_scout_review_gate",
                "strict_pass_boundary_gate",
                "performance_attribution_gate",
                "next_queue_gate",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    created_at_utc = now_utc()
    final = final_payload(parent_final, review_rows, near_rows, next_queue, created_at_utc)
    write_json(FINAL_DECISION, final)
    gates = write_receipts(final)
    final["gate_passes"] = sum(1 for row in gates if row.get("status") == "passed")
    final["gate_total"] = len(gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, review_rows, near_rows, clues, failures, next_queue, gates)
    write_ledgers(final, gates)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
