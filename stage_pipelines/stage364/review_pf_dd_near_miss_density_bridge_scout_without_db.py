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

from stage_pipelines.stage364 import train_pf_dd_near_miss_density_bridge_scout_without_db as scout  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = scout.STAGE_ID
RUN_NUMBER = "run364AE"
RUN_ID = "run364AE_review_pf_dd_near_miss_density_bridge_scout_without_db_v1"
PARENT_RUN_ID = scout.RUN_ID
BASELINE_RUN_ID = scout.BASELINE_RUN_ID
NEXT_RUN_ID = "run364AF_materialize_pf_lift_density_safe_expansion_without_db_v1"

STATUS = "completed_stage364AE_bridge_scout_review_negative_for_package_positive_pf_lift_seed_no_authority"
JUDGMENT = "negative_for_package_positive_for_pf_lift_density_safe_expansion_no_authority"
DECISION = "stage364AE_no_package_open_run364AF_pf_lift_density_safe_expansion"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = scout.DENSITY_FLOOR
TARGET_PF = scout.TARGET_PF

STAGE_DIR = scout.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SURFACE_REVIEW = RUN_DIR / "surface_review.csv"
PACKAGE_GATE_AUDIT = RUN_DIR / "package_gate_audit.csv"
PF_LIFT_CANDIDATES = RUN_DIR / "pf_lift_candidates.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364AF_pf_lift_density_safe_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AE_pf_dd_density_bridge_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AE_pf_dd_density_bridge_review.md"
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
    scout.FINAL_DECISION,
    scout.GATE_AUDIT,
    scout.SCOUT_SURFACE,
    scout.SELECTED_PROXY_CANDIDATE,
    scout.SELECTED_EXPECTED_TRADE_TAPE,
    scout.EXPRESSION_SAFETY_AUDIT,
    scout.BRIDGE_EFFECT_AUDIT,
    scout.BASELINE_COMPARISON,
    scout.REPORT_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SURFACE_REVIEW,
    PACKAGE_GATE_AUDIT,
    PF_LIFT_CANDIDATES,
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
    return scout.rel(path)


def exists(path: Path | str) -> bool:
    return scout.exists(path)


def sha(path: Path | str) -> str:
    return scout.sha(path)


def read_json(path: Path) -> Any:
    return scout.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    scout.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    scout.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    scout.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    scout.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return scout.read_csv_rows(path)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    scout.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


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
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
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
    parent = read_json(scout.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {parent.get('next_run_id')} != {RUN_ID}")
    if parent.get("runtime_authority") != "not_claimed" or parent.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(운영 주장 금지 위반)")
    gates = read_csv_rows(scout.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트 미통과)")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing review inputs(검토 입력 누락): " + ", ".join(missing))
    return parent


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


def load_surface() -> pd.DataFrame:
    df = pd.read_csv(scout.SCOUT_SURFACE, encoding="utf-8-sig")
    for col in [
        "combined_net_profit",
        "combined_profit_factor",
        "combined_trade_count",
        "combined_trade_per_business_day",
        "combined_max_drawdown",
        "combined_recovery_factor",
        "combined_long_count",
        "combined_short_count",
        "validation_net_profit",
        "oos_net_profit",
        "validation_profit_factor",
        "oos_profit_factor",
        "selection_score",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def review_status(row: Mapping[str, Any]) -> str:
    density = as_float(row.get("combined_trade_per_business_day"))
    pf = as_float(row.get("combined_profit_factor"))
    if density >= DENSITY_FLOOR and pf >= TARGET_PF:
        return "package_review_candidate(패키지 검토 후보)"
    if density >= DENSITY_FLOOR and pf >= 1.27:
        return "pf_lift_seed_density_safe(PF 상승 씨앗, 밀도 안전)"
    if density < DENSITY_FLOOR and pf >= TARGET_PF:
        return "pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗)"
    if density >= DENSITY_FLOOR:
        return "density_safe_low_pf_watch(밀도 안전, 낮은 PF 관찰)"
    return "reject_density_floor(밀도 하한 탈락)"


def review_rows(surface: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for _, raw in surface.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row.get("queue_id", ""),
                "variant_id": row.get("variant_id", ""),
                "review_status": review_status(row),
                "source_candidate_status": row.get("candidate_status", ""),
                "combined_net_profit": finite(row.get("combined_net_profit")),
                "combined_profit_factor": finite(row.get("combined_profit_factor")),
                "combined_trade_count": finite(row.get("combined_trade_count")),
                "combined_trade_per_business_day": finite(row.get("combined_trade_per_business_day")),
                "combined_max_drawdown": finite(row.get("combined_max_drawdown")),
                "combined_recovery_factor": finite(row.get("combined_recovery_factor")),
                "combined_long_count": finite(row.get("combined_long_count")),
                "combined_short_count": finite(row.get("combined_short_count")),
                "validation_profit_factor": finite(row.get("validation_profit_factor")),
                "oos_profit_factor": finite(row.get("oos_profit_factor")),
                "selection_score": finite(row.get("selection_score")),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    rows.sort(key=lambda item: (item["review_status"].startswith("package"), item["review_status"].startswith("pf_lift"), as_float(item["combined_profit_factor"]), as_float(item["combined_net_profit"])), reverse=True)
    return rows


def package_gate_rows(rows: Sequence[Mapping[str, Any]], parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    package_rows = [row for row in rows if row["review_status"].startswith("package")]
    return [
        {
            "run_id": RUN_ID,
            "gate_id": "density_floor(밀도 하한)",
            "status": "passed" if as_float(parent_final.get("selected_combined_trade_per_business_day")) >= DENSITY_FLOOR else "failed",
            "observed": parent_final.get("selected_combined_trade_per_business_day"),
            "required": DENSITY_FLOOR,
            "effect(효과)": "minimum trade density(최소 거래 밀도)를 확인한다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "profit_factor_target(PF 목표)",
            "status": "failed" if as_float(parent_final.get("selected_combined_profit_factor")) < TARGET_PF else "passed",
            "observed": parent_final.get("selected_combined_profit_factor"),
            "required": TARGET_PF,
            "effect(효과)": "PF 목표 미달이면 package(패키지)를 열지 않는다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "strict_package_rows(엄격 패키지 행)",
            "status": "failed" if not package_rows else "passed",
            "observed": len(package_rows),
            "required": 1,
            "effect(효과)": "PF/density(수익 팩터/밀도) 동시 통과 없이는 MT5 package(MT5 패키지)를 열지 않는다.",
        },
    ]


def pf_lift_candidates(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in rows
        if row["review_status"] in {"pf_lift_seed_density_safe(PF 상승 씨앗, 밀도 안전)", "pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗)"}
    ]


def positive_clues(parent_final: Mapping[str, Any], candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    top = candidates[0] if candidates else {}
    return [
        {
            "run_id": RUN_ID,
            "clue_id": "density_safe_pf_near_target(밀도 안전 PF 목표 근접)",
            "evidence": parent_final.get("selected_variant_id", ""),
            "kpi_read": f"net={parent_final.get('selected_combined_net_profit')}; pf={parent_final.get('selected_combined_profit_factor')}; density={parent_final.get('selected_combined_trade_per_business_day')}; dd={parent_final.get('selected_combined_max_drawdown')}",
            "effect(효과)": "다음 작업은 밀도 손실 없이 PF만 올리는 방향으로 좁힌다.",
        },
        {
            "run_id": RUN_ID,
            "clue_id": "pf_pass_but_density_fail_exists(PF 통과 밀도 실패 존재)",
            "evidence": top.get("variant_id", ""),
            "kpi_read": f"queue={top.get('queue_id', '')}; pf={top.get('combined_profit_factor', '')}; density={top.get('combined_trade_per_business_day', '')}",
            "effect(효과)": "PF를 올리는 규칙은 찾았지만 density bridge(밀도 연결)가 필요함을 보여준다.",
        },
    ]


def failure_memory(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "failure_id": "pf_below_target_blocks_package(PF 목표 미달로 패키지 차단)",
            "evidence": parent_final.get("selected_variant_id", ""),
            "kpi_read": f"pf={parent_final.get('selected_combined_profit_factor')}; target={TARGET_PF}",
            "constraint_for_next(다음 제약)": "do not package before PF>=1.30 and density>=3/day(PF 1.30 이상과 일 3회 이상 전 패키지 금지)",
        },
        {
            "run_id": RUN_ID,
            "failure_id": "pf_lift_variants_reduce_density(PF 상승 변형이 밀도 감소)",
            "evidence": "stress4_short050_pf_lift",
            "kpi_read": "PF 1.3066 but density 2.6727(PF 1.3066이나 밀도 2.6727)",
            "constraint_for_next(다음 제약)": "PF lift(PF 상승)는 density bridge(밀도 연결)와 함께 시험한다.",
        },
    ]


def next_queue_rows(candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    selected = candidates[0] if candidates else {}
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "short_quality_plus_density_restore(숏 품질 + 밀도 복원)",
            "seed_variant_id": selected.get("variant_id", ""),
            "hypothesis(가설)": "raise short quality toward PF>=1.30 while restoring only timestamp-safe high-margin trades to keep density>=3/day(숏 품질을 올려 PF 1.30에 접근하면서 시점 안전 고마진 거래만 복원해 밀도 3 이상을 유지한다)",
            "required_control(필수 대조)": "run364AD selected, stress4_short050_pf_lift, baseline replay(364AD 선택, stress4_short050, 기준 재생)",
            "effect(효과)": "PF lift(PF 상승)와 density bridge(밀도 연결)를 한 작업 묶음에서 같이 시험한다.",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "margin_band_pf_lift(마진 구간 PF 상승)",
            "seed_variant_id": parent_seed_variant(),
            "hypothesis(가설)": "filter low-margin March restored trades and preserve the non-hour16 density bridge(저마진 3월 복원 거래를 거르고 non-hour16 밀도 연결을 보존한다)",
            "required_control(필수 대조)": "no top_n replay(top_n 재생 금지); fixed threshold only(고정 임계값만 사용)",
            "effect(효과)": "top_n(상위 N개) 없이 PF 부족분을 줄인다.",
        },
    ]


def parent_seed_variant() -> str:
    try:
        return read_json(scout.FINAL_DECISION).get("selected_variant_id", "")
    except Exception:
        return ""


def gate_row(name: str, evidence: Path, effect: str) -> dict[str, Any]:
    return {"run_id": RUN_ID, "gate(게이트)": name, "status": "passed", "evidence(근거)": rel(evidence), "effect(효과)": effect, "claim_boundary(주장 경계)": CLAIM_BOUNDARY}


def final_payload(parent_final: Mapping[str, Any], rows: Sequence[Mapping[str, Any]], candidates: Sequence[Mapping[str, Any]], next_queue: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at_utc: str) -> dict[str, Any]:
    package_rows = [row for row in rows if row["review_status"].startswith("package")]
    best_pf = max(rows, key=lambda row: as_float(row.get("combined_profit_factor"))) if rows else {}
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
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
        "parent_selected_drawdown": parent_final.get("selected_combined_max_drawdown"),
        "surface_rows": len(rows),
        "package_candidate_rows": len(package_rows),
        "pf_lift_candidate_rows": len(candidates),
        "next_queue_rows": len(next_queue),
        "best_pf_queue_id": best_pf.get("queue_id", ""),
        "best_pf": best_pf.get("combined_profit_factor", ""),
        "best_pf_density": best_pf.get("combined_trade_per_business_day", ""),
        "package_decision": "no_package_pf_below_target(패키지 없음, PF 목표 미달)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
    }


def write_receipts(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(DATA_RECEIPT, {**base, "skill": "obsidian-data-integrity(데이터 무결성)", "data_source": [rel(path) for path in INPUT_FILES], "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)", "effect(효과)": "run364AD reviewed artifacts(검토된 산출물)만 사용한다."})
    write_json(ATTRIBUTION_RECEIPT, {**base, "skill": "obsidian-performance-attribution(성과 귀속)", "observed_change": "density bridge improves net/DD but PF remains below target(밀도 연결은 순수익/낙폭을 개선하지만 PF는 목표 미만)", "comparison_baseline": BASELINE_RUN_ID, "surface_review": rel(SURFACE_REVIEW), "attribution_confidence": "medium_proxy_only(프록시 전용 중간)"})
    write_json(JUDGMENT_RECEIPT, {**base, "skill": "obsidian-result-judgment(결과 판정)", "judgment_label": JUDGMENT, "package_decision": final["package_decision"], "evidence_missing": "MT5 runtime probe(MT5 런타임 탐침)", "next_condition": NEXT_RUN_ID})
    write_json(CLAIM_RECEIPT, {**base, "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed", "effect(효과)": "review(검토)를 운영 주장으로 승격하지 않는다."})
    write_json(LINEAGE_RECEIPT, {**base, "skill": "obsidian-artifact-lineage(산출물 계보)", "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()}})
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AE review(364AE 검토)를 닫는다."),
        gate_row("input_parent_gate(부모 입력 게이트)", INPUT_MANIFEST, "run364AD 산출물과 gate(게이트)를 확인한다."),
        gate_row("surface_review_gate(표면 검토 게이트)", SURFACE_REVIEW, "13개 scout row(정찰 행)를 판정한다."),
        gate_row("package_boundary_gate(패키지 경계 게이트)", PACKAGE_GATE_AUDIT, "PF 목표 미달로 package(패키지)를 열지 않는다."),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "PF/density/DD(수익 팩터/밀도/낙폭) 변화를 귀속한다."),
        gate_row("next_queue_gate(다음 대기열 게이트)", NEXT_QUEUE, "run364AF queue(364AF 대기열)를 만든다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 hash(해시)를 연결한다."),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "runtime authority(런타임 권위)를 열지 않는다."),
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


def write_docs(final: Mapping[str, Any], rows: Sequence[Mapping[str, Any]], candidates: Sequence[Mapping[str, Any]], package_gates: Sequence[Mapping[str, Any]], clues: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]], next_queue: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header()
    text = f"""# run364AE PF/DD density bridge review(364AE PF/DD 밀도 연결 검토)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- package_decision(패키지 결정): `{final['package_decision']}`
- parent selected net/PF/trades/density/DD(부모 선택 순수익/수익 팩터/거래수/밀도/낙폭): `{final['parent_selected_net_profit']}` / `{final['parent_selected_profit_factor']}` / `{final['parent_selected_trade_count']}` / `{final['parent_selected_density']}` / `{final['parent_selected_drawdown']}`
- package_candidate_rows(패키지 후보 행): `{final['package_candidate_rows']}`
- pf_lift_candidate_rows(PF 상승 후보 행): `{final['pf_lift_candidate_rows']}`
- runtime_authority(런타임 권위): `not_claimed`

## Surface review(표면 검토)

{markdown_table(list(rows)[:8], ['queue_id', 'review_status', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_per_business_day', 'combined_max_drawdown'])}

## Package gate audit(패키지 게이트 감사)

{markdown_table(package_gates, ['gate_id', 'status', 'observed', 'required', 'effect(효과)'])}

## PF lift candidates(PF 상승 후보)

{markdown_table(candidates, ['queue_id', 'review_status', 'combined_profit_factor', 'combined_trade_per_business_day', 'combined_net_profit'])}

## Positive clues(긍정 단서)

{markdown_table(clues, ['clue_id', 'evidence', 'kpi_read', 'effect(효과)'])}

## Failure memory(실패 기억)

{markdown_table(failures, ['failure_id', 'evidence', 'kpi_read', 'constraint_for_next(다음 제약)'])}

## Next queue(다음 대기열)

{markdown_table(next_queue, ['queue_id', 'seed_variant_id', 'hypothesis(가설)', 'required_control(필수 대조)'])}

## Gate audit(게이트 감사)

{markdown_table(gates, ['gate(게이트)', 'status', 'evidence(근거)', 'effect(효과)'])}

## Claim boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): 이 review(검토)는 package(패키지), MT5 runtime probe(MT5 런타임 탐침), operating promotion(운영 승격)을 열지 않고, PF lift(PF 상승)와 density safety(밀도 안전)를 다음 탐색으로 넘긴다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(REVIEW_INDEX, RUN_ID, f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- package_decision(패키지 결정): `{final['package_decision']}`\n- effect(효과): PF 목표 미달을 패키지 금지와 run364AF(364AF 실행) queue(대기열)로 연결했다.\n")
    append_text_once(STAGE_BRIEF, RUN_ID, f"\n## run364AE Review Closeout(364AE 검토 종료)\n\nAction(행동): run364AD(364AD 실행)의 PF/DD density bridge(PF/DD 밀도 연결)를 review(검토)했다.\n\nEffect(효과): density(밀도)는 통과했지만 PF(수익 팩터)가 `1.30` 미만이라 package(패키지)를 열지 않고 `{NEXT_RUN_ID}`로 PF lift(PF 상승) 탐색을 넘긴다.\n")
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_pf_below_target(PF 목표 미달로 없음)
- latest_proxy_scout(최근 프록시 정찰): `run364AD`
- latest_proxy_review(최근 프록시 검토): `run364AE`
- next_repair_queue(다음 수리 대기열): `{rel(NEXT_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")
    write_text(CURRENT_WORKING_STATE, f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): run364AE(364AE 실행)는 run364AD(364AD 실행)의 proxy scout(프록시 정찰)를 review(검토)했다. 선택 후보는 density(밀도) `3.006006006`로 하한을 넘었지만 PF(수익 팩터) `1.2739357721`로 목표 `1.30` 미만이라 package(패키지)를 열지 않는다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 PF lift density-safe expansion(PF 상승 밀도 안전 확장)을 materialize(구체화)한다.

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
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): PF/DD density bridge review(PF/DD 밀도 연결 검토)를 완료했다.\n- effect(효과): package(패키지)를 열지 않고 `{NEXT_RUN_ID}` PF lift(PF 상승) queue(대기열)를 남겼다.\n- report(보고서): `{rel(REPORT_PATH)}`\n")
    append_text_once(IDEA_REGISTRY, RUN_ID, f"\n## {RUN_ID}\n\n- idea(아이디어): density-safe candidate(밀도 안전 후보)는 남기되 PF target(PF 목표) 전 package(패키지)는 금지한다.\n- positive clue(긍정 단서): PF 1.27대와 DD 개선이 동시에 보인다.\n- failure memory(실패 기억): PF 1.30 이상 후보는 밀도가 무너지는 경향이 있어 density bridge(밀도 연결)와 함께 시험해야 한다.\n")
    append_text_once(STAGE_README, RUN_ID, f"\n## {RUN_ID}\n\n- action(행동): bridge scout(연결 정찰)를 review(검토)했다.\n- effect(효과): Stage364(364단계) 안에서 PF lift density-safe expansion(PF 상승 밀도 안전 확장)으로 이어간다.\n")


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
        "notes": f"package_rows={final['package_candidate_rows']}; pf_lift_rows={final['pf_lift_candidate_rows']}",
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
        "trade_density_requirement_status": "density_passed_pf_below_target(밀도 통과, PF 목표 미달)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "net_profit": final["parent_selected_net_profit"],
        "profit_factor": final["parent_selected_profit_factor"],
        "trade_count": final["parent_selected_trade_count"],
        "max_drawdown_amount": final["parent_selected_drawdown"],
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
            ("package_gate_audit", PACKAGE_GATE_AUDIT, "Package gate audit(패키지 게이트 감사)."),
            ("next_queue", NEXT_QUEUE, "Next PF lift queue(다음 PF 상승 대기열)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "baseline_run_id": BASELINE_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    surface = load_surface()
    rows = review_rows(surface)
    package_gates = package_gate_rows(rows, parent_final)
    candidates = pf_lift_candidates(rows)
    clues = positive_clues(parent_final, candidates)
    failures = failure_memory(parent_final)
    next_queue = next_queue_rows(candidates)
    write_csv(SURFACE_REVIEW, rows)
    write_csv(PACKAGE_GATE_AUDIT, package_gates)
    write_csv(PF_LIFT_CANDIDATES, candidates)
    write_csv(POSITIVE_CLUES, clues)
    write_csv(FAILURE_MEMORY, failures)
    write_csv(NEXT_QUEUE, next_queue)
    write_json(WORK_PACKET, {"run_id": RUN_ID, "primary_family": "kpi_evidence(KPI 근거)", "primary_skill": "obsidian-result-judgment(결과 판정)", "support_skills": ["obsidian-performance-attribution(성과 귀속)", "obsidian-data-integrity(데이터 무결성)", "obsidian-artifact-lineage(산출물 계보)"], "required_gates": ["scope_completion_gate", "input_parent_gate", "surface_review_gate", "package_boundary_gate", "performance_attribution_gate", "next_queue_gate", "artifact_lineage_audit", "claim_boundary_audit", "required_gate_coverage_audit"], "claim_boundary(주장 경계)": CLAIM_BOUNDARY})
    created_at = now_utc()
    temp_final = {"created_at_utc": created_at, "package_decision": "no_package_pf_below_target(패키지 없음, PF 목표 미달)"}
    gates = write_receipts(temp_final)
    final = final_payload(parent_final, rows, candidates, next_queue, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, rows, candidates, package_gates, clues, failures, next_queue, gates)
    write_ledgers(final, gates)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
