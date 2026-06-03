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

from stage_pipelines.stage364 import train_hold6_pf_dd_repair_offensive_scout_without_db as parent  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AQ"
RUN_ID = "run364AQ_review_hold6_pf_dd_repair_offensive_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.PARENT_RUN_ID
NEXT_RUN_ID = "run364AR_materialize_threshold_edge_pf_gap_repair_inputs_without_db_v1"

STATUS = "completed_stage364AQ_hold6_pf_dd_repair_review_negative_for_package_threshold_edge_clue_no_authority"
JUDGMENT = "negative_for_package_positive_for_threshold_edge_pf_dd_seed_no_authority"
DECISION = "stage364AQ_no_package_open_run364AR_threshold_edge_pf_gap_repair_inputs"
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
PACKAGE_GATE_AUDIT = RUN_DIR / "package_gate_audit.csv"
POLICY_FAILURE_ATTRIBUTION = RUN_DIR / "policy_failure_attribution.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364AR_materialization_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AQ_hold6_pf_dd_repair_offensive_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AQ_hold6_pf_dd_repair_offensive_review.md"
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
    parent.RUN364AQ_QUEUE,
    parent.REPORT_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SURFACE_REVIEW,
    PACKAGE_GATE_AUDIT,
    POLICY_FAILURE_ATTRIBUTION,
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
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


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


def validate_inputs() -> Mapping[str, Any]:
    parent_final = read_json(parent.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if parent_final.get("runtime_authority") != "not_claimed" or parent_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 gate, 게이트가 모두 통과하지 않음)")
    if int(parent_final.get("strict_pass_rows", -1)) != 0:
        raise RuntimeError("unexpected strict pass rows for review path(검토 경로의 엄격 통과 행 수가 예상과 다름)")
    surface = read_csv_rows(parent.SCOUT_SURFACE)
    if len(surface) != 7:
        raise RuntimeError(f"unexpected AP surface rows(AP 표면 행 수 이상): {len(surface)}")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AQ inputs(364AQ 입력 누락): " + ", ".join(missing))
    return parent_final


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


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "hold6_pf_dd_repair_proxy_scout_surface.csv":
        return "parent scout surface(부모 정찰 표면)"
    if name == "queue_replay_audit.csv":
        return "parent replay audit(부모 재생 감사)"
    if name == "run364AQ_review_queue.csv":
        return "parent review queue(부모 검토 대기열)"
    if "summary" in name:
        return "segment summary(구간 요약)"
    if name.endswith(".json"):
        return "decision or receipt(결정 또는 영수증)"
    return "supporting evidence(보조 근거)"


def load_surface() -> pd.DataFrame:
    df = pd.read_csv(parent.SCOUT_SURFACE, encoding="utf-8-sig")
    for col in [
        "combined_net_profit",
        "combined_profit_factor",
        "combined_trade_count",
        "combined_trade_per_business_day",
        "combined_expectancy",
        "combined_max_drawdown",
        "combined_recovery_factor",
        "combined_long_count",
        "combined_short_count",
        "validation_net_profit",
        "validation_profit_factor",
        "oos_net_profit",
        "oos_profit_factor",
        "pf_delta_vs_run364AO_hold6_seed",
        "density_delta_vs_run364AO_hold6_seed",
        "dd_delta_vs_run364AO_hold6_seed",
        "selection_score",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def review_status(row: Mapping[str, Any]) -> str:
    pf = as_float(row.get("combined_profit_factor"))
    density = as_float(row.get("combined_trade_per_business_day"))
    val_net = as_float(row.get("validation_net_profit"))
    oos_net = as_float(row.get("oos_net_profit"))
    short_count = as_float(row.get("combined_short_count"))
    pf_delta = as_float(row.get("pf_delta_vs_run364AO_hold6_seed"))
    dd_delta = as_float(row.get("dd_delta_vs_run364AO_hold6_seed"))
    if pf >= TARGET_PF and density >= DENSITY_FLOOR and val_net > 0 and oos_net > 0 and short_count > 0:
        return "package_candidate(패키지 후보)"
    if pf >= TARGET_PF and density < DENSITY_FLOOR:
        return "pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗)"
    if density >= DENSITY_FLOOR and pf_delta > 0 and dd_delta > 0 and pf < TARGET_PF:
        return "pf_dd_lift_density_safe_seed(PF/DD 개선, 밀도 안전 씨앗)"
    if density >= DENSITY_FLOOR and dd_delta > 0 and pf < TARGET_PF:
        return "dd_lift_density_safe_seed(DD 개선, 밀도 안전 씨앗)"
    if density >= DENSITY_FLOOR and pf < TARGET_PF:
        return "density_safe_pf_fail(밀도 안전, PF 실패)"
    return "reject_or_watch(거절 또는 관찰)"


def surface_review_rows(surface: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, raw in surface.iterrows():
        row = raw.to_dict()
        status = review_status(row)
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row.get("queue_id", ""),
                "variant_id": row.get("variant_id", ""),
                "review_status": status,
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
                "pf_delta_vs_hold6": finite(row.get("pf_delta_vs_run364AO_hold6_seed")),
                "density_delta_vs_hold6": finite(row.get("density_delta_vs_run364AO_hold6_seed")),
                "dd_delta_vs_hold6": finite(row.get("dd_delta_vs_run364AO_hold6_seed")),
                "selection_score": finite(row.get("selection_score")),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rank = {
        "package_candidate": 6,
        "pf_dd_lift_density_safe_seed": 5,
        "dd_lift_density_safe_seed": 4,
        "density_safe_pf_fail": 3,
        "pf_pass_density_fail_seed": 2,
    }
    rows.sort(
        key=lambda item: (
            max((score for prefix, score in rank.items() if str(item["review_status"]).startswith(prefix)), default=0),
            as_float(item["combined_profit_factor"]),
            as_float(item["combined_trade_per_business_day"]),
            as_float(item["combined_net_profit"]),
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
            as_float(row.get("combined_trade_per_business_day")),
            as_float(row.get("combined_short_count")),
            as_float(row.get("combined_profit_factor")),
        ),
    )


def package_gate_rows(parent_final: Mapping[str, Any], review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    package_rows = [row for row in review_rows if str(row.get("review_status", "")).startswith("package_candidate")]
    selected_pf = as_float(parent_final.get("selected_combined_profit_factor"))
    selected_density = as_float(parent_final.get("selected_combined_trade_per_business_day"))
    selected_dd = as_float(parent_final.get("selected_combined_max_drawdown"))
    return [
        {
            "run_id": RUN_ID,
            "gate_id": "strict_package_rows(엄격 패키지 행)",
            "status": "failed" if not package_rows else "passed",
            "observed": len(package_rows),
            "required": 1,
            "effect": "PF/density/split/side 조건을 동시에 만족하지 못해 package(패키지)를 닫는다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "selected_profit_factor_target(선택 PF 목표)",
            "status": "failed" if selected_pf < TARGET_PF else "passed",
            "observed": selected_pf,
            "required": TARGET_PF,
            "effect": "선택 후보의 PF(수익 팩터)가 목표 미달이라 운영 후보가 아니다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "selected_density_floor(선택 밀도 하한)",
            "status": "passed" if selected_density >= DENSITY_FLOOR else "failed",
            "observed": selected_density,
            "required": DENSITY_FLOOR,
            "effect": "밀도는 살아 있어 다음 탐색 씨앗으로 보존한다.",
        },
        {
            "run_id": RUN_ID,
            "gate_id": "selected_drawdown_quality(선택 낙폭 품질)",
            "status": "failed" if selected_dd < -147.924 else "passed",
            "observed": selected_dd,
            "required": ">= -147.924 threshold-edge clue(임계값 경계 단서 이상)",
            "effect": "선택 대조보다 threshold edge(임계값 경계)가 낙폭 품질을 더 잘 고쳤다.",
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


def policy_failure_rows(review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in review_rows:
        pf = as_float(row.get("combined_profit_factor"))
        density = as_float(row.get("combined_trade_per_business_day"))
        dd_delta = as_float(row.get("dd_delta_vs_hold6"))
        if pf >= TARGET_PF and density < DENSITY_FLOOR:
            cause = "pf_good_density_shortfall(PF 양호, 밀도 부족)"
        elif density >= DENSITY_FLOOR and pf < TARGET_PF and dd_delta > 0:
            cause = "pf_gap_after_dd_repair(낙폭 수리 뒤 PF 간극)"
        elif density >= DENSITY_FLOOR and pf < TARGET_PF:
            cause = "density_safe_pf_shortfall(밀도 안전, PF 부족)"
        else:
            cause = "weak_or_watch(약함 또는 관찰)"
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row.get("queue_id", ""),
                "variant_id": row.get("variant_id", ""),
                "cause": cause,
                "combined_net_profit": row.get("combined_net_profit", ""),
                "combined_profit_factor": row.get("combined_profit_factor", ""),
                "combined_trade_per_business_day": row.get("combined_trade_per_business_day", ""),
                "combined_max_drawdown": row.get("combined_max_drawdown", ""),
                "effect": "다음 materialization(구체화)에서 PF 간극과 DD 수리 축을 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def positive_clue_rows(parent_final: Mapping[str, Any], review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    pf_dd = best_with_prefix(review_rows, "pf_dd_lift_density_safe_seed")
    dd_lift = best_with_prefix(review_rows, "dd_lift_density_safe_seed")
    pf_pass = best_with_prefix(review_rows, "pf_pass_density_fail_seed")
    return [
        {
            "run_id": RUN_ID,
            "clue_id": "threshold_edge_pf_dd_lift(임계값 경계 PF/DD 개선)",
            "evidence": pf_dd.get("queue_id", ""),
            "kpi_read": f"net={pf_dd.get('combined_net_profit')}; pf={pf_dd.get('combined_profit_factor')}; density={pf_dd.get('combined_trade_per_business_day')}; dd={pf_dd.get('combined_max_drawdown')}",
            "salvage_value": "PF and DD improved while density stayed above 3/day(PF와 DD가 개선되고 밀도 3/day 이상 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "clue_id": "late_long_pf_lift_density_safe(후반 롱 PF 개선, 밀도 안전)",
            "evidence": dd_lift.get("queue_id", ""),
            "kpi_read": f"net={dd_lift.get('combined_net_profit')}; pf={dd_lift.get('combined_profit_factor')}; density={dd_lift.get('combined_trade_per_business_day')}; dd={dd_lift.get('combined_max_drawdown')}",
            "salvage_value": "PF lift is stronger but short side thins(PF 개선은 강하지만 숏이 얇아짐)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "clue_id": "sparse_pf_anchor_density_gap(희소 PF 기준 밀도 간극)",
            "evidence": pf_pass.get("queue_id", ""),
            "kpi_read": f"net={pf_pass.get('combined_net_profit')}; pf={pf_pass.get('combined_profit_factor')}; density={pf_pass.get('combined_trade_per_business_day')}; dd={pf_pass.get('combined_max_drawdown')}",
            "salvage_value": "PF>=1.30 exists but density below 3/day(PF 1.30 이상은 있으나 밀도 3/day 미만)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def failure_memory_rows(parent_final: Mapping[str, Any], review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "failure_id": "strict_pass_zero(엄격 통과 0)",
            "evidence": rel(parent.SCOUT_SURFACE),
            "failure": "No row passed PF>=1.30 and density>=3/day together(PF 1.30 이상과 밀도 3/day 이상 동시 통과 없음)",
            "constraint_for_next": "next run cannot package or MT5 probe without new strict proxy pass(다음 실행은 새 엄격 프록시 통과 없이 패키지나 MT5 탐침 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "failure_id": "hold6_anchor_pf_below_target(6봉 기준 PF 목표 미달)",
            "evidence": parent_final.get("selected_variant_id", ""),
            "failure": f"hold6 PF={parent_final.get('selected_combined_profit_factor')} below {TARGET_PF}",
            "constraint_for_next": "preserve density while targeting PF gap about 0.02(밀도를 보존하며 약 0.02 PF 간극을 겨냥)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "failure_id": "sparse_pf_density_below_floor(희소 PF 밀도 하한 미달)",
            "evidence": "sparse PF rows(PF 희소 행)",
            "failure": "PF-pass rows remain around 2.66/day density(PF 통과 행은 밀도 약 2.66/day에 머묾)",
            "constraint_for_next": "do not use trade splitting to fake density(거래 쪼개기로 밀도를 만들지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def next_queue_rows(review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    threshold = best_with_prefix(review_rows, "pf_dd_lift_density_safe_seed")
    late = best_with_prefix(review_rows, "dd_lift_density_safe_seed")
    pf_pass = best_with_prefix(review_rows, "pf_pass_density_fail_seed")
    seeds = {
        "threshold": threshold.get("variant_id", ""),
        "late": late.get("variant_id", ""),
        "pf_pass": pf_pass.get("variant_id", ""),
    }
    base = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "forbidden": "top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지)",
        "timestamp_boundary": "entry_time_known_only(진입 시점에 알려진 값만 사용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    specs = [
        (1, "threshold_edge_hold6_control", seeds["threshold"], "control", "replay threshold-edge PF/DD lift(임계값 경계 PF/DD 개선 재생)", "hold density>=3 and DD near -148 while lifting PF(PF 상승 중 밀도 3 이상과 DD -148 근처 유지)"),
        (2, "late_long_hold6_control", seeds["late"], "control", "replay late-long PF lift(후반 롱 PF 개선 재생)", "test PF lift but watch short-side collapse(PF 개선 시험, 숏 붕괴 관찰)"),
        (3, "threshold_edge_hold5_probe", seeds["threshold"], "candidate", "shorten threshold-edge hold to 5(임계값 경계 보유 5로 단축)", "reduce DD and possibly lift PF without losing density(밀도 손실 없이 DD 축소와 PF 상승 시도)"),
        (4, "threshold_edge_hold4_probe", seeds["threshold"], "candidate", "shorten threshold-edge hold to 4(임계값 경계 보유 4로 단축)", "stress trade shape for PF/DD(PF/DD 거래 형태 압박)"),
        (5, "threshold_edge_floor001_probe", seeds["threshold"], "candidate", "micro floor 0.001 on threshold edge(임계값 경계 마진 하한 0.001)", "remove weakest low-margin trades lightly(약한 저마진 거래만 가볍게 제거)"),
        (6, "threshold_edge_late_long_blend_probe", seeds["threshold"], "candidate", "blend threshold edge with late-long patch(임계값 경계와 후반 롱 패치 결합)", "try PF lift while keeping threshold-edge DD(임계값 경계 DD를 유지하며 PF 상승 시도)"),
        (7, "pf_pass_density_bridge_hold6_probe", seeds["pf_pass"], "candidate", "apply hold6 shape to sparse PF density bridge(희소 PF 밀도 연결에 6봉 형태 적용)", "bridge density without splitting trades(거래 쪼개기 없이 밀도 연결)"),
        (8, "loss_guard_policy_implementation_gate", seeds["threshold"], "guardrail", "implement or explicitly skip loss guard policy(손실 가드 정책 구현 또는 명시 건너뜀)", "avoid silent new-policy execution(새 정책 조용한 실행 방지)"),
    ]
    rows = []
    for rank, queue_id, source_variant_id, queue_type, question, effect in specs:
        rows.append(
            {
                **base,
                "queue_rank": rank,
                "queue_id": queue_id,
                "source_variant_id": source_variant_id,
                "queue_type": queue_type,
                "materialization_question": question,
                "expected_effect": effect,
            }
        )
    return rows


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
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "input_parent_gate",
                "package_gate_audit",
                "failure_memory_gate",
                "positive_clue_gate",
                "next_queue_gate",
                "data_integrity_audit",
                "performance_attribution_gate",
                "result_judgment_gate",
                "artifact_lineage_audit",
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
            "time_axis": "entry-time replay review only(진입 시점 재생 검토 전용)",
            "feature_label_boundary": "no new feature or label; review only(새 피처 또는 라벨 없음, 검토 전용)",
            "split_boundary": "validation and oos remain separate in source surface(원천 표면에서 검증/표본외 분리 유지)",
            "leakage_risk": "next queue forbids OOS threshold selection(다음 대기열은 표본외 임계값 선택 금지)",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "skill": "obsidian-performance-attribution(성과 귀속)",
            "observed_change": "threshold edge lifted PF and DD but did not reach PF 1.30(임계값 경계가 PF와 DD를 개선했지만 PF 1.30 미달)",
            "comparison_baseline": PARENT_RUN_ID,
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
            "result_subject": RUN_ID,
            "evidence_available": [rel(SURFACE_REVIEW), rel(PACKAGE_GATE_AUDIT), rel(POSITIVE_CLUES), rel(FAILURE_MEMORY)],
            "evidence_missing": "MT5 runtime probe(MT5 런타임 탐침)",
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "negative for package, positive for next offensive seed(패키지는 부정, 다음 공격 씨앗은 긍정)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "review(검토)를 운영 주장으로 연결하지 않는다.",
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
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AQ review(364AQ 검토)를 완료했다."),
        gate_row("input_parent_gate(부모 입력 게이트)", INPUT_MANIFEST, "run364AP 산출물을 확인했다."),
        gate_row("package_gate_audit(패키지 게이트 감사)", PACKAGE_GATE_AUDIT, "strict package(엄격 패키지)가 없음을 기록했다."),
        gate_row("failure_memory_gate(실패 기억 게이트)", FAILURE_MEMORY, "실패를 다음 제약으로 전환했다."),
        gate_row("positive_clue_gate(긍정 단서 게이트)", POSITIVE_CLUES, "threshold edge(임계값 경계) 단서를 보존했다."),
        gate_row("next_queue_gate(다음 대기열 게이트)", NEXT_QUEUE, "run364AR 대기열을 만들었다."),
        gate_row("data_integrity_audit(데이터 무결성 감사)", DATA_RECEIPT, "timestamp-safe(시점 안전) 경계를 기록했다."),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "PF/DD 개선과 밀도 실패 원인을 분리했다."),
        gate_row("result_judgment_gate(결과 판정 게이트)", JUDGMENT_RECEIPT, "패키지 부정, 씨앗 긍정으로 판정했다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 hash(해시)를 연결했다."),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "운영 승격을 주장하지 않았다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "필수 gate(게이트)를 종료 기록에 연결했다."),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def final_payload(parent_final: Mapping[str, Any], review_rows: Sequence[Mapping[str, Any]], next_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    package_rows = [row for row in review_rows if str(row.get("review_status", "")).startswith("package_candidate")]
    pf_dd_rows = [row for row in review_rows if str(row.get("review_status", "")).startswith("pf_dd_lift_density_safe_seed")]
    pf_pass_density_fail_rows = [row for row in review_rows if str(row.get("review_status", "")).startswith("pf_pass_density_fail_seed")]
    threshold = best_with_prefix(review_rows, "pf_dd_lift_density_safe_seed")
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
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "reviewed_scout_rows": len(review_rows),
        "package_candidate_rows": len(package_rows),
        "pf_dd_lift_density_safe_rows": len(pf_dd_rows),
        "pf_pass_density_fail_rows": len(pf_pass_density_fail_rows),
        "next_queue_rows": len(next_rows),
        "selected_parent_net_profit": parent_final.get("selected_combined_net_profit"),
        "selected_parent_profit_factor": parent_final.get("selected_combined_profit_factor"),
        "selected_parent_density": parent_final.get("selected_combined_trade_per_business_day"),
        "selected_parent_drawdown": parent_final.get("selected_combined_max_drawdown"),
        "positive_clue_variant_id": threshold.get("variant_id", ""),
        "positive_clue_profit_factor": threshold.get("combined_profit_factor", ""),
        "positive_clue_density": threshold.get("combined_trade_per_business_day", ""),
        "positive_clue_drawdown": threshold.get("combined_max_drawdown", ""),
        "package_decision": "no_package_strict_rows_zero(PF/density 동시 통과 없음)",
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


def write_docs(final: Mapping[str, Any], review_rows: Sequence[Mapping[str, Any]], clues: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header()
    text = f"""# run364AQ hold6 PF/DD repair review(364AQ 6봉 PF/DD 수리 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- package_candidate_rows(패키지 후보 행): `{final['package_candidate_rows']}`
- pf_dd_lift_density_safe_rows(PF/DD 개선, 밀도 안전 행): `{final['pf_dd_lift_density_safe_rows']}`
- pf_pass_density_fail_rows(PF 통과, 밀도 실패 행): `{final['pf_pass_density_fail_rows']}`
- runtime_authority(런타임 권위): `not_claimed`

## Reviewed Surface(검토 표면)

{markdown_table(review_rows, ['queue_id', 'review_status', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_per_business_day', 'combined_max_drawdown', 'combined_short_count'])}

## Positive Clues(긍정 단서)

{markdown_table(clues, ['clue_id', 'evidence', 'kpi_read', 'salvage_value'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): run364AQ(364AQ 실행)는 package(패키지)를 만들지 않고, threshold edge(임계값 경계) 단서를 run364AR(364AR 실행) 입력으로 넘긴다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- package_candidate_rows(패키지 후보 행): `{final['package_candidate_rows']}`\n- next_action(다음 행동): `{NEXT_RUN_ID}`\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364AQ Hold6 PF/DD Repair Review Closeout",
        f"\n## run364AQ Hold6 PF/DD Repair Review Closeout(364AQ 6봉 PF/DD 수리 검토 종료)\n\nAction(행동): run364AP(364AP 실행) proxy surface(프록시 표면)를 검토해 package(패키지)를 부정하고 threshold edge(임계값 경계) PF/DD 개선 단서를 보존했다.\n\nEffect(효과): Stage364(364단계) 안에서 stage(단계) 분기 없이 run364AR(364AR 실행) materialization(구체화)로 이어간다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_review_negative_for_package(패키지 부정 검토라 없음)
- latest_proxy_review(최근 프록시 검토): `{RUN_ID}`
- package_decision(패키지 결정): `{final['package_decision']}`
- preserved_clues(보존 단서): threshold_edge_pf_dd_lift(임계값 경계 PF/DD 개선), sparse_pf_density_gap(희소 PF 밀도 간극)
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

current_truth(현재 진실): run364AQ(364AQ 실행)는 run364AP(364AP 실행)를 검토해 package_candidate_rows(패키지 후보 행) `0`을 확인했다. threshold edge(임계값 경계)는 PF(수익 팩터) `{final['positive_clue_profit_factor']}`, density(밀도) `{final['positive_clue_density']}`, DD(낙폭) `{final['positive_clue_drawdown']}`로 PF/DD 개선 단서지만 운영 후보는 아니다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 threshold edge(임계값 경계) PF gap(PF 간극) 수리 입력을 구체화한다.

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
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): hold6 PF/DD repair review(6봉 PF/DD 수리 검토)를 닫았다.\n- effect(효과): package(패키지)는 부정하고 `{NEXT_RUN_ID}` queue(대기열)를 만들었다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): threshold edge(임계값 경계)가 PF/DD를 동시에 조금 개선하지만 PF 1.30에는 부족하다.\n- effect(효과): 보유 기간, 미세 하한, late-long blend(후반 롱 결합) 축으로 다음 공격 탐색을 연다.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- negative_result(부정 결과): strict_pass_rows(엄격 통과 행) 0, package_candidate_rows(패키지 후보 행) 0.\n- effect(효과): MT5 runtime probe(MT5 런타임 탐침)로 승격하지 않고 PF gap(PF 간극) 수리 queue(대기열)로 낮춘다.\n",
    )
    append_text_once(
        STAGE_README,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- action(행동): run364AQ(364AQ 실행) review(검토)를 닫았다.\n- effect(효과): Stage364(364단계) 안에서 다음 materialization(구체화)로 이어간다.\n",
    )


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "lane": "review(검토)",
        "scoreboard_lane": "review(검토)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        "notes": f"package_rows={final['package_candidate_rows']}; pf_dd_lift_rows={final['pf_dd_lift_density_safe_rows']}; next_queue_rows={final['next_queue_rows']}",
        "family": "result_judgment(결과 판정)",
        "primary_report": rel(REPORT_PATH),
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
        "work_family": "result_judgment(결과 판정)",
        "trade_density_requirement_status": "review_negative_for_package_density_clue_preserved(패키지 부정 검토, 밀도 단서 보존)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "evidence_scope": "proxy_review_no_authority(프록시 검토, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can threshold-edge PF/DD lift become a strict PF-density pass?(임계값 경계 PF/DD 개선이 엄격 PF-밀도 통과가 될 수 있는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for subrun_id, record_view, tier_scope, kpi_scope in [
        (f"{RUN_ID}__Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "proxy review metrics(프록시 검토 지표)"),
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
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    surface = load_surface()
    review_rows = surface_review_rows(surface)
    package_rows = package_gate_rows(parent_final, review_rows)
    policy_rows = policy_failure_rows(review_rows)
    clue_rows = positive_clue_rows(parent_final, review_rows)
    failure_rows = failure_memory_rows(parent_final, review_rows)
    next_rows = next_queue_rows(review_rows)
    write_csv(SURFACE_REVIEW, review_rows)
    write_csv(PACKAGE_GATE_AUDIT, package_rows)
    write_csv(POLICY_FAILURE_ATTRIBUTION, policy_rows)
    write_csv(POSITIVE_CLUES, clue_rows)
    write_csv(FAILURE_MEMORY, failure_rows)
    write_csv(NEXT_QUEUE, next_rows)
    write_work_packet()
    created_at = now_utc()
    gates = write_receipts({"created_at_utc": created_at})
    final = final_payload(parent_final, review_rows, next_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, review_rows, clue_rows, gates)
    write_ledgers(final, gates)
    parent.repair_run_registry_line_endings(RUN_ID)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
