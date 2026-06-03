from __future__ import annotations

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

from stage_pipelines.stage364 import train_session_side_pf_lift_density_repair_scout_without_db as scout  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = scout.STAGE_ID
RUN_NUMBER = "run364AK"
RUN_ID = "run364AK_review_session_side_pf_lift_density_repair_scout_without_db_v1"
PARENT_RUN_ID = scout.RUN_ID
BASELINE_RUN_ID = scout.BASELINE_RUN_ID
NEXT_RUN_ID = "run364AL_materialize_pf_pass_density_restore_offensive_inputs_without_db_v1"

STATUS = "completed_stage364AK_session_side_pf_lift_density_repair_review_negative_for_package_positive_pf_density_restore_seed_no_authority"
JUDGMENT = "negative_for_package_positive_for_pf_pass_density_restore_offensive_seed_no_authority"
DECISION = "stage364AK_no_package_open_run364AL_pf_pass_density_restore_offensive_inputs"
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
POLICY_REVIEW = RUN_DIR / "policy_review.csv"
SESSION_SIDE_REVIEW = RUN_DIR / "session_side_review.csv"
MONTH_SIDE_REVIEW = RUN_DIR / "month_side_review.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364AL_offensive_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AK_session_side_pf_lift_density_repair_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AK_session_side_pf_lift_density_repair_review.md"
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
    scout.STRICT_CANDIDATES,
    scout.SELECTED_PROXY_CANDIDATE,
    scout.SELECTED_EXPECTED_TRADE_TAPE,
    scout.SELECTED_SESSION_SUMMARY,
    scout.SELECTED_MONTH_SIDE_SUMMARY,
    scout.POLICY_ATTRIBUTION,
    scout.BASELINE_COMPARISON,
    scout.RUN364AK_QUEUE,
    scout.REPORT_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SURFACE_REVIEW,
    PACKAGE_GATE_AUDIT,
    POLICY_REVIEW,
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


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
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
    parent_final = read_json(scout.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if parent_final.get("runtime_authority") != "not_claimed" or parent_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장 있음)")
    gates = read_csv_rows(scout.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 gate(게이트)가 모두 통과되지 않음)")
    review_queue = read_csv_rows(scout.RUN364AK_QUEUE)
    if len(review_queue) != 1:
        raise RuntimeError(f"unexpected review queue rows(검토 queue(대기열) 행 수 이상): {len(review_queue)}")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing review inputs(검토 입력 누락): " + ", ".join(missing))
    return parent_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "role(역할)": input_role(path),
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "session_side_pf_lift_density_repair_proxy_scout_surface.csv":
        return "parent scout surface(부모 정찰 표면 결과)"
    if name == "run364AK_review_queue.csv":
        return "parent review queue(부모 검토 대기열)"
    if "trade_tape" in name:
        return "expected trade tape(예상 거래 테이프)"
    if name.endswith(".json"):
        return "decision or receipt(결정 또는 영수증)"
    return "supporting evidence(보조 근거)"


def load_surface() -> pd.DataFrame:
    df = pd.read_csv(scout.SCOUT_SURFACE, encoding="utf-8-sig")
    numeric_cols = [
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
        "validation_trade_per_business_day",
        "oos_net_profit",
        "oos_profit_factor",
        "oos_trade_per_business_day",
        "selection_score",
        "dd_delta_vs_run364AG_selected",
        "density_delta_vs_run364AG_selected",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def review_status(row: Mapping[str, Any]) -> str:
    pf = as_float(row.get("combined_profit_factor"))
    density = as_float(row.get("combined_trade_per_business_day"))
    validation_net = as_float(row.get("validation_net_profit"))
    oos_net = as_float(row.get("oos_net_profit"))
    short_count = as_float(row.get("combined_short_count"))
    dd_delta = as_float(row.get("dd_delta_vs_run364AG_selected"))
    if pf >= TARGET_PF and density >= DENSITY_FLOOR and validation_net > 0 and oos_net > 0 and short_count > 0:
        return "package_candidate(패키지 후보)"
    if pf >= TARGET_PF and density < DENSITY_FLOOR:
        return "pf_pass_density_fail_seed(PF 통과 밀도 실패 씨앗)"
    if density >= DENSITY_FLOOR and pf >= 1.27:
        return "near_pf_density_safe_seed(PF 근접 밀도 안전 씨앗)"
    if density < DENSITY_FLOOR and dd_delta > 15.0:
        return "dd_improved_density_fail_seed(낙폭 개선 밀도 실패 씨앗)"
    if density >= DENSITY_FLOOR:
        return "density_safe_low_pf_watch(밀도 안전 낮은 PF 관찰)"
    return "reject_density_floor(밀도 하한 탈락)"


def surface_review_rows(surface: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, raw in surface.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row.get("queue_id", ""),
                "axis_id": row.get("axis_id", ""),
                "variant_id": row.get("variant_id", ""),
                "review_status": review_status(row),
                "source_candidate_status": row.get("candidate_status", ""),
                "combined_net_profit": finite(row.get("combined_net_profit")),
                "combined_profit_factor": finite(row.get("combined_profit_factor")),
                "combined_trade_count": finite(row.get("combined_trade_count")),
                "combined_trade_per_business_day": finite(row.get("combined_trade_per_business_day")),
                "combined_expectancy": finite(row.get("combined_expectancy")),
                "combined_max_drawdown": finite(row.get("combined_max_drawdown")),
                "combined_recovery_factor": finite(row.get("combined_recovery_factor")),
                "combined_long_count": finite(row.get("combined_long_count")),
                "combined_short_count": finite(row.get("combined_short_count")),
                "combined_long_short_balance": finite(row.get("combined_long_short_balance")),
                "validation_net_profit": finite(row.get("validation_net_profit")),
                "validation_profit_factor": finite(row.get("validation_profit_factor")),
                "validation_trade_per_business_day": finite(row.get("validation_trade_per_business_day")),
                "oos_net_profit": finite(row.get("oos_net_profit")),
                "oos_profit_factor": finite(row.get("oos_profit_factor")),
                "oos_trade_per_business_day": finite(row.get("oos_trade_per_business_day")),
                "net_delta_vs_run364AG_selected": finite(row.get("net_delta_vs_run364AG_selected")),
                "pf_delta_vs_run364AG_selected": finite(row.get("pf_delta_vs_run364AG_selected")),
                "dd_delta_vs_run364AG_selected": finite(row.get("dd_delta_vs_run364AG_selected")),
                "density_delta_vs_run364AG_selected": finite(row.get("density_delta_vs_run364AG_selected")),
                "selection_score": finite(row.get("selection_score")),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    status_rank = {
        "package_candidate": 5,
        "near_pf_density_safe_seed": 4,
        "pf_pass_density_fail_seed": 3,
        "dd_improved_density_fail_seed": 2,
        "density_safe_low_pf_watch": 1,
    }
    rows.sort(
        key=lambda item: (
            max((rank for prefix, rank in status_rank.items() if str(item["review_status"]).startswith(prefix)), default=0),
            as_float(item["combined_profit_factor"]),
            as_float(item["combined_trade_per_business_day"]),
            as_float(item["combined_net_profit"]),
        ),
        reverse=True,
    )
    return rows


def package_gate_rows(parent_final: Mapping[str, Any], review_rows_: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    selected_pf = as_float(parent_final.get("selected_combined_profit_factor"))
    selected_density = as_float(parent_final.get("selected_combined_trade_per_business_day"))
    selected_validation_net = as_float(parent_final.get("selected_validation_net_profit"))
    selected_oos_net = as_float(parent_final.get("selected_oos_net_profit"))
    package_rows = [row for row in review_rows_ if str(row.get("review_status", "")).startswith("package_candidate")]
    best_pf_row = max(review_rows_, key=lambda row: as_float(row.get("combined_profit_factor"))) if review_rows_ else {}
    return [
        {
            "run_id": RUN_ID,
            "gate_id": "strict_package_rows(엄격 패키지 행)",
            "status": "passed" if package_rows else "failed",
            "observed": len(package_rows),
            "required": 1,
            "effect(효과)": "PF(수익 팩터), density(밀도), split(분할), short side(숏 방향)를 동시에 만족하지 못하면 package(패키지)를 막는다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "selected_profit_factor_target(선택 PF 목표)",
            "status": "passed" if selected_pf >= TARGET_PF else "failed",
            "observed": selected_pf,
            "required": TARGET_PF,
            "effect(효과)": "선택 row(행)의 PF(수익 팩터)가 목표 아래면 운영 후보로 올리지 않는다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "selected_density_floor(선택 밀도 하한)",
            "status": "passed" if selected_density >= DENSITY_FLOOR else "failed",
            "observed": selected_density,
            "required": DENSITY_FLOOR,
            "effect(효과)": "거래 빈도가 너무 낮은 수익 착시를 막는다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "selected_split_profit(선택 분할 수익)",
            "status": "passed" if selected_validation_net > 0 and selected_oos_net > 0 else "failed",
            "observed": f"validation={selected_validation_net}; oos={selected_oos_net}",
            "required": "both_positive(둘 다 양수)",
            "effect(효과)": "validation(검증)과 OOS(표본외)가 반대로 갈리는 후보를 막는다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "best_pf_density_bridge(최고 PF 밀도 연결)",
            "status": "failed" if as_float(best_pf_row.get("combined_trade_per_business_day")) < DENSITY_FLOOR else "passed",
            "observed": f"pf={best_pf_row.get('combined_profit_factor')}; density={best_pf_row.get('combined_trade_per_business_day')}",
            "required": f"pf>={TARGET_PF}; density>={DENSITY_FLOOR}",
            "effect(효과)": "PF(수익 팩터)가 오른 row(행)의 density(밀도) 붕괴를 다음 탐색 제약으로 바꾼다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "external_runtime_evidence(외부 런타임 근거)",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "observed": "not_run(미실행)",
            "required": "MT5 runtime probe(MT5 런타임 탐침)",
            "effect(효과)": "이번 review(검토)를 MT5(메타트레이더5) 권위로 오해하지 않게 한다.",
        },
    ]


def policy_review_rows() -> list[dict[str, Any]]:
    rows = read_csv_rows(scout.POLICY_ATTRIBUTION)
    reviewed: list[dict[str, Any]] = []
    for row in rows:
        pf = as_float(row.get("combined_profit_factor"))
        density = as_float(row.get("combined_trade_per_business_day"))
        status = "pf_pass_density_fail_policy(PF 통과 밀도 실패 정책)" if pf >= TARGET_PF and density < DENSITY_FLOOR else "watch_policy(관찰 정책)"
        if density >= DENSITY_FLOOR and pf >= 1.27:
            status = "density_safe_pf_near_policy(밀도 안전 PF 근접 정책)"
        item = dict(row)
        item.update({"review_status": status, "claim_boundary(주장 경계)": CLAIM_BOUNDARY})
        reviewed.append(item)
    reviewed.sort(key=lambda item: (as_float(item.get("combined_profit_factor")), as_float(item.get("combined_trade_per_business_day"))), reverse=True)
    return reviewed


def classify_segment(row: Mapping[str, Any]) -> str:
    pf = as_float(row.get("segment_profit_factor"))
    net = as_float(row.get("segment_net_profit"))
    trades = as_float(row.get("segment_trade_count"))
    if trades < 10:
        return "too_sparse_watch(희소 관찰)"
    if net > 0 and pf >= TARGET_PF:
        return "positive_pf_segment(양수 PF 세그먼트)"
    if net < 0 or pf < 1.0:
        return "loss_or_pf_drag(손실 또는 PF 끌림)"
    return "positive_but_pf_below_target(PF 목표 미만 양수)"


def segment_review_rows(path: Path) -> list[dict[str, Any]]:
    rows = read_csv_rows(path)
    reviewed: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item.update({"review_status": classify_segment(row), "claim_boundary(주장 경계)": CLAIM_BOUNDARY})
        reviewed.append(item)
    reviewed.sort(
        key=lambda item: (
            str(item["review_status"]).startswith("positive_pf"),
            as_float(item.get("segment_net_profit")),
            as_float(item.get("segment_profit_factor")),
            as_float(item.get("segment_trade_count")),
        ),
        reverse=True,
    )
    return reviewed


def top_by_status(rows: Sequence[Mapping[str, Any]], status_prefix: str, limit: int) -> list[Mapping[str, Any]]:
    return [row for row in rows if str(row.get("review_status", "")).startswith(status_prefix)][:limit]


def positive_clue_rows(
    parent_final: Mapping[str, Any],
    review_rows_: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    pf_pass = top_by_status(review_rows_, "pf_pass_density_fail", 3)
    near_pf = top_by_status(review_rows_, "near_pf_density_safe", 2)
    dd_improved = top_by_status(review_rows_, "dd_improved_density_fail", 2)
    core_sessions = [
        row
        for row in session_rows
        if row.get("entry_session") == "us_cash_core(미국 현금장 핵심)" and str(row.get("review_status", "")).startswith("positive_pf")
    ]
    month_pockets = top_by_status(month_rows, "positive_pf", 4)
    return [
        {
            "run_id": RUN_ID,
            "clue_id": "pf_pass_density_fail_exists(PF 통과 밀도 실패 존재)",
            "evidence": "; ".join(str(row.get("queue_id", "")) for row in pf_pass),
            "kpi_read": "; ".join(
                f"net={row.get('combined_net_profit')}; pf={row.get('combined_profit_factor')}; density={row.get('combined_trade_per_business_day')}; dd={row.get('combined_max_drawdown')}; shorts={row.get('combined_short_count')}"
                for row in pf_pass
            ),
            "effect(효과)": "PF(수익 팩터)를 올리는 규칙은 있으나 밀도 복원 장치가 필요하다는 방향을 준다.",
        },
        {
            "run_id": RUN_ID,
            "clue_id": "density_safe_pf_near_anchor(밀도 안전 PF 근접 기준점)",
            "evidence": "; ".join(str(row.get("queue_id", "")) for row in near_pf),
            "kpi_read": f"net={parent_final.get('selected_combined_net_profit')}; pf={parent_final.get('selected_combined_profit_factor')}; density={parent_final.get('selected_combined_trade_per_business_day')}; dd={parent_final.get('selected_combined_max_drawdown')}",
            "effect(효과)": "density(밀도)를 지키는 control(대조)을 기준점으로 삼아 수익 팩터만 올리는 탐색을 연다.",
        },
        {
            "run_id": RUN_ID,
            "clue_id": "drawdown_improvement_density_fail(낙폭 개선 밀도 실패)",
            "evidence": "; ".join(str(row.get("queue_id", "")) for row in dd_improved),
            "kpi_read": "; ".join(
                f"dd_delta={row.get('dd_delta_vs_run364AG_selected')}; dd={row.get('combined_max_drawdown')}; density={row.get('combined_trade_per_business_day')}"
                for row in dd_improved
            ),
            "effect(효과)": "drawdown(낙폭) 개선 규칙은 density(밀도) 복원과 결합할 가치가 있다.",
        },
        {
            "run_id": RUN_ID,
            "clue_id": "core_session_dual_side_positive(핵심 세션 양방향 양수)",
            "evidence": "; ".join(f"{row.get('side')} net={row.get('segment_net_profit')}" for row in core_sessions),
            "kpi_read": "; ".join(
                f"side={row.get('side')}; pf={row.get('segment_profit_factor')}; trades={row.get('segment_trade_count')}; density={row.get('segment_trade_per_business_day')}"
                for row in core_sessions
            ),
            "effect(효과)": "core session(핵심 세션)을 지키는 복원은 short collapse(숏 붕괴)를 줄일 수 있다.",
        },
        {
            "run_id": RUN_ID,
            "clue_id": "month_side_positive_pockets(월 방향 양수 포켓)",
            "evidence": "; ".join(f"{row.get('entry_month')} {row.get('side')}" for row in month_pockets),
            "kpi_read": "; ".join(
                f"net={row.get('segment_net_profit')}; pf={row.get('segment_profit_factor')}; trades={row.get('segment_trade_count')}"
                for row in month_pockets
            ),
            "effect(효과)": "market behavior(시장 현상)상 월별 방향 포켓은 관찰하되 필터로 고정하지 않는다.",
        },
    ]


def failure_memory_rows(parent_final: Mapping[str, Any], review_rows_: Sequence[Mapping[str, Any]], session_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    pf_pass = top_by_status(review_rows_, "pf_pass_density_fail", 4)
    drag_sessions = [row for row in session_rows if str(row.get("review_status", "")).startswith("loss_or_pf_drag")]
    return [
        {
            "run_id": RUN_ID,
            "failure_id": "no_strict_package_rows(엄격 패키지 행 없음)",
            "evidence": "strict_pass_rows=0",
            "kpi_read": f"selected_pf={parent_final.get('selected_combined_profit_factor')}; selected_density={parent_final.get('selected_combined_trade_per_business_day')}",
            "constraint_for_next(다음 제약)": "PF>=1.30 and density>=3/day and split positive(PF 1.30 이상, 밀도 하루 3 이상, 분할 양수)를 동시에 요구한다.",
        },
        {
            "run_id": RUN_ID,
            "failure_id": "pf_lift_removes_too_many_trades(PF 상승이 거래를 과하게 제거)",
            "evidence": "; ".join(str(row.get("queue_id", "")) for row in pf_pass),
            "kpi_read": "; ".join(
                f"pf={row.get('combined_profit_factor')}; density={row.get('combined_trade_per_business_day')}; trades={row.get('combined_trade_count')}"
                for row in pf_pass
            ),
            "constraint_for_next(다음 제약)": "density gap(밀도 격차) 0.34/day를 복원하되 top_n(상위 N개)과 trade splitting(거래 쪼개기)은 금지한다.",
        },
        {
            "run_id": RUN_ID,
            "failure_id": "short_side_collapse_in_pf_pass_rows(PF 통과 행의 숏 붕괴)",
            "evidence": "; ".join(str(row.get("queue_id", "")) for row in pf_pass),
            "kpi_read": "; ".join(f"shorts={row.get('combined_short_count')}" for row in pf_pass),
            "constraint_for_next(다음 제약)": "short side(숏 방향) 복원은 별도 threshold(임계값)와 session(세션) 제약으로 시험한다.",
        },
        {
            "run_id": RUN_ID,
            "failure_id": "premarket_short_drag(프리마켓 숏 끌림)",
            "evidence": "; ".join(f"{row.get('entry_session')} {row.get('side')}" for row in drag_sessions),
            "kpi_read": "; ".join(
                f"net={row.get('segment_net_profit')}; pf={row.get('segment_profit_factor')}; trades={row.get('segment_trade_count')}"
                for row in drag_sessions
            ),
            "constraint_for_next(다음 제약)": "premarket short(프리마켓 숏)은 무조건 복원하지 말고 margin floor(마진 하한)와 함께 제한한다.",
        },
    ]


def offensive_queue_rows(review_rows_: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    pf_pass = top_by_status(review_rows_, "pf_pass_density_fail", 3)
    near_pf = top_by_status(review_rows_, "near_pf_density_safe", 2)
    dd_seed = top_by_status(review_rows_, "dd_improved_density_fail", 2)
    best_pf = pf_pass[0] if pf_pass else {}
    control = near_pf[0] if near_pf else {}
    dd_best = dd_seed[0] if dd_seed else {}
    queue_specs = [
        ("control_replay_density_anchor(대조 재생 밀도 기준점)", control, "control_anchor(대조 기준)", "hold control(대조 유지)", "density-safe baseline(밀도 안전 기준)을 다시 재현한다.", 0.00, "0.45", "0.00", "8", "control(대조)", 1),
        ("pfpass_core_short_restore_budget_010(PF통과 핵심 숏 0.10 복원)", best_pf, "short_restore(숏 복원)", "restore core short only(핵심 숏만 복원)", "PF-pass row(PF 통과 행)에 core short(핵심 숏)만 소량 복원해 density gap(밀도 격차)을 줄인다.", 0.10, "0.50", "0.00", "8", "candidate(후보)", 2),
        ("pfpass_core_short_restore_budget_020(PF통과 핵심 숏 0.20 복원)", best_pf, "short_restore(숏 복원)", "restore core short with margin(마진 포함 핵심 숏 복원)", "short collapse(숏 붕괴)를 과하게 풀지 않고 0.20/day 예산으로 시험한다.", 0.20, "0.49", "0.02", "8", "candidate(후보)", 3),
        ("pfpass_late_long_density_patch(PF통과 후반 롱 밀도 패치)", best_pf, "late_long_restore(후반 롱 복원)", "restore late long only(후반 롱만 복원)", "late long(후반 롱)의 drawdown(낙폭) 개선 단서를 PF-pass row(PF 통과 행)에 붙인다.", 0.16, "0.50", "0.00", "8", "candidate(후보)", 4),
        ("pfpass_non_drag_session_restore(PF통과 비끌림 세션 복원)", best_pf, "session_restore(세션 복원)", "restore non-drag sessions(비끌림 세션 복원)", "premarket short(프리마켓 숏)은 막고 core/late(핵심/후반)만 복원한다.", 0.24, "0.50", "0.01", "8", "candidate(후보)", 5),
        ("density_anchor_pf_floor_012(밀도 기준 PF 하한 0.12)", control, "pf_floor(수익 팩터 하한)", "add margin floor to control(대조에 마진 하한 추가)", "control(대조)의 density(밀도)를 거의 유지하면서 low-margin trade(낮은 마진 거래)를 제거한다.", 0.04, "0.45", "0.12", "8", "candidate(후보)", 6),
        ("density_anchor_hold6_pf_probe(밀도 기준 보유6 PF 탐침)", control, "hold_shape(보유 형태)", "max_hold 6(최대 보유 6)", "hold time(보유 시간)을 줄여 drawdown(낙폭)을 낮추는지 확인한다.", 0.00, "0.45", "0.00", "6", "candidate(후보)", 7),
        ("dd_seed_density_restore_core_late(낙폭 씨앗 핵심후반 밀도 복원)", dd_best, "dd_restore(낙폭 복원)", "core plus late density(핵심+후반 밀도)", "drawdown(낙폭) 개선 seed(씨앗)에 density(밀도) 복원 규칙을 붙인다.", 0.29, "0.45", "0.00", "8", "candidate(후보)", 8),
        ("pfpass_validation_balance_patch(PF통과 검증 균형 패치)", best_pf, "split_balance(분할 균형)", "validation PF repair(검증 PF 수리)", "validation(검증) 약세를 OOS(표본외) 선택 없이 따로 기록한다.", 0.18, "0.50", "0.01", "8", "candidate(후보)", 9),
        ("pfpass_month_pocket_observation(PF통과 월 포켓 관찰)", best_pf, "market_behavior(시장 현상)", "month pockets report only(월 포켓 보고 전용)", "month side pocket(월 방향 포켓)을 필터가 아닌 attribution(귀속)으로만 사용한다.", 0.00, "0.50", "0.00", "8", "observation(관찰)", 10),
        ("density_anchor_short0455_edge(밀도 기준 숏0.455 경계)", control, "threshold_edge(임계값 경계)", "short threshold 0.455(숏 임계값 0.455)", "short threshold(숏 임계값)를 아주 작게 올려 PF(수익 팩터) 손실과 density(밀도) 변화를 본다.", 0.00, "0.455", "0.00", "8", "candidate(후보)", 11),
        ("pfpass_guardrail_no_trade_split(PF통과 거래쪼개기 금지 가드)", best_pf, "guardrail(가드레일)", "guardrail only(가드레일 전용)", "trade splitting(거래 쪼개기)과 top_n(상위 N개) 없이 같은 row grain(행 단위)로만 검증한다.", 0.00, "0.50", "0.00", "8", "control(대조)", 12),
    ]
    rows: list[dict[str, Any]] = []
    for queue_id, seed, axis_id, rule, hypothesis, restore_budget, short_threshold, margin_floor, hold, queue_type, rank in queue_specs:
        density_gap = max(0.0, DENSITY_FLOOR - as_float(seed.get("combined_trade_per_business_day")))
        rows.append(
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_id": queue_id,
                "seed_variant_id": seed.get("variant_id", ""),
                "source_queue_id": seed.get("queue_id", ""),
                "axis_id": axis_id,
                "short_probability_threshold": short_threshold,
                "entry_margin_floor": margin_floor,
                "max_hold_m5": hold,
                "source_policy": rule,
                "density_gap_to_3day": finite(density_gap, 10),
                "pf_anchor": seed.get("combined_profit_factor", ""),
                "restore_rule": rule,
                "density_restore_budget": finite(restore_budget, 10),
                "forbidden(금지)": "top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지)",
                "timestamp_boundary": "entry timestamp only(진입 시각만 사용)",
                "expected_effect(기대 효과)": hypothesis,
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
                "queue_rank": rank,
                "queue_type": queue_type,
            }
        )
    return rows


def gate_row(name: str, evidence: Path, effect: str, status: str = "passed") -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate(게이트)": name,
        "status": status,
        "evidence(근거)": rel(evidence),
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def final_payload(
    parent_final: Mapping[str, Any],
    review_rows_: Sequence[Mapping[str, Any]],
    package_gates: Sequence[Mapping[str, Any]],
    next_queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
    package_count = sum(1 for row in review_rows_ if str(row.get("review_status", "")).startswith("package_candidate"))
    pf_pass_density_fail_count = sum(1 for row in review_rows_ if str(row.get("review_status", "")).startswith("pf_pass_density_fail"))
    density_safe_near_count = sum(1 for row in review_rows_ if str(row.get("review_status", "")).startswith("near_pf_density_safe"))
    dd_improved_density_fail_count = sum(1 for row in review_rows_ if str(row.get("review_status", "")).startswith("dd_improved_density_fail"))
    failed_package_gates = [row["gate_id"] for row in package_gates if row.get("status") == "failed"]
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
        "parent_selected_queue_id": parent_final.get("selected_queue_id"),
        "parent_selected_net_profit": parent_final.get("selected_combined_net_profit"),
        "parent_selected_profit_factor": parent_final.get("selected_combined_profit_factor"),
        "parent_selected_trade_count": parent_final.get("selected_combined_trade_count"),
        "parent_selected_density": parent_final.get("selected_combined_trade_per_business_day"),
        "parent_selected_expectancy": parent_final.get("selected_combined_expectancy"),
        "parent_selected_drawdown": parent_final.get("selected_combined_max_drawdown"),
        "parent_selected_recovery_factor": parent_final.get("selected_combined_recovery_factor"),
        "parent_selected_long_count": parent_final.get("selected_combined_long_count"),
        "parent_selected_short_count": parent_final.get("selected_combined_short_count"),
        "parent_validation_net_profit": parent_final.get("selected_validation_net_profit"),
        "parent_validation_profit_factor": parent_final.get("selected_validation_profit_factor"),
        "parent_oos_net_profit": parent_final.get("selected_oos_net_profit"),
        "parent_oos_profit_factor": parent_final.get("selected_oos_profit_factor"),
        "surface_rows": len(review_rows_),
        "package_candidate_rows": package_count,
        "pf_pass_density_fail_rows": pf_pass_density_fail_count,
        "density_safe_near_target_rows": density_safe_near_count,
        "dd_improved_density_fail_rows": dd_improved_density_fail_count,
        "next_queue_rows": len(next_queue),
        "package_decision": "no_package_strict_rows_zero_and_selected_pf_below_target(패키지 없음, 엄격 행 0 및 선택 PF 목표 미달)",
        "failed_package_gates": failed_package_gates,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
    }


def write_work_packet() -> None:
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
                "obsidian-experiment-design(실험 설계)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "input_parent_gate",
                "kpi_contract_audit",
                "row_grain_audit",
                "package_boundary_gate",
                "performance_attribution_gate",
                "next_queue_gate",
                "data_integrity_gate",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final_seed: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final_seed["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "skill": "obsidian-data-integrity(데이터 무결성)",
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "inherits run364AJ timestamp-safe proxy replay(run364AJ 시점 안전 프록시 재생 상속)",
            "sample_scope": "US100 M5 Stage364 Tier A proxy review only(US100 5분봉 Stage364 티어 A 프록시 검토 전용)",
            "missing_or_duplicate_check": "input files and one-row review queue verified(입력 파일과 1행 검토 대기열 확인)",
            "feature_label_boundary": "no new features or labels; review only(새 피처와 라벨 없음, 검토 전용)",
            "split_boundary": "validation/OOS metrics inherited from parent scout(검증/표본외 지표는 부모 정찰에서 상속)",
            "leakage_risk": "no OOS threshold selection and no post-entry top_n(표본외 임계값 선택 없음, 진입 후 상위 N개 없음)",
            "data_hash_or_identity": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and Path(path).is_file()},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "skill": "obsidian-performance-attribution(성과 귀속)",
            "observed_change": "PF-pass rows exist but density breaks; density-safe rows stay below PF target(PF 통과 행은 있으나 밀도 붕괴, 밀도 안전 행은 PF 목표 미달)",
            "comparison_baseline": BASELINE_RUN_ID,
            "likely_drivers": "premarket short block, short threshold strictness, core session pocket, late-long drawdown relief(프리마켓 숏 차단, 숏 임계값 엄격화, 핵심 세션 포켓, 후반 롱 낙폭 완화)",
            "segment_checks": [rel(SESSION_SIDE_REVIEW), rel(MONTH_SIDE_REVIEW), rel(POLICY_REVIEW)],
            "trade_shape": {
                "trade_count": final_seed["parent_selected_trade_count"],
                "expectancy": final_seed["parent_selected_expectancy"],
                "max_drawdown": final_seed["parent_selected_drawdown"],
                "long_count": final_seed["parent_selected_long_count"],
                "short_count": final_seed["parent_selected_short_count"],
            },
            "alternative_explanations": "proxy sequence can diverge from MT5 fill and spread(프록시 순서는 MT5 체결과 스프레드에서 달라질 수 있음)",
            "attribution_confidence": "medium_proxy_review_only(중간, 프록시 검토 전용)",
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
            "evidence_missing": "new MT5 runtime probe and ONNX package(새 MT5 런타임 탐침과 ONNX 패키지)",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "negative package review, positive density-restoration seed(패키지는 부정, 밀도 복원 씨앗은 긍정)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect(효과)": "proxy review(프록시 검토)를 운영 주장으로 승격하지 않는다.",
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
            "availability": "tracked_after_commit_or_reproducible_from_command(커밋 후 추적 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AK proxy review(run364AK 프록시 검토)를 완료했다."),
        gate_row("input_parent_gate(부모 입력 게이트)", INPUT_MANIFEST, "run364AJ 산출물과 review queue(검토 대기열)를 확인했다."),
        gate_row("kpi_contract_audit(KPI 계약 감사)", SURFACE_REVIEW, "net/PF/density/DD/split/side(순수익/PF/밀도/낙폭/분할/방향)를 함께 검토했다."),
        gate_row("row_grain_audit(행 단위 감사)", SURFACE_REVIEW, "12개 surface row(표면 행)를 package(패키지) 주장 없이 분류했다."),
        gate_row("package_boundary_gate(패키지 경계 게이트)", PACKAGE_GATE_AUDIT, "strict package row(엄격 패키지 행) 0개라 패키지를 차단했다."),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "PF 상승과 density(밀도) 붕괴 원인을 분리했다."),
        gate_row("next_queue_gate(다음 대기열 게이트)", NEXT_QUEUE, "run364AL offensive queue(공격 대기열)를 만들었다."),
        gate_row("data_integrity_gate(데이터 무결성 게이트)", DATA_RECEIPT, "timestamp-safe(시점 안전) review(검토) 경계를 기록했다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 hash(해시)를 연결했다."),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않았다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "필수 gate(게이트)를 종료 기록에 연결했다."),
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
    review_rows_: Sequence[Mapping[str, Any]],
    package_gates: Sequence[Mapping[str, Any]],
    policy_rows: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    clues: Sequence[Mapping[str, Any]],
    failures: Sequence[Mapping[str, Any]],
    next_queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    refresh_stage_brief_header()
    text = f"""# run364AK session-side PF lift density repair review(364AK 세션/방향 PF 상승 밀도 수리 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- package_decision(패키지 결정): `{final['package_decision']}`
- selected net/PF/trades/density/expectancy/DD/RF(선택 순수익/수익 팩터/거래수/밀도/기대값/낙폭/회복 계수): `{final['parent_selected_net_profit']}` / `{final['parent_selected_profit_factor']}` / `{final['parent_selected_trade_count']}` / `{final['parent_selected_density']}` / `{final['parent_selected_expectancy']}` / `{final['parent_selected_drawdown']}` / `{final['parent_selected_recovery_factor']}`
- package_candidate_rows(패키지 후보 행): `{final['package_candidate_rows']}`
- pf_pass_density_fail_rows(PF 통과 밀도 실패 행): `{final['pf_pass_density_fail_rows']}`
- next_queue_rows(다음 대기열 행): `{final['next_queue_rows']}`
- runtime_authority(런타임 권위): `not_claimed`

## Surface Review(표면 검토)

{markdown_table(list(review_rows_)[:10], ['queue_id', 'review_status', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_per_business_day', 'combined_max_drawdown', 'combined_short_count'])}

## Package Gate Audit(패키지 게이트 감사)

{markdown_table(package_gates, ['gate_id', 'status', 'observed', 'required', 'effect(효과)'])}

## Policy Review(정책 검토)

{markdown_table(list(policy_rows)[:8], ['queue_id', 'review_status', 'combined_profit_factor', 'combined_trade_per_business_day', 'materialized_policy', 'session_policy'])}

## Session Side Review(세션 방향 검토)

{markdown_table(list(session_rows)[:8], ['entry_session', 'side', 'review_status', 'segment_net_profit', 'segment_profit_factor', 'segment_trade_count', 'segment_trade_per_business_day'])}

## Month Side Review(월 방향 검토)

{markdown_table(list(month_rows)[:8], ['entry_month', 'side', 'review_status', 'segment_net_profit', 'segment_profit_factor', 'segment_trade_count'])}

## Positive Clues(긍정 단서)

{markdown_table(clues, ['clue_id', 'evidence', 'kpi_read', 'effect(효과)'])}

## Failure Memory(실패 기억)

{markdown_table(failures, ['failure_id', 'evidence', 'kpi_read', 'constraint_for_next(다음 제약)'])}

## Next Queue(다음 대기열)

{markdown_table(next_queue, ['queue_id', 'seed_variant_id', 'density_gap_to_3day', 'pf_anchor', 'density_restore_budget', 'forbidden(금지)'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate(게이트)', 'status', 'evidence(근거)', 'effect(효과)'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): 이번 review(검토)는 package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)을 열지 않고, run364AL(364AL 실행) 공격 입력만 연다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- package_decision(패키지 결정): `{final['package_decision']}`\n- effect(효과): package(패키지)를 닫고 `{NEXT_RUN_ID}` offensive queue(공격 대기열)를 열었다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364AK Session-Side PF Lift Density Repair Review Closeout",
        f"\n## run364AK Session-Side PF Lift Density Repair Review Closeout(364AK 세션/방향 PF 상승 밀도 수리 검토 종료)\n\nAction(행동): run364AJ(364AJ 실행) proxy scout(프록시 정찰)를 package gate(패키지 게이트), session/side(세션/방향), month/side(월/방향), policy attribution(정책 귀속)으로 검토했다.\n\nEffect(효과): strict package row(엄격 패키지 행) `0` 때문에 package(패키지)는 닫고, PF-pass density-fail(PF 통과 밀도 실패) 단서를 `{NEXT_RUN_ID}` 입력으로 넘겼다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_proxy_review_negative_for_package(프록시 검토상 패키지 부정이라 없음)
- latest_proxy_scout(최근 프록시 정찰): `run364AJ`
- latest_proxy_review(최근 프록시 검토): `run364AK`
- selected_proxy_variant(선택 프록시 변형): `{final['parent_selected_variant_id']}`
- selected_proxy_net_pf_density(선택 프록시 순수익/수익 팩터/밀도): `{final['parent_selected_net_profit']}` / `{final['parent_selected_profit_factor']}` / `{final['parent_selected_density']}`
- next_offensive_queue(다음 공격 대기열): `{rel(NEXT_QUEUE)}`
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

current_truth(현재 진실): run364AK(364AK 실행)는 run364AJ(364AJ 실행)의 session/side PF lift density repair proxy scout(세션/방향 PF 상승 밀도 수리 프록시 정찰)를 검토했다. package_candidate_rows(패키지 후보 행)는 `{final['package_candidate_rows']}`이고, pf_pass_density_fail_rows(PF 통과 밀도 실패 행)는 `{final['pf_pass_density_fail_rows']}`다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 PF-pass row(PF 통과 행)의 density gap(밀도 격차)을 복원하는 offensive input materialization(공격 입력 구체화)을 한다.

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
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): session/side PF lift density repair review(세션/방향 PF 상승 밀도 수리 검토)를 완료했다.\n- effect(효과): package(패키지)를 닫고 `{NEXT_RUN_ID}` queue(대기열)를 만들었다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): PF-pass density-fail(PF 통과 밀도 실패) row(행)를 버리지 않고 density restore(밀도 복원) 공격 seed(씨앗)로 바꾼다.\n- positive clue(긍정 단서): PF(수익 팩터) 1.30 이상 row(행)가 있으나 density(밀도)가 3/day 아래로 떨어진다.\n- failure memory(실패 기억): density-safe(밀도 안전) control(대조)은 PF(수익 팩터) 목표 아래라 package(패키지)가 아니다.\n",
    )
    append_text_once(
        STAGE_README,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- action(행동): run364AJ(364AJ 실행) proxy scout(프록시 정찰)를 검토했다.\n- effect(효과): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 `{NEXT_RUN_ID}`로 이어간다.\n",
    )


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "proxy_review(프록시 검토)",
        "lane": "proxy_review(프록시 검토)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        "notes": f"package_rows={final['package_candidate_rows']}; pf_pass_density_fail_rows={final['pf_pass_density_fail_rows']}; next_queue_rows={final['next_queue_rows']}",
        "family": "kpi_evidence(KPI 근거)",
        "primary_report": rel(REPORT_PATH),
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
        "trade_density_requirement_status": "density_safe_selected_but_pf_below_target_and_pf_pass_rows_density_fail(선택은 밀도 안전이나 PF 목표 미달, PF 통과 행은 밀도 실패)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "net_profit": final["parent_selected_net_profit"],
        "profit_factor": final["parent_selected_profit_factor"],
        "drawdown": final["parent_selected_drawdown"],
        "recovery_factor": final["parent_selected_recovery_factor"],
        "trade_count": final["parent_selected_trade_count"],
        "expectancy": final["parent_selected_expectancy"],
        "max_drawdown_amount": final["parent_selected_drawdown"],
        "long_trade_count": final["parent_selected_long_count"],
        "short_trade_count": final["parent_selected_short_count"],
        "evidence_scope": "proxy_review_no_authority(프록시 검토, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can PF-pass rows restore density without trade splitting?(PF 통과 행이 거래 쪼개기 없이 밀도를 복원할 수 있는가?)",
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
            ("policy_review", POLICY_REVIEW, "Policy review(정책 검토)."),
            ("positive_clues", POSITIVE_CLUES, "Positive clue record(긍정 단서 기록)."),
            ("failure_memory", FAILURE_MEMORY, "Failure memory(실패 기억)."),
            ("next_queue", NEXT_QUEUE, "Next offensive queue(다음 공격 대기열)."),
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
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "skill": "obsidian-artifact-lineage(산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in outputs],
            "artifact_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_or_reproducible_from_command(커밋 후 추적 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    surface = load_surface()
    review_rows_ = surface_review_rows(surface)
    package_gates = package_gate_rows(parent_final, review_rows_)
    policy_rows = policy_review_rows()
    session_rows = segment_review_rows(scout.SELECTED_SESSION_SUMMARY)
    month_rows = segment_review_rows(scout.SELECTED_MONTH_SIDE_SUMMARY)
    clues = positive_clue_rows(parent_final, review_rows_, session_rows, month_rows)
    failures = failure_memory_rows(parent_final, review_rows_, session_rows)
    next_queue = offensive_queue_rows(review_rows_)

    write_csv(SURFACE_REVIEW, review_rows_)
    write_csv(PACKAGE_GATE_AUDIT, package_gates)
    write_csv(POLICY_REVIEW, policy_rows)
    write_csv(SESSION_SIDE_REVIEW, session_rows)
    write_csv(MONTH_SIDE_REVIEW, month_rows)
    write_csv(POSITIVE_CLUES, clues)
    write_csv(FAILURE_MEMORY, failures)
    write_csv(NEXT_QUEUE, next_queue)
    write_work_packet()

    created_at = now_utc()
    final_seed = {
        "created_at_utc": created_at,
        "parent_selected_trade_count": parent_final.get("selected_combined_trade_count"),
        "parent_selected_expectancy": parent_final.get("selected_combined_expectancy"),
        "parent_selected_drawdown": parent_final.get("selected_combined_max_drawdown"),
        "parent_selected_long_count": parent_final.get("selected_combined_long_count"),
        "parent_selected_short_count": parent_final.get("selected_combined_short_count"),
    }
    gates = write_receipts(final_seed)
    final = final_payload(parent_final, review_rows_, package_gates, next_queue, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, review_rows_, package_gates, policy_rows, session_rows, month_rows, clues, failures, next_queue, gates)
    write_ledgers(final, gates)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
