from __future__ import annotations

import csv
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

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage364 import review_bx03_guard_stack_runtime_probe_without_db as cb  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = cb.STAGE_ID
RUN_NUMBER = "run364CC"
RUN_ID = "run364CC_materialize_swap_stable_reprobe_and_source_guard_inputs_without_db_v1"
PARENT_RUN_ID = cb.RUN_ID
NEXT_RUN_ID = "run364CD_execute_swap_stable_reprobe_and_source_guard_mt5_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_input_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = cb.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
SWAP_NEUTRAL_SCORE_SURFACE = RUN_DIR / "swap_neutral_score_surface.csv"
SAME_SESSION_PAIR_MATRIX = RUN_DIR / "same_session_reprobe_pair_matrix.csv"
SOURCE_GUARD_CANDIDATE_MATRIX = RUN_DIR / "source_guard_candidate_matrix.csv"
CALENDAR_CONSTRAINT_MEMORY = RUN_DIR / "calendar_constraint_memory.csv"
TESTER_IDENTITY_REQUIREMENTS = RUN_DIR / "tester_identity_requirements.csv"
SOURCE_SET_CLONE_PLAN = RUN_DIR / "source_set_clone_plan.csv"
CD_RUNTIME_QUEUE = RUN_DIR / "run364CD_runtime_attempt_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CC_swap_stable_reprobe_and_source_guard_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CC_swap_stable_reprobe_and_source_guard_inputs.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

SOURCE_CB_FINAL = cb.FINAL_DECISION
SOURCE_CB_QUEUE = cb.NEXT_QUEUE
SOURCE_CB_PAIR_DELTAS = cb.PAIR_DELTAS
SOURCE_CB_SWAP_RECONCILIATION = cb.SWAP_RECONCILIATION
SOURCE_CB_ATTRIBUTION_BY_VARIANT = cb.ATTRIBUTION_BY_VARIANT
SOURCE_CB_ATTRIBUTION_BY_SOURCE = cb.ATTRIBUTION_BY_SOURCE
SOURCE_CB_COMMON_IDENTITY = cb.COMMON_ARTIFACT_IDENTITY
SOURCE_CB_SET_DIFF = cb.SET_PARAMETER_DIFF
SOURCE_CB_REPORT = cb.REPORT_PATH
SOURCE_CA_SCOREBOARD = cb.SOURCE_CA_SCOREBOARD
SOURCE_CA_SET_MANIFEST = cb.SOURCE_CA_SET_MANIFEST
SOURCE_BX_SET_MANIFEST = cb.SOURCE_BX_SET_MANIFEST
SOURCE_CA_TESTER_IDENTITY = cb.SOURCE_CA_TESTER_IDENTITY
SOURCE_BX_TESTER_IDENTITY = cb.SOURCE_BX_TESTER_IDENTITY
SOURCE_CA_POLICY = cb.SOURCE_CA_POLICY
SOURCE_BX_POLICY = cb.SOURCE_BX_POLICY
SOURCE_EA = cb.ca.SOURCE_EA
MT5_INPUT_CONTRACT = cb.ca.MT5_INPUT_CONTRACT

SOURCE_BX3_SET = cb.BX3_SET
SOURCE_CA01_SET = cb.CA01_SET
SOURCE_CA02_SET = cb.CA02_SET
SOURCE_CA03_SET = cb.CA03_SET
SOURCE_CA06_SET = cb.CA06_SET

INPUT_FILES = [
    SOURCE_CB_FINAL,
    SOURCE_CB_QUEUE,
    SOURCE_CB_PAIR_DELTAS,
    SOURCE_CB_SWAP_RECONCILIATION,
    SOURCE_CB_ATTRIBUTION_BY_VARIANT,
    SOURCE_CB_ATTRIBUTION_BY_SOURCE,
    SOURCE_CB_COMMON_IDENTITY,
    SOURCE_CB_SET_DIFF,
    SOURCE_CB_REPORT,
    SOURCE_CA_SCOREBOARD,
    SOURCE_CA_SET_MANIFEST,
    SOURCE_BX_SET_MANIFEST,
    SOURCE_CA_TESTER_IDENTITY,
    SOURCE_BX_TESTER_IDENTITY,
    SOURCE_CA_POLICY,
    SOURCE_BX_POLICY,
    SOURCE_EA,
    MT5_INPUT_CONTRACT,
    SOURCE_BX3_SET,
    SOURCE_CA01_SET,
    SOURCE_CA02_SET,
    SOURCE_CA03_SET,
    SOURCE_CA06_SET,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    SWAP_NEUTRAL_SCORE_SURFACE,
    SAME_SESSION_PAIR_MATRIX,
    SOURCE_GUARD_CANDIDATE_MATRIX,
    CALENDAR_CONSTRAINT_MEMORY,
    TESTER_IDENTITY_REQUIREMENTS,
    SOURCE_SET_CLONE_PLAN,
    CD_RUNTIME_QUEUE,
    EXPERIMENT_RECEIPT,
    RUNTIME_RECEIPT,
    BACKTEST_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
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
    return cb.rel(path)


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def sha(path: Path | str) -> str:
    candidate = Path(path)
    return sha256_file(candidate) if exists(candidate) and io_path(candidate).is_file() else ""


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: Any) -> None:
    cb.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    cb.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    cb.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    cb.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    cb.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except (TypeError, ValueError):
            pass
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
    if not math.isfinite(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    shown = list(rows)[:limit]
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")).replace("|", "\\|") for col in columns) + " |" for row in shown]
    return "\n".join([header, sep, *body])


def hour_in_range(hour: int, start_hour: int, end_hour: int) -> bool:
    normalized_hour = hour % 24
    normalized_start = start_hour % 24
    normalized_end = 24 if end_hour == 24 else end_hour % 24
    if normalized_end == 24:
        return normalized_start <= normalized_hour < 24
    if normalized_start == normalized_end:
        return True
    if normalized_start < normalized_end:
        return normalized_start <= normalized_hour < normalized_end
    return normalized_hour >= normalized_start or normalized_hour < normalized_end


def covered_hours(start_hour: int, end_hour: int) -> str:
    return "|".join(str(hour) for hour in range(24) if hour_in_range(hour, start_hour, end_hour))


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CC inputs(CC 입력 누락): " + ", ".join(missing))
    parent_final = read_json(SOURCE_CB_FINAL)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CB next_run_id mismatch(CB 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    forbidden = ["runtime_authority", "operating_promotion", "goal_achieve"]
    if any(parent_final.get(key) != "not_claimed" for key in forbidden):
        raise RuntimeError("CB has forbidden authority claim(CB 금지 권위 주장 존재)")
    return parent_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CC swap/source guard materialization source(CC 스왑/원천 가드 구체화 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def metric_by_variant() -> dict[str, dict[str, str]]:
    return {row["variant_id"]: row for row in read_csv_rows(SOURCE_CB_ATTRIBUTION_BY_VARIANT)}


def queue_seed_rows() -> list[dict[str, str]]:
    return read_csv_rows(SOURCE_CB_QUEUE)


def pair_delta_rows() -> list[dict[str, str]]:
    return read_csv_rows(SOURCE_CB_PAIR_DELTAS)


def source_set_hash(variant_id: str) -> tuple[Path, str]:
    path_map = {
        "bx03_hour17_overlay_plus_weak_late_session_firewall": SOURCE_BX3_SET,
        "ca01_bx03_semantics_control": SOURCE_CA01_SET,
        "ca02_december_h22_only_long_block_isolation": SOURCE_CA02_SET,
        "ca03_december_h21_h23_long_block_stress": SOURCE_CA03_SET,
        "ca06_native_short_same_calendar_control": SOURCE_CA06_SET,
    }
    path = path_map[variant_id]
    return path, sha(path)


def swap_surface_rows(metrics: Mapping[str, Mapping[str, Any]], pairs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    pair_notes = {
        row["left_variant_id"]: row["interpretation"] for row in pairs if row.get("pair_id") == "ca01_vs_bx3_reproducibility_control"
    }
    pair_notes["bx03_hour17_overlay_plus_weak_late_session_firewall"] = "same_trade_path_same_gross_swap_cost_drift(동일 거래 경로/동일 총손익/스왑 비용 흔들림)"
    rows = []
    for variant_id, role in [
        ("bx03_hour17_overlay_plus_weak_late_session_firewall", "prior_bx3_reference(이전 BX3 참고)"),
        ("ca01_bx03_semantics_control", "current_best_ca_control(현재 최선 CA 대조)"),
        ("ca02_december_h22_only_long_block_isolation", "negative_calendar_memory(부정 달력 기억)"),
        ("ca03_december_h21_h23_long_block_stress", "no_increment_h23_memory(h23 무효 증가 기억)"),
        ("ca06_native_short_same_calendar_control", "native_short_source_control(기본 숏 원천 대조)"),
    ]:
        metric = metrics[variant_id]
        gross = as_float(metric.get("gross_profit"))
        swap = as_float(metric.get("swap"))
        commission = as_float(metric.get("commission"))
        net = as_float(metric.get("net_profit"))
        rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "role": role,
                "trade_count": int(as_float(metric.get("trade_count"))),
                "net_profit": finite(net, 2),
                "gross_profit": finite(gross, 2),
                "swap": finite(swap, 2),
                "commission": finite(commission, 2),
                "cost_layer": finite(swap + commission, 2),
                "swap_neutral_score": finite(gross + commission, 2),
                "net_score": finite(net, 2),
                "gross_rank_role": "use_for_signal_path_sanity(신호 경로 점검용)",
                "net_rank_role": "use_only_after_same_session_cost_check(동일 세션 비용 확인 뒤 사용)",
                "cost_drift_note": pair_notes.get(variant_id, "variant_specific_cost_layer(변형별 비용 계층)"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def runtime_queue_rows(metrics: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    specs = [
        {
            "candidate_id": "cd01_bx3_clone_current_session",
            "source_variant_id": "bx03_hour17_overlay_plus_weak_late_session_firewall",
            "runtime_priority": 1,
            "variant_role": "same_session_prior_bx3_clone(동일 세션 이전 BX3 복제)",
            "synthetic_enabled": True,
            "synthetic_hours": "17",
            "calendar_start_hour": 21,
            "calendar_end_hour": 23,
            "source_set": SOURCE_BX3_SET,
            "queue_status": "ready_for_runtime_probe(런타임 탐침 준비)",
            "comparison_pair": "cd01_vs_cd02_swap_stability_control",
            "expected_learning": "anchor prior BX3 in the same swap table(같은 스왑 표에서 이전 BX3 고정)",
        },
        {
            "candidate_id": "cd02_ca01_clone_current_session",
            "source_variant_id": "ca01_bx03_semantics_control",
            "runtime_priority": 2,
            "variant_role": "same_session_ca01_clone(동일 세션 CA01 복제)",
            "synthetic_enabled": True,
            "synthetic_hours": "17",
            "calendar_start_hour": 21,
            "calendar_end_hour": 23,
            "source_set": SOURCE_CA01_SET,
            "queue_status": "ready_for_runtime_probe(런타임 탐침 준비)",
            "comparison_pair": "cd01_vs_cd02_swap_stability_control",
            "expected_learning": "prove whether CA01/BX3 net gap was run-time swap drift(CA01/BX3 순수익 차이가 실행 시점 스왑 흔들림인지 확인)",
        },
        {
            "candidate_id": "cd03_native_short_same_calendar_current_session",
            "source_variant_id": "ca06_native_short_same_calendar_control",
            "runtime_priority": 3,
            "variant_role": "same_session_native_short_control(동일 세션 기본 숏 대조)",
            "synthetic_enabled": False,
            "synthetic_hours": "",
            "calendar_start_hour": 21,
            "calendar_end_hour": 23,
            "source_set": SOURCE_CA06_SET,
            "queue_status": "ready_for_runtime_probe(런타임 탐침 준비)",
            "comparison_pair": "cd02_vs_cd03_source_overlay_value",
            "expected_learning": "retest h17 synthetic overlay value with the same cost table(같은 비용 표에서 17시 합성 오버레이 가치 재검사)",
        },
        {
            "candidate_id": "cd04_h22_only_negative_control_deferred",
            "source_variant_id": "ca02_december_h22_only_long_block_isolation",
            "runtime_priority": 8,
            "variant_role": "deferred_negative_calendar_control(보류 부정 달력 대조)",
            "synthetic_enabled": True,
            "synthetic_hours": "17",
            "calendar_start_hour": 22,
            "calendar_end_hour": 23,
            "source_set": SOURCE_CA02_SET,
            "queue_status": "deferred_negative_memory(부정 기억 보류)",
            "comparison_pair": "not_in_cd_default_queue",
            "expected_learning": "do not reopen h21 longs unless later evidence demands it(나중 근거 전에는 h21 롱 재개 금지)",
        },
        {
            "candidate_id": "cd05_h21_h23_no_increment_deferred",
            "source_variant_id": "ca03_december_h21_h23_long_block_stress",
            "runtime_priority": 9,
            "variant_role": "deferred_no_increment_calendar_stress(보류 무증분 달력 압박)",
            "synthetic_enabled": True,
            "synthetic_hours": "17",
            "calendar_start_hour": 21,
            "calendar_end_hour": 24,
            "source_set": SOURCE_CA03_SET,
            "queue_status": "deferred_no_increment_memory(무증분 기억 보류)",
            "comparison_pair": "not_in_cd_default_queue",
            "expected_learning": "h23 expansion had no observed effect and is not first-line(h23 확장은 관측 효과가 없어 1순위 아님)",
        },
    ]
    for spec in specs:
        metric = metrics[spec["source_variant_id"]]
        rows.append(
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "candidate_id": spec["candidate_id"],
                "source_variant_id": spec["source_variant_id"],
                "runtime_priority": spec["runtime_priority"],
                "variant_role": spec["variant_role"],
                "synthetic_enabled": spec["synthetic_enabled"],
                "synthetic_hours": spec["synthetic_hours"],
                "synthetic_p_short_min": 0.4375,
                "synthetic_margin_vs_long_min": 0.075,
                "calendar_enabled": True,
                "calendar_side": "long",
                "calendar_month": 12,
                "calendar_start_hour": spec["calendar_start_hour"],
                "calendar_end_hour": spec["calendar_end_hour"],
                "covered_hours": covered_hours(spec["calendar_start_hour"], spec["calendar_end_hour"]),
                "source_set_path": rel(spec["source_set"]),
                "source_set_sha256": sha(spec["source_set"]),
                "expected_net_anchor": finite(metric.get("net_profit"), 2),
                "expected_gross_anchor": finite(metric.get("gross_profit"), 2),
                "expected_swap_anchor": finite(metric.get("swap"), 2),
                "expected_trade_count_anchor": int(as_float(metric.get("trade_count"))),
                "queue_status": spec["queue_status"],
                "comparison_pair": spec["comparison_pair"],
                "expected_learning": spec["expected_learning"],
                "timestamp_safety": "entry_known_month_hour_and_closed_bar_probabilities(진입 시점 월/시간과 닫힌 봉 확률만 사용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def source_set_clone_rows(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in queue_rows:
        if not str(row["queue_status"]).startswith("ready_for_runtime_probe"):
            continue
        rows.append(
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "candidate_id": row["candidate_id"],
                "source_set_path": row["source_set_path"],
                "source_set_sha256": row["source_set_sha256"],
                "target_set_name": f"{row['candidate_id']}_swap_stable_reprobe.set",
                "clone_action": "copy_params_not_logic(로직이 아니라 파라미터 복제)",
                "effect": "keeps EA entrypoint and module identity stable(EA 진입점과 모듈 정체성 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def same_session_pair_rows(queue_rows: Sequence[Mapping[str, Any]], parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    by_id = {row["candidate_id"]: row for row in queue_rows}
    return [
        {
            "run_id": RUN_ID,
            "pair_id": "cd01_vs_cd02_swap_stability_control",
            "left_candidate_id": "cd02_ca01_clone_current_session",
            "right_candidate_id": "cd01_bx3_clone_current_session",
            "required_same_session_batch": True,
            "expected_trade_count_delta": 0,
            "expected_gross_delta": 0.0,
            "prior_swap_delta": parent_final.get("ca01_vs_bx3_swap_delta"),
            "prior_net_delta": parent_final.get("ca01_vs_bx3_net_delta"),
            "success_condition": "same trade path and abs(swap/net delta) <= 1.00(동일 거래 경로 및 스왑/순수익 차이 절댓값 1.00 이하)",
            "failure_condition": "same path still has material swap/net drift(같은 경로인데 스왑/순수익 드리프트가 계속 큼)",
            "left_source_set": by_id["cd02_ca01_clone_current_session"]["source_set_path"],
            "right_source_set": by_id["cd01_bx3_clone_current_session"]["source_set_path"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "pair_id": "cd02_vs_cd03_source_overlay_value",
            "left_candidate_id": "cd02_ca01_clone_current_session",
            "right_candidate_id": "cd03_native_short_same_calendar_current_session",
            "required_same_session_batch": True,
            "expected_trade_count_delta": 6,
            "expected_gross_delta": 41.09,
            "prior_swap_delta": 0.0,
            "prior_net_delta": parent_final.get("ca01_vs_ca06_overlay_net_delta"),
            "success_condition": "h17 synthetic overlay keeps positive net lift against native short control(17시 합성 오버레이가 기본 숏 대조 대비 순수익 우위 유지)",
            "failure_condition": "overlay lift disappears or costs reverse it(오버레이 우위가 사라지거나 비용이 뒤집음)",
            "left_source_set": by_id["cd02_ca01_clone_current_session"]["source_set_path"],
            "right_source_set": by_id["cd03_native_short_same_calendar_current_session"]["source_set_path"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def source_guard_rows(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "guard_id": "preserve_h17_synthetic_overlay_seed",
            "guard_type": "source_guard_seed(원천 가드 씨앗)",
            "rule": "keep synthetic short overlay at hour 17(17시 합성 숏 오버레이 유지)",
            "evidence": f"CA01 vs CA06 net delta {parent_final.get('ca01_vs_ca06_overlay_net_delta')}",
            "next_use": "cd02_vs_cd03 same-session source value pair(CD02/CD03 동일 세션 원천 가치 쌍)",
            "status": "materialized_for_reprobe(재탐침용 구체화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guard_id": "keep_h21_h22_december_long_block",
            "guard_type": "calendar_constraint(달력 제약)",
            "rule": "keep December long block hours 21-23 exclusive end(12월 롱 차단 21-23, 종료 시간 제외)",
            "evidence": f"h22-only isolation added {parent_final.get('ca02_added_trade_count')} trades and net {parent_final.get('ca02_added_trade_net')}",
            "next_use": "default CD ready queue(CD 기본 준비 대기열)",
            "status": "kept_as_failure_memory(실패 기억으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guard_id": "separate_gross_net_swap_layers",
            "guard_type": "score_guard(점수 가드)",
            "rule": "rank signal path with gross layer before mutable swap layer(변동 스왑 계층 전 총손익 계층으로 신호 경로 판독)",
            "evidence": f"CA01 vs BX3 gross delta {parent_final.get('ca01_vs_bx3_gross_delta')} and swap delta {parent_final.get('ca01_vs_bx3_swap_delta')}",
            "next_use": "swap neutral score surface(스왑 중립 점수 표면)",
            "status": "materialized_for_review(리뷰용 구체화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def calendar_memory_rows(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "memory_id": "reject_h22_only_isolation_for_default_cd",
            "finding": "h22-only isolation reopened h21 longs and hurt net(h22 단독 분리는 h21 롱을 재개해 순수익을 낮춤)",
            "metric": f"added_trades={parent_final.get('ca02_added_trade_count')}; added_net={parent_final.get('ca02_added_trade_net')}",
            "constraint": "do not use h22-only as default runtime queue(h22 단독을 기본 런타임 대기열에 넣지 않음)",
            "reopen_condition": "new evidence shows h21 block is the real drag(새 근거가 h21 차단을 진짜 부담으로 보일 때)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "memory_id": "defer_h23_expansion_no_increment",
            "finding": "h21-h23 stress had no incremental trade effect(h21-h23 압박은 추가 거래 효과 없음)",
            "metric": f"ca03_vs_ca01_net_delta={parent_final.get('ca03_vs_ca01_net_delta')}",
            "constraint": "do not spend first CD slot on h23 expansion(CD 첫 슬롯을 h23 확장에 쓰지 않음)",
            "reopen_condition": "drawdown-specific evidence targets h23(h23을 겨냥한 낙폭 근거가 생길 때)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def tester_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "identity_item": "symbol_timeframe(심볼/시간프레임)",
            "required_value": "US100 M5",
            "source_evidence": rel(SOURCE_CA_TESTER_IDENTITY),
            "effect": "same broker symbol contract(같은 브로커 심볼 계약 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "identity_item": "tester_model(테스터 모델)",
            "required_value": "Model=4 Every tick based on real ticks(실제 틱 기반 모든 틱)",
            "source_evidence": rel(SOURCE_CA_TESTER_IDENTITY),
            "effect": "cost and fill path stays comparable(비용과 체결 경로 비교 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "identity_item": "account(계좌)",
            "required_value": "Deposit=500; Leverage=100; fixed_lot=0.1(예치금 500, 레버리지 100, 고정 0.1랏)",
            "source_evidence": rel(SOURCE_CA_TESTER_IDENTITY),
            "effect": "drawdown and recovery factor stay comparable(낙폭과 회복 계수 비교 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "identity_item": "runtime_contract(런타임 계약)",
            "required_value": "same ONNX, feature order, probability tape, EA entrypoint(동일 온엑스, 피처 순서, 확률 테이프, EA 진입점)",
            "source_evidence": rel(SOURCE_CB_COMMON_IDENTITY),
            "effect": "signal path changes cannot hide in artifact drift(신호 경로 변화가 산출물 드리프트에 숨지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(queue_rows: Sequence[Mapping[str, Any]], pair_rows: Sequence[Mapping[str, Any]], source_rows: Sequence[Mapping[str, Any]], receipts_written: bool) -> list[dict[str, Any]]:
    ready_count = sum(1 for row in queue_rows if str(row["queue_status"]).startswith("ready_for_runtime_probe"))
    gates = [
        {
            "gate": "work_packet_schema_lint",
            "status": "passed" if exists(WORK_PACKET) else "failed",
            "evidence": rel(WORK_PACKET),
            "effect": "primary family and required gates are explicit(주 작업군과 필수 게이트 명시)",
        },
        {
            "gate": "input_lineage_gate",
            "status": "passed" if all(exists(path) for path in INPUT_FILES) else "failed",
            "evidence": rel(INPUT_MANIFEST),
            "effect": "CB evidence and source sets are connected(CB 근거와 원천 설정 연결)",
        },
        {
            "gate": "same_session_reprobe_design_gate",
            "status": "passed" if ready_count >= 3 and any(row["pair_id"] == "cd01_vs_cd02_swap_stability_control" for row in pair_rows) else "failed",
            "evidence": rel(SAME_SESSION_PAIR_MATRIX),
            "effect": "swap drift can be isolated in one MT5 batch(스왑 드리프트를 한 MT5 묶음에서 분리 가능)",
        },
        {
            "gate": "source_guard_design_gate",
            "status": "passed" if any(row["guard_id"] == "preserve_h17_synthetic_overlay_seed" for row in source_rows) else "failed",
            "evidence": rel(SOURCE_GUARD_CANDIDATE_MATRIX),
            "effect": "offensive h17 source clue is preserved(공격적 17시 원천 단서 유지)",
        },
        {
            "gate": "runtime_handoff_queue_gate",
            "status": "passed" if ready_count == 3 else "failed",
            "evidence": rel(CD_RUNTIME_QUEUE),
            "effect": "CD has exactly three default runtime attempts(CD 기본 런타임 시도 3개 고정)",
        },
        {
            "gate": "required_gate_coverage_audit",
            "status": "passed" if receipts_written else "failed",
            "evidence": rel(GATE_AUDIT),
            "effect": "receipts and gates are linked(영수증과 게이트 연결)",
        },
        {
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "no runtime authority or operating promotion is claimed(런타임 권위나 운영 승격 주장 없음)",
        },
    ]
    return gates


def final_payload(
    parent_final: Mapping[str, Any],
    queue_rows: Sequence[Mapping[str, Any]],
    pair_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    ready_count = sum(1 for row in queue_rows if str(row["queue_status"]).startswith("ready_for_runtime_probe"))
    deferred_count = len(queue_rows) - ready_count
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": "completed_stage364CC_swap_stable_reprobe_and_source_guard_inputs_materialized_open_cd_no_authority",
        "judgment": "experiment_design_materialized_swap_stable_reprobe_and_source_guard_runtime_handoff_ready_no_authority",
        "decision": "stage364CC_open_run364CD_execute_same_session_swap_stable_reprobe",
        "created_at_utc": created_at,
        "runtime_ready_candidate_count": ready_count,
        "deferred_memory_candidate_count": deferred_count,
        "same_session_pair_count": len(pair_rows),
        "best_variant_id": parent_final.get("best_variant_id"),
        "best_mt5_net_profit": parent_final.get("best_mt5_net_profit"),
        "best_mt5_profit_factor": parent_final.get("best_mt5_profit_factor"),
        "best_mt5_expectancy": parent_final.get("best_mt5_expectancy"),
        "best_mt5_trade_count": parent_final.get("best_mt5_trade_count"),
        "best_mt5_density": parent_final.get("best_mt5_density"),
        "best_mt5_recovery_factor": parent_final.get("best_mt5_recovery_factor"),
        "best_mt5_equity_drawdown_amount": parent_final.get("best_mt5_equity_drawdown_amount"),
        "ca01_vs_bx3_common_trade_count": parent_final.get("ca01_vs_bx3_common_trade_count"),
        "ca01_vs_bx3_gross_delta": parent_final.get("ca01_vs_bx3_gross_delta"),
        "ca01_vs_bx3_swap_delta": parent_final.get("ca01_vs_bx3_swap_delta"),
        "ca01_vs_bx3_net_delta": parent_final.get("ca01_vs_bx3_net_delta"),
        "ca01_vs_ca06_overlay_net_delta": parent_final.get("ca01_vs_ca06_overlay_net_delta"),
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run_materialization_only",
        "external_verification_status": "out_of_scope_by_claim_materialization_only(주장 범위 밖, 구체화 전용)",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "CA01/BX3 profit gap is mutable swap-table drift, while h17 synthetic overlay remains a usable source clue(CA01/BX3 수익 차이는 변동 스왑 표 드리프트이고, 17시 합성 오버레이는 쓸 수 있는 원천 단서다)",
            "decision_use": "choose the next MT5 runtime probe queue and scoring layer(다음 MT5 런타임 탐침 대기열과 점수 계층 선택)",
            "comparison_baseline": "prior BX3, CA01, and native short same-calendar control(이전 BX3, CA01, 기본 숏 동일 달력 대조)",
            "control_variables": ["same ONNX(동일 온엑스)", "same feature order(동일 피처 순서)", "same EA entrypoint(EA 진입점 동일)", "US100 M5 real-tick tester(US100 M5 실제 틱 테스터)"],
            "changed_variables": ["run namespace(실행 이름공간)", "source set cloned into CD(CD로 복제할 원천 설정)", "default queue membership(기본 대기열 구성)"],
            "sample_scope": "MT5 validation OOS runtime probe handoff(MT5 검증 OOS 런타임 탐침 인계)",
            "success_criteria": "CD shows same trade path and near-zero swap/net delta for BX3 vs CA01(CD에서 BX3와 CA01 거래 경로 동일 및 스왑/순수익 차이 0 근처)",
            "failure_criteria": "same path remains materially swap-sensitive or h17 overlay loses source value(같은 경로가 계속 스왑 민감하거나 17시 오버레이 가치 상실)",
            "invalid_conditions": ["MT5 report missing(MT5 보고서 누락)", "source set hash mismatch(원천 설정 해시 불일치)", "tester identity drift(테스터 정체성 드리프트)"],
            "stop_conditions": "do not claim runtime authority until same-session evidence is reviewed(동일 세션 근거 리뷰 전 런타임 권위 주장 금지)",
            "evidence_plan": [rel(CD_RUNTIME_QUEUE), rel(SAME_SESSION_PAIR_MATRIX), rel(SWAP_NEUTRAL_SCORE_SURFACE)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": [rel(SOURCE_CB_PAIR_DELTAS), rel(SOURCE_CB_SWAP_RECONCILIATION), rel(SWAP_NEUTRAL_SCORE_SURFACE)],
            "runtime_path": [rel(CD_RUNTIME_QUEUE), rel(SOURCE_SET_CLONE_PLAN), rel(TESTER_IDENTITY_REQUIREMENTS), rel(SOURCE_EA)],
            "shared_contract": "same model, feature order, EA entrypoint, tester identity, and parameter-only variants(동일 모델, 피처 순서, EA 진입점, 테스터 정체성, 파라미터 전용 변형)",
            "known_differences": "CD will use a new run namespace and must execute in one same-session batch(CD는 새 실행 이름공간을 쓰며 한 동일 세션 묶음으로 실행해야 함)",
            "parity_check": "not_run_materialization_only; next CD must provide tester output(구체화 전용이라 미실행, 다음 CD가 테스터 출력을 제공해야 함)",
            "parity_identity": {
                "source_bx3_set_sha256": sha(SOURCE_BX3_SET),
                "source_ca01_set_sha256": sha(SOURCE_CA01_SET),
                "source_ca06_set_sha256": sha(SOURCE_CA06_SET),
                "common_identity_evidence": rel(SOURCE_CB_COMMON_IDENTITY),
            },
            "runtime_claim_boundary": "runtime_input_materialization_only(런타임 입력 구체화 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            "run_id": RUN_ID,
            "tester_identity": rel(TESTER_IDENTITY_REQUIREMENTS),
            "ea_identity": [rel(SOURCE_EA), rel(SOURCE_CB_COMMON_IDENTITY)],
            "report_identity": "previous CB reviewed reports only; no new CD report yet(이전 CB 리뷰 보고서만, 새 CD 보고서 없음)",
            "trade_evidence": [rel(SOURCE_CB_ATTRIBUTION_BY_VARIANT), rel(SOURCE_CB_PAIR_DELTAS)],
            "cost_assumptions": "broker Strategy Tester swap is treated as mutable until same-session reprobe closes it(브로커 전략 테스터 스왑은 동일 세션 재탐침 전까지 변동 가능 비용으로 취급)",
            "forensic_checks": [rel(SOURCE_CB_SWAP_RECONCILIATION), rel(SOURCE_CB_SET_DIFF), rel(TESTER_IDENTITY_REQUIREMENTS)],
            "backtest_judgment": "usable_for_handoff_with_boundary(경계부 인계용 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "swap-stable reprobe and source guard input materialization(스왑 안정 재탐침 및 원천 가드 입력 구체화)",
            "evidence_available": [rel(CD_RUNTIME_QUEUE), rel(SAME_SESSION_PAIR_MATRIX), rel(SOURCE_GUARD_CANDIDATE_MATRIX)],
            "evidence_missing": ["new MT5 CD execution(새 MT5 CD 실행)", "forward replay(전진 재생)", "runtime authority closure(런타임 권위 폐쇄)"],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "The next run is now narrowed to one same-session cost test and one source-value control(다음 실행은 동일 세션 비용 시험 1개와 원천 가치 대조 1개로 좁혀졌다).",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "runtime handoff inputs materialized only(런타임 인계 입력 구체화만)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "new_model_training": final["new_model_training"],
            "new_mt5_execution": final["new_mt5_execution"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_closeout(종료 뒤 추적됨)",
            "lineage_judgment": "connected_with_materialization_boundary(구체화 경계로 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(
    final: Mapping[str, Any],
    queue_rows: Sequence[Mapping[str, Any]],
    pair_rows: Sequence[Mapping[str, Any]],
    surface_rows: Sequence[Mapping[str, Any]],
    guard_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    ready_rows = [row for row in queue_rows if str(row["queue_status"]).startswith("ready_for_runtime_probe")]
    report = f"""# run364CC swap-stable reprobe and source guard inputs(364CC 스왑 안정 재탐침 및 원천 가드 입력)

## Result(결과)

Action(행동): CB review(CB 리뷰)의 trade path(거래 경로), gross/net/swap(총손익/순수익/스왑), set hash(설정 해시)를 읽어 CD MT5 runtime probe(CD MT5 런타임 탐침) 입력으로 materialize(구체화)했다.

Effect(효과): CA01과 BX3의 신호 경로가 같은지, 아니면 swap table(스왑 표)만 흔들렸는지 다음 실행에서 한 묶음으로 확인할 수 있게 됐다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next(다음): `{NEXT_RUN_ID}`
- ready candidates(준비 후보): `{final['runtime_ready_candidate_count']}`
- gate(게이트): `{final['gate_passes']}/{final['gate_total']}`

## Runtime Queue(런타임 대기열)

{markdown_table(ready_rows, ['candidate_id', 'runtime_priority', 'source_variant_id', 'synthetic_enabled', 'calendar_start_hour', 'calendar_end_hour', 'expected_net_anchor'], 8)}

## Same-Session Pairs(동일 세션 쌍)

{markdown_table(pair_rows, ['pair_id', 'left_candidate_id', 'right_candidate_id', 'prior_swap_delta', 'success_condition'], 8)}

## Swap-Neutral Surface(스왑 중립 표면)

{markdown_table(surface_rows, ['variant_id', 'net_profit', 'gross_profit', 'swap', 'swap_neutral_score', 'net_rank_role'], 8)}

## Source Guard(원천 가드)

{markdown_table(guard_rows, ['guard_id', 'guard_type', 'status', 'evidence'], 8)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Boundary(경계)

CC는 input materialization(입력 구체화)만 주장한다. 새 MT5 execution(MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision: Stage364CC swap-stable reprobe and source guard inputs(결정: 364CC 스왑 안정 재탐침 및 원천 가드 입력)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Action(행동): CD queue(CD 대기열)에 `cd01_bx3_clone_current_session`, `cd02_ca01_clone_current_session`, `cd03_native_short_same_calendar_current_session` 세 가지 runtime attempt(런타임 시도)를 넣었다.

Effect(효과): 같은 MT5 session(동일 MT5 세션)에서 BX3와 CA01의 swap/net delta(스왑/순수익 차이)를 재측정하고, h17 synthetic overlay(17시 합성 오버레이)가 native short control(기본 숏 대조)을 여전히 이기는지 확인할 수 있다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, "<!-- run364CC -->", f"\n<!-- run364CC -->\n- `{RUN_ID}`: swap-stable reprobe and source guard inputs(스왑 안정 재탐침 및 원천 가드 입력) -> `{rel(REPORT_PATH)}`\n")
    append_text_once(STAGE_README, "<!-- run364CC -->", f"\n<!-- run364CC -->\n## run364CC swap-stable reprobe and source guard inputs(스왑 안정 재탐침 및 원천 가드 입력)\n\n`{final['judgment']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364CC` materialized(구체화 완료) same-session swap-stable reprobe(동일 세션 스왑 안정 재탐침)와 source guard seed(원천 가드 씨앗). CD default queue(CD 기본 대기열)는 BX3 clone(BX3 복제), CA01 clone(CA01 복제), native short same-calendar control(기본 숏 동일 달력 대조) 3개다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 한 세션 묶음으로 실행하고, BX3/CA01 trade path(거래 경로), gross/net/swap(총손익/순수익/스왑), h17 overlay value(17시 오버레이 가치)를 리뷰한다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Runtime probe reviewed best variant(리뷰된 런타임 탐침 최선 변형): `{final['best_variant_id']}`

Best CA MT5 KPI(최선 CA MT5 핵심 성과 지표): net `{final['best_mt5_net_profit']}`, PF `{final['best_mt5_profit_factor']}`, trades `{final['best_mt5_trade_count']}`, density `{final['best_mt5_density']}`, recovery `{final['best_mt5_recovery_factor']}`, equity DD `{final['best_mt5_equity_drawdown_amount']}`.

Current handoff(현재 인계): CD same-session queue(CD 동일 세션 대기열) `{final['runtime_ready_candidate_count']}` ready candidates(준비 후보), `{final['deferred_memory_candidate_count']}` deferred memory candidates(보류 기억 후보).

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, "<!-- run364CC -->", f"\n<!-- run364CC -->\n- {final['created_at_utc']} `{RUN_ID}` materialized swap-stable reprobe and source guard runtime inputs(스왑 안정 재탐침 및 원천 가드 런타임 입력 구체화). Judgment(판정): `{final['judgment']}`.\n")
    append_text_once(
        IDEA_REGISTRY,
        "<!-- run364CC_swap_source_guard_handoff -->",
        "\n<!-- run364CC_swap_source_guard_handoff -->\n- Idea(아이디어): BX3와 CA01의 trade path(거래 경로)가 같으므로 next runtime probe(다음 런타임 탐침)는 same-session swap stability(동일 세션 스왑 안정성)와 h17 synthetic overlay source value(17시 합성 오버레이 원천 가치)를 같이 본다. Effect(효과): 비용 드리프트와 원천 단서를 분리해 다음 공격 탐색을 덜 흐리게 만든다.\n",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "lane": "runtime_input_materialization(런타임 입력 구체화)",
        "family": "experiment_design(실험 설계)",
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["runtime_ready_candidate_count"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(CD_RUNTIME_QUEUE),
        "result_status": final["status"],
        "net_profit": final["best_mt5_net_profit"],
        "profit_factor": final["best_mt5_profit_factor"],
        "expectancy": final["best_mt5_expectancy"],
        "trade_count": final["best_mt5_trade_count"],
        "trade_density_per_feature_day": final["best_mt5_density"],
        "recovery_factor": final["best_mt5_recovery_factor"],
        "max_drawdown_amount": final["best_mt5_equity_drawdown_amount"],
        "trade_density_requirement_status": "inherited_parent_passed_density_floor(상위 실행 밀도 하한 통과 상속)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_design(실험 설계)",
        "evidence_boundary": "materialization_only(구체화 전용)",
        "external_verification_status": final["external_verification_status"],
        "next_action": NEXT_RUN_ID,
        "question": "Can BX3/CA01 swap drift be isolated in one same-session runtime batch?(BX3/CA01 스왑 드리프트를 동일 세션 런타임 묶음에서 분리할 수 있는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for view, tier, scope in [
        ("Tier A used(Tier A 사용)", "Tier A", "runtime_input_materialization"),
        ("Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required"),
        ("actual routed total(실제 라우팅 전체)", "Tier A+B", "runtime_input_materialization"),
    ]:
        ledger_rows.append(
            {
                **common,
                "ledger_row_id": f"{RUN_ID}::{tier.replace(' ', '_').replace('+', 'B')}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": scope,
                "view": view,
                "tier": tier,
                "metric_scope": scope,
                "notes": "Tier B missing_required(Tier B 필수 누락); no fallback source(대체 원천 없음).",
            }
        )
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)

    artifact_rows = []
    for artifact_type, path in [
        ("final_decision", FINAL_DECISION),
        ("cd_runtime_queue", CD_RUNTIME_QUEUE),
        ("same_session_pair_matrix", SAME_SESSION_PAIR_MATRIX),
        ("swap_neutral_score_surface", SWAP_NEUTRAL_SCORE_SURFACE),
        ("source_guard_candidate_matrix", SOURCE_GUARD_CANDIDATE_MATRIX),
        ("report", REPORT_PATH),
        ("script", Path(__file__)),
        ("gate_audit", GATE_AUDIT),
    ]:
        artifact_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha(path),
                "created_at": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
                "created_at_utc": final["created_at_utc"],
                "notes": "runtime handoff materialization artifact(런타임 인계 구체화 산출물)",
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)


def write_run_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "producer": rel(Path(__file__)),
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()],
            "final_decision": rel(FINAL_DECISION),
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": final["created_at_utc"],
        },
    )


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    parent_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "work_packet_schema_lint",
                "input_lineage_gate",
                "same_session_reprobe_design_gate",
                "source_guard_design_gate",
                "runtime_handoff_queue_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    metrics = metric_by_variant()
    pairs = pair_delta_rows()
    surface_rows = swap_surface_rows(metrics, pairs)
    queue_rows = runtime_queue_rows(metrics)
    clone_rows = source_set_clone_rows(queue_rows)
    pair_rows = same_session_pair_rows(queue_rows, parent_final)
    guard_rows = source_guard_rows(parent_final)
    memory_rows = calendar_memory_rows(parent_final)
    tester_rows = tester_identity_rows()
    write_csv(SWAP_NEUTRAL_SCORE_SURFACE, surface_rows)
    write_csv(CD_RUNTIME_QUEUE, queue_rows)
    write_csv(SOURCE_SET_CLONE_PLAN, clone_rows)
    write_csv(SAME_SESSION_PAIR_MATRIX, pair_rows)
    write_csv(SOURCE_GUARD_CANDIDATE_MATRIX, guard_rows)
    write_csv(CALENDAR_CONSTRAINT_MEMORY, memory_rows)
    write_csv(TESTER_IDENTITY_REQUIREMENTS, tester_rows)
    gates = build_gates(queue_rows, pair_rows, guard_rows, receipts_written=False)
    final = final_payload(parent_final, queue_rows, pair_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = build_gates(queue_rows, pair_rows, guard_rows, receipts_written=True)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(parent_final, queue_rows, pair_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, queue_rows, pair_rows, surface_rows, guard_rows, gates)
    write_ledgers(final)
    write_run_manifest(final)
    write_receipts(final)
    write_run_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
