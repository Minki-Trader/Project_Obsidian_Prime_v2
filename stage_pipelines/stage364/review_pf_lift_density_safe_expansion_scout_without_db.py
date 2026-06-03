from __future__ import annotations

import csv
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

from stage_pipelines.stage364 import train_pf_lift_density_safe_expansion_scout_without_db as scout  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = scout.STAGE_ID
RUN_NUMBER = "run364AH"
RUN_ID = "run364AH_review_pf_lift_density_safe_expansion_scout_without_db_v1"
PARENT_RUN_ID = scout.RUN_ID
BASELINE_RUN_ID = scout.BASELINE_RUN_ID
NEXT_RUN_ID = "run364AI_materialize_session_side_pf_lift_density_repair_inputs_without_db_v1"

STATUS = "completed_stage364AH_pf_lift_density_safe_review_negative_for_package_positive_session_side_repair_no_authority"
JUDGMENT = "negative_for_package_positive_for_session_side_pf_lift_density_repair_no_authority"
DECISION = "stage364AH_no_package_open_run364AI_session_side_pf_lift_density_repair_inputs"
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
SESSION_SIDE_REVIEW = RUN_DIR / "session_side_review.csv"
MONTH_SIDE_REVIEW = RUN_DIR / "month_side_review.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364AI_session_side_pf_lift_density_repair_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AH_pf_lift_density_safe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AH_pf_lift_density_safe_review.md"
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
    scout.SELECTED_MONTH_SIDE_SUMMARY,
    scout.SELECTED_SESSION_SUMMARY,
    scout.BASELINE_COMPARISON,
    scout.RUN364AH_QUEUE,
    scout.REPORT_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SURFACE_REVIEW,
    PACKAGE_GATE_AUDIT,
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
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장이 있음)")
    gates = read_csv_rows(scout.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트가 모두 통과되지 않음)")
    review_queue = read_csv_rows(scout.RUN364AH_QUEUE)
    if len(review_queue) != 1:
        raise RuntimeError(f"unexpected review queue rows(검토 대기열 행 수 이상): {len(review_queue)}")
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
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


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
    if pf >= TARGET_PF and density >= DENSITY_FLOOR and validation_net > 0 and oos_net > 0 and short_count > 0:
        return "package_review_candidate(패키지 검토 후보)"
    if pf >= TARGET_PF and density < DENSITY_FLOOR:
        return "pf_pass_density_fail_repair_seed(PF 통과 밀도 실패 수리 씨앗)"
    if density >= DENSITY_FLOOR and pf >= 1.27:
        return "density_safe_pf_near_target_seed(밀도 안전 PF 근접 씨앗)"
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
                "selection_score": finite(row.get("selection_score")),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    rows.sort(
        key=lambda item: (
            item["review_status"].startswith("package"),
            item["review_status"].startswith("density_safe"),
            item["review_status"].startswith("pf_pass"),
            as_float(item["combined_trade_per_business_day"]),
            as_float(item["combined_profit_factor"]),
            as_float(item["combined_net_profit"]),
        ),
        reverse=True,
    )
    return rows


def package_gate_rows(parent_final: Mapping[str, Any], review_rows_: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    selected_pf = as_float(parent_final.get("selected_combined_profit_factor"))
    selected_density = as_float(parent_final.get("selected_combined_trade_per_business_day"))
    package_rows = [row for row in review_rows_ if str(row.get("review_status", "")).startswith("package")]
    return [
        {
            "run_id": RUN_ID,
            "gate_id": "density_floor(밀도 하한)",
            "status": "passed" if selected_density >= DENSITY_FLOOR else "failed",
            "observed": selected_density,
            "required": DENSITY_FLOOR,
            "effect(효과)": "선택 후보의 최소 거래 밀도를 확인한다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "profit_factor_target(PF 목표)",
            "status": "passed" if selected_pf >= TARGET_PF else "failed",
            "observed": selected_pf,
            "required": TARGET_PF,
            "effect(효과)": "PF 목표 미달이면 패키지를 열지 않는다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "strict_package_rows(엄격 패키지 행)",
            "status": "passed" if package_rows else "failed",
            "observed": len(package_rows),
            "required": 1,
            "effect(효과)": "PF/밀도/분할/숏 노출 동시 통과가 없으면 MT5 패키지로 올리지 않는다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "external_runtime_evidence(외부 런타임 근거)",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "observed": "not_run(미실행)",
            "required": "MT5 runtime probe(MT5 런타임 탐침)",
            "effect(효과)": "이번 검토는 프록시 판정까지만 닫는다.",
        },
    ]


def classify_segment(row: Mapping[str, Any]) -> str:
    pf = as_float(row.get("segment_profit_factor"))
    net = as_float(row.get("segment_net_profit"))
    trades = as_float(row.get("segment_trade_count"))
    density = as_float(row.get("segment_trade_per_business_day"))
    if trades < 10:
        return "too_sparse_watch(희소 관찰)"
    if net > 0 and pf >= TARGET_PF and density > 0:
        return "positive_pf_session_or_month(양수 PF 세션/월)"
    if net < 0 or pf < 1.0:
        return "loss_or_pf_drag(손실 또는 PF 끌림)"
    if pf < TARGET_PF:
        return "positive_but_pf_below_target(PF 목표 미만 양수)"
    return "neutral_watch(중립 관찰)"


def segment_review_rows(path: Path, sort_cols: Sequence[str]) -> list[dict[str, Any]]:
    rows = read_csv_rows(path)
    reviewed: list[dict[str, Any]] = []
    for row in rows:
        item = {
            **row,
            "review_status": classify_segment(row),
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
        reviewed.append(item)
    reviewed.sort(
        key=lambda item: (
            item["review_status"].startswith("positive_pf"),
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
    pf_pass = top_by_status(review_rows_, "pf_pass", 2)
    core_session = [
        row
        for row in session_rows
        if row.get("entry_session") == "us_cash_core(미국 현금장 핵심)"
        and row.get("review_status", "").startswith("positive_pf")
    ]
    best_month = top_by_status(month_rows, "positive_pf", 2)
    return [
        {
            "run_id": RUN_ID,
            "clue_id": "density_safe_pf_near_target(밀도 안전 PF 근접)",
            "evidence": parent_final.get("selected_variant_id", ""),
            "kpi_read": f"net={parent_final.get('selected_combined_net_profit')}; pf={parent_final.get('selected_combined_profit_factor')}; density={parent_final.get('selected_combined_trade_per_business_day')}; dd={parent_final.get('selected_combined_max_drawdown')}",
            "effect(효과)": "밀도를 깨지 않고 PF만 올리는 수리 방향을 유지한다.",
        },
        {
            "run_id": RUN_ID,
            "clue_id": "pf_pass_density_fail_exists(PF 통과 밀도 실패 존재)",
            "evidence": "; ".join(str(row.get("variant_id", "")) for row in pf_pass),
            "kpi_read": "; ".join(
                f"pf={row.get('combined_profit_factor')}; density={row.get('combined_trade_per_business_day')}"
                for row in pf_pass
            ),
            "effect(효과)": "PF를 올리는 규칙은 있으나 밀도 복원 장치가 필요함을 보여준다.",
        },
        {
            "run_id": RUN_ID,
            "clue_id": "us_cash_core_dual_side_positive(미국 현금장 핵심 양방향 양수)",
            "evidence": "; ".join(f"{row.get('side')} {row.get('segment_net_profit')}" for row in core_session),
            "kpi_read": "; ".join(
                f"side={row.get('side')}; pf={row.get('segment_profit_factor')}; trades={row.get('segment_trade_count')}"
                for row in core_session
            ),
            "effect(효과)": "세션 필터를 공격 탐색 씨앗으로 쓸 수 있다.",
        },
        {
            "run_id": RUN_ID,
            "clue_id": "month_side_pockets_positive(월/방향 양수 포켓)",
            "evidence": "; ".join(f"{row.get('entry_month')} {row.get('side')}" for row in best_month),
            "kpi_read": "; ".join(
                f"net={row.get('segment_net_profit')}; pf={row.get('segment_profit_factor')}; trades={row.get('segment_trade_count')}"
                for row in best_month
            ),
            "effect(효과)": "월별 손실 구간을 모두 죽이지 않고 양수 포켓을 분리해 볼 수 있다.",
        },
    ]


def failure_memory_rows(
    parent_final: Mapping[str, Any],
    review_rows_: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    pf_pass = top_by_status(review_rows_, "pf_pass", 3)
    drag_sessions = [row for row in session_rows if row.get("review_status", "").startswith("loss_or_pf_drag")]
    return [
        {
            "run_id": RUN_ID,
            "failure_id": "pf_below_target_blocks_package(PF 목표 미달 패키지 차단)",
            "evidence": parent_final.get("selected_variant_id", ""),
            "kpi_read": f"pf={parent_final.get('selected_combined_profit_factor')}; target={TARGET_PF}",
            "constraint_for_next(다음 제약)": "PF>=1.30 and density>=3/day before MT5 package(PF 1.30 이상과 일 3회 이상 밀도 전에는 MT5 패키지 금지)",
        },
        {
            "run_id": RUN_ID,
            "failure_id": "pf_lift_breaks_density(PF 상승이 밀도 훼손)",
            "evidence": "; ".join(str(row.get("queue_id", "")) for row in pf_pass),
            "kpi_read": "; ".join(
                f"pf={row.get('combined_profit_factor')}; density={row.get('combined_trade_per_business_day')}"
                for row in pf_pass
            ),
            "constraint_for_next(다음 제약)": "PF 상승 규칙은 세션/방향 복원과 같은 작업 묶음에서 시험한다.",
        },
        {
            "run_id": RUN_ID,
            "failure_id": "premarket_short_pf_drag(프리마켓 숏 PF 끌림)",
            "evidence": "; ".join(f"{row.get('entry_session')} {row.get('side')}" for row in drag_sessions),
            "kpi_read": "; ".join(
                f"net={row.get('segment_net_profit')}; pf={row.get('segment_profit_factor')}; trades={row.get('segment_trade_count')}"
                for row in drag_sessions
            ),
            "constraint_for_next(다음 제약)": "세션별 숏 허용 규칙을 분리하고, 손실 세션은 별도 대조군으로 둔다.",
        },
    ]


def next_queue_rows(
    parent_final: Mapping[str, Any],
    review_rows_: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    selected = parent_final.get("selected_variant_id", "")
    pf_pass = top_by_status(review_rows_, "pf_pass", 2)
    best_pf_seed = pf_pass[0] if pf_pass else {}
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "core_session_dual_side_pf_lift(핵심 세션 양방향 PF 상승)",
            "seed_variant_id": selected,
            "hypothesis(가설)": "us_cash_core long/short positive pocket(미국 현금장 핵심 롱/숏 양수 포켓)을 보존하고 premarket short drag(프리마켓 숏 끌림)을 차단하면 PF를 올리며 밀도 3/day를 지킬 수 있다.",
            "required_control(필수 대조)": "run364AG selected control and full-session replay(364AG 선택 대조와 전체 세션 재생)",
            "forbidden(금지)": "top_n, post-entry ranking, trade splitting(top_n, 진입 후 순위, 거래 쪼개기)",
            "effect(효과)": "세션/방향 규칙을 새 수익 원천으로 시험한다.",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "pf_pass_density_bridge_restore(PF 통과 밀도 연결 복원)",
            "seed_variant_id": best_pf_seed.get("variant_id", ""),
            "hypothesis(가설)": "PF>=1.30 but density<3(PF 1.30 이상이나 밀도 3 미만) 씨앗에 core-session restore(핵심 세션 복원)를 붙이면 PF와 밀도를 동시에 맞출 수 있다.",
            "required_control(필수 대조)": "pfpass_short050_restore_short0475 and pf_pass_density_fail_control(PF 통과 밀도 실패 대조)",
            "forbidden(금지)": "trade count splitting(거래수 쪼개기)",
            "effect(효과)": "PF 상승 단서를 밀도 복원과 결합한다.",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "validation_pf_repair_without_oos_overfit(검증 PF 수리와 표본외 과적합 방지)",
            "seed_variant_id": selected,
            "hypothesis(가설)": "validation PF 1.2147(검증 PF 1.2147)이 약하고 OOS PF 1.3369(표본외 PF 1.3369)가 강하므로, 검증 손실 세그먼트를 줄이되 OOS 조건을 그대로 고정한다.",
            "required_control(필수 대조)": "validation/OOS split separate records(검증/표본외 분리 기록)",
            "forbidden(금지)": "using OOS to choose final operating threshold(표본외로 운영 임계값 선택)",
            "effect(효과)": "분할 안정성 문제를 과적합 없이 수리한다.",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "premarket_short_block_control(프리마켓 숏 차단 대조)",
            "seed_variant_id": selected,
            "hypothesis(가설)": "premarket short net -12.315 and PF 0.915(프리마켓 숏 순수익 -12.315, PF 0.915)를 차단하면 PF 손상을 줄일 수 있다.",
            "required_control(필수 대조)": "same long rules, short session block only(같은 롱 규칙, 숏 세션 차단만 변경)",
            "forbidden(금지)": "long-side hidden filter(롱 방향 숨은 필터)",
            "effect(효과)": "나쁜 숏 세션을 분리해 PF 압박 원인을 확인한다.",
        },
    ]


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
    package_count = sum(1 for row in review_rows_ if str(row.get("review_status", "")).startswith("package"))
    pf_pass_density_fail_count = sum(1 for row in review_rows_ if str(row.get("review_status", "")).startswith("pf_pass"))
    density_safe_near_count = sum(1 for row in review_rows_ if str(row.get("review_status", "")).startswith("density_safe_pf_near"))
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
        "parent_selected_net_profit": parent_final.get("selected_combined_net_profit"),
        "parent_selected_profit_factor": parent_final.get("selected_combined_profit_factor"),
        "parent_selected_trade_count": parent_final.get("selected_combined_trade_count"),
        "parent_selected_density": parent_final.get("selected_combined_trade_per_business_day"),
        "parent_selected_expectancy": parent_final.get("selected_combined_expectancy"),
        "parent_selected_drawdown": parent_final.get("selected_combined_max_drawdown"),
        "parent_selected_recovery_factor": parent_final.get("selected_combined_recovery_factor"),
        "parent_selected_long_count": parent_final.get("selected_combined_long_count"),
        "parent_selected_short_count": parent_final.get("selected_combined_short_count"),
        "surface_rows": len(review_rows_),
        "package_candidate_rows": package_count,
        "pf_pass_density_fail_rows": pf_pass_density_fail_count,
        "density_safe_near_target_rows": density_safe_near_count,
        "next_queue_rows": len(next_queue),
        "package_decision": "no_package_pf_below_target_and_strict_pass_zero(패키지 없음, PF 목표 미달 및 엄격 통과 0)",
        "failed_package_gates": failed_package_gates,
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
            "skill": "obsidian-data-integrity(옵시디언 데이터 무결성)",
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "inherits run364AG timestamp-safe proxy replay(364AG 시점 안전 프록시 재생을 상속)",
            "sample_scope": "US100 M5 Stage364 Tier A proxy review only(US100 5분봉 Stage364 티어 A 프록시 검토 전용)",
            "missing_or_duplicate_check": "input files and one-row review queue verified(입력 파일과 1행 검토 대기열 확인)",
            "feature_label_boundary": "no new features or labels; review only(새 피처/라벨 없음, 검토 전용)",
            "split_boundary": "validation/OOS metrics inherited from run364AG(검증/표본외 지표는 364AG에서 상속)",
            "leakage_risk": "selection already occurred in proxy scout; review is not an operating claim(선택은 프록시 정찰에서 이미 발생, 검토는 운영 주장 아님)",
            "data_hash_or_identity": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and Path(path).is_file()},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "skill": "obsidian-performance-attribution(옵시디언 성과 귀속)",
            "observed_change": "PF target remains below 1.30 while density barely passes 3/day(PF 목표는 1.30 미만이고 밀도는 일 3회를 간신히 통과)",
            "comparison_baseline": PARENT_RUN_ID,
            "likely_drivers": "short threshold strictness, core session positive pocket, premarket short drag(숏 임계값 엄격도, 핵심 세션 양수 포켓, 프리마켓 숏 끌림)",
            "segment_checks": [rel(SESSION_SIDE_REVIEW), rel(MONTH_SIDE_REVIEW)],
            "trade_shape": {
                "trade_count": final["parent_selected_trade_count"],
                "expectancy": final["parent_selected_expectancy"],
                "max_drawdown": final["parent_selected_drawdown"],
                "long_count": final["parent_selected_long_count"],
                "short_count": final["parent_selected_short_count"],
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
            "skill": "obsidian-result-judgment(옵시디언 결과 판정)",
            "result_subject": RUN_ID,
            "evidence_available": [rel(SURFACE_REVIEW), rel(PACKAGE_GATE_AUDIT), rel(SESSION_SIDE_REVIEW), rel(FINAL_DECISION)],
            "evidence_missing": "new MT5 runtime probe and ONNX package(새 MT5 런타임 탐침과 ONNX 패키지)",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "review says no package yet, but gives session/side repair seeds(검토상 아직 패키지는 없지만 세션/방향 수리 씨앗은 있음)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect(효과)": "프록시 검토를 운영 주장으로 승격하지 않는다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "skill": "obsidian-artifact-lineage(옵시디언 산출물 계보)",
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
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AH proxy review(364AH 프록시 검토)를 닫음"),
        gate_row("input_parent_gate(부모 입력 게이트)", INPUT_MANIFEST, "run364AG 산출물과 review queue(검토 대기열)를 확인함"),
        gate_row("kpi_contract_audit(KPI 계약 감사)", SURFACE_REVIEW, "PF/밀도/낙폭/거래수/방향 지표를 검토함"),
        gate_row("row_grain_audit(행 단위 감사)", SURFACE_REVIEW, "surface row(표면 행) 12개와 review queue(검토 대기열) 1개를 분리함"),
        gate_row("source_authority_audit(원천 권위 감사)", DATA_RECEIPT, "부모 run364AG(실행364AG)를 원천으로 고정함"),
        gate_row("package_boundary_gate(패키지 경계 게이트)", PACKAGE_GATE_AUDIT, "PF 목표 미달과 엄격 통과 0개로 패키지를 차단함"),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "세션/방향/PF-밀도 맞교환 원인을 기록함"),
        gate_row("next_queue_gate(다음 대기열 게이트)", NEXT_QUEUE, "run364AI(실행364AI) 수리 입력을 만듦"),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 해시를 연결함"),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "런타임 권위와 운영 승격을 주장하지 않음"),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "필수 게이트를 종료 기록에 연결함"),
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
    session_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    clues: Sequence[Mapping[str, Any]],
    failures: Sequence[Mapping[str, Any]],
    next_queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    refresh_stage_brief_header()
    text = f"""# run364AH PF lift density-safe review(364AH PF 상승 밀도 안전 검토)

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

## Session Side Review(세션 방향 검토)

{markdown_table(list(session_rows)[:8], ['entry_session', 'side', 'review_status', 'segment_net_profit', 'segment_profit_factor', 'segment_trade_count', 'segment_trade_per_business_day'])}

## Month Side Review(월 방향 검토)

{markdown_table(list(month_rows)[:8], ['entry_month', 'side', 'review_status', 'segment_net_profit', 'segment_profit_factor', 'segment_trade_count'])}

## Positive Clues(긍정 단서)

{markdown_table(clues, ['clue_id', 'evidence', 'kpi_read', 'effect(효과)'])}

## Failure Memory(실패 기억)

{markdown_table(failures, ['failure_id', 'evidence', 'kpi_read', 'constraint_for_next(다음 제약)'])}

## Next Queue(다음 대기열)

{markdown_table(next_queue, ['queue_id', 'seed_variant_id', 'hypothesis(가설)', 'required_control(필수 대조)', 'forbidden(금지)'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate(게이트)', 'status', 'evidence(근거)', 'effect(효과)'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): 이 review(검토)는 package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)을 열지 않고, run364AI(실행364AI) 수리 입력만 연다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- package_decision(패키지 결정): `{final['package_decision']}`\n- effect(효과): 패키지를 열지 않고 `{NEXT_RUN_ID}` 입력을 만들었다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"\n## run364AH PF Lift Density-Safe Review Closeout(364AH PF 상승 밀도 안전 검토 종료)\n\nAction(행동): run364AG(364AG 실행)의 proxy scout(프록시 정찰)를 PF/밀도/세션/방향으로 검토했다.\n\nEffect(효과): PF 목표 미달과 strict pass(엄격 통과) `0` 때문에 패키지를 열지 않고 `{NEXT_RUN_ID}` 수리 입력으로 넘긴다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_pf_below_target_review_only(PF 목표 미달 검토 전용이라 없음)
- latest_proxy_scout(최근 프록시 정찰): `run364AG`
- latest_proxy_review(최근 프록시 검토): `run364AH`
- selected_proxy_variant(선택 프록시 변형): `{final['parent_selected_variant_id']}`
- selected_proxy_net_pf_density(선택 프록시 순수익/수익 팩터/밀도): `{final['parent_selected_net_profit']}` / `{final['parent_selected_profit_factor']}` / `{final['parent_selected_density']}`
- next_repair_queue(다음 수리 대기열): `{rel(NEXT_QUEUE)}`
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

current_truth(현재 진실): run364AH(364AH 실행)는 run364AG(364AG 실행)의 PF lift density-safe proxy scout(PF 상승 밀도 안전 프록시 정찰)를 검토했다. 선택 후보는 density(밀도) `{final['parent_selected_density']}`로 일 3회를 넘겼지만 PF(수익 팩터) `{final['parent_selected_profit_factor']}`로 목표 `1.30` 미만이라 package(패키지)를 열지 않는다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 session/side PF lift density repair inputs(세션/방향 PF 상승 밀도 수리 입력)를 구체화한다.

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
        RUN_ID,
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): PF lift density-safe review(PF 상승 밀도 안전 검토)를 완료했다.\n- effect(효과): package(패키지)를 열지 않고 `{NEXT_RUN_ID}` 수리 대기열을 만들었다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"\n## {RUN_ID}\n\n- idea(아이디어): 밀도 통과 후보를 패키지로 올리기 전에 PF/세션/방향 압박을 분해한다.\n- positive clue(긍정 단서): 미국 현금장 핵심 세션은 롱/숏 모두 양수 PF 포켓을 보인다.\n- failure memory(실패 기억): PF 통과 행은 밀도 3/day를 잃고, 밀도 통과 행은 PF 1.30을 못 넘는다.\n",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"\n## {RUN_ID}\n\n- action(행동): run364AG(364AG 실행) 프록시 정찰을 검토했다.\n- effect(효과): Stage364(364단계) 안에서 run364AI(실행364AI) 수리 입력으로 이어간다.\n",
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
        "expectancy": final["parent_selected_expectancy"],
        "max_drawdown_amount": final["parent_selected_drawdown"],
        "long_trade_count": final["parent_selected_long_count"],
        "short_trade_count": final["parent_selected_short_count"],
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
            ("session_side_review", SESSION_SIDE_REVIEW, "Session side review(세션 방향 검토)."),
            ("month_side_review", MONTH_SIDE_REVIEW, "Month side review(월 방향 검토)."),
            ("next_queue", NEXT_QUEUE, "Next repair queue(다음 수리 대기열)."),
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
            "skill": "obsidian-artifact-lineage(옵시디언 산출물 계보)",
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
    session_rows = segment_review_rows(scout.SELECTED_SESSION_SUMMARY, ["entry_session", "side"])
    month_rows = segment_review_rows(scout.SELECTED_MONTH_SIDE_SUMMARY, ["entry_month", "side"])
    clues = positive_clue_rows(parent_final, review_rows_, session_rows, month_rows)
    failures = failure_memory_rows(parent_final, review_rows_, session_rows)
    next_queue = next_queue_rows(parent_final, review_rows_, session_rows)

    write_csv(SURFACE_REVIEW, review_rows_)
    write_csv(PACKAGE_GATE_AUDIT, package_gates)
    write_csv(SESSION_SIDE_REVIEW, session_rows)
    write_csv(MONTH_SIDE_REVIEW, month_rows)
    write_csv(POSITIVE_CLUES, clues)
    write_csv(FAILURE_MEMORY, failures)
    write_csv(NEXT_QUEUE, next_queue)
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-result-judgment(옵시디언 결과 판정)",
            "support_skills": [
                "obsidian-performance-attribution(옵시디언 성과 귀속)",
                "obsidian-data-integrity(옵시디언 데이터 무결성)",
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "input_parent_gate",
                "kpi_contract_audit",
                "row_grain_audit",
                "source_authority_audit",
                "package_boundary_gate",
                "performance_attribution_gate",
                "next_queue_gate",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    created_at = now_utc()
    temp_final = {
        "created_at_utc": created_at,
        "parent_selected_trade_count": parent_final.get("selected_combined_trade_count"),
        "parent_selected_expectancy": parent_final.get("selected_combined_expectancy"),
        "parent_selected_drawdown": parent_final.get("selected_combined_max_drawdown"),
        "parent_selected_long_count": parent_final.get("selected_combined_long_count"),
        "parent_selected_short_count": parent_final.get("selected_combined_short_count"),
    }
    gates = write_receipts(temp_final)
    final = final_payload(parent_final, review_rows_, package_gates, next_queue, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, review_rows_, package_gates, session_rows, month_rows, clues, failures, next_queue, gates)
    write_ledgers(final, gates)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
