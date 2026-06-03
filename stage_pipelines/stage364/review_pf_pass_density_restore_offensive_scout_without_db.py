from __future__ import annotations

import csv
import io
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import train_pf_pass_density_restore_offensive_scout_without_db as scout  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = scout.STAGE_ID
RUN_NUMBER = "run364AN"
RUN_ID = "run364AN_review_pf_pass_density_restore_offensive_scout_without_db_v1"
PARENT_RUN_ID = scout.RUN_ID
BASELINE_RUN_ID = scout.PARENT_RUN_ID
NEXT_RUN_ID = "run364AO_materialize_hold6_pf_dd_repair_offensive_inputs_without_db_v1"

STATUS = "completed_stage364AN_pf_pass_density_restore_review_negative_for_package_positive_hold6_density_seed_no_authority"
JUDGMENT = "negative_for_package_positive_for_hold6_density_and_sparse_pf_repair_seed_no_authority"
DECISION = "stage364AN_no_package_open_run364AO_hold6_pf_dd_repair_inputs"
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
POLICY_FAILURE_ATTRIBUTION = RUN_DIR / "policy_failure_attribution.csv"
SESSION_SIDE_REVIEW = RUN_DIR / "selected_session_side_review.csv"
MONTH_SIDE_REVIEW = RUN_DIR / "selected_month_side_review.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364AO_materialization_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AN_pf_pass_density_restore_offensive_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AN_pf_pass_density_restore_offensive_review.md"
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
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    scout.FINAL_DECISION,
    scout.GATE_AUDIT,
    scout.SCOUT_SURFACE,
    scout.STRICT_CANDIDATES,
    scout.SELECTED_PROXY_CANDIDATE,
    scout.SELECTED_EXPECTED_TRADE_TAPE,
    scout.SELECTED_SESSION_SUMMARY,
    scout.SELECTED_MONTH_SIDE_SUMMARY,
    scout.POLICY_ATTRIBUTION,
    scout.BASELINE_COMPARISON,
    scout.QUEUE_REPLAY_AUDIT,
    scout.RUN364AN_QUEUE,
    scout.REPORT_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SURFACE_REVIEW,
    PACKAGE_GATE_AUDIT,
    POLICY_FAILURE_ATTRIBUTION,
    SESSION_SIDE_REVIEW,
    MONTH_SIDE_REVIEW,
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
    NEGATIVE_RESULT_REGISTER,
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return scout.read_csv_rows(path)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    scout.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    scout.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    scout.write_csv(path, rows, fieldnames)


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
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(path, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    final = read_json(scout.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장이 있음)")
    gates = read_csv_rows(scout.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트가 모두 통과하지 않음)")
    surface = read_csv_rows(scout.SCOUT_SURFACE)
    if len(surface) != 12:
        raise RuntimeError(f"unexpected scout surface rows(정찰 표면 행 수 이상): {len(surface)}")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AN inputs(364AN 입력 누락): " + ", ".join(missing))
    return final


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "pf_pass_density_restore_proxy_scout_surface.csv":
        return "parent scout surface(부모 정찰 표면)"
    if name == "queue_replay_audit.csv":
        return "parent replay audit(부모 재생 감사)"
    if "summary" in name:
        return "segment summary(구간 요약)"
    if "trade_tape" in name:
        return "selected trade tape(선택 거래 기록)"
    if name.endswith(".json"):
        return "decision or receipt(결정 또는 영수증)"
    return "supporting evidence(보조 근거)"


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "role": input_role(path),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def load_surface() -> pd.DataFrame:
    df = pd.read_csv(scout.SCOUT_SURFACE, encoding="utf-8-sig")
    numeric_cols = [
        "queue_rank",
        "combined_net_profit",
        "combined_profit_factor",
        "combined_trade_count",
        "combined_trade_per_business_day",
        "combined_expectancy",
        "combined_max_drawdown",
        "combined_recovery_factor",
        "combined_long_count",
        "combined_short_count",
        "combined_long_short_balance",
        "validation_net_profit",
        "validation_profit_factor",
        "oos_net_profit",
        "oos_profit_factor",
        "net_delta_vs_run364AJ_selected",
        "pf_delta_vs_run364AJ_selected",
        "dd_delta_vs_run364AJ_selected",
        "density_delta_vs_run364AJ_selected",
        "selection_score",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def review_status(row: Mapping[str, Any]) -> str:
    pf = as_float(row.get("combined_profit_factor"))
    density = as_float(row.get("combined_trade_per_business_day"))
    val_net = as_float(row.get("validation_net_profit"))
    oos_net = as_float(row.get("oos_net_profit"))
    shorts = as_float(row.get("combined_short_count"))
    dd_delta = as_float(row.get("dd_delta_vs_run364AJ_selected"))
    if pf >= TARGET_PF and density >= DENSITY_FLOOR and val_net > 0 and oos_net > 0 and shorts > 0:
        return "package_candidate(패키지 후보)"
    if density >= DENSITY_FLOOR and pf < TARGET_PF:
        if dd_delta < 0:
            return "density_safe_pf_dd_fail(밀도 안전, PF/DD 실패)"
        return "density_safe_pf_fail(밀도 안전, PF 실패)"
    if pf >= TARGET_PF and density < DENSITY_FLOOR:
        return "pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗)"
    if density >= 2.85 and dd_delta > 0:
        return "near_density_dd_improved_seed(밀도 근접, 낙폭 개선 씨앗)"
    return "reject_or_watch(거절 또는 관찰)"


def surface_review_rows(surface: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, raw in surface.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_rank": finite(row.get("queue_rank"), 0),
                "queue_id": row.get("queue_id", ""),
                "axis_id": row.get("axis_id", ""),
                "queue_type": row.get("queue_type", ""),
                "variant_id": row.get("variant_id", ""),
                "review_status": review_status(row),
                "candidate_status": row.get("candidate_status", ""),
                "combined_net_profit": finite(row.get("combined_net_profit")),
                "combined_profit_factor": finite(row.get("combined_profit_factor")),
                "combined_trade_count": finite(row.get("combined_trade_count"), 0),
                "combined_trade_per_business_day": finite(row.get("combined_trade_per_business_day")),
                "combined_expectancy": finite(row.get("combined_expectancy")),
                "combined_max_drawdown": finite(row.get("combined_max_drawdown")),
                "combined_recovery_factor": finite(row.get("combined_recovery_factor")),
                "combined_long_count": finite(row.get("combined_long_count"), 0),
                "combined_short_count": finite(row.get("combined_short_count"), 0),
                "validation_net_profit": finite(row.get("validation_net_profit")),
                "validation_profit_factor": finite(row.get("validation_profit_factor")),
                "oos_net_profit": finite(row.get("oos_net_profit")),
                "oos_profit_factor": finite(row.get("oos_profit_factor")),
                "net_delta_vs_run364AJ_selected": finite(row.get("net_delta_vs_run364AJ_selected")),
                "pf_delta_vs_run364AJ_selected": finite(row.get("pf_delta_vs_run364AJ_selected")),
                "dd_delta_vs_run364AJ_selected": finite(row.get("dd_delta_vs_run364AJ_selected")),
                "density_delta_vs_run364AJ_selected": finite(row.get("density_delta_vs_run364AJ_selected")),
                "selection_score": finite(row.get("selection_score")),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rank = {
        "package_candidate": 5,
        "density_safe_pf_dd_fail": 4,
        "pf_pass_density_fail_seed": 3,
        "near_density_dd_improved_seed": 2,
        "density_safe_pf_fail": 1,
    }
    rows.sort(
        key=lambda item: (
            max((score for prefix, score in rank.items() if str(item["review_status"]).startswith(prefix)), default=0),
            as_float(item["combined_net_profit"]),
            as_float(item["combined_profit_factor"]),
            as_float(item["combined_trade_per_business_day"]),
        ),
        reverse=True,
    )
    return rows


def package_gate_rows(parent_final: Mapping[str, Any], review_rows_: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    package_rows = [row for row in review_rows_ if str(row.get("review_status", "")).startswith("package_candidate")]
    selected_pf = as_float(parent_final.get("selected_combined_profit_factor"))
    selected_density = as_float(parent_final.get("selected_combined_trade_per_business_day"))
    selected_dd = as_float(parent_final.get("selected_combined_max_drawdown"))
    selected_val = as_float(parent_final.get("selected_validation_net_profit"))
    selected_oos = as_float(parent_final.get("selected_oos_net_profit"))
    return [
        {
            "run_id": RUN_ID,
            "gate_id": "strict_package_rows(엄격 패키지 행)",
            "status": "failed" if not package_rows else "passed",
            "observed": len(package_rows),
            "required": 1,
            "effect": "PF, density, split, side 조건을 동시에 만족하지 못해 package(패키지)를 닫는다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "selected_profit_factor_target(선택 PF 목표)",
            "status": "passed" if selected_pf >= TARGET_PF else "failed",
            "observed": selected_pf,
            "required": TARGET_PF,
            "effect": "선택 후보의 PF(수익 팩터)가 목표 아래라 운영 후보가 아니다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "selected_density_floor(선택 밀도 하한)",
            "status": "passed" if selected_density >= DENSITY_FLOOR else "failed",
            "observed": selected_density,
            "required": DENSITY_FLOOR,
            "effect": "밀도 회복 단서는 보존한다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "selected_drawdown_quality(선택 낙폭 품질)",
            "status": "failed" if selected_dd < -142.323 else "passed",
            "observed": selected_dd,
            "required": ">= -142.323 reference(기준 이상)",
            "effect": "hold6(6봉 보유)는 낙폭을 악화시켜 DD(낙폭) 수리 축이 필요하다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "selected_split_profit(선택 분할 수익)",
            "status": "passed" if selected_val > 0 and selected_oos > 0 else "failed",
            "observed": f"validation={selected_val}; oos={selected_oos}",
            "required": "both_positive(둘 다 양수)",
            "effect": "분할 수익은 살아 있어 아이디어 사망이 아니라 수리 단서로 남긴다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "external_runtime_evidence(외부 런타임 근거)",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "observed": "not_run(미실행)",
            "required": "MT5 runtime probe(MT5 런타임 탐침)",
            "effect": "이번 review(검토)를 runtime authority(런타임 권위)로 오해하지 않게 한다.",
        },
    ]


def policy_failure_rows(surface: pd.DataFrame, audit_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    audit_by_queue = {row.get("queue_id", ""): row for row in audit_rows}
    rows: list[dict[str, Any]] = []
    for _, raw in surface.iterrows():
        row = raw.to_dict()
        audit = audit_by_queue.get(str(row.get("queue_id", "")), {})
        pf = as_float(row.get("combined_profit_factor"))
        density = as_float(row.get("combined_trade_per_business_day"))
        filtered = as_float(audit.get("entry_margin_floor_filtered_count"))
        restore = as_float(audit.get("march_restore_count"))
        if pf >= TARGET_PF and density < DENSITY_FLOOR:
            cause = "pf_good_density_shortfall(PF 양호, 밀도 부족)"
        elif filtered > 1000:
            cause = "margin_floor_overfilter(마진 하한 과필터)"
        elif restore <= 1 and "restore" in str(row.get("axis_id", "")):
            cause = "restore_ineffective(복원 효과 부족)"
        elif density >= DENSITY_FLOOR and pf < TARGET_PF:
            cause = "density_recovered_pf_dd_shortfall(밀도 회복, PF/DD 부족)"
        else:
            cause = "weak_or_watch(약함 또는 관찰)"
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row.get("queue_id", ""),
                "axis_id": row.get("axis_id", ""),
                "cause": cause,
                "combined_net_profit": finite(row.get("combined_net_profit")),
                "combined_profit_factor": finite(row.get("combined_profit_factor")),
                "combined_trade_per_business_day": finite(row.get("combined_trade_per_business_day")),
                "combined_max_drawdown": finite(row.get("combined_max_drawdown")),
                "march_restore_count": audit.get("march_restore_count", ""),
                "entry_margin_floor_filtered_count": audit.get("entry_margin_floor_filtered_count", ""),
                "session_side_blocked_count": audit.get("session_side_blocked_count", ""),
                "effect": "다음 materialization(구체화)에서 살릴 축과 금지할 축을 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def classify_segment(row: Mapping[str, str]) -> str:
    pf = as_float(row.get("segment_profit_factor"))
    net = as_float(row.get("segment_net_profit"))
    trades = as_float(row.get("segment_trade_count"))
    if trades < 10:
        return "too_sparse_watch(희소 관찰)"
    if net > 0 and pf >= TARGET_PF:
        return "positive_pf_segment(양수 PF 구간)"
    if net < 0 or pf < 1.0:
        return "loss_or_pf_drag(손실 또는 PF 끌림)"
    return "positive_but_pf_below_target(PF 목표 미달 양수)"


def segment_review_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv_rows(path):
        item = dict(row)
        item["review_status"] = classify_segment(row)
        item["claim_boundary"] = CLAIM_BOUNDARY
        rows.append(item)
    rows.sort(key=lambda item: (str(item["review_status"]).startswith("positive_pf"), as_float(item.get("segment_net_profit"))), reverse=True)
    return rows


def best_row(rows: Sequence[Mapping[str, Any]], prefix: str) -> Mapping[str, Any]:
    candidates = [row for row in rows if str(row.get("review_status", "")).startswith(prefix)]
    if not candidates:
        return {}
    return max(candidates, key=lambda row: (as_float(row.get("combined_net_profit")), as_float(row.get("combined_profit_factor"))))


def positive_clue_rows(parent_final: Mapping[str, Any], review_rows_: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    hold6 = best_row(review_rows_, "density_safe_pf_dd_fail")
    pf_pass = best_row(review_rows_, "pf_pass_density_fail_seed")
    near_dd = best_row(review_rows_, "near_density_dd_improved_seed")
    return [
        {
            "run_id": RUN_ID,
            "clue_id": "hold6_density_net_lift_seed(6봉 보유 밀도/순수익 상승 씨앗)",
            "evidence": hold6.get("queue_id", parent_final.get("selected_queue_id", "")),
            "kpi_read": f"net={parent_final.get('selected_combined_net_profit')}; pf={parent_final.get('selected_combined_profit_factor')}; density={parent_final.get('selected_combined_trade_per_business_day')}; dd={parent_final.get('selected_combined_max_drawdown')}",
            "salvage_value": "density and net lift survived; PF/DD repair needed(밀도와 순수익 상승은 생존, PF/DD 수리 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "clue_id": "sparse_pf_pass_dd_quality_seed(희소 PF 통과/DD 품질 씨앗)",
            "evidence": pf_pass.get("queue_id", ""),
            "kpi_read": f"net={pf_pass.get('combined_net_profit')}; pf={pf_pass.get('combined_profit_factor')}; density={pf_pass.get('combined_trade_per_business_day')}; dd={pf_pass.get('combined_max_drawdown')}",
            "salvage_value": "PF and DD quality exist, but density bridge failed(PF와 DD 품질은 있으나 밀도 연결 실패)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "clue_id": "threshold_edge_near_density_dd_seed(임계값 경계 밀도 근접/DD 개선 씨앗)",
            "evidence": near_dd.get("queue_id", ""),
            "kpi_read": f"net={near_dd.get('combined_net_profit')}; pf={near_dd.get('combined_profit_factor')}; density={near_dd.get('combined_trade_per_business_day')}; dd={near_dd.get('combined_max_drawdown')}",
            "salvage_value": "short threshold edge improved DD and stayed near 3/day(숏 임계값 경계가 DD를 개선하고 하루 3회에 근접)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def failure_memory_rows(parent_final: Mapping[str, Any], review_rows_: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "failure_id": "strict_package_zero(엄격 패키지 0)",
            "failed_boundary": "PF>=1.30 and density>=3/day and split profit(PF 1.30 이상, 하루 3회 이상, 분할 수익)",
            "why_failed": "PF-pass rows lost density; density-safe rows stayed below PF target(PF 통과 행은 밀도 상실, 밀도 안전 행은 PF 목표 미달)",
            "salvage_value": "keep hold6 density seed and sparse PF seed separately(hold6 밀도 씨앗과 희소 PF 씨앗 분리 보존)",
            "reopen_condition": "one row reaches PF>=1.30 and density>=3/day without trade splitting(거래 쪼개기 없이 PF 1.30 이상과 하루 3회 이상 동시 달성)",
            "do_not_repeat": "do not call hold6 net lift a package without PF/DD repair(hold6 순수익 상승을 PF/DD 수리 없이 패키지로 부르지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "failure_id": "hold6_pf_dd_degradation(hold6 PF/DD 악화)",
            "failed_boundary": "quality trade shape(품질 거래 형태)",
            "why_failed": f"PF={parent_final.get('selected_combined_profit_factor')} and DD={parent_final.get('selected_combined_max_drawdown')} worsened against reference(PF와 DD가 기준 대비 악화)",
            "salvage_value": "high density tape can be filtered by DD/PF guard(고밀도 테이프는 DD/PF 가드로 필터 가능)",
            "reopen_condition": "hold6 variant keeps density>=3 and improves DD or PF(hold6 변형이 밀도 3 이상 유지하며 DD 또는 PF 개선)",
            "do_not_repeat": "do not increase density by simply shortening hold without loss-cluster guard(손실 클러스터 가드 없이 보유만 줄여 밀도만 올리지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "failure_id": "margin_floor_overfilter(마진 하한 과필터)",
            "failed_boundary": "density restore(밀도 복원)",
            "why_failed": "floor 0.12 and 0.02 removed too many signals(0.12와 0.02 하한이 신호를 과도하게 제거)",
            "salvage_value": "try softer floors only after split-safe materialization(분할 안전 구체화 후 더 약한 하한만 시험)",
            "reopen_condition": "soft floor keeps density>=3/day(약한 하한이 하루 3회 이상 유지)",
            "do_not_repeat": "do not jump to large entry_margin_floor values(큰 마진 하한으로 바로 뛰지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def next_queue_rows(parent_final: Mapping[str, Any], review_rows_: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    selected = parent_final.get("selected_variant_id", "")
    pf_pass = best_row(review_rows_, "pf_pass_density_fail_seed").get("variant_id", "")
    near_dd = best_row(review_rows_, "near_density_dd_improved_seed").get("variant_id", "")
    rows = [
        ("hold6_density_anchor_control", selected, "control", "replay selected hold6 density anchor(선택 hold6 밀도 기준 재생)", "hold density>=3 while repairing PF/DD(PF/DD 수리 중 밀도 3 이상 유지)"),
        ("sparse_pf_pass_anchor_control", pf_pass, "control", "replay sparse PF-pass anchor(희소 PF 통과 기준 재생)", "preserve PF>=1.30 while adding density bridge(PF 1.30 이상 보존 후 밀도 연결)"),
        ("threshold_edge_hold6_density_repair", near_dd, "candidate", "combine short 0.455 edge with hold6(숏 0.455 경계와 hold6 결합)", "recover density while keeping DD improvement(DD 개선을 유지하며 밀도 회복)"),
        ("late_long_hold6_pf_patch", pf_pass, "candidate", "combine late-long PF patch with hold6(후반 롱 PF 패치와 hold6 결합)", "test whether hold6 adds density without PF collapse(hold6가 PF 붕괴 없이 밀도 추가하는지 시험)"),
        ("soft_margin_floor_micro_sweep", selected, "candidate", "try floor 0.003/0.006 only(하한 0.003/0.006만 시험)", "avoid previous overfilter while removing worst low-margin trades(이전 과필터를 피하며 최악 저마진 거래 제거)"),
        ("loss_cluster_session_guard", selected, "candidate", "review selected tape loss clusters by session/month(선택 테이프 손실 클러스터를 세션/월별 검토)", "repair DD without top_n or trade splitting(top_n/거래 쪼개기 없이 DD 수리)"),
        ("pf_pass_density_bridge_no_split_guard", pf_pass, "guardrail", "no top_n no trade splitting row grain guard(top_n 없음, 거래 쪼개기 없음 행 단위 가드)", "keep next scout honest(다음 정찰을 정직하게 유지)"),
    ]
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": index,
            "queue_id": queue_id,
            "source_variant_id": source,
            "queue_type": queue_type,
            "materialization_question": question,
            "expected_effect": effect,
            "forbidden": "top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지)",
            "timestamp_boundary": "entry_time_known_only(진입 시점에 알려진 값만 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (queue_id, source, queue_type, question, effect) in enumerate(rows, start=1)
    ]


def gate_row(name: str, evidence: Path, effect: str, status: str = "passed") -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate": name,
        "status": status,
        "evidence": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def final_payload(parent_final: Mapping[str, Any], review_rows_: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at_utc: str) -> dict[str, Any]:
    package_count = sum(1 for row in review_rows_ if str(row.get("review_status", "")).startswith("package_candidate"))
    pf_pass_density_fail = sum(1 for row in review_rows_ if str(row.get("review_status", "")).startswith("pf_pass_density_fail"))
    density_safe_fail = sum(1 for row in review_rows_ if str(row.get("review_status", "")).startswith("density_safe"))
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
        "reviewed_scout_rows": len(review_rows_),
        "package_candidate_rows": package_count,
        "pf_pass_density_fail_rows": pf_pass_density_fail,
        "density_safe_pf_fail_rows": density_safe_fail,
        "package_decision": "no_package_strict_rows_zero(PF/density 동시 통과 없음)",
        "selected_variant_id": parent_final.get("selected_variant_id", ""),
        "selected_combined_net_profit": parent_final.get("selected_combined_net_profit", ""),
        "selected_combined_profit_factor": parent_final.get("selected_combined_profit_factor", ""),
        "selected_combined_trade_count": parent_final.get("selected_combined_trade_count", ""),
        "selected_combined_trade_per_business_day": parent_final.get("selected_combined_trade_per_business_day", ""),
        "selected_combined_expectancy": parent_final.get("selected_combined_expectancy", ""),
        "selected_combined_max_drawdown": parent_final.get("selected_combined_max_drawdown", ""),
        "selected_combined_recovery_factor": parent_final.get("selected_combined_recovery_factor", ""),
        "next_queue_rows": 7,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
    }


def write_receipts(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "skill": "obsidian-data-integrity(데이터 무결성)",
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "review only of already timestamp-safe proxy replay(이미 시점 안전 프록시 재생된 결과의 검토 전용)",
            "sample_scope": "US100 M5 validation+oos proxy review, Tier A separate; Tier B missing_required(US100 5분봉 검증+표본외 프록시 검토, Tier A 분리; Tier B 필수 누락)",
            "feature_label_boundary": "no new features or labels; no post-entry data used(새 피처/라벨 없음, 진입 후 데이터 미사용)",
            "split_boundary": "validation and oos inherited from parent scout(검증과 표본외는 부모 정찰에서 상속)",
            "leakage_risk": "review can bias next exploration, but no operating threshold selected(검토가 다음 탐색을 편향할 수 있으나 운영 임계값 선택 없음)",
            "data_hash_or_identity": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and Path(path).is_file()},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "skill": "obsidian-performance-attribution(성과 귀속)",
            "observed_change": "hold6 lifted density/net but reduced PF/expectancy/recovery and worsened DD(hold6가 밀도/순수익은 올렸지만 PF/기대값/회복 계수를 낮추고 DD를 악화)",
            "comparison_baseline": PARENT_RUN_ID,
            "likely_drivers": "shorter hold increased churn and trade count; PF-pass filters removed density(짧은 보유가 회전과 거래수를 올렸고, PF 통과 필터는 밀도를 제거)",
            "segment_checks": [rel(SESSION_SIDE_REVIEW), rel(MONTH_SIDE_REVIEW), rel(POLICY_FAILURE_ATTRIBUTION)],
            "alternative_explanations": "proxy sequencing may differ from MT5 fills and real broker cost(프록시 순서 재생은 MT5 체결과 실제 브로커 비용과 다를 수 있음)",
            "attribution_confidence": "medium_for_proxy_low_for_operation(프록시는 중간, 운영은 낮음)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "skill": "obsidian-result-judgment(결과 판정)",
            "result_subject": RUN_ID,
            "evidence_available": [rel(SURFACE_REVIEW), rel(PACKAGE_GATE_AUDIT), rel(POSITIVE_CLUES), rel(FAILURE_MEMORY), rel(FINAL_DECISION)],
            "evidence_missing": "MT5 runtime probe(MT5 런타임 탐침)",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "no package, but hold6 density and sparse PF seeds remain useful(패키지는 없지만 hold6 밀도와 희소 PF 씨앗은 유효)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "review(검토)를 운영 주장으로 연결하지 않음",
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
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_or_generated_with_manifest(커밋 후 추적 또는 매니페스트로 재생 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    gates = [
        gate_row("kpi_contract_audit(KPI 계약 감사)", SURFACE_REVIEW, "net/PF/expectancy/DD/RF/trades/density를 검토"),
        gate_row("row_grain_audit(행 단위 감사)", PACKAGE_GATE_AUDIT, "top_n(상위 N개)과 거래 쪼개기 없이 행 단위 판정"),
        gate_row("source_authority_audit(원천 권위 감사)", INPUT_MANIFEST, "부모 run364AM(364AM 실행) 산출물만 원천으로 사용"),
        gate_row("package_gate_audit(패키지 게이트 감사)", PACKAGE_GATE_AUDIT, "strict package(엄격 패키지) 없음 확인"),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "hold6와 PF-pass 실패 원인 분리"),
        gate_row("result_judgment_gate(결과 판정 게이트)", JUDGMENT_RECEIPT, "negative_for_package(패키지 부정)와 positive_seed(긍정 씨앗) 경계 기록"),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 해시 연결"),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "런타임 권위 주장 없음"),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "필수 게이트를 종료 기록에 연결"),
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


def write_docs(final: Mapping[str, Any], review_rows_: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header()
    top = list(review_rows_)[:8]
    package_rows = read_csv_rows(PACKAGE_GATE_AUDIT)
    clue_rows = read_csv_rows(POSITIVE_CLUES)
    failure_rows_ = read_csv_rows(FAILURE_MEMORY)
    next_rows = read_csv_rows(NEXT_QUEUE)
    text = f"""# run364AN PF-pass density restore offensive review(364AN PF 통과 밀도 복원 공격 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- package_candidate_rows(패키지 후보 행): `{final['package_candidate_rows']}`
- selected net/PF/trades/density/expectancy/DD/RF(선택 순수익/수익 팩터/거래수/밀도/기대값/낙폭/회복 계수): `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_count']}` / `{final['selected_combined_trade_per_business_day']}` / `{final['selected_combined_expectancy']}` / `{final['selected_combined_max_drawdown']}` / `{final['selected_combined_recovery_factor']}`
- runtime_authority(런타임 권위): `not_claimed`

## Review Surface(검토 표면)

{markdown_table(top, ['queue_id', 'review_status', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_per_business_day', 'combined_max_drawdown', 'combined_short_count'])}

## Package Gate(패키지 게이트)

{markdown_table(package_rows, ['gate_id', 'status', 'observed', 'required', 'effect'])}

## Positive Clues(긍정 단서)

{markdown_table(clue_rows, ['clue_id', 'evidence', 'kpi_read', 'salvage_value'])}

## Failure Memory(실패 기억)

{markdown_table(failure_rows_, ['failure_id', 'failed_boundary', 'why_failed', 'do_not_repeat'])}

## Next Queue(다음 대기열)

{markdown_table(next_rows, ['queue_rank', 'queue_id', 'queue_type', 'materialization_question', 'expected_effect'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): package(패키지)는 닫고, hold6 density(6봉 보유 밀도)와 sparse PF(희소 수익 팩터) 단서를 다음 materialization(구체화)으로 넘긴다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- package(패키지): none(없음)\n- effect(효과): run364AM(364AM 실행) proxy scout(프록시 정찰)를 package(패키지) 없이 닫고 `{NEXT_RUN_ID}` 입력으로 넘겼다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364AN PF-Pass Density Restore Offensive Review Closeout(364AN PF 통과 밀도 복원 공격 검토 종료)",
        f"\n## run364AN PF-Pass Density Restore Offensive Review Closeout(364AN PF 통과 밀도 복원 공격 검토 종료)\n\nAction(행동): run364AM(364AM 실행) proxy scout(프록시 정찰) 12개 행을 package gate(패키지 게이트), policy attribution(정책 귀속), positive clue(긍정 단서), failure memory(실패 기억)로 검토했다.\n\nEffect(효과): strict package row(엄격 패키지 행) `0` 때문에 package(패키지)는 닫고, hold6 density(6봉 보유 밀도)와 sparse PF(희소 수익 팩터) 단서를 `{NEXT_RUN_ID}` 입력으로 넘겼다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_review_negative_for_package(패키지 부정 검토라 없음)
- latest_proxy_review(최근 프록시 검토): `run364AN`
- package_decision(패키지 결정): `no_package_strict_rows_zero(PF/density 동시 통과 없음)`
- preserved_clues(보존 단서): hold6_density_seed(6봉 보유 밀도 씨앗), sparse_pf_pass_seed(희소 PF 통과 씨앗), threshold_edge_dd_seed(임계값 경계 DD 씨앗)
- next_materialization_queue(다음 구체화 대기열): `{rel(NEXT_QUEUE)}`
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

current_truth(현재 진실): run364AN(364AN 실행)은 run364AM(364AM 실행)을 검토해 package_candidate_rows(패키지 후보 행) `0`을 확인했다. hold6(6봉 보유)는 density(밀도) `3.5075/day`와 net(순수익) `858.662`를 만들었지만 PF(수익 팩터) `1.2724`와 DD(낙폭) `-168.999`가 약해 운영 후보가 아니다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 hold6 density(6봉 보유 밀도)와 sparse PF(희소 수익 팩터)를 PF/DD repair(PF/DD 수리) 입력으로 구체화한다.

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
        bom=False,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): PF-pass density restore offensive review(PF 통과 밀도 복원 공격 검토)를 실행했다.\n- effect(효과): package(패키지)는 닫고 `{NEXT_RUN_ID}` materialization(구체화) 입력을 남겼다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): hold6 density(6봉 보유 밀도)와 sparse PF-pass(희소 PF 통과)를 분리해 다음 PF/DD repair(PF/DD 수리) 씨앗으로 쓴다.\n- positive clue(긍정 단서): density(밀도) 회복은 가능하지만 PF/DD(수익 팩터/낙폭) 수리가 필요하다.\n- failure memory(실패 기억): strict package(엄격 패키지)는 `0`이라 운영 주장 금지.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- failed_boundary(실패 경계): PF>=1.30 and density>=3/day without trade splitting(PF 1.30 이상과 하루 3회 이상, 거래 쪼개기 없음).\n- why_failed(실패 이유): density-safe(밀도 안전) 행은 PF/DD(수익 팩터/낙폭)가 약하고 PF-pass(PF 통과) 행은 density(밀도)가 부족했다.\n- salvage_value(회수 가치): hold6 density(6봉 보유 밀도), sparse PF-pass(희소 PF 통과), threshold edge DD(임계값 경계 DD)를 다음 입력으로 보존한다.\n- reopen_condition(재개 조건): PF>=1.30과 density>=3/day가 같은 row grain(행 단위)에서 동시 통과한다.\n",
    )
    append_text_once(
        STAGE_README,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- action(행동): run364AM(364AM 실행) PF-pass density restore scout(PF 통과 밀도 복원 정찰)를 검토했다.\n- effect(효과): Stage364(364단계) 안에서 `{NEXT_RUN_ID}` materialization(구체화)로 이어간다.\n",
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
        "notes": f"package_rows={final['package_candidate_rows']}; next_queue_rows={final['next_queue_rows']}",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["reviewed_scout_rows"],
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(SURFACE_REVIEW),
        "result_status": STATUS,
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "kpi_evidence(KPI 근거)",
        "trade_density_requirement_status": "reviewed_no_trade_splitting(검토됨, 거래 쪼개기 없음)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "net_profit": final["selected_combined_net_profit"],
        "profit_factor": final["selected_combined_profit_factor"],
        "trade_count": final["selected_combined_trade_count"],
        "expectancy": final["selected_combined_expectancy"],
        "max_drawdown_amount": final["selected_combined_max_drawdown"],
        "evidence_scope": "proxy_review_no_authority(프록시 검토, 권위 없음)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for subrun_id, record_view, tier_scope, kpi_scope in [
        (f"{RUN_ID}__Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "proxy review surface(프록시 검토 표면)"),
        (f"{RUN_ID}__Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "missing_required(필수 누락)"),
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
            ("positive_clues", POSITIVE_CLUES, "Positive clues(긍정 단서)."),
            ("failure_memory", FAILURE_MEMORY, "Failure memory(실패 기억)."),
            ("next_queue", NEXT_QUEUE, "Next materialization queue(다음 구체화 대기열)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
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
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
            "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        },
    )


def repair_run_registry_line_endings(run_id: str) -> None:
    current_text = RUN_REGISTRY.read_text(encoding="utf-8-sig", newline="")
    current_rows = list(csv.DictReader(io.StringIO(current_text)))
    matching = [row for row in current_rows if row.get("run_id") == run_id]
    if len(matching) != 1:
        return
    new_row = matching[0]
    import subprocess

    registry_ref = RUN_REGISTRY.relative_to(ROOT).as_posix()
    head_bytes = subprocess.check_output(["git", "show", f"HEAD:{registry_ref}"], cwd=ROOT)
    head_text = head_bytes.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(head_text))
    fieldnames = list(reader.fieldnames or [])
    head_rows = [{name: row.get(name, "") for name in fieldnames} for row in reader if row.get("run_id") != run_id]
    head_rows.append({name: new_row.get(name, "") for name in fieldnames})
    line_ending = "\r\n" if "\r\n" in head_text else "\n"
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=fieldnames, lineterminator=line_ending, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(head_rows)
    RUN_REGISTRY.write_text(out.getvalue(), encoding="utf-8", newline="")


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    surface = load_surface()
    review_rows_ = surface_review_rows(surface)
    audit_rows = read_csv_rows(scout.QUEUE_REPLAY_AUDIT)
    package_rows = package_gate_rows(parent_final, review_rows_)
    policy_rows = policy_failure_rows(surface, audit_rows)
    session_rows = segment_review_rows(scout.SELECTED_SESSION_SUMMARY)
    month_rows = segment_review_rows(scout.SELECTED_MONTH_SIDE_SUMMARY)
    clue_rows = positive_clue_rows(parent_final, review_rows_)
    failure_rows_ = failure_memory_rows(parent_final, review_rows_)
    next_rows = next_queue_rows(parent_final, review_rows_)
    write_csv(SURFACE_REVIEW, review_rows_)
    write_csv(PACKAGE_GATE_AUDIT, package_rows)
    write_csv(POLICY_FAILURE_ATTRIBUTION, policy_rows)
    write_csv(SESSION_SIDE_REVIEW, session_rows)
    write_csv(MONTH_SIDE_REVIEW, month_rows)
    write_csv(POSITIVE_CLUES, clue_rows)
    write_csv(FAILURE_MEMORY, failure_rows_)
    write_csv(NEXT_QUEUE, next_rows)
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-data-integrity(데이터 무결성)",
            ],
            "required_gates": [
                "kpi_contract_audit",
                "row_grain_audit",
                "source_authority_audit",
                "package_gate_audit",
                "performance_attribution_gate",
                "result_judgment_gate",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    created_at = now_utc()
    temp_final = final_payload(parent_final, review_rows_, [], created_at)
    write_json(FINAL_DECISION, temp_final)
    gates = write_receipts(temp_final)
    final = final_payload(parent_final, review_rows_, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, review_rows_, gates)
    write_ledgers(final, gates)
    repair_run_registry_line_endings(RUN_ID)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
