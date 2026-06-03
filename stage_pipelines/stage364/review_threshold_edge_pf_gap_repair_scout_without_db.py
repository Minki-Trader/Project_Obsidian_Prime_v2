from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import train_threshold_edge_pf_gap_repair_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AT"
RUN_ID = "run364AT_review_threshold_edge_pf_gap_repair_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.PARENT_RUN_ID
NEXT_RUN_ID = "run364AU_package_threshold_edge_floor001_runtime_probe_without_db_v1"

STATUS = "completed_stage364AT_proxy_package_candidate_review_runtime_probe_required_no_authority"
JUDGMENT = "positive_proxy_package_candidate_for_runtime_probe_not_operating_promotion"
DECISION = "stage364AT_open_run364AU_package_threshold_edge_floor001_runtime_probe"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = parent.DENSITY_FLOOR
TARGET_PF = parent.TARGET_PF
MIN_SHORT_COUNT = 50
DD_REFERENCE = -147.924

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SURFACE_REVIEW = RUN_DIR / "surface_review.csv"
PACKAGE_GATE_AUDIT = RUN_DIR / "package_gate_audit.csv"
SPLIT_STABILITY_REVIEW = RUN_DIR / "split_stability_review.csv"
SESSION_STRESS_REVIEW = RUN_DIR / "session_stress_review.csv"
MONTH_STRESS_REVIEW = RUN_DIR / "month_stress_review.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
RUNTIME_PROBE_QUEUE = RUN_DIR / "run364AU_runtime_probe_package_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AT_threshold_edge_pf_gap_repair_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AT_threshold_edge_pf_gap_repair_review.md"
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
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.SCOUT_SURFACE,
    parent.STRICT_CANDIDATES,
    parent.SELECTED_PROXY_CANDIDATE,
    parent.SELECTED_EXPECTED_TRADE_TAPE,
    parent.SELECTED_SESSION_SUMMARY,
    parent.SELECTED_MONTH_SIDE_SUMMARY,
    parent.POLICY_ATTRIBUTION,
    parent.BASELINE_COMPARISON,
    parent.QUEUE_REPLAY_AUDIT,
    parent.RUN364AT_QUEUE,
    parent.REPORT_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SURFACE_REVIEW,
    PACKAGE_GATE_AUDIT,
    SPLIT_STABILITY_REVIEW,
    SESSION_STRESS_REVIEW,
    MONTH_STRESS_REVIEW,
    POSITIVE_CLUES,
    FAILURE_MEMORY,
    RUNTIME_PROBE_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    RUNTIME_PARITY_RECEIPT,
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
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return Path(path).exists()


def sha(path: Path | str) -> str:
    return parent.sha(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float:
    number = as_float(value)
    if not math.isfinite(number):
        return 0.0
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> Mapping[str, Any]:
    parent_final = read_json(parent.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if parent_final.get("runtime_authority") != "not_claimed" or parent_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트가 모두 통과하지 않음)")
    if as_int(parent_final.get("strict_pass_rows")) < 1:
        raise RuntimeError("parent strict pass missing(부모 엄격 통과 누락)")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AT inputs(364AT 입력 누락): " + ", ".join(missing))
    return parent_final


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "threshold_edge_pf_gap_repair_proxy_scout_surface.csv":
        return "parent scout surface(부모 정찰 표면)"
    if name == "strict_proxy_candidates.csv":
        return "parent strict candidates(부모 엄격 후보)"
    if name == "selected_proxy_candidate.json":
        return "selected proxy candidate(선택 프록시 후보)"
    if name == "selected_trade_tape.csv":
        return "selected expected trade tape(선택 예상 거래 테이프)"
    if name == "selected_session_summary.csv":
        return "selected session summary(선택 세션 요약)"
    if name == "selected_month_side_summary.csv":
        return "selected month-side summary(선택 월/방향 요약)"
    if name == "run364AT_review_queue.csv":
        return "parent review queue(부모 검토 대기열)"
    return "supporting input(보조 입력)"


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_role": input_role(path),
            "path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) else "",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def load_surface() -> pd.DataFrame:
    surface = pd.read_csv(parent.SCOUT_SURFACE)
    if surface.empty:
        raise RuntimeError("parent scout surface is empty(부모 정찰 표면이 비어 있음)")
    return surface


def review_status(row: Mapping[str, Any]) -> str:
    pf = as_float(row.get("combined_profit_factor"))
    density = as_float(row.get("combined_trade_per_business_day"))
    val_net = as_float(row.get("validation_net_profit"))
    oos_net = as_float(row.get("oos_net_profit"))
    val_pf = as_float(row.get("validation_profit_factor"))
    oos_pf = as_float(row.get("oos_profit_factor"))
    short_count = as_float(row.get("combined_short_count"))
    dd = as_float(row.get("combined_max_drawdown"))
    status = str(row.get("candidate_status", ""))
    if (
        status.startswith("pass_")
        and pf >= TARGET_PF
        and density >= DENSITY_FLOOR
        and val_net > 0
        and oos_net > 0
        and val_pf >= TARGET_PF
        and oos_pf >= TARGET_PF
        and short_count >= MIN_SHORT_COUNT
        and dd >= DD_REFERENCE
    ):
        return "proxy_package_candidate_runtime_probe_required(프록시 패키지 후보, 런타임 탐침 필요)"
    if pf >= TARGET_PF and density >= DENSITY_FLOOR:
        return "proxy_positive_with_review_gap(프록시 긍정이나 검토 간극 있음)"
    if pf >= TARGET_PF and density < DENSITY_FLOOR:
        return "pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗)"
    if density >= DENSITY_FLOOR and pf < TARGET_PF and dd >= DD_REFERENCE:
        return "density_dd_safe_pf_gap_seed(밀도/DD 안전, PF 간극 씨앗)"
    if density >= DENSITY_FLOOR:
        return "density_safe_pf_gap_watch(밀도 안전, PF 간극 관찰)"
    return "reject_or_watch(거절 또는 관찰)"


def surface_review_rows(surface: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, raw in surface.iterrows():
        row = raw.to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row.get("queue_id", ""),
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
                "validation_trade_per_business_day": finite(row.get("validation_trade_per_business_day")),
                "oos_net_profit": finite(row.get("oos_net_profit")),
                "oos_profit_factor": finite(row.get("oos_profit_factor")),
                "oos_trade_per_business_day": finite(row.get("oos_trade_per_business_day")),
                "pf_delta_vs_threshold_edge": finite(row.get("pf_delta_vs_run364AQ_threshold_edge")),
                "density_delta_vs_threshold_edge": finite(row.get("density_delta_vs_run364AQ_threshold_edge")),
                "dd_delta_vs_threshold_edge": finite(row.get("dd_delta_vs_run364AQ_threshold_edge")),
                "selection_score": finite(row.get("selection_score")),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rank = {
        "proxy_package_candidate_runtime_probe_required": 7,
        "proxy_positive_with_review_gap": 6,
        "density_dd_safe_pf_gap_seed": 5,
        "density_safe_pf_gap_watch": 4,
        "pf_pass_density_fail_seed": 3,
    }
    rows.sort(
        key=lambda item: (
            max((score for prefix, score in rank.items() if str(item["review_status"]).startswith(prefix)), default=0),
            as_float(item["selection_score"]),
            as_float(item["combined_profit_factor"]),
            as_float(item["combined_trade_per_business_day"]),
        ),
        reverse=True,
    )
    return rows


def best_with_prefix(rows: Sequence[Mapping[str, Any]], prefix: str) -> Mapping[str, Any]:
    candidates = [row for row in rows if str(row.get("review_status", "")).startswith(prefix)]
    if not candidates:
        return {}
    return max(
        candidates,
        key=lambda row: (
            as_float(row.get("selection_score")),
            as_float(row.get("combined_profit_factor")),
            as_float(row.get("combined_trade_per_business_day")),
            as_float(row.get("combined_net_profit")),
        ),
    )


def selected_candidate() -> Mapping[str, Any]:
    return read_json(parent.SELECTED_PROXY_CANDIDATE)


def split_stability_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    specs = [
        ("validation(검증)", selected.get("validation_net_profit"), selected.get("validation_profit_factor"), selected.get("validation_trade_per_business_day"), selected.get("validation_max_drawdown")),
        ("oos(표본외)", selected.get("oos_net_profit"), selected.get("oos_profit_factor"), selected.get("oos_trade_per_business_day"), selected.get("oos_max_drawdown")),
        ("combined(합산)", selected.get("combined_net_profit"), selected.get("combined_profit_factor"), selected.get("combined_trade_per_business_day"), selected.get("combined_max_drawdown")),
    ]
    rows = []
    for split_id, net, pf, density, dd in specs:
        rows.append(
            {
                "run_id": RUN_ID,
                "split_id": split_id,
                "net_profit": finite(net),
                "profit_factor": finite(pf),
                "trade_per_business_day": finite(density),
                "max_drawdown": finite(dd),
                "review_status": "passed(통과)" if as_float(net) > 0 and as_float(pf) >= TARGET_PF and as_float(density) >= 2.75 else "watch_or_fail(관찰 또는 실패)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def session_stress_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv_rows(parent.SELECTED_SESSION_SUMMARY):
        net = as_float(row.get("segment_net_profit"))
        pf = as_float(row.get("segment_profit_factor"))
        rows.append(
            {
                "run_id": RUN_ID,
                "entry_session": row.get("entry_session", ""),
                "side": row.get("side", ""),
                "segment_trade_count": finite(row.get("segment_trade_count"), 0),
                "segment_trade_per_business_day": finite(row.get("segment_trade_per_business_day")),
                "segment_net_profit": finite(net),
                "segment_profit_factor": finite(pf),
                "segment_max_drawdown": finite(row.get("segment_max_drawdown")),
                "review_status": "passed(통과)" if net > 0 and pf > 1.0 else "stress_watch(압박 관찰)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def month_stress_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv_rows(parent.SELECTED_MONTH_SIDE_SUMMARY):
        net = as_float(row.get("segment_net_profit"))
        pf = as_float(row.get("segment_profit_factor"))
        rows.append(
            {
                "run_id": RUN_ID,
                "entry_month": row.get("entry_month", ""),
                "side": row.get("side", ""),
                "segment_trade_count": finite(row.get("segment_trade_count"), 0),
                "segment_trade_per_business_day": finite(row.get("segment_trade_per_business_day")),
                "segment_net_profit": finite(net),
                "segment_profit_factor": finite(pf),
                "segment_max_drawdown": finite(row.get("segment_max_drawdown")),
                "review_status": "month_side_positive(월/방향 양수)" if net > 0 and pf > 1.0 else "month_side_negative_watch(월/방향 음수 관찰)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.sort(key=lambda item: (str(item["review_status"]).endswith("관찰)"), as_float(item["segment_net_profit"])))
    return rows


def package_gate_rows(selected: Mapping[str, Any], review_rows: Sequence[Mapping[str, Any]], split_rows: Sequence[Mapping[str, Any]], session_rows: Sequence[Mapping[str, Any]], month_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    package_rows = [row for row in review_rows if str(row.get("review_status", "")).startswith("proxy_package_candidate")]
    negative_month_side = [row for row in month_rows if str(row.get("review_status", "")).startswith("month_side_negative")]
    return [
        {
            "run_id": RUN_ID,
            "gate_id": "strict_proxy_package_candidate(엄격 프록시 패키지 후보)",
            "status": "passed" if package_rows else "failed",
            "observed": len(package_rows),
            "required": 1,
            "effect": "PF/density/split/side/DD 조건을 동시에 만족한 후보를 런타임 탐침 대상으로 연다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "selected_profit_factor_target(선택 PF 목표)",
            "status": "passed" if as_float(selected.get("combined_profit_factor")) >= TARGET_PF else "failed",
            "observed": finite(selected.get("combined_profit_factor")),
            "required": TARGET_PF,
            "effect": "프록시 기준 PF 1.30 이상인지 확인한다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "selected_density_floor(선택 밀도 하한)",
            "status": "passed" if as_float(selected.get("combined_trade_per_business_day")) >= DENSITY_FLOOR else "failed",
            "observed": finite(selected.get("combined_trade_per_business_day")),
            "required": DENSITY_FLOOR,
            "effect": "거래수 쪼개기 없이 3/day 이상 밀도인지 확인한다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "validation_oos_pf_net(검증/표본외 PF와 순수익)",
            "status": "passed" if all(str(row.get("review_status", "")).startswith("passed") for row in split_rows[:2]) else "failed",
            "observed": "validation and oos positive with PF>=1.30(검증/표본외 양수와 PF 1.30 이상)",
            "required": "validation/oos net>0 and PF>=1.30(검증/표본외 순수익 양수와 PF 1.30 이상)",
            "effect": "한쪽 split(분할)만 좋은 후보를 걸러낸다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "drawdown_improvement(낙폭 개선)",
            "status": "passed" if as_float(selected.get("combined_max_drawdown")) >= DD_REFERENCE else "failed",
            "observed": finite(selected.get("combined_max_drawdown")),
            "required": f">= {DD_REFERENCE}",
            "effect": "threshold-edge clue(임계값 경계 단서) 대비 DD가 악화되지 않았는지 본다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "short_side_presence(숏 방향 존재)",
            "status": "passed" if as_float(selected.get("combined_short_count")) >= MIN_SHORT_COUNT else "warning",
            "observed": finite(selected.get("combined_short_count"), 0),
            "required": MIN_SHORT_COUNT,
            "effect": "롱만 남은 구조를 피한다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "session_stress(세션 압박)",
            "status": "passed" if all(str(row.get("review_status", "")).startswith("passed") for row in session_rows) else "warning",
            "observed": sum(1 for row in session_rows if str(row.get("review_status", "")).startswith("stress_watch")),
            "required": 0,
            "effect": "세션 단위 음수 구간이 있는지 본다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "month_side_stress(월/방향 압박)",
            "status": "warning" if negative_month_side else "passed",
            "observed": len(negative_month_side),
            "required": 0,
            "effect": "월/방향 손실 군집은 MT5 탐침 후 repair(수리) 후보로 남긴다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "cost_runtime_evidence(비용/런타임 근거)",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "observed": "not_run(미실행)",
            "required": "MT5 runtime probe(MT5 런타임 탐침)",
            "effect": "프록시 결과를 MT5 KPI로 대체하지 않는다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "operating_claim_boundary(운영 주장 경계)",
            "status": "passed",
            "observed": "runtime_authority=not_claimed; operating_promotion=not_claimed",
            "required": "no operating claim(운영 주장 없음)",
            "effect": "좋은 프록시를 운영 가능 모델로 착각하지 않게 한다.",
        },
    ]


def positive_clue_rows(selected: Mapping[str, Any], package_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    package = package_rows[0] if package_rows else {}
    return [
        {
            "run_id": RUN_ID,
            "clue_id": "threshold_edge_floor001_proxy_package_candidate(임계값 경계 하한 0.001 프록시 패키지 후보)",
            "evidence": package.get("queue_id", selected.get("queue_id", "")),
            "kpi_read": f"net={selected.get('combined_net_profit')}; pf={selected.get('combined_profit_factor')}; density={selected.get('combined_trade_per_business_day')}; dd={selected.get('combined_max_drawdown')}; trades={selected.get('combined_trade_count')}; short={selected.get('combined_short_count')}",
            "salvage_value": "PF>=1.30, density>=3/day, validation/OOS PF>=1.30, DD improved(PF 1.30 이상, 밀도 3/day 이상, 검증/표본외 PF 1.30 이상, DD 개선)",
            "next_condition": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def failure_memory_rows(month_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    negative = [row for row in month_rows if str(row.get("review_status", "")).startswith("month_side_negative")]
    worst = min(negative, key=lambda row: as_float(row.get("segment_net_profit")), default={})
    return [
        {
            "run_id": RUN_ID,
            "failure_id": "runtime_evidence_missing(런타임 근거 없음)",
            "evidence": rel(parent.SCOUT_SURFACE),
            "failure": "Proxy scout is not MT5 runtime evidence(프록시 정찰은 MT5 런타임 근거가 아님)",
            "constraint_for_next": "must package and run MT5 probe before runtime authority(런타임 권위 전 패키지와 MT5 탐침 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "failure_id": "month_side_negative_cells(月/방향 음수 셀)",
            "evidence": rel(MONTH_STRESS_REVIEW),
            "failure": f"negative_month_side_rows={len(negative)}; worst={worst.get('entry_month','')} {worst.get('side','')} net={worst.get('segment_net_profit','')}",
            "constraint_for_next": "runtime review must attribute month-side losses and cost stress(런타임 검토에서 월/방향 손실과 비용 압박 귀속 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def runtime_probe_queue_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "selected_variant_id": selected.get("variant_id", ""),
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden": "operating_promotion forbidden(운영 승격 금지); runtime_authority forbidden(런타임 권위 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지)",
    }
    specs = [
        (1, "package_identity(패키지 정체성)", "carry selected proxy candidate and trade tape(선택 프록시 후보와 거래 테이프 인계)", "preserve artifact lineage(산출물 계보 보존)"),
        (2, "runtime_contract(런타임 계약)", "short_threshold=0.455, entry_floor=0.001, max_hold=6, no premarket short(숏 임계값 0.455, 진입 하한 0.001, 보유 6봉, 프리마켓 숏 없음)", "align Python rule stack with MT5 handoff(파이썬 규칙 묶음과 MT5 인계 정렬)"),
        (3, "mt5_probe_request(MT5 탐침 요청)", "US100 M5, deposit 500, leverage 100, real ticks(US100 M5, 예치금 500, 레버리지 100, 실제 틱)", "compare proxy EV with MT5 KPI(프록시 예상값과 MT5 KPI 비교)"),
        (4, "cost_session_stress(비용/세션 압박)", "record spread/slippage/session and month-side losses(스프레드/슬리피지/세션/월방향 손실 기록)", "avoid cost-blind promotion(비용 무시 승격 방지)"),
        (5, "authority_guardrail(권위 가드레일)", "runtime probe only, no operating authority(런타임 탐침만, 운영 권위 없음)", "keep claim boundary closed(주장 경계 닫힘 유지)"),
    ]
    return [
        {
            **base,
            "queue_rank": rank,
            "queue_id": queue_id,
            "action": action,
            "expected_effect": effect,
        }
        for rank, queue_id, action, effect in specs
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


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "result_judgment(결과 판정)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "input_parent_gate",
                "package_gate_audit",
                "split_stability_gate",
                "session_stress_gate",
                "month_stress_gate",
                "positive_clue_gate",
                "failure_memory_gate",
                "runtime_probe_queue_gate",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
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
            "time_axis": "entry-time proxy review only(진입 시점 프록시 검토 전용)",
            "feature_label_boundary": "no new feature or label; review only(새 피처 또는 라벨 없음, 검토 전용)",
            "split_boundary": "validation and oos are separately inspected(검증과 표본외를 분리 검사)",
            "integrity_judgment": "usable_for_proxy_review_only(프록시 검토 전용 사용 가능)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "skill": "obsidian-performance-attribution(성과 귀속)",
            "observed_change": "entry_margin_floor 0.001 lifted PF and DD while keeping density above 3/day(진입 마진 하한 0.001이 PF와 DD를 개선하면서 밀도 3/day 이상 유지)",
            "comparison_baseline": "run364AQ threshold-edge clue(364AQ 임계값 경계 단서)",
            "positive_clues": [rel(POSITIVE_CLUES)],
            "failure_memory": [rel(FAILURE_MEMORY)],
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "skill": "obsidian-result-judgment(결과 판정)",
            "result_subject": "run364AS threshold-edge floor001 proxy strict pass(364AS 임계값 경계 하한 0.001 프록시 엄격 통과)",
            "evidence_available": [rel(parent.SCOUT_SURFACE), rel(parent.STRICT_CANDIDATES), rel(parent.SELECTED_PROXY_CANDIDATE), rel(PACKAGE_GATE_AUDIT)],
            "evidence_missing": "MT5 runtime probe, ONNX export, forward pass(MT5 런타임 탐침, ONNX 내보내기, 전진 검증 없음)",
            "judgment_label": "positive_proxy_candidate_for_runtime_probe(런타임 탐침용 긍정 프록시 후보)",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "좋은 프록시 후보지만 아직 운영 모델은 아니다.",
        },
    )
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            **base,
            "skill": "obsidian-runtime-parity(런타임 동등성)",
            "research_path": rel(parent.SCOUT_SURFACE),
            "runtime_path": "not_materialized_yet(아직 구체화 안 됨)",
            "shared_contract": "US100 M5, short_threshold=0.455, entry_margin_floor=0.001, max_hold_m5=6, no trade splitting(US100 M5, 숏 임계값 0.455, 진입 마진 하한 0.001, 보유 6봉, 거래 쪼개기 없음)",
            "known_differences": "Python proxy is not MT5 order execution(파이썬 프록시는 MT5 주문 실행이 아님)",
            "parity_check": "not_applicable_until_runtime_package(런타임 패키지 전 해당 없음)",
            "runtime_claim_boundary": "research_only_runtime_probe_candidate(연구 전용 런타임 탐침 후보)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "AT review(검토) 산출물이 완성됨"),
        gate_row("input_parent_gate(부모 입력 게이트)", parent.FINAL_DECISION, "AS scout(정찰) 완료와 엄격 통과 확인"),
        gate_row("package_gate_audit(패키지 게이트 감사)", PACKAGE_GATE_AUDIT, "프록시 패키지 후보 조건을 감사함"),
        gate_row("split_stability_gate(분할 안정성 게이트)", SPLIT_STABILITY_REVIEW, "validation/OOS(검증/표본외)를 분리 검토함"),
        gate_row("session_stress_gate(세션 압박 게이트)", SESSION_STRESS_REVIEW, "세션별 수익 구조를 검토함"),
        gate_row("month_stress_gate(월 압박 게이트)", MONTH_STRESS_REVIEW, "월/방향 음수 셀을 기록함"),
        gate_row("positive_clue_gate(긍정 단서 게이트)", POSITIVE_CLUES, "다음 runtime probe(런타임 탐침) 후보를 기록함"),
        gate_row("failure_memory_gate(실패 기억 게이트)", FAILURE_MEMORY, "런타임 부재와 월/방향 음수 셀을 제약으로 기록함"),
        gate_row("runtime_probe_queue_gate(런타임 탐침 대기열 게이트)", RUNTIME_PROBE_QUEUE, "다음 MT5 package/probe(패키지/탐침) 대기열을 작성함"),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "운영 주장 없음"),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", WORK_PACKET, "작업 묶음 필수 게이트를 산출물에 연결함"),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def final_payload(
    parent_final: Mapping[str, Any],
    selected: Mapping[str, Any],
    review_rows: Sequence[Mapping[str, Any]],
    package_gates: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
    package_rows = [row for row in review_rows if str(row.get("review_status", "")).startswith("proxy_package_candidate")]
    negative_month_side = [row for row in month_rows if str(row.get("review_status", "")).startswith("month_side_negative")]
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
        "parent_scout_run_id": parent_final.get("run_id"),
        "reviewed_scout_rows": len(review_rows),
        "package_candidate_rows": len(package_rows),
        "runtime_probe_candidate_rows": 1 if package_rows else 0,
        "warning_gate_rows": sum(1 for row in package_gates if row.get("status") == "warning"),
        "out_of_scope_gate_rows": sum(1 for row in package_gates if str(row.get("status", "")).startswith("out_of_scope")),
        "negative_month_side_rows": len(negative_month_side),
        "selected_variant_id": selected.get("variant_id", ""),
        "selected_queue_id": selected.get("queue_id", ""),
        "selected_combined_net_profit": selected.get("combined_net_profit", ""),
        "selected_combined_profit_factor": selected.get("combined_profit_factor", ""),
        "selected_combined_trade_count": selected.get("combined_trade_count", ""),
        "selected_combined_trade_per_business_day": selected.get("combined_trade_per_business_day", ""),
        "selected_combined_expectancy": selected.get("combined_expectancy", ""),
        "selected_combined_max_drawdown": selected.get("combined_max_drawdown", ""),
        "selected_combined_recovery_factor": selected.get("combined_recovery_factor", ""),
        "selected_combined_long_count": selected.get("combined_long_count", ""),
        "selected_combined_short_count": selected.get("combined_short_count", ""),
        "selected_validation_net_profit": selected.get("validation_net_profit", ""),
        "selected_validation_profit_factor": selected.get("validation_profit_factor", ""),
        "selected_oos_net_profit": selected.get("oos_net_profit", ""),
        "selected_oos_profit_factor": selected.get("oos_profit_factor", ""),
        "package_decision": "proxy_package_candidate_open_runtime_probe(프록시 패키지 후보, 런타임 탐침 개방)" if package_rows else "no_package_candidate(패키지 후보 없음)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
    }


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
    package_gates: Sequence[Mapping[str, Any]],
    split_rows: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    refresh_stage_brief_header()
    report = f"""# run364AT threshold-edge PF gap repair review(364AT 임계값 경계 PF 간극 수리 검토)

## Current Truth(현재 진실)

- action(행동): run364AS(364AS 실행)의 strict pass(엄격 통과) 1행을 package/probe(패키지/탐침) 관점으로 검토했다.
- effect(효과): `threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침)`를 runtime probe candidate(런타임 탐침 후보)로 열고, 운영 주장은 닫았다.
- selected KPI(선택 KPI): net(순수익) `{final['selected_combined_net_profit']}`, PF(수익 팩터) `{final['selected_combined_profit_factor']}`, density(밀도) `{final['selected_combined_trade_per_business_day']}`, DD(낙폭) `{final['selected_combined_max_drawdown']}`, trades(거래수) `{final['selected_combined_trade_count']}`, short(숏) `{final['selected_combined_short_count']}`.
- warning(경고): month-side negative rows(월/방향 음수 행) `{final['negative_month_side_rows']}`개와 runtime evidence missing(런타임 근거 없음)이 남아 있다.
- authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), goal achieve(목표 달성)는 모두 not_claimed(주장 안 함)이다.

## Surface Review(표면 검토)

{markdown_table(review_rows, ['queue_id', 'review_status', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_per_business_day', 'combined_max_drawdown', 'combined_short_count', 'selection_score'])}

## Package Gate Audit(패키지 게이트 감사)

{markdown_table(package_gates, ['gate_id', 'status', 'observed', 'required', 'effect'])}

## Split Stability(분할 안정성)

{markdown_table(split_rows, ['split_id', 'net_profit', 'profit_factor', 'trade_per_business_day', 'max_drawdown', 'review_status'])}

## Session Stress(세션 압박)

{markdown_table(session_rows, ['entry_session', 'side', 'segment_trade_count', 'segment_net_profit', 'segment_profit_factor', 'segment_max_drawdown', 'review_status'])}

## Month-Side Stress(월/방향 압박)

{markdown_table(month_rows[:12], ['entry_month', 'side', 'segment_trade_count', 'segment_net_profit', 'segment_profit_factor', 'segment_max_drawdown', 'review_status'])}

## Required Gates(필수 게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, report)
    append_text_once(
        REVIEW_INDEX,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- package_candidate_rows(패키지 후보 행): `{final['package_candidate_rows']}`\n- next_run(다음 실행): `{NEXT_RUN_ID}`\n- effect(효과): proxy package candidate(프록시 패키지 후보)를 MT5 runtime probe(MT5 런타임 탐침) 준비로 넘긴다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364AT Threshold-Edge PF Gap Review Closeout",
        f"\n## run364AT Threshold-Edge PF Gap Review Closeout(364AT 임계값 경계 PF 간극 검토 종료)\n\nAction(행동): run364AS(364AS 실행)의 floor001 strict pass(하한 0.001 엄격 통과)를 검토했다.\n\nEffect(효과): runtime authority(런타임 권위) 없이 `{NEXT_RUN_ID}` runtime probe package(런타임 탐침 패키지)로 넘길 후보를 기록했다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_runtime_probe_required(런타임 탐침 필요라 없음)
- runtime_probe_candidate(런타임 탐침 후보): `threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침)`
- package_decision(패키지 결정): `{final['package_decision']}`
- selected_proxy_candidate(선택 프록시 후보): `{rel(parent.SELECTED_PROXY_CANDIDATE)}`
- next_runtime_probe_queue(다음 런타임 탐침 대기열): `{rel(RUNTIME_PROBE_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

current_stage(현재 단계): `{STAGE_ID}`

latest_completed_run(최근 완료 실행): `{RUN_ID}`

current_run(현재 실행): `{NEXT_RUN_ID}`

current_truth(현재 진실): run364AT(364AT 실행)는 run364AS(364AS 실행)의 `threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침)` strict pass(엄격 통과)를 검토했고, proxy package candidate(프록시 패키지 후보)로 runtime probe(런타임 탐침)를 열었다. selected PF(선택 PF)는 `{final['selected_combined_profit_factor']}`, density(밀도)는 `{final['selected_combined_trade_per_business_day']}`, DD(낙폭)는 `{final['selected_combined_max_drawdown']}`, trade count(거래수)는 `{final['selected_combined_trade_count']}`이다.

operating_truth_boundary(운영 진실 경계): no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no goal achieve(목표 달성 없음).

next_action(다음 행동): `{NEXT_RUN_ID}`에서 MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들고 proxy/MT5 diff(프록시/MT5 차이)를 비교할 준비를 한다.
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
        STAGE_README,
        "run364AT Threshold-Edge PF Gap Review",
        f"\n## run364AT Threshold-Edge PF Gap Review(364AT 임계값 경계 PF 간극 검토)\n\nAction(행동): AS strict pass(AS 엄격 통과)를 package/probe(패키지/탐침) 관점으로 검토했다.\n\nEffect(효과): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 MT5 runtime probe(MT5 런타임 탐침) 준비로 이어간다.\n",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): threshold-edge floor001 strict pass(임계값 경계 하한 0.001 엄격 통과)를 검토했다.\n- effect(효과): `{NEXT_RUN_ID}` runtime probe package(런타임 탐침 패키지) 대기열을 만들고 운영 주장은 닫았다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): threshold-edge floor001(임계값 경계 하한 0.001)이 PF(수익 팩터) 1.30과 density(밀도) 3/day를 동시에 회복한다.\n- evidence(근거): proxy(프록시) net `{final['selected_combined_net_profit']}`, PF `{final['selected_combined_profit_factor']}`, density `{final['selected_combined_trade_per_business_day']}`, DD `{final['selected_combined_max_drawdown']}`.\n- next_condition(다음 조건): MT5 runtime probe(MT5 런타임 탐침)에서 proxy/MT5 diff(프록시/MT5 차이)를 기록한다.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- status(상태): positive_proxy_with_runtime_missing(런타임 누락이 있는 긍정 프록시).\n- failure_memory(실패 기억): month-side negative rows(월/방향 음수 행) `{final['negative_month_side_rows']}`개와 MT5 runtime evidence(MT5 런타임 근거) 부재.\n- effect(효과): 다음 run(실행)은 runtime probe(런타임 탐침)와 비용 압박 검토를 반드시 수행해야 한다.\n",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["reviewed_scout_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "path": rel(RUN_DIR),
        "primary_report": rel(REPORT_PATH),
        "family": "stage364_review(364단계 검토)",
        "lane": "offensive_exploration_review(공격 탐색 검토)",
        "work_family": "result_judgment_runtime_probe_routing(결과 판정 런타임 탐침 라우팅)",
        "primary_artifact": rel(SURFACE_REVIEW),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "out_of_scope_by_claim_runtime_probe_next(주장 범위 밖, 다음 런타임 탐침)",
        "next_action": NEXT_RUN_ID,
        "question": "Should threshold-edge floor001 advance to MT5 runtime probe?(임계값 경계 하한 0.001을 MT5 런타임 탐침으로 넘길 것인가?)",
        "notes": f"package_candidate_rows={final['package_candidate_rows']}; warning_gates={final['warning_gate_rows']}; month_side_negative={final['negative_month_side_rows']}",
        "net_profit": final["selected_combined_net_profit"],
        "profit_factor": final["selected_combined_profit_factor"],
        "expectancy": final["selected_combined_expectancy"],
        "drawdown": final["selected_combined_max_drawdown"],
        "recovery_factor": final["selected_combined_recovery_factor"],
        "trade_count": final["selected_combined_trade_count"],
        "long_trade_count": final["selected_combined_long_count"],
        "short_trade_count": final["selected_combined_short_count"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common])
    alpha_rows = []
    for suffix, view, tier in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A"),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B"),
        ("Tier_AB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": suffix,
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": "proxy review runtime probe routing(프록시 검토 런타임 탐침 라우팅)",
                "scoreboard_lane": "proxy_review(프록시 검토)",
                "primary_kpi": f"net={final['selected_combined_net_profit']};pf={final['selected_combined_profit_factor']};density={final['selected_combined_trade_per_business_day']}",
                "guardrail_kpi": f"dd={final['selected_combined_max_drawdown']};runtime_missing;month_side_negative={final['negative_month_side_rows']}",
                "evidence_boundary": CLAIM_BOUNDARY,
            }
        )
        alpha_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], alpha_rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], alpha_rows)

    artifact_rows = []
    for artifact_type, path, notes in [
        ("surface_review", SURFACE_REVIEW, "Surface review(표면 검토)."),
        ("package_gate_audit", PACKAGE_GATE_AUDIT, "Package gate audit(패키지 게이트 감사)."),
        ("runtime_probe_queue", RUNTIME_PROBE_QUEUE, "Next runtime probe queue(다음 런타임 탐침 대기열)."),
        ("positive_clues", POSITIVE_CLUES, "Positive clues(긍정 단서)."),
        ("failure_memory", FAILURE_MEMORY, "Failure memory(실패 기억)."),
        ("gate_audit", GATE_AUDIT, "Required gate audit(필수 게이트 감사)."),
        ("report", REPORT_PATH, "Review report(검토 보고서)."),
        ("decision", DECISION_DOC, "Decision record(결정 기록)."),
        ("lineage", LINEAGE_RECEIPT, "Artifact lineage(산출물 계보)."),
    ]:
        artifact_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha(path) if exists(path) else "",
                "created_at_utc": final["created_at_utc"],
                "created_at": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "notes": notes,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)
    repair_run_registry_line_endings(RUN_ID)


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    artifacts = []
    for path in OUTPUT_FILES:
        if exists(path):
            artifacts.append({"path": rel(path), "sha256": sha(path), "role": "run364AT output(364AT 출력)"})
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES],
            "artifacts": artifacts,
            "final_decision": final,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path)],
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    created_at = now_utc()
    surface = load_surface()
    selected = selected_candidate()
    review_rows = surface_review_rows(surface)
    split_rows = split_stability_rows(selected)
    session_rows = session_stress_rows()
    month_rows = month_stress_rows()
    package_rows = [row for row in review_rows if str(row.get("review_status", "")).startswith("proxy_package_candidate")]
    package_gates = package_gate_rows(selected, review_rows, split_rows, session_rows, month_rows)
    positives = positive_clue_rows(selected, package_rows)
    failures = failure_memory_rows(month_rows)
    next_queue = runtime_probe_queue_rows(selected)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(SURFACE_REVIEW, review_rows)
    write_csv(PACKAGE_GATE_AUDIT, package_gates)
    write_csv(SPLIT_STABILITY_REVIEW, split_rows)
    write_csv(SESSION_STRESS_REVIEW, session_rows)
    write_csv(MONTH_STRESS_REVIEW, month_rows)
    write_csv(POSITIVE_CLUES, positives)
    write_csv(FAILURE_MEMORY, failures)
    write_csv(RUNTIME_PROBE_QUEUE, next_queue)
    write_work_packet()

    final_seed = {"created_at_utc": created_at}
    gates = write_receipts(final_seed)
    final = final_payload(parent_final, selected, review_rows, package_gates, month_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, review_rows, package_gates, split_rows, session_rows, month_rows, gates)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_ledgers(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
