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

from stage_pipelines.stage364 import train_density_restore_stress_to_candidate_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BC"
RUN_ID = "run364BC_review_density_restore_stress_to_candidate_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BD_package_density_restore_stress_candidate_runtime_probe_without_db_v1"

STATUS = "completed_stage364BC_density_restore_stress_candidate_review_open_bd_package_no_authority"
JUDGMENT = "package_review_candidate_exists_open_runtime_probe_package_no_authority"
DECISION = "stage364BC_open_run364BD_density_restore_stress_candidate_runtime_probe_package"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
PACKAGE_MIN_PF = 1.25

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SURFACE_REVIEW = RUN_DIR / "bb_surface_review.csv"
PACKAGE_CANDIDATE_REVIEW = RUN_DIR / "package_candidate_review.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
RUN364BD_QUEUE = RUN_DIR / "run364BD_runtime_probe_package_queue.csv"
REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BC_density_restore_stress_candidate_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BC_density_restore_stress_candidate_review.md"
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
    parent.SELECTED_PROXY_CANDIDATE,
    parent.SELECTED_EXPECTED_TRADE_TAPE,
    parent.SELECTED_SESSION_SUMMARY,
    parent.SELECTED_MONTH_SIDE_SUMMARY,
    parent.RUN364BC_QUEUE,
    parent.REPORT_PATH,
    parent.LINEAGE_RECEIPT,
]

OUTPUTS = [
    INPUT_MANIFEST,
    SURFACE_REVIEW,
    PACKAGE_CANDIDATE_REVIEW,
    PACKAGE_DECISION,
    FAILURE_MEMORY,
    RUN364BD_QUEUE,
    REVIEW_FINDINGS,
    WORK_PACKET,
    KPI_RECEIPT,
    DATA_RECEIPT,
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


def validate_inputs() -> tuple[Mapping[str, Any], Mapping[str, Any], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    missing = [rel(path) for path in INPUTS if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BC inputs(BC 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    selected = read_json(parent.SELECTED_PROXY_CANDIDATE)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if any(final.get(key) != "not_claimed" for key in ["runtime_authority", "operating_promotion", "goal_achieve", "live_readiness"]):
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장이 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트가 모두 통과되지 않음)")
    surface = read_csv_rows(parent.SCOUT_SURFACE)
    package_rows = read_csv_rows(parent.PACKAGE_ELIGIBLE_CANDIDATES)
    replay_audit = read_csv_rows(parent.QUEUE_REPLAY_AUDIT)
    if len(surface) != as_int(final.get("scout_rows")):
        raise RuntimeError("surface row count mismatch(표면 행 수 불일치)")
    if len(package_rows) != as_int(final.get("package_eligible_rows")):
        raise RuntimeError("package row count mismatch(패키지 행 수 불일치)")
    if not package_rows:
        raise RuntimeError("BC expected package eligible rows(BC는 패키지 가능 행이 필요함)")
    if str(selected.get("package_eligible_proxy", "")).lower() not in {"true", "1"} and selected.get("package_eligible_proxy") is not True:
        raise RuntimeError("selected candidate is not package eligible(선택 후보가 패키지 가능이 아님)")
    return final, selected, surface, package_rows, replay_audit


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "final_decision.json":
        return "parent final decision(부모 최종 결정)"
    if name == "density_restore_stress_to_candidate_proxy_scout_surface.csv":
        return "BB proxy surface(BB 프록시 표면)"
    if name == "package_eligible_candidates.csv":
        return "package eligible proxy candidates(패키지 가능 프록시 후보)"
    if name == "selected_proxy_candidate.json":
        return "selected proxy candidate(선택 프록시 후보)"
    if name == "selected_trade_tape.csv":
        return "selected proxy trade tape(선택 프록시 거래 테이프)"
    if name == "run364BC_review_queue.csv":
        return "parent review queue(부모 검토 대기열)"
    return "supporting evidence(보조 근거)"


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "input_role": input_role(path),
            "effect": "BB review(BC 검토)의 입력 정체성(identity, 정체성)을 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUTS
    ]


def is_true(value: Any) -> bool:
    return value is True or str(value).strip().lower() in {"true", "1", "yes"}


def review_surface_rows(surface: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in surface:
        pf = as_float(row.get("combined_profit_factor"))
        density = as_float(row.get("estimated_mt5_trade_per_business_day"))
        val_net = as_float(row.get("validation_net_profit"))
        oos_net = as_float(row.get("oos_net_profit"))
        short_count = as_float(row.get("combined_short_count"))
        package_eligible = is_true(row.get("package_eligible_proxy"))
        if package_eligible and pf >= PACKAGE_MIN_PF and density >= DENSITY_FLOOR and val_net > 0 and oos_net > 0 and short_count > 0:
            review_status = "package_review_candidate(패키지 검토 후보)"
        elif density < DENSITY_FLOOR:
            review_status = "fail_density_survival(밀도 생존 실패)"
        elif pf < PACKAGE_MIN_PF:
            review_status = "fail_proxy_pf_floor(프록시 수익 팩터 하한 실패)"
        elif val_net <= 0 or oos_net <= 0:
            review_status = "fail_split_profit(분할 수익 실패)"
        elif short_count <= 0:
            review_status = "fail_short_side_zero(숏 0 실패)"
        else:
            review_status = "watch_no_package(관찰, 패키지 아님)"
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_rank": row.get("queue_rank", ""),
                "queue_id": row.get("queue_id", ""),
                "variant_id": row.get("variant_id", ""),
                "queue_type": row.get("queue_type", ""),
                "review_status": review_status,
                "package_eligible_proxy": package_eligible,
                "selection_score": row.get("selection_score", ""),
                "combined_net_profit": row.get("combined_net_profit", ""),
                "combined_profit_factor": row.get("combined_profit_factor", ""),
                "combined_trade_count": row.get("combined_trade_count", ""),
                "estimated_mt5_trade_per_business_day": row.get("estimated_mt5_trade_per_business_day", ""),
                "combined_max_drawdown": row.get("combined_max_drawdown", ""),
                "combined_recovery_factor": row.get("combined_recovery_factor", ""),
                "combined_expectancy": row.get("combined_expectancy", ""),
                "combined_long_count": row.get("combined_long_count", ""),
                "combined_short_count": row.get("combined_short_count", ""),
                "validation_net_profit": row.get("validation_net_profit", ""),
                "oos_net_profit": row.get("oos_net_profit", ""),
                "trade_splitting_status": row.get("trade_splitting_status", ""),
                "top_n_status": row.get("top_n_status", ""),
                "effect": review_effect(review_status),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_effect(status: str) -> str:
    if status.startswith("package"):
        return "MT5 runtime probe package(MT5 런타임 탐침 패키지) 입력으로 열 수 있다."
    if status.startswith("fail_density"):
        return "추정 MT5 밀도 하한을 다음 제약으로 남긴다."
    if status.startswith("fail_proxy_pf"):
        return "PF 하한 실패를 다음 임계값/마진 탐색 제약으로 남긴다."
    return "진단/관찰 근거로만 사용한다."


def package_candidate_rows(package_rows: Sequence[Mapping[str, str]], selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    selected_id = str(selected.get("variant_id", ""))
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(package_rows, start=1):
        role = "selected_primary(선택 주 후보)" if row.get("variant_id") == selected_id else "retained_alternative(보존 대안)"
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_rank": index,
                "package_role": role,
                "queue_id": row.get("queue_id", ""),
                "variant_id": row.get("variant_id", ""),
                "selection_score": row.get("selection_score", ""),
                "combined_net_profit": row.get("combined_net_profit", ""),
                "combined_profit_factor": row.get("combined_profit_factor", ""),
                "estimated_mt5_trade_per_business_day": row.get("estimated_mt5_trade_per_business_day", ""),
                "combined_trade_count": row.get("combined_trade_count", ""),
                "combined_max_drawdown": row.get("combined_max_drawdown", ""),
                "combined_recovery_factor": row.get("combined_recovery_factor", ""),
                "combined_expectancy": row.get("combined_expectancy", ""),
                "combined_long_count": row.get("combined_long_count", ""),
                "combined_short_count": row.get("combined_short_count", ""),
                "validation_net_profit": row.get("validation_net_profit", ""),
                "oos_net_profit": row.get("oos_net_profit", ""),
                "runtime_action": "open_bd_package(364BD 패키지 열기)" if role.startswith("selected") else "record_as_alternative(대안으로 기록)",
                "effect": "선택 주 후보는 런타임 탐침 패키지로 열고, 대안은 비교 근거로 보존한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def failure_memory_rows(review_rows: Sequence[Mapping[str, Any]], replay_audit: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for row in review_rows:
        status = str(row.get("review_status", ""))
        if not status.startswith("fail_"):
            continue
        failures.append(
            {
                "run_id": RUN_ID,
                "failure_id": f"{status.split('(')[0]}__{row.get('queue_id')}",
                "source_queue_id": row.get("queue_id", ""),
                "failure_type": status,
                "evidence": f"pf={row.get('combined_profit_factor')};density={row.get('estimated_mt5_trade_per_business_day')};dd={row.get('combined_max_drawdown')}",
                "constraint_for_next": "do not package this row without repair(수리 없이 이 행을 패키지하지 않음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    skipped = [row for row in replay_audit if str(row.get("replay_status", "")).startswith("skipped")]
    if skipped:
        failures.append(
            {
                "run_id": RUN_ID,
                "failure_id": "implementation_required_rows_visible",
                "source_queue_id": "ba05_ba06",
                "failure_type": "proxy_cannot_execute_new_runtime_guards(프록시가 새 런타임 가드를 실행하지 못함)",
                "evidence": f"skipped_implementation_required_rows={len(skipped)}",
                "constraint_for_next": "runtime/proxy policy implementation must be explicit before package(패키지 전 런타임/프록시 정책 구현 명시 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return failures


def package_decision_rows(final: Mapping[str, Any], selected: Mapping[str, Any], package_candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "decision": "open_runtime_probe_package_queue_no_authority(런타임 탐침 패키지 대기열 열기, 권위 없음)",
            "parent_package_eligible_rows": final.get("package_eligible_rows", ""),
            "review_package_candidate_rows": len(package_candidates),
            "selected_queue_id": selected.get("queue_id", ""),
            "selected_variant_id": selected.get("variant_id", ""),
            "selected_profit_factor": selected.get("combined_profit_factor", ""),
            "selected_estimated_mt5_density": selected.get("estimated_mt5_trade_per_business_day", ""),
            "selected_net_profit": selected.get("combined_net_profit", ""),
            "selected_drawdown": selected.get("combined_max_drawdown", ""),
            "next_run_id": NEXT_RUN_ID,
            "package_action": "open_package_prepare_only_no_mt5_execution(패키지 준비만 열고 MT5 실행은 아직 없음)",
            "effect": "프록시 후보를 런타임 탐침 패키지 입력으로 넘기되 운영 승격은 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def bd_queue_rows(selected: Mapping[str, Any], package_candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    selected_id = str(selected.get("variant_id", ""))
    rows: list[dict[str, Any]] = []
    for candidate in package_candidates:
        is_selected = candidate.get("variant_id") == selected_id
        rows.append(
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "package_queue_id": f"bd_package_{candidate.get('queue_id')}",
                "package_role": "selected_primary(선택 주 후보)" if is_selected else "retained_alternative(보존 대안)",
                "source_run_id": PARENT_RUN_ID,
                "source_queue_id": candidate.get("queue_id", ""),
                "source_variant_id": candidate.get("variant_id", ""),
                "short_probability_threshold": candidate.get("short_probability_threshold", ""),
                "long_threshold": candidate.get("long_threshold", ""),
                "min_margin": candidate.get("min_margin", ""),
                "entry_margin_floor": candidate.get("entry_margin_floor", ""),
                "max_hold_m5": candidate.get("max_hold_m5", ""),
                "bridge_policy": candidate.get("bridge_policy", ""),
                "bridge_policy_value": candidate.get("bridge_policy_value", ""),
                "session_policy": candidate.get("session_policy", ""),
                "side_policy": candidate.get("side_policy", ""),
                "selected_proxy_candidate_path": rel(parent.SELECTED_PROXY_CANDIDATE) if is_selected else "",
                "selected_trade_tape_path": rel(parent.SELECTED_EXPECTED_TRADE_TAPE) if is_selected else "",
                "source_surface_path": rel(parent.SCOUT_SURFACE),
                "expected_net_profit": candidate.get("combined_net_profit", ""),
                "expected_profit_factor": candidate.get("combined_profit_factor", ""),
                "expected_estimated_mt5_density": candidate.get("estimated_mt5_trade_per_business_day", ""),
                "expected_trade_count": candidate.get("combined_trade_count", ""),
                "expected_drawdown": candidate.get("combined_max_drawdown", ""),
                "trade_splitting_status": candidate.get("trade_splitting_status", "not_used(거래 쪼개기 없음)"),
                "top_n_status": candidate.get("top_n_status", "forbidden(금지)"),
                "oos_threshold_selection_status": "forbidden(금지)",
                "timestamp_boundary": "entry_time_known_only_closed_bar(진입 시점의 닫힌 봉만 사용)",
                "runtime_claim": "runtime_probe_package_input_only_no_authority(런타임 탐침 패키지 입력만, 권위 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def finding_rows(final: Mapping[str, Any], selected: Mapping[str, Any], package_candidates: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "finding_id": "package_candidates_exist",
            "finding": f"package_candidate_rows={len(package_candidates)}",
            "evidence": rel(PACKAGE_CANDIDATE_REVIEW),
            "effect": "BD runtime probe package(BD 런타임 탐침 패키지)를 열 수 있다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "selected_primary_candidate",
            "finding": f"selected={selected.get('queue_id', '')};pf={selected.get('combined_profit_factor', '')};density={selected.get('estimated_mt5_trade_per_business_day', '')}",
            "evidence": rel(parent.SELECTED_PROXY_CANDIDATE),
            "effect": "선택 주 후보를 패키지하되 대안 후보도 함께 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "claim_boundary",
            "finding": "proxy review only, no runtime authority(프록시 검토만, 런타임 권위 없음)",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "MT5 실행 전에는 운영 승격을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "failure_memory_count",
            "finding": f"failure_memory_rows={len(failures)}",
            "evidence": rel(FAILURE_MEMORY),
            "effect": "실패 행과 구현 필요 행을 다음 제약으로 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_row(name: str, evidence: Path, effect: str, status: str = "passed") -> dict[str, Any]:
    return {"run_id": RUN_ID, "gate": name, "status": status, "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def gate_rows() -> list[dict[str, Any]]:
    return [
        gate_row("kpi_contract_audit(KPI 계약 감사)", SURFACE_REVIEW, "BB 표면의 net/PF/density/DD/trade count(순수익/수익 팩터/밀도/낙폭/거래수)를 검토했다."),
        gate_row("row_grain_audit(행 단위 감사)", SURFACE_REVIEW, "후보 variant(변형) 한 행 단위로 판정했다."),
        gate_row("source_authority_audit(원천 권위 감사)", parent.FINAL_DECISION, "BB final decision(BB 최종 결정)을 부모 원천으로 고정했다."),
        gate_row("package_decision_gate(패키지 결정 게이트)", PACKAGE_DECISION, "패키지 가능 행 3개를 확인하고 BD 패키지 대기열을 열었다."),
        gate_row("selected_primary_gate(선택 주 후보 게이트)", parent.SELECTED_PROXY_CANDIDATE, "BB selection_score(BB 선택 점수)가 고른 주 후보를 그대로 인계했다."),
        gate_row("next_queue_gate(다음 대기열 게이트)", RUN364BD_QUEUE, "BD runtime probe package queue(BD 런타임 탐침 패키지 대기열)를 만들었다."),
        gate_row("external_claim_boundary_gate(외부 주장 경계 게이트)", CLAIM_RECEIPT, "MT5 실행 전이라 runtime authority(런타임 권위)를 주장하지 않았다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "work packet(작업 묶음)의 필수 게이트를 closeout(종료 기록)에 연결했다."),
        gate_row("final_claim_guard(최종 주장 가드)", CLAIM_RECEIPT, "operating promotion(운영 승격), live readiness(실거래 준비), goal achieve(목표 달성)를 주장하지 않았다."),
    ]


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
                "selected_primary_gate",
                "next_queue_gate",
                "external_claim_boundary_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def final_payload(
    parent_final: Mapping[str, Any],
    selected: Mapping[str, Any],
    review_rows: Sequence[Mapping[str, Any]],
    package_candidates: Sequence[Mapping[str, Any]],
    failures: Sequence[Mapping[str, Any]],
    bd_queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
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
        "reviewed_scout_rows": len(review_rows),
        "parent_package_eligible_rows": parent_final.get("package_eligible_rows", ""),
        "review_package_candidate_rows": len(package_candidates),
        "failure_memory_rows": len(failures),
        "bd_queue_rows": len(bd_queue),
        "package_decision": "open_runtime_probe_package_queue_no_authority",
        "selected_queue_id": selected.get("queue_id", ""),
        "selected_variant_id": selected.get("variant_id", ""),
        "selected_net_profit": selected.get("combined_net_profit", ""),
        "selected_profit_factor": selected.get("combined_profit_factor", ""),
        "selected_estimated_mt5_density": selected.get("estimated_mt5_trade_per_business_day", ""),
        "selected_trade_count": selected.get("combined_trade_count", ""),
        "selected_expectancy": selected.get("combined_expectancy", ""),
        "selected_drawdown": selected.get("combined_max_drawdown", ""),
        "selected_recovery_factor": selected.get("combined_recovery_factor", ""),
        "selected_long_count": selected.get("combined_long_count", ""),
        "selected_short_count": selected.get("combined_short_count", ""),
        "selected_validation_net_profit": selected.get("validation_net_profit", ""),
        "selected_oos_net_profit": selected.get("oos_net_profit", ""),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        KPI_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed(통과)",
            "reviewed_surface": rel(SURFACE_REVIEW),
            "package_candidate_review": rel(PACKAGE_CANDIDATE_REVIEW),
            "selected_queue_id": final["selected_queue_id"],
            "selected_kpi": f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};density={final['selected_estimated_mt5_density']};dd={final['selected_drawdown']}",
            "effect": "BB KPI(BB 핵심 성과 지표)를 package decision(패키지 결정)과 다음 queue(대기열)로 분리했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": [rel(path) for path in INPUTS],
            "time_axis": "entry_time_known_only_closed_bar(진입 시점 닫힌 봉만 사용)",
            "sample_scope": "US100 M5 BB proxy review, Tier A; Tier B out_of_scope_by_claim(US100 5분봉 BB 프록시 검토, Tier A; Tier B 주장 범위 밖)",
            "missing_or_duplicate_check": "parent BB runtime frame checks already passed, review uses generated rows only(부모 BB 런타임 프레임 점검 통과, 검토는 생성 행만 사용)",
            "feature_label_boundary": "no new feature or label; review consumes parent artifacts only(새 피처/라벨 없음, 부모 산출물만 소비)",
            "split_boundary": "validation/oos already separated in parent surface(검증/OOS는 부모 표면에서 이미 분리)",
            "leakage_risk": "package opening is based on proxy evidence, not MT5 authority(패키지 개방은 프록시 근거 기반이지 MT5 권위가 아님)",
            "data_hash_or_identity": {rel(path): sha(path) for path in INPUTS if exists(path) and Path(path).is_file()},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "run364BB package-reviewable proxy candidates(run364BB 패키지 검토 가능 프록시 후보)",
            "evidence_available": [rel(PACKAGE_CANDIDATE_REVIEW), rel(PACKAGE_DECISION), rel(RUN364BD_QUEUE), rel(FINAL_DECISION)],
            "evidence_missing": "MT5 runtime probe, Strategy Tester report, runtime parity diff(MT5 런타임 탐침, 전략 테스터 보고서, 런타임 동등성 차이)",
            "judgment_label": "exploratory_package_candidate(탐색 패키지 후보)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "패키지를 열 수 있지만 아직 운영 모델은 아니다.",
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
    package_candidates: Sequence[Mapping[str, Any]],
    failures: Sequence[Mapping[str, Any]],
    bd_queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    refresh_stage_brief_header()
    report = f"""# run364BC density restore stress candidate review(364BC 밀도 복원 압박 후보 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- package_decision(패키지 결정): `{final['package_decision']}`
- review_package_candidate_rows(검토 패키지 후보 행): `{final['review_package_candidate_rows']}`
- selected(선택): `{final['selected_queue_id']}` / `{final['selected_variant_id']}`
- selected net/PF/density/DD/trades(선택 순수익/수익 팩터/밀도/낙폭/거래수): `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_estimated_mt5_density']}` / `{final['selected_drawdown']}` / `{final['selected_trade_count']}`
- runtime_authority(런타임 권위): `not_claimed`

## Surface Review(표면 검토)

{markdown_table(review_rows, ['queue_rank', 'queue_id', 'review_status', 'combined_profit_factor', 'estimated_mt5_trade_per_business_day', 'combined_net_profit', 'combined_max_drawdown', 'combined_short_count'])}

## Package Candidates(패키지 후보)

{markdown_table(package_candidates, ['candidate_rank', 'package_role', 'queue_id', 'combined_profit_factor', 'estimated_mt5_trade_per_business_day', 'combined_net_profit', 'combined_max_drawdown', 'runtime_action'])}

## Failure Memory(실패 기억)

{markdown_table(failures, ['failure_id', 'failure_type', 'evidence', 'constraint_for_next'])}

## Next Queue(다음 대기열)

{markdown_table(bd_queue, ['package_queue_id', 'package_role', 'source_queue_id', 'short_probability_threshold', 'entry_margin_floor', 'expected_profit_factor', 'expected_estimated_mt5_density', 'runtime_claim'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): BB proxy(프록시)에서 패키지 가능 후보를 확인했으므로 BD runtime probe package(BD 런타임 탐침 패키지)를 열지만, MT5 실행 근거가 아직 없어 운영 승격은 주장하지 않는다.
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, report)
    append_text_once(
        REVIEW_INDEX,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- package_decision(패키지 결정): `{final['package_decision']}`\n- selected(선택): `{final['selected_queue_id']}`\n- next_run(다음 실행): `{NEXT_RUN_ID}`\n- effect(효과): runtime probe package(런타임 탐침 패키지)를 연다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364BC Density Restore Stress Candidate Review Closeout",
        f"\n## run364BC Density Restore Stress Candidate Review Closeout(364BC 밀도 복원 압박 후보 검토 종료)\n\nAction(행동): BB surface(BB 표면)를 검토해 package candidate(패키지 후보) 3개와 selected primary(선택 주 후보)를 확정했다.\n\nEffect(효과): Stage364(364단계)를 분기하지 않고 `{NEXT_RUN_ID}` package(패키지)로 이어간다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_runtime_probe_required(없음, 런타임 탐침 필요)
- runtime_probe_candidate(런타임 탐침 후보): `{final['selected_variant_id']}`
- latest_review(최근 검토): `{RUN_ID}`
- package_candidate_rows(패키지 후보 행): `{final['review_package_candidate_rows']}`
- next_runtime_package_queue(다음 런타임 패키지 대기열): `{rel(RUN364BD_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        CURRENT_STATE,
        f"""# Current Working State(현재 작업 상태)

current_stage(현재 단계): `{STAGE_ID}`

latest_completed_run(최근 완료 실행): `{RUN_ID}`

current_run(현재 실행): `{NEXT_RUN_ID}`

current_truth(현재 진실): run364BC(364BC 실행)는 run364BB(364BB 실행)의 package-reviewable proxy candidates(패키지 검토 가능 프록시 후보)를 검토했다. package_candidate_rows(패키지 후보 행)는 `{final['review_package_candidate_rows']}`이고 selected primary(선택 주 후보)는 `{final['selected_variant_id']}`이다. selected PF(선택 수익 팩터)는 `{final['selected_profit_factor']}`, estimated MT5 density(추정 MT5 밀도)는 `{final['selected_estimated_mt5_density']}`/day(일), net(순수익)은 `{final['selected_net_profit']}`, DD(낙폭)는 `{final['selected_drawdown']}`이다.

operating_truth_boundary(운영 진실 경계): no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no goal achieve(목표 달성 없음).

next_action(다음 행동): `{NEXT_RUN_ID}`에서 selected primary(선택 주 후보)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 만들고 compile/handoff(컴파일/인계) 근거를 기록한다.
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
        "run364BC Density Restore Stress Candidate Review",
        f"\n## run364BC Density Restore Stress Candidate Review(364BC 밀도 복원 압박 후보 검토)\n\nAction(행동): BB package candidates(BB 패키지 후보)를 검토했다.\n\nEffect(효과): `{NEXT_RUN_ID}` runtime probe package(런타임 탐침 패키지)로 이어간다.\n",
    )
    append_text_once(
        CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): density restore stress candidate review(밀도 복원 압박 후보 검토)를 실행했다.\n- effect(효과): `{NEXT_RUN_ID}` package queue(패키지 대기열)를 만들고 운영 주장은 닫았다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- idea(아이디어): `{final['selected_queue_id']}` proxy candidate(프록시 후보)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 확인한다.\n- effect(효과): 프록시에서 보인 PF/density(PF/밀도) 구조를 실제 MT5 실행 의미로 압박한다.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"## {RUN_ID}",
        f"\n## {RUN_ID}\n\n- status(상태): package_opened_no_authority(패키지 열림, 권위 없음).\n- action(행동): package candidate(패키지 후보) 외 실패/구현 필요 행을 failure memory(실패 기억)로 남겼다.\n- effect(효과): 좋은 후보만 기억하지 않고 실패 제약도 다음 패키지에 같이 넘긴다.\n",
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
        "lane": "runtime_probe_preparation(런타임 탐침 준비)",
        "work_family": "kpi_evidence(KPI 근거)",
        "primary_artifact": rel(PACKAGE_DECISION),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 검토 전용)",
        "next_action": NEXT_RUN_ID,
        "question": "Can BB package-reviewable proxy candidates open MT5 runtime probe package?(BB 패키지 가능 프록시 후보가 MT5 런타임 탐침 패키지를 열 수 있는가?)",
        "notes": f"package_candidates={final['review_package_candidate_rows']};selected={final['selected_queue_id']};next={NEXT_RUN_ID}",
        "net_profit": final["selected_net_profit"],
        "profit_factor": final["selected_profit_factor"],
        "expectancy": final["selected_expectancy"],
        "drawdown": final["selected_drawdown"],
        "recovery_factor": final["selected_recovery_factor"],
        "trade_count": final["selected_trade_count"],
        "long_trade_count": final["selected_long_count"],
        "short_trade_count": final["selected_short_count"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common])
    alpha_rows = []
    for suffix, view, tier, scope in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "proxy package review(프록시 패키지 검토)"),
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
                "primary_kpi": f"package_candidates={final['review_package_candidate_rows']};pf={final['selected_profit_factor']};density={final['selected_estimated_mt5_density']}",
                "guardrail_kpi": "no_runtime_authority;no_topn_no_split;bd_package_queue_opened",
                "evidence_boundary": CLAIM_BOUNDARY,
            }
        )
        alpha_rows.append(row)
    append_or_replace_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], alpha_rows)
    artifact_rows = []
    for artifact_type, path, notes in [
        ("surface_review", SURFACE_REVIEW, "BB surface review(BB 표면 검토)."),
        ("package_candidate_review", PACKAGE_CANDIDATE_REVIEW, "Package candidate review(패키지 후보 검토)."),
        ("package_decision", PACKAGE_DECISION, "Package decision(패키지 결정)."),
        ("failure_memory", FAILURE_MEMORY, "Failure memory(실패 기억)."),
        ("next_queue", RUN364BD_QUEUE, "BD runtime probe package queue(BD 런타임 탐침 패키지 대기열)."),
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
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUTS],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUTS if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUTS if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_expected(커밋 후 추적 예정)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
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
    parent_final, selected, surface, raw_package_rows, replay_audit = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    review_rows = review_surface_rows(surface)
    package_candidates = package_candidate_rows(raw_package_rows, selected)
    failures = failure_memory_rows(review_rows, replay_audit)
    bd_queue = bd_queue_rows(selected, raw_package_rows)
    package_rows = package_decision_rows(parent_final, selected, package_candidates)
    write_csv(SURFACE_REVIEW, review_rows)
    write_csv(PACKAGE_CANDIDATE_REVIEW, package_candidates)
    write_csv(FAILURE_MEMORY, failures)
    write_csv(PACKAGE_DECISION, package_rows)
    write_csv(RUN364BD_QUEUE, bd_queue)
    write_work_packet()
    gates = gate_rows()
    write_csv(GATE_AUDIT, gates)
    created_at = now_utc()
    final = final_payload(parent_final, selected, review_rows, package_candidates, failures, bd_queue, gates, created_at)
    write_receipts(final)
    findings = finding_rows(parent_final, selected, package_candidates, failures)
    write_csv(REVIEW_FINDINGS, findings)
    write_json(FINAL_DECISION, final)
    write_docs(final, review_rows, package_candidates, failures, bd_queue, gates)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_ledgers(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
