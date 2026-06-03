from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import train_threshold_edge_density_restore_cost_session_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AZ"
RUN_ID = "run364AZ_review_threshold_edge_density_restore_cost_session_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
PACKAGE_RUN_ID = parent.PACKAGE_RUN_ID
NEXT_RUN_ID = "run364BA_materialize_density_restore_stress_to_candidate_inputs_without_db_v1"

STATUS = "completed_stage364AZ_density_restore_scout_review_no_package_open_ba_materialization_no_authority"
JUDGMENT = "no_package_eligible_proxy_stress_pass_positive_clue_open_ba_materialization_no_authority"
DECISION = "stage364AZ_open_run364BA_density_restore_stress_to_candidate_materialization"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
TARGET_PF = 1.20
PACKAGE_MIN_PF = 1.25

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SURFACE_REVIEW = RUN_DIR / "ay_surface_review.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
RUN364BA_QUEUE = RUN_DIR / "run364BA_materialization_queue.csv"
REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AZ_density_restore_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AZ_density_restore_review.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

INPUTS = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.SCOUT_SURFACE,
    parent.STRICT_CANDIDATES,
    parent.PACKAGE_ELIGIBLE_CANDIDATES,
    parent.QUEUE_REPLAY_AUDIT,
    parent.DENSITY_SURVIVAL_COMPARISON,
    parent.SELECTED_SESSION_SUMMARY,
    parent.SELECTED_MONTH_SIDE_SUMMARY,
    parent.RUN364AZ_QUEUE,
    parent.REPORT_PATH,
    parent.LINEAGE_RECEIPT,
]

OUTPUTS = [
    INPUT_MANIFEST,
    SURFACE_REVIEW,
    POSITIVE_CLUES,
    FAILURE_MEMORY,
    PACKAGE_DECISION,
    RUN364BA_QUEUE,
    REVIEW_FINDINGS,
    WORK_PACKET,
    KPI_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_csv_rows(path)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


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
    missing = [rel(path) for path in INPUTS if not exists(path)]
    if missing:
        raise FileNotFoundError("missing AZ inputs(AZ 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if any(final.get(key) != "not_claimed" for key in ["runtime_authority", "operating_promotion", "goal_achieve", "live_readiness"]):
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장이 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트가 모두 통과되지 않음)")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in INPUTS:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "input_role": input_role(path),
                "effect": "AY review(AY 검토) 입력 정체성을 고정해 package decision(패키지 결정)과 다음 queue(대기열)를 추적 가능하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "final_decision.json":
        return "parent final decision(부모 최종 결정)"
    if name == "density_restore_cost_session_proxy_scout_surface.csv":
        return "AY proxy surface(AY 프록시 표면)"
    if name == "strict_proxy_candidates.csv":
        return "strict proxy candidates(엄격 프록시 후보)"
    if name == "package_eligible_candidates.csv":
        return "package eligibility evidence(패키지 가능 근거)"
    if name in {"selected_session_summary.csv", "selected_month_side_summary.csv"}:
        return "performance attribution(성과 귀속)"
    if name == "run364AZ_review_queue.csv":
        return "parent review queue(부모 검토 대기열)"
    return "supporting evidence(보조 근거)"


def review_surface_rows(surface: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row in surface:
        pf = as_float(row.get("combined_profit_factor"))
        density = as_float(row.get("estimated_mt5_trade_per_business_day"))
        package_eligible = str(row.get("package_eligible_proxy", "")).lower() == "true"
        queue_type = str(row.get("queue_type", ""))
        if package_eligible:
            review_status = "package_review_candidate(패키지 검토 후보)"
        elif density >= DENSITY_FLOOR and pf >= PACKAGE_MIN_PF and queue_type.startswith("stress"):
            review_status = "positive_clue_stress_not_package(긍정 단서, 압박이라 패키지 아님)"
        elif density >= DENSITY_FLOOR and pf >= TARGET_PF:
            review_status = "diagnostic_positive_not_package(진단 긍정, 패키지 아님)"
        elif density < DENSITY_FLOOR:
            review_status = "fail_density_survival(밀도 생존 실패)"
        else:
            review_status = "watch_no_package(관찰, 패키지 아님)"
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_rank": row.get("queue_rank", ""),
                "queue_id": row.get("queue_id", ""),
                "variant_id": row.get("variant_id", ""),
                "queue_type": queue_type,
                "parent_candidate_status": row.get("candidate_status", ""),
                "review_status": review_status,
                "package_eligible_proxy": package_eligible,
                "combined_net_profit": row.get("combined_net_profit", ""),
                "combined_profit_factor": row.get("combined_profit_factor", ""),
                "combined_trade_count": row.get("combined_trade_count", ""),
                "estimated_mt5_trade_per_business_day": row.get("estimated_mt5_trade_per_business_day", ""),
                "combined_max_drawdown": row.get("combined_max_drawdown", ""),
                "combined_short_count": row.get("combined_short_count", ""),
                "validation_net_profit": row.get("validation_net_profit", ""),
                "oos_net_profit": row.get("oos_net_profit", ""),
                "effect": review_effect(review_status),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_effect(status: str) -> str:
    if status.startswith("package"):
        return "패키지 검토 대상으로 올릴 수 있다."
    if status.startswith("positive_clue"):
        return "운영 후보가 아니라 다음 물질화 씨앗으로 쓴다."
    if status.startswith("fail_density"):
        return "밀도 하한 실패 기억으로 다음 하한 설계 제약에 쓴다."
    return "진단/관찰 근거로만 사용한다."


def positive_clue_rows(review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    positives = []
    for row in review_rows:
        if "positive" not in str(row.get("review_status", "")):
            continue
        positives.append(
            {
                "run_id": RUN_ID,
                "clue_id": f"positive_{row.get('queue_id')}",
                "source_queue_id": row.get("queue_id", ""),
                "variant_id": row.get("variant_id", ""),
                "clue_type": row.get("review_status", ""),
                "net_profit": row.get("combined_net_profit", ""),
                "profit_factor": row.get("combined_profit_factor", ""),
                "estimated_mt5_density": row.get("estimated_mt5_trade_per_business_day", ""),
                "drawdown": row.get("combined_max_drawdown", ""),
                "short_count": row.get("combined_short_count", ""),
                "use_as": "BA materialization seed(BA 물질화 씨앗)",
                "effect": "압박 통과를 package claim(패키지 주장)이 아니라 후보화 입력으로 바꾼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return positives


def failure_memory_rows(review_rows: Sequence[Mapping[str, Any]], skipped_count: int, package_count: int) -> list[dict[str, Any]]:
    failures = []
    for row in review_rows:
        if str(row.get("review_status", "")).startswith("fail_density"):
            failures.append(
                {
                    "run_id": RUN_ID,
                    "failure_id": f"density_survival_{row.get('queue_id')}",
                    "source_queue_id": row.get("queue_id", ""),
                    "failure_type": "estimated_mt5_density_below_floor(추정 MT5 밀도 하한 미달)",
                    "evidence": f"estimated_density={row.get('estimated_mt5_trade_per_business_day')};pf={row.get('combined_profit_factor')}",
                    "constraint_for_next": "BA queue must preserve density buffer above 3/day after AW survival ratio(BA 대기열은 AW 생존비 적용 뒤 3/day 완충을 유지해야 함)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if package_count == 0:
        failures.append(
            {
                "run_id": RUN_ID,
                "failure_id": "no_package_eligible_rows",
                "source_queue_id": "run364AY_surface",
                "failure_type": "package_eligible_zero(패키지 가능 행 0)",
                "evidence": "AY package_eligible_rows=0",
                "constraint_for_next": "do not create MT5 package until stress clue is re-materialized as candidate(압박 단서가 후보로 재물질화되기 전 MT5 패키지 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if skipped_count:
        failures.append(
            {
                "run_id": RUN_ID,
                "failure_id": "implementation_required_rows_visible",
                "source_queue_id": "ax04_ax06",
                "failure_type": "proxy_cannot_execute_new_runtime_guards(프록시가 새 런타임 가드를 실행하지 못함)",
                "evidence": f"skipped_implementation_required_rows={skipped_count}",
                "constraint_for_next": "runtime/proxy policy implementation must be explicit before package(패키지 전 런타임/프록시 정책 구현 명시 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    failures.append(
        {
            "run_id": RUN_ID,
            "failure_id": "weak_month_side_buckets",
            "source_queue_id": "selected_month_side_summary",
            "failure_type": "sep_dec_and_long_tail_stress_visible(9/12월 및 롱 꼬리 압박 가시화)",
            "evidence": "2025-12 long=-83.865; 2025-09 short=-23.864; 2025-07 long=-24.465",
            "constraint_for_next": "soft stress labels only; no hard month deletion without MT5 evidence(부드러운 압박 라벨만, MT5 근거 없는 월 강제 삭제 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return failures


def package_decision_rows(final: Mapping[str, Any], review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    package_count = sum(1 for row in review_rows if bool(row.get("package_eligible_proxy")))
    best = best_positive(review_rows)
    decision = (
        "no_package_open_ba_materialization(패키지 없음, BA 물질화 개방)"
        if package_count == 0
        else "package_review_candidate_exists(패키지 검토 후보 있음)"
    )
    return [
        {
            "run_id": RUN_ID,
            "decision": decision,
            "parent_package_eligible_rows": final.get("package_eligible_rows", ""),
            "review_package_eligible_rows": package_count,
            "selected_positive_clue_queue_id": best.get("queue_id", ""),
            "selected_positive_clue_pf": best.get("combined_profit_factor", ""),
            "selected_positive_clue_estimated_density": best.get("estimated_mt5_trade_per_business_day", ""),
            "package_action": "do_not_package(패키지하지 않음)" if package_count == 0 else "review_package_possible(패키지 가능성 검토)",
            "effect": "패키지 가능 행이 없으면 MT5 실행으로 가지 않고 다음 후보화 물질화로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def best_positive(review_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    positives = [row for row in review_rows if "positive" in str(row.get("review_status", ""))]
    if not positives:
        return {}
    return sorted(
        positives,
        key=lambda row: (
            as_float(row.get("combined_profit_factor")),
            as_float(row.get("estimated_mt5_trade_per_business_day")),
            as_float(row.get("combined_net_profit")),
        ),
        reverse=True,
    )[0]


def ba_queue_rows(review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_queue = {str(row.get("queue_id")): row for row in review_rows}
    ax03 = by_queue.get("ax03_short_restore_ps450_floor050_stress", {})
    ax08 = by_queue.get("ax08_density_overstress_floor000", {})
    ax01 = by_queue.get("ax01_density_buffer_floor075_controlled_expand", {})
    rows = [
        ba_row(
            1,
            "ba01_ax03_stress_to_candidate_floor050_ps450",
            "stress_to_candidate(압박 후보를 후보로 전환)",
            ax03,
            0.450,
            0.00050,
            "no",
            "convert strongest PF/density stress pass into candidate review seed(가장 강한 PF/밀도 압박 통과를 후보 검토 씨앗으로 전환)",
        ),
        ba_row(
            2,
            "ba02_between_ax03_ax08_floor025_ps450",
            "density_buffer_midpoint(밀도 완충 중간점)",
            ax08,
            0.450,
            0.00025,
            "no",
            "search between ax03 density safety and ax08 over-stress buffer(ax03 밀도 안전과 ax08 과압박 완충 사이 탐색)",
        ),
        ba_row(
            3,
            "ba03_short_balance_ps448_floor050",
            "short_balance_offense(숏 균형 공격)",
            ax03,
            0.448,
            0.00050,
            "no",
            "test slightly lower short threshold while keeping floor050(하한 0.00050을 유지하며 숏 임계값을 더 낮춤)",
        ),
        ba_row(
            4,
            "ba04_candidate_floor075_density_rescue_ps450",
            "candidate_density_rescue(후보 밀도 구조)",
            ax01,
            0.450,
            0.00075,
            "no",
            "borrow ax01 PF discipline but add short threshold density rescue(ax01 PF 규율에 숏 임계값 밀도 복원을 더함)",
        ),
        ba_row(
            5,
            "ba05_hour18_19_margin_guard_implementation_seed",
            "runtime_policy_implementation_seed(런타임 정책 구현 씨앗)",
            ax08,
            0.450,
            0.00025,
            "yes_runtime_policy_hour18_19_margin_guard(18/19시 마진 가드 런타임 정책 필요)",
            "make skipped ax04 explicit implementation work before package(ax04 건너뜀을 패키지 전 구현 작업으로 명시)",
        ),
        ba_row(
            6,
            "ba06_tail_dd_guard_diagnostic_seed",
            "equity_tail_diagnostic_seed(수익곡선 꼬리 진단 씨앗)",
            ax08,
            0.450,
            0.00025,
            "yes_account_state_guard_not_proxy_only(계정 상태 가드는 프록시만으로 불가)",
            "carry ax06 tail risk as diagnostic not hidden runtime filter(ax06 꼬리 위험을 숨은 런타임 필터가 아니라 진단으로 유지)",
        ),
    ]
    return rows


def ba_row(
    rank: int,
    queue_id: str,
    axis_id: str,
    source: Mapping[str, Any],
    short_threshold: float,
    entry_floor: float,
    implementation_required: str,
    expected_effect: str,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "queue_rank": rank,
        "queue_id": queue_id,
        "axis_id": axis_id,
        "source_ay_queue_id": source.get("queue_id", ""),
        "source_variant_id": source.get("variant_id", ""),
        "source_review_status": source.get("review_status", ""),
        "short_probability_threshold": short_threshold,
        "long_threshold": 0.0,
        "min_margin": -0.000562137088,
        "entry_margin_floor": entry_floor,
        "max_hold_m5": 6,
        "source_proxy_pf": source.get("combined_profit_factor", ""),
        "source_proxy_net": source.get("combined_net_profit", ""),
        "source_estimated_mt5_density": source.get("estimated_mt5_trade_per_business_day", ""),
        "source_drawdown": source.get("combined_max_drawdown", ""),
        "implementation_required": implementation_required,
        "trade_splitting_status": "not_used(거래 쪼개기 없음)",
        "top_n_status": "forbidden(금지)",
        "oos_threshold_selection_status": "forbidden(금지)",
        "timestamp_boundary": "entry_time_known_only_closed_bar(진입 시점에 알려진 닫힌 봉만 사용)",
        "success_criteria": "estimated_mt5_density>=3.0 and PF>=1.25 without trade splitting(추정 MT5 밀도 3.0 이상, PF 1.25 이상, 거래 쪼개기 없음)",
        "failure_criteria": "package_eligible remains zero or DD/cost stress worsens(패키지 가능 행 0 유지 또는 DD/비용 압박 악화)",
        "expected_effect": expected_effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def finding_rows(review_rows: Sequence[Mapping[str, Any]], positives: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best = best_positive(review_rows)
    return [
        {
            "run_id": RUN_ID,
            "finding_id": "package_denied",
            "finding": "package_eligible_rows=0, no MT5 package(패키지 가능 행 0, MT5 패키지 없음)",
            "evidence": rel(parent.PACKAGE_ELIGIBLE_CANDIDATES),
            "effect": "운영 주장과 런타임 탐침 패키지를 열지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "best_positive_clue",
            "finding": f"best positive clue(최고 긍정 단서)={best.get('queue_id', '')}",
            "evidence": f"pf={best.get('combined_profit_factor', '')};density={best.get('estimated_mt5_trade_per_business_day', '')};dd={best.get('combined_max_drawdown', '')}",
            "effect": "BA 물질화의 첫 후보 씨앗으로 쓴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "failure_memory_count",
            "finding": f"failure_memory_rows={len(failures)};positive_clue_rows={len(positives)}",
            "evidence": f"{rel(FAILURE_MEMORY)};{rel(POSITIVE_CLUES)}",
            "effect": "실패 기억은 제약으로, 긍정 단서는 공격 씨앗으로 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
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
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "required_gates": [
                "kpi_contract_audit",
                "row_grain_audit",
                "source_authority_audit",
                "package_decision_gate",
                "next_queue_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final_seed: Mapping[str, Any]) -> None:
    write_json(
        KPI_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "reviewed_surface": rel(SURFACE_REVIEW),
            "package_decision": rel(PACKAGE_DECISION),
            "selected_positive_clue_queue_id": final_seed.get("selected_positive_clue_queue_id", ""),
            "effect": "AY KPI(핵심 성과 지표)를 패키지 가능/긍정 단서/실패 기억으로 분리했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "positive_clues": rel(POSITIVE_CLUES),
            "failure_memory": rel(FAILURE_MEMORY),
            "month_session_inputs": [rel(parent.SELECTED_SESSION_SUMMARY), rel(parent.SELECTED_MONTH_SIDE_SUMMARY)],
            "effect": "세션/월 손실을 hard delete(강제 삭제)가 아닌 다음 제약으로 남겼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "judgment": JUDGMENT,
            "package": "not_opened(열지 않음)",
            "next_condition": NEXT_RUN_ID,
            "effect": "stress pass(압박 통과)를 운영 주장으로 승격하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_rows() -> list[dict[str, Any]]:
    return [
        gate_row("kpi_contract_audit(KPI 계약 감사)", SURFACE_REVIEW, "AY surface(AY 표면)의 net/PF/density/DD(순수익/수익 팩터/밀도/낙폭)를 검토한다."),
        gate_row("row_grain_audit(행 단위 감사)", SURFACE_REVIEW, "AY scout row(스카우트 행) 단위로 판정을 남긴다."),
        gate_row("source_authority_audit(원천 권위 감사)", parent.FINAL_DECISION, "AY final decision(최종 결정)을 부모 원천으로 고정한다."),
        gate_row("package_decision_gate(패키지 결정 게이트)", PACKAGE_DECISION, "package_eligible_rows=0이면 MT5 package(MT5 패키지)를 열지 않는다."),
        gate_row("positive_clue_gate(긍정 단서 게이트)", POSITIVE_CLUES, "압박 통과 단서를 BA materialization(BA 물질화) 씨앗으로 분리한다."),
        gate_row("failure_memory_gate(실패 기억 게이트)", FAILURE_MEMORY, "밀도 하한 실패와 구현 필요 행을 다음 제약으로 남긴다."),
        gate_row("next_queue_gate(다음 대기열 게이트)", RUN364BA_QUEUE, "BA materialization queue(BA 물질화 대기열)를 만든다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "work packet(작업 묶음)의 필수 게이트를 closeout(종료 기록)에 연결한다."),
        gate_row("final_claim_guard(최종 주장 가드)", CLAIM_RECEIPT, "runtime authority(런타임 권위), operating promotion(운영 승격), goal achieve(목표 달성)를 주장하지 않는다."),
    ]


def final_payload(
    parent_final: Mapping[str, Any],
    review_rows: Sequence[Mapping[str, Any]],
    positives: Sequence[Mapping[str, Any]],
    failures: Sequence[Mapping[str, Any]],
    ba_queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
    best = best_positive(review_rows)
    package_count = sum(1 for row in review_rows if bool(row.get("package_eligible_proxy")))
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "reviewed_scout_rows": len(review_rows),
        "parent_strict_proxy_pass_rows": parent_final.get("strict_proxy_pass_rows", ""),
        "parent_package_eligible_rows": parent_final.get("package_eligible_rows", ""),
        "review_package_eligible_rows": package_count,
        "positive_clue_rows": len(positives),
        "failure_memory_rows": len(failures),
        "ba_queue_rows": len(ba_queue),
        "package_decision": "not_opened_no_package_eligible_rows",
        "selected_positive_clue_queue_id": best.get("queue_id", ""),
        "selected_positive_clue_variant_id": best.get("variant_id", ""),
        "selected_positive_clue_pf": best.get("combined_profit_factor", ""),
        "selected_positive_clue_net": best.get("combined_net_profit", ""),
        "selected_positive_clue_estimated_mt5_density": best.get("estimated_mt5_trade_per_business_day", ""),
        "selected_positive_clue_drawdown": best.get("combined_max_drawdown", ""),
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
    positives: Sequence[Mapping[str, Any]],
    failures: Sequence[Mapping[str, Any]],
    ba_queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    refresh_stage_brief_header()
    report = f"""# run364AZ density restore scout review(364AZ 밀도 복원 스카우트 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- package_decision(패키지 결정): `{final['package_decision']}`
- review_package_eligible_rows(검토 패키지 가능 행): `{final['review_package_eligible_rows']}`
- selected_positive_clue(선택 긍정 단서): `{final['selected_positive_clue_queue_id']}` PF `{final['selected_positive_clue_pf']}`, estimated MT5 density(추정 MT5 밀도) `{final['selected_positive_clue_estimated_mt5_density']}`
- BA queue rows(BA 대기열 행): `{final['ba_queue_rows']}`
- runtime_authority(런타임 권위): `not_claimed`

## Surface Review(표면 검토)

{markdown_table(review_rows, ['queue_rank', 'queue_id', 'review_status', 'combined_profit_factor', 'estimated_mt5_trade_per_business_day', 'combined_net_profit', 'combined_max_drawdown', 'combined_short_count'])}

## Positive Clues(긍정 단서)

{markdown_table(positives, ['clue_id', 'source_queue_id', 'profit_factor', 'estimated_mt5_density', 'drawdown', 'use_as'])}

## Failure Memory(실패 기억)

{markdown_table(failures, ['failure_id', 'failure_type', 'evidence', 'constraint_for_next'])}

## Next Queue(다음 대기열)

{markdown_table(ba_queue, ['queue_rank', 'queue_id', 'axis_id', 'short_probability_threshold', 'entry_margin_floor', 'implementation_required', 'expected_effect'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): AZ는 AY stress pass(AY 압박 통과)를 MT5 package(MT5 패키지)가 아니라 BA materialization(BA 물질화) 입력으로 바꿔 Stage364(364단계)를 계속 밀고 간다.
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, report)
    append_text_once(
        REVIEW_INDEX,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- package_decision(패키지 결정): `{final['package_decision']}`\n- next_run(다음 실행): `{NEXT_RUN_ID}`\n- effect(효과): stress pass(압박 통과)를 BA materialization(BA 물질화) 대기열로 넘겼다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364AZ Density Restore Scout Review Closeout",
        f"\n## run364AZ Density Restore Scout Review Closeout(364AZ 밀도 복원 스카우트 검토 종료)\n\nAction(행동): AY proxy surface(AY 프록시 표면)를 검토했다.\n\nEffect(효과): package_eligible_rows(패키지 가능 행) 0을 운영 주장 없이 닫고 `{NEXT_RUN_ID}` 물질화로 이어간다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_no_package_eligible_rows(없음, 패키지 가능 행 0)
- latest_review(최근 검토): `{RUN_ID}`
- selected_positive_clue(선택 긍정 단서): `{final['selected_positive_clue_queue_id']}`
- next_materialization_queue(다음 물질화 대기열): `{rel(RUN364BA_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        CURRENT_STATE,
        f"""# Current Working State(현재 작업 상태)

current_stage(현재 단계): `{STAGE_ID}`

latest_completed_run(최근 완료 실행): `{RUN_ID}`

current_run(현재 실행): `{NEXT_RUN_ID}`

current_truth(현재 진실): run364AZ(364AZ 실행)는 AY density restore proxy scout(AY 밀도 복원 프록시 스카우트)를 검토했다. package_eligible_rows(패키지 가능 행)는 `0`이라 MT5 package(MT5 패키지)를 열지 않았다. best positive clue(최고 긍정 단서)는 `{final['selected_positive_clue_queue_id']}`이고 PF(수익 팩터)는 `{final['selected_positive_clue_pf']}`, estimated MT5 density(추정 MT5 밀도)는 `{final['selected_positive_clue_estimated_mt5_density']}`/day(일)이다.

operating_truth_boundary(운영 진실 경계): no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no goal achieve(목표 달성 없음).

next_action(다음 행동): `{NEXT_RUN_ID}`에서 stress pass(압박 통과)를 candidate(후보)로 재물질화하고, hour18/19 margin guard(18/19시 마진 가드)와 tail DD guard(꼬리 낙폭 가드)의 구현 필요성을 명시한다.
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
        "run364AZ Density Restore Scout Review",
        f"\n## run364AZ Density Restore Scout Review(364AZ 밀도 복원 스카우트 검토)\n\nAction(행동): AY surface(AY 표면)를 package decision(패키지 결정)과 BA queue(BA 대기열)로 검토했다.\n\nEffect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `{NEXT_RUN_ID}`로 이어간다.\n",
    )
    append_text_once(
        CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): density restore scout review(밀도 복원 스카우트 검토)를 실행했다.\n- effect(효과): package(패키지)는 열지 않고 `{NEXT_RUN_ID}` materialization queue(물질화 대기열)를 만들었다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): stress pass(압박 통과) `{final['selected_positive_clue_queue_id']}`를 candidate(후보)로 재물질화한다.\n- effect(효과): package ineligible(패키지 부적격)을 idea-dead(아이디어 사망)로 닫지 않고 공격 탐색 씨앗으로 쓴다.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- status(상태): no_package_eligible_rows(패키지 가능 행 0).\n- action(행동): MT5 package(MT5 패키지)를 열지 않았다.\n- effect(효과): 운영 주장을 막고 BA materialization(BA 물질화)로 수익 원천 탐색을 계속한다.\n",
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
        "family": "stage364_proxy_review(364단계 프록시 검토)",
        "lane": "offensive_exploration(공격 탐색)",
        "work_family": "kpi_evidence(KPI 근거)",
        "primary_artifact": rel(SURFACE_REVIEW),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "not_started_review_only(검토 전용이라 시작 안 함)",
        "next_action": NEXT_RUN_ID,
        "question": "Can AY stress pass be promoted to package or materialized as candidate?(AY 압박 통과를 패키지로 올릴 수 있는가, 아니면 후보로 재물질화해야 하는가?)",
        "notes": f"package=0;positive={final['positive_clue_rows']};failures={final['failure_memory_rows']};next_queue={final['ba_queue_rows']}",
        "net_profit": final["selected_positive_clue_net"],
        "profit_factor": final["selected_positive_clue_pf"],
        "drawdown": final["selected_positive_clue_drawdown"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common])
    alpha_rows = []
    for suffix, view, tier, scope in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "proxy review(프록시 검토)"),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim_no_tier_b_fallback(주장 범위 밖, Tier B 대체 없음)"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A review plus Tier B out_of_scope(Tier A 검토 + Tier B 범위 밖)"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": suffix,
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": scope,
                "scoreboard_lane": "proxy_review(프록시 검토)",
                "primary_kpi": f"package=0;best={final['selected_positive_clue_queue_id']};pf={final['selected_positive_clue_pf']};density={final['selected_positive_clue_estimated_mt5_density']}",
                "guardrail_kpi": "no_runtime_no_package;no_topn_no_split",
                "evidence_boundary": CLAIM_BOUNDARY,
            }
        )
        alpha_rows.append(row)
    append_or_replace_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], alpha_rows)

    artifact_rows = []
    for artifact_type, path, notes in [
        ("surface_review", SURFACE_REVIEW, "AY surface review(AY 표면 검토)."),
        ("package_decision", PACKAGE_DECISION, "Package decision(패키지 결정)."),
        ("positive_clues", POSITIVE_CLUES, "Positive clues(긍정 단서)."),
        ("failure_memory", FAILURE_MEMORY, "Failure memory(실패 기억)."),
        ("next_queue", RUN364BA_QUEUE, "BA materialization queue(BA 물질화 대기열)."),
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
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUTS],
            "artifacts": [{"path": rel(path), "sha256": sha(path), "role": "run364AZ output(364AZ 출력)"} for path in OUTPUTS if exists(path)],
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
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUTS],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUTS if exists(path)],
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    surface = read_csv_rows(parent.SCOUT_SURFACE)
    replay_audit = read_csv_rows(parent.QUEUE_REPLAY_AUDIT)
    skipped_count = sum(1 for row in replay_audit if str(row.get("replay_status", "")).startswith("skipped"))
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    review_rows = review_surface_rows(surface)
    positives = positive_clue_rows(review_rows)
    package_rows = package_decision_rows(parent_final, review_rows)
    failures = failure_memory_rows(review_rows, skipped_count, as_int(parent_final.get("package_eligible_rows")))
    ba_queue = ba_queue_rows(review_rows)
    findings = finding_rows(review_rows, positives, failures)

    write_csv(SURFACE_REVIEW, review_rows)
    write_csv(POSITIVE_CLUES, positives)
    write_csv(FAILURE_MEMORY, failures)
    write_csv(PACKAGE_DECISION, package_rows)
    write_csv(RUN364BA_QUEUE, ba_queue)
    write_csv(REVIEW_FINDINGS, findings)
    write_work_packet()

    created_at = now_utc()
    final_seed = {
        "selected_positive_clue_queue_id": best_positive(review_rows).get("queue_id", ""),
    }
    write_receipts(final_seed)
    gates = gate_rows()
    write_csv(GATE_AUDIT, gates)
    final = final_payload(parent_final, review_rows, positives, failures, ba_queue, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, review_rows, positives, failures, ba_queue, gates)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_ledgers(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
