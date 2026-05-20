from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import run267N_pool_wide_ablation_replacement_materialization as source_materializer
from stage_pipelines.stage267 import run267O_pool_wide_balance_timeslice_trade_quality_review as source_review


STAGE_ID = source_materializer.STAGE_ID
SOURCE_RUN_ID = source_review.RUN_ID
RUN_NUMBER = "run267P"
RUN_ID = "run267P_stage267_pool_wide_internal_feature_order_confirmation_and_adapter_design_v1"
STATUS = "run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design_completed"
NEXT_ACTION = "run267Q_materialize_internal_feature_order_confirmed_adapter_candidates"
CLAIM_BOUNDARY = source_materializer.CLAIM_BOUNDARY

STAGE_ROOT = source_materializer.STAGE_ROOT
REVIEWS_ROOT = source_materializer.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_internal_feature_order_confirmation_and_adapter_design"

SOURCE_CANDIDATE_TEST_REVIEW_PATH = source_review.CANDIDATE_TEST_REVIEW_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_TEST_AXIS_SUMMARY_PATH = source_review.TEST_AXIS_SUMMARY_PATH
SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_VARIANT_MANIFEST_PATH = source_materializer.VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_materializer.RUNTIME_CONTRACT_PATH
SOURCE_FEATURE_DIAGNOSTICS_PATH = source_materializer.FEATURE_DIAGNOSTICS_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = source_materializer.ATTEMPT_MANIFEST_PATH

INTERNAL_FEATURE_ORDER_AUDIT_PATH = RUN_ROOT / "internal_feature_order_audit.csv"
ADAPTER_DESIGN_QUEUE_PATH = RUN_ROOT / "adapter_design_queue.csv"
CANDIDATE_AXIS_DECISION_PATH = RUN_ROOT / "candidate_axis_decision.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design.py")

STAGE_LEDGER_PATH = source_materializer.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_materializer.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_materializer.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_materializer.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_materializer.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_materializer.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_materializer.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_materializer.REVIEW_INDEX_PATH

VOLATILITY_TESTS = {"abl_volatility_bandwidth", "rep_volatility_atr"}
CORE_P0_CANDIDATES = {"s264_aih", "s264_aia"}
STRESS_WATCH_CANDIDATES = {"s258_stc"}
CONTROL_WATCH_CANDIDATES = {"s264_lc", "s262_lih"}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    changed = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            changed = True
            break
    if not changed:
        lines.append(replacement)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def replace_existing_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            break
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def index_rows(rows: Iterable[Mapping[str, Any]], keys: Sequence[str]) -> dict[tuple[str, ...], dict[str, Any]]:
    indexed: dict[tuple[str, ...], dict[str, Any]] = {}
    for row in rows:
        indexed[tuple(str(row.get(key, "")) for key in keys)] = dict(row)
    return indexed


def weak_flags(row: Mapping[str, Any]) -> list[str]:
    flags: list[str] = []
    if as_float(row.get("net_profit")) < 0.0:
        flags.append("net_negative")
    if as_float(row.get("profit_factor")) < 1.0:
        flags.append("pf_below_1")
    if as_float(row.get("report_equity_drawdown_percent")) >= 35.0:
        flags.append("dd_ge_35")
    if as_float(row.get("worst_month_net")) <= -100.0:
        flags.append("severe_month_le_-100")
    if as_float(row.get("weakest_session_net")) <= -150.0:
        flags.append("severe_session_le_-150")
    if as_float(row.get("weakest_hour_net")) <= -140.0:
        flags.append("severe_hour_le_-140")
    if as_float(row.get("weakest_weekday_net")) <= -120.0:
        flags.append("severe_weekday_le_-120")
    if as_int(row.get("negative_month_count")) >= 6:
        flags.append("negative_month_count_ge_6")
    if as_float(row.get("weakest_chron_net")) < 0.0:
        flags.append("chron_segment_negative")
    return flags


def path_status(*paths: str) -> str:
    missing = [path for path in paths if path and not path_exists(repo_path(path))]
    return "available" if not missing else "missing:" + ";".join(missing)


def feature_order_check(manifest: Mapping[str, Any], contract: Mapping[str, Any], diagnostic: Mapping[str, Any]) -> dict[str, Any]:
    feature_order = str(manifest.get("feature_order", ""))
    feature_names = [item for item in feature_order.split(";") if item]
    recomputed_hash = ordered_hash(feature_names) if feature_names else ""
    manifest_hash = str(manifest.get("feature_order_hash", ""))
    contract_hash = str(contract.get("feature_order_hash", ""))
    diagnostic_hash = str(diagnostic.get("feature_order_hash", ""))
    manifest_count = as_int(manifest.get("feature_count"), -1)
    contract_count = as_int(contract.get("feature_count"), -1)
    diagnostic_count = as_int(diagnostic.get("feature_count"), -1)
    added_feature = str(manifest.get("added_feature", ""))
    materialization_boundary = str(manifest.get("materialization_boundary", ""))
    variant_index = str(manifest.get("variant_feature_index", ""))
    proxy_boundary = materialization_boundary.startswith("proxy_adapter_variant")
    direct_boundary = materialization_boundary.startswith("direct_runtime_surface_ablation")

    hash_match = bool(manifest_hash and manifest_hash == contract_hash == diagnostic_hash == recomputed_hash)
    count_match = manifest_count >= 0 and manifest_count == contract_count == diagnostic_count == len(feature_names)
    if proxy_boundary:
        added_policy_ok = bool(added_feature and feature_names and added_feature == feature_names[-1] and variant_index == str(manifest_count - 1))
        added_policy = "proxy_added_feature_appended" if added_policy_ok else "proxy_added_feature_policy_mismatch"
    elif direct_boundary:
        added_policy_ok = not added_feature
        added_policy = "direct_surface_no_added_feature" if added_policy_ok else "direct_surface_unexpected_added_feature"
    else:
        added_policy_ok = False
        added_policy = "unknown_materialization_boundary"

    status_bits = []
    if not hash_match:
        status_bits.append("hash_mismatch")
    if not count_match:
        status_bits.append("feature_count_mismatch")
    if not added_policy_ok:
        status_bits.append(added_policy)
    feature_order_status = "matched" if not status_bits else ";".join(status_bits)
    return {
        "feature_order_status": feature_order_status,
        "manifest_contract_hash_match": manifest_hash == contract_hash if manifest_hash and contract_hash else False,
        "manifest_diagnostic_hash_match": manifest_hash == diagnostic_hash if manifest_hash and diagnostic_hash else False,
        "recomputed_hash_match": manifest_hash == recomputed_hash if manifest_hash and recomputed_hash else False,
        "feature_count_match": count_match,
        "added_feature_policy": added_policy,
        "feature_order_hash": manifest_hash,
        "recomputed_feature_order_hash": recomputed_hash,
        "feature_count": manifest_count,
        "feature_order": feature_order,
        "added_feature": added_feature,
        "variant_feature_index": variant_index,
    }


def metric_read(row: Mapping[str, Any]) -> str:
    if str(row.get("review_read", "")).startswith("strong_curve_clue"):
        return "strong_curve_clue"
    if as_float(row.get("net_profit")) < 0.0 or as_float(row.get("profit_factor")) < 1.0:
        return "failure_memory"
    if as_float(row.get("profit_factor")) >= 1.2 and as_float(row.get("report_equity_drawdown_percent")) < 25.0:
        return "constructive_watch"
    return "hold_or_weak_watch"


def decision_for(row: Mapping[str, Any], order_status: str, flags: Sequence[str]) -> tuple[str, str, str, str]:
    candidate = str(row.get("candidate_alias", ""))
    test_id = str(row.get("test_id", ""))
    boundary = str(row.get("materialization_boundary", ""))
    strong = str(row.get("review_read", "")).startswith("strong_curve_clue")
    proxy = boundary.startswith("proxy_adapter_variant")
    direct = boundary.startswith("direct_runtime_surface_ablation")
    order_ok = order_status == "matched"
    net = as_float(row.get("net_profit"))
    pf = as_float(row.get("profit_factor"))

    if direct and strong and test_id == "abl_gate_variant_rule":
        return (
            "direct_gate_audit_control_not_adapter",
            "AUDIT",
            "direct gate(직접 게이트) 비활성화는 강한 단서지만 Adapter(어댑터) 내부 피처 확장이 아니므로 별도 감사로 보낸다.",
            "run267Q_direct_gate_rank_contrast_before_any_adapter_use",
        )
    if net < 0.0 or pf < 1.0:
        return (
            "failure_memory_do_not_repeat",
            "FAIL",
            "순수익 또는 PF(profit factor, 수익 팩터)가 무너져 다음 Adapter(어댑터) 큐에서 제외한다.",
            "preserve_failure_memory_only",
        )
    if proxy and strong and order_ok and candidate in CORE_P0_CANDIDATES and test_id in VOLATILITY_TESTS:
        return (
            "adapter_design_p0_internal_feature_order_confirmed",
            "P0",
            "volatility/ATR(변동성/ATR) 축이 두 핵심 후보에서 반복되어 내부 Adapter(어댑터) 설계 후보로 보낸다.",
            "run267Q_materialize_internal_volatility_axis_adapter_variants",
        )
    if proxy and strong and order_ok and candidate in STRESS_WATCH_CANDIDATES and test_id == "abl_volatility_bandwidth":
        return (
            "adapter_design_p1_stress_watch",
            "P1",
            "stress challenger(압박 도전자) 단서는 있지만 후보 전체 안정성은 약해 P1 watch(P1 관찰)로 둔다.",
            "run267Q_include_as_stress_watch_if_capacity_allows",
        )
    if proxy and strong and order_ok and candidate in CONTROL_WATCH_CANDIDATES and test_id in VOLATILITY_TESTS:
        return (
            "adapter_design_p1_control_or_salvage_watch",
            "P1",
            "control/salvage(통제/회수) 단서로는 의미가 있지만 후보군 실패 기억 때문에 P0로 올리지 않는다.",
            "run267Q_include_as_control_watch_if_direct_gate_contrast_passes",
        )
    if "severe_month_le_-100" in flags or "negative_month_count_ge_6" in flags:
        return (
            "hold_due_to_time_slice_fragility",
            "HOLD",
            "약한 월 또는 음수 월 수가 불편해 현재 Adapter(어댑터) 큐에서는 대기한다.",
            "revisit_after_broader_period_pressure",
        )
    if "trend_strength" in test_id:
        return (
            "hold_trend_axis_weak_or_duplicate",
            "HOLD",
            "trend strength(추세 강도) 축은 반복 강한 단서가 아니어서 지금은 확장하지 않는다.",
            "preserve_axis_memory_no_materialization",
        )
    return (
        "hold_no_adapter_queue",
        "HOLD",
        "강한 구조 단서로 보기에는 부족해 다음 Adapter(어댑터) 큐에서 제외한다.",
        "preserve_as_diagnostic_context",
    )


def build_internal_audit() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    candidate_rows = read_csv(SOURCE_CANDIDATE_TEST_REVIEW_PATH)
    manifest_by_key = index_rows(read_csv(SOURCE_VARIANT_MANIFEST_PATH), ("candidate_alias", "test_id"))
    contract_by_key = index_rows(read_csv(SOURCE_RUNTIME_CONTRACT_PATH), ("candidate_alias", "test_id"))
    diagnostic_by_key = index_rows(read_csv(SOURCE_FEATURE_DIAGNOSTICS_PATH), ("candidate_alias", "test_id"))
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    worst_slice_by_key: dict[tuple[str, str], dict[str, str]] = {}
    for row in sorted(negative_rows, key=lambda item: as_float(item.get("net_profit"))):
        key = (str(row.get("candidate_alias", "")), str(row.get("test_id", "")))
        worst_slice_by_key.setdefault(key, row)

    audit_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    for row in candidate_rows:
        key = (str(row.get("candidate_alias", "")), str(row.get("test_id", "")))
        manifest = manifest_by_key.get(key, {})
        contract = contract_by_key.get(key, {})
        diagnostic = diagnostic_by_key.get(key, {})
        order = feature_order_check(manifest, contract, diagnostic) if manifest and contract and diagnostic else {
            "feature_order_status": "missing_manifest_contract_or_diagnostic",
            "manifest_contract_hash_match": False,
            "manifest_diagnostic_hash_match": False,
            "recomputed_hash_match": False,
            "feature_count_match": False,
            "added_feature_policy": "missing_manifest_contract_or_diagnostic",
            "feature_order_hash": "",
            "recomputed_feature_order_hash": "",
            "feature_count": "",
            "feature_order": "",
            "added_feature": "",
            "variant_feature_index": "",
        }
        flags = weak_flags(row)
        decision_class, priority, reason, next_check = decision_for(row, str(order["feature_order_status"]), flags)
        path_availability = path_status(
            str(manifest.get("source_feature_file", "")),
            str(manifest.get("feature_file", "")),
            str(manifest.get("model_file", "")),
        )
        chart_path = str(row.get("source_chart_path", ""))
        source_chart_available = path_exists(repo_path(chart_path)) if chart_path else False
        worst_slice = worst_slice_by_key.get(key, {})
        audit_row = {
            "queue_id": manifest.get("queue_id", ""),
            "source_run_id": SOURCE_RUN_ID,
            "candidate_id": row.get("candidate_id", ""),
            "candidate_alias": row.get("candidate_alias", ""),
            "candidate_role": row.get("candidate_role", ""),
            "test_id": row.get("test_id", ""),
            "test_type": row.get("test_type", ""),
            "feature_family": manifest.get("feature_family", ""),
            "materialization_boundary": row.get("materialization_boundary", ""),
            "model_materialization_type": manifest.get("model_materialization_type", ""),
            "metric_read": metric_read(row),
            "decision_class": decision_class,
            "decision_priority": priority,
            "decision_reason": reason,
            "next_check": next_check,
            "feature_order_status": order["feature_order_status"],
            "manifest_contract_hash_match": order["manifest_contract_hash_match"],
            "manifest_diagnostic_hash_match": order["manifest_diagnostic_hash_match"],
            "recomputed_hash_match": order["recomputed_hash_match"],
            "feature_count_match": order["feature_count_match"],
            "added_feature_policy": order["added_feature_policy"],
            "feature_count": order["feature_count"],
            "feature_order_hash": order["feature_order_hash"],
            "recomputed_feature_order_hash": order["recomputed_feature_order_hash"],
            "added_feature": order["added_feature"],
            "variant_feature_index": order["variant_feature_index"],
            "feature_order": order["feature_order"],
            "path_availability": path_availability,
            "source_chart_available": source_chart_available,
            "net_profit": as_float(row.get("net_profit")),
            "profit_factor": as_float(row.get("profit_factor")),
            "report_equity_drawdown_percent": as_float(row.get("report_equity_drawdown_percent")),
            "trade_count": as_int(row.get("trade_count")),
            "recovery_factor": as_float(row.get("recovery_factor")),
            "worst_month": row.get("worst_month", ""),
            "worst_month_net": as_float(row.get("worst_month_net")),
            "negative_month_count": as_int(row.get("negative_month_count")),
            "positive_month_ratio": as_float(row.get("positive_month_ratio")),
            "weakest_chron_segment": row.get("weakest_chron_segment", ""),
            "weakest_chron_net": as_float(row.get("weakest_chron_net")),
            "weakest_session_report": row.get("weakest_session_report", ""),
            "weakest_session_net": as_float(row.get("weakest_session_net")),
            "weakest_hour_report": row.get("weakest_hour_report", ""),
            "weakest_hour_net": as_float(row.get("weakest_hour_net")),
            "weakest_weekday": row.get("weakest_weekday", ""),
            "weakest_weekday_net": as_float(row.get("weakest_weekday_net")),
            "weak_flags": flags,
            "worst_negative_slice_axis": worst_slice.get("axis", ""),
            "worst_negative_slice_bucket": worst_slice.get("bucket", ""),
            "worst_negative_slice_net": as_float(worst_slice.get("net_profit")) if worst_slice else "",
            "source_feature_file": manifest.get("source_feature_file", ""),
            "feature_file": manifest.get("feature_file", ""),
            "model_file": manifest.get("model_file", ""),
            "runtime_contract_boundary": contract.get("runtime_claim_boundary", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        audit_rows.append(audit_row)
        if flags or decision_class in {"failure_memory_do_not_repeat", "hold_due_to_time_slice_fragility", "hold_trend_axis_weak_or_duplicate"}:
            failure_rows.append(
                {
                    "candidate_alias": audit_row["candidate_alias"],
                    "candidate_id": audit_row["candidate_id"],
                    "test_id": audit_row["test_id"],
                    "decision_class": decision_class,
                    "failure_flags": flags,
                    "worst_month": audit_row["worst_month"],
                    "worst_month_net": audit_row["worst_month_net"],
                    "worst_negative_slice_axis": audit_row["worst_negative_slice_axis"],
                    "worst_negative_slice_bucket": audit_row["worst_negative_slice_bucket"],
                    "worst_negative_slice_net": audit_row["worst_negative_slice_net"],
                    "do_not_repeat_without": "broader_period_or_internal_feature_rebuild_evidence",
                    "salvage_condition": "only_revisit_if_new_adapter_structure_reduces_same_weak_slice_without_trade_count_collapse",
                }
            )
    audit_rows.sort(key=lambda item: (str(item["decision_priority"]), -as_float(item["net_profit"]), str(item["candidate_alias"]), str(item["test_id"])))
    queue_rows = build_adapter_queue(audit_rows)
    return audit_rows, queue_rows, failure_rows


def build_adapter_queue(audit_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    queue_rows: list[dict[str, Any]] = []
    selected = [
        row
        for row in audit_rows
        if row.get("decision_priority") in {"P0", "P1", "AUDIT"}
    ]
    priority_order = {"P0": 0, "AUDIT": 1, "P1": 2}
    for index, row in enumerate(
        sorted(selected, key=lambda item: (priority_order.get(str(item.get("decision_priority")), 9), -as_float(item.get("net_profit")), str(item.get("candidate_alias")))),
        start=1,
    ):
        priority = str(row.get("decision_priority", ""))
        if priority == "P0":
            required_action = "rebuild proxy score(대체 점수)를 explicit internal adapter feature(명시 내부 어댑터 피처)로 물질화하고 feature order(피처 순서)를 고정한다"
            stop_rule = "same 2024 weak slices(2024 약한 구간)가 재발하거나 trade count(거래 수)가 300 아래로 무너지면 중단한다"
        elif priority == "AUDIT":
            required_action = "direct gate/rank contrast(직접 게이트/순위 대조)를 먼저 수행하고 Adapter(어댑터) 후보로 승격하지 않는다"
            stop_rule = "gate_variant(게이트 변형)이 rank_bucket failure(순위 구간 실패)와 같은 약점을 보이면 direct branch(직접 분기)를 종료한다"
        else:
            required_action = "P0 결과와 같은 산출물 형식으로만 보조 비교하고 단독 후보로 올리지 않는다"
            stop_rule = "P0보다 curve(곡선) 또는 weak slice(약한 구간)가 나쁘면 failure memory(실패 기억)로 낮춘다"
        queue_rows.append(
            {
                "queue_order": index,
                "priority": priority,
                "queue_class": row.get("decision_class", ""),
                "source_queue_id": row.get("queue_id", ""),
                "candidate_alias": row.get("candidate_alias", ""),
                "candidate_id": row.get("candidate_id", ""),
                "candidate_role": row.get("candidate_role", ""),
                "test_id": row.get("test_id", ""),
                "feature_family": row.get("feature_family", ""),
                "materialization_boundary": row.get("materialization_boundary", ""),
                "hypothesis": row.get("decision_reason", ""),
                "required_adapter_action": required_action,
                "required_feature_order_action": f"feature_order_status={row.get('feature_order_status')}; feature_order_hash={row.get('feature_order_hash')}",
                "risk_runtime_checks": "risk/ATR(위험/ATR), set/ini identity(설정/초기화 정체성), score table(점수표), trade list(거래 목록), curve/time-slice(곡선/시간구간)를 함께 확인한다",
                "stop_rule": stop_rule,
                "next_materialization_candidate": row.get("next_check", ""),
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return queue_rows


def build_candidate_decisions(audit_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in audit_rows:
        grouped[str(row.get("candidate_alias", ""))].append(row)
    decisions: list[dict[str, Any]] = []
    for candidate, rows in sorted(grouped.items()):
        priorities = Counter(str(row.get("decision_priority", "")) for row in rows)
        metric_reads = Counter(str(row.get("metric_read", "")) for row in rows)
        worst_month_floor = min(as_float(row.get("worst_month_net")) for row in rows)
        worst_slice_values = [as_float(row.get("worst_negative_slice_net")) for row in rows if row.get("worst_negative_slice_net") != ""]
        worst_slice_floor = min(worst_slice_values) if worst_slice_values else ""
        p0_tests = [str(row.get("test_id", "")) for row in rows if row.get("decision_priority") == "P0"]
        p1_tests = [str(row.get("test_id", "")) for row in rows if row.get("decision_priority") == "P1"]
        audit_tests = [str(row.get("test_id", "")) for row in rows if row.get("decision_priority") == "AUDIT"]
        if len(p0_tests) >= 2:
            decision = "advance_volatility_proxy_to_adapter_design_p0_no_selection"
            next_action = "materialize_internal_volatility_adapter_variants"
        elif audit_tests:
            decision = "retain_direct_gate_audit_control_no_adapter_selection"
            next_action = "contrast_direct_gate_with_rank_failure_before_adapter"
        elif p1_tests:
            decision = "retain_as_watch_or_stress_control_no_selection"
            next_action = "use_as_control_only_if_p0_materialization_needs_reference"
        else:
            decision = "hold_or_failure_memory_no_selection"
            next_action = "preserve_context_no_materialization"
        first = rows[0]
        decisions.append(
            {
                "candidate_alias": candidate,
                "candidate_id": first.get("candidate_id", ""),
                "candidate_role": first.get("candidate_role", ""),
                "total_tests": len(rows),
                "strong_curve_clues": metric_reads.get("strong_curve_clue", 0),
                "p0_adapter_rows": priorities.get("P0", 0),
                "p1_watch_rows": priorities.get("P1", 0),
                "direct_audit_rows": priorities.get("AUDIT", 0),
                "failure_rows": priorities.get("FAIL", 0),
                "hold_rows": priorities.get("HOLD", 0),
                "p0_tests": p0_tests,
                "p1_tests": p1_tests,
                "audit_tests": audit_tests,
                "worst_month_floor": worst_month_floor,
                "worst_negative_slice_floor": worst_slice_floor,
                "candidate_decision": decision,
                "next_action": next_action,
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return decisions


def report_markdown(result: Mapping[str, Any]) -> str:
    audit_rows = list(result["internal_feature_order_audit"])
    queue_rows = list(result["adapter_design_queue"])
    candidate_decisions = list(result["candidate_axis_decision"])
    failure_rows = list(result["failure_memory"])[:12]
    p0_rows = [row for row in queue_rows if row.get("priority") == "P0"]
    lines = [
        "# Stage267 Run267P Internal Feature Order Confirmation and Adapter Design(267P 내부 피처 순서 확인 및 어댑터 설계)",
        "",
        "## Summary(요약)",
        "",
        f"- status(상태): `{result['status']}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        "- action(행동): run267O(267O 실행)의 강한 KPI(핵심 성과 지표) 단서를 run267N(267N 실행)의 feature order(피처 순서), runtime contract(런타임 계약), materialization boundary(물질화 경계)와 다시 대조했다.",
        "- effect(효과): proxy clue(대체 단서), direct gate clue(직접 게이트 단서), failure memory(실패 기억)를 분리해 다음 Adapter(어댑터) 물질화가 숫자만 따라가지 않게 했다.",
        f"- audit_rows(감사 행): `{len(audit_rows)}`",
        f"- adapter_queue_rows(어댑터 큐 행): `{len(queue_rows)}`",
        f"- p0_adapter_rows(P0 어댑터 행): `{len(p0_rows)}`",
        f"- failure_memory_rows(실패 기억 행): `{len(result['failure_memory'])}`",
        f"- selected_candidate(선택 후보): `{result['selected_candidate']}`",
        f"- ONNX readiness(ONNX 준비): `{result['onnx_readiness']}`",
        f"- Goal Achieve(목표 달성): `{result['goal_achieve']}`",
        f"- next_action(다음 행동): `{result['next_action']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "이전 stage(단계) 연구는 버려지지 않았지만, 충분히 펼쳐졌다고 보기는 어렵다. run267P(267P 실행)는 그 빈칸을 줄이는 작업이다.",
        "특히 run267O(267O 실행)에서 좋아 보인 volatility/ATR(변동성/ATR) 축은 아직 true internal feature ablation(진짜 내부 피처 제거)이 아니라 proxy adapter variant(대체 어댑터 변형)이다.",
        "그래서 이번 결론은 후보 선택이 아니라, 어떤 단서를 Adapter(어댑터) 설계로 넘길 수 있고 어떤 단서는 실패 기억으로 묶어야 하는지 정리한 것이다.",
        "",
        "## Adapter Design Queue(어댑터 설계 큐)",
        "",
        "| priority(우선순위) | candidate(후보) | test(시험) | class(분류) | action(행동) |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in queue_rows:
        lines.append(
            f"| `{row['priority']}` | `{row['candidate_alias']}` | `{row['test_id']}` | `{row['queue_class']}` | {row['required_adapter_action']} |"
        )
    lines.extend(
        [
            "",
            "## Candidate Decisions(후보별 판정)",
            "",
            "| candidate(후보) | P0 | P1 | audit(감사) | failures(실패) | decision(판정) |",
            "| --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in candidate_decisions:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['p0_adapter_rows']} | {row['p1_watch_rows']} | {row['direct_audit_rows']} | {row['failure_rows']} | `{row['candidate_decision']}` |"
        )
    lines.extend(
        [
            "",
            "## Failure Memory(실패 기억)",
            "",
            "| candidate(후보) | test(시험) | flags(표식) | worst month(최악 월) | slice(구간) |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in failure_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['test_id']}` | `{row['failure_flags']}` | `{row['worst_month']}` {cell(row['worst_month_net'])} | `{row['worst_negative_slice_axis']}` `{row['worst_negative_slice_bucket']}` {cell(row['worst_negative_slice_net'])} |"
        )
    lines.extend(
        [
            "",
            "## Performance Attribution(성과 귀속)",
            "",
            "- observed_change(관측 변화): volatility/ATR(변동성/ATR) proxy(대체) 축은 `s264_aih`와 `s264_aia`에서 반복 단서가 되었고, `s264_lc`의 gate variant(게이트 변형)는 숫자는 강하지만 직접 런타임 표면 변경이다.",
            "- likely_driver(가능 원인): 변동성 압축/확장 문맥이 2024년 약한 구간의 손실폭을 줄였을 수 있다.",
            "- weakness(약점): `s264_lc` gate variant(게이트 변형)는 session_07_12(07~12시 세션)와 hour 22(22시) 약점이 크고, gate rank bucket(게이트 순위 구간)은 실패 기억이다.",
            "- attribution_boundary(귀속 경계): 이번 실행은 설계 감사이며, Adapter(어댑터) 물질화나 MT5(MetaTrader 5, 메타트레이더5) 재실행 결과가 아니다.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- source_candidate_test_review(원천 후보-시험 검토): `{rel(SOURCE_CANDIDATE_TEST_REVIEW_PATH)}`",
            f"- source_variant_manifest(원천 변형 목록): `{rel(SOURCE_VARIANT_MANIFEST_PATH)}`",
            f"- internal_feature_order_audit(내부 피처 순서 감사): `{rel(INTERNAL_FEATURE_ORDER_AUDIT_PATH)}`",
            f"- adapter_design_queue(어댑터 설계 큐): `{rel(ADAPTER_DESIGN_QUEUE_PATH)}`",
            f"- candidate_axis_decision(후보 축 판정): `{rel(CANDIDATE_AXIS_DECISION_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design`.",
            "- judgment_label(판정 라벨): `design_audit_completed_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).",
        ]
    )
    return "\n".join(lines)


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    judgment = "design_audit_completed_no_candidate_selection"
    p0_count = sum(1 for row in result["adapter_design_queue"] if row.get("priority") == "P0")
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "pool_wide_internal_feature_order_confirmation_and_adapter_design",
            "tier_scope": "Tier A and Tier A+B historical 2024 pool-wide P0 design audit",
            "scoreboard": "feature_order_boundary_adapter_queue_audit",
            "status": STATUS,
            "judgment": judgment,
            "evidence_boundary": "design_audit_only_no_mt5_execution_no_candidate_selection_no_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"audit_rows={len(result['internal_feature_order_audit'])};adapter_queue_rows={len(result['adapter_design_queue'])};p0_rows={p0_count};next_action={NEXT_ACTION};selected_candidate=none.",
        },
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_internal_feature_order_adapter_design",
            "status": STATUS,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "notes": f"Run267P design audit from run267N/O evidence; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__pool_wide_internal_feature_order_confirmation_and_adapter_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "pool_wide_internal_feature_order_confirmation_and_adapter_design",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "pool_wide_internal_feature_order_confirmation_and_adapter_design",
            "tier_scope": "Tier A and Tier A+B historical 2024 pool-wide P0 design audit",
            "kpi_scope": "feature_order_boundary_adapter_queue_audit",
            "scoreboard_lane": "adapter_design_queue",
            "status": STATUS,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"audit_rows={len(result['internal_feature_order_audit'])};adapter_queue_rows={len(result['adapter_design_queue'])};p0_rows={p0_count}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "not_applicable_design_audit_consumes_run267N_mt5_evidence",
            "notes": f"Next action: {NEXT_ACTION}.",
        },
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "subrun_id",
            "parent_run_id",
            "record_view",
            "tier_scope",
            "kpi_scope",
            "scoreboard_lane",
            "status",
            "judgment",
            "path",
            "primary_kpi",
            "guardrail_kpi",
            "external_verification_status",
            "notes",
        ),
    )

    entries = (
        ("stage267_run267P_adapter_design_audit_script", "producer_script", PRODUCER_PATH, "Builds run267P internal feature order and adapter design audit."),
        ("stage267_run267P_internal_feature_order_audit", "internal_feature_order_audit", INTERNAL_FEATURE_ORDER_AUDIT_PATH, "Run267P feature order/runtime contract boundary audit."),
        ("stage267_run267P_adapter_design_queue", "adapter_design_queue", ADAPTER_DESIGN_QUEUE_PATH, "Run267P next adapter design/materialization queue."),
        ("stage267_run267P_candidate_axis_decision", "candidate_axis_decision", CANDIDATE_AXIS_DECISION_PATH, "Run267P candidate-level axis decisions."),
        ("stage267_run267P_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267P failure memory and do-not-repeat guardrails."),
        ("stage267_run267P_lineage", "lineage", LINEAGE_PATH, "Run267P artifact lineage."),
        ("stage267_run267P_review_result", "review_result", REVIEW_RESULT_PATH, "Run267P review result payload."),
        ("stage267_run267P_review_report", "review_report", REPORT_PATH, "User-facing run267P adapter design audit report."),
    )
    registry_rows = read_csv(ARTIFACT_REGISTRY_PATH)
    replacement = {
        artifact_id: {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    }
    merged = [row for row in registry_rows if row.get("artifact_id") not in replacement]
    merged.extend(replacement.values())
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_current_docs(result: Mapping[str, Any]) -> None:
    review_line = f"- Stage267(267단계) run267P internal feature order confirmation and Adapter design(내부 피처 순서 확인 및 어댑터 설계): `{rel(REPORT_PATH)}`"
    index_line = f"- run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design(267P 내부 피처 순서 확인 및 어댑터 설계): `{rel(REPORT_PATH)}`"
    summary_line = (
        "Run267P(267P 실행)는 run267O(267O 실행)의 강한 단서를 run267N(267N 실행)의 feature order(피처 순서), runtime contract(런타임 계약), "
        "materialization boundary(물질화 경계)와 대조해 Adapter design queue(어댑터 설계 큐)와 failure memory(실패 기억)를 만들었다.\n"
        "Effect(효과): selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 없고, 다음 run267Q(267Q 실행)는 내부 피처 순서가 확인된 후보만 물질화 대상으로 삼는다."
    )

    for path, line, anchor in (
        (CURRENT_WORKING_STATE_PATH, review_line, "stage267_run267O_pool_wide_balance_timeslice_trade_quality_review.md"),
        (SELECTION_STATUS_PATH, index_line, "run267O_pool_wide_balance_timeslice_trade_quality_review"),
        (REVIEW_INDEX_PATH, index_line, "run267O_pool_wide_balance_timeslice_trade_quality_review"),
    ):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_existing_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_existing_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_existing_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_internal_feature_order_confirmation_and_adapter_design`")
            text = replace_existing_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
            text = replace_existing_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(
                text,
                "## Current Next Action",
                f"- latest_design(최신 설계): run267P(267P 실행) internal feature order confirmation and Adapter design(내부 피처 순서 확인 및 어댑터 설계) audit rows(감사 행) `{len(result['internal_feature_order_audit'])}`, adapter queue rows(어댑터 큐 행) `{len(result['adapter_design_queue'])}`, report(보고서) `{rel(REPORT_PATH)}`.",
            )
            text = replace_line_prefix(
                text,
                "- action(행동):",
                "- action(행동): run267P(267P 실행)는 run267O(267O 실행)의 강한 단서를 feature order(피처 순서), runtime contract(런타임 계약), Adapter design queue(어댑터 설계 큐)로 감사했다.",
            )
            text = replace_line_prefix(
                text,
                "- effect(효과):",
                "- effect(효과): 다음 작업은 내부 피처 순서가 확인된 volatility/ATR(변동성/ATR) 축을 물질화하되 선택 후보(selected candidate, 선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
            )
        elif path == SELECTION_STATUS_PATH:
            text = replace_existing_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_existing_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_existing_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_existing_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        else:
            text = replace_existing_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_existing_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_existing_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = append_after_contains(text, anchor, line)
        text = append_after_contains(text, "Run267O(267O 실행)는", summary_line)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = workspace.replace(f"current_run_id: {SOURCE_RUN_ID}", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace("status: run267O_pool_wide_balance_timeslice_trade_quality_review_completed", f"status: {STATUS}")
    workspace = workspace.replace(f"last_completed_run_id: {SOURCE_RUN_ID}", f"last_completed_run_id: {RUN_ID}")
    workspace = workspace.replace("next_action: run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design", f"next_action: {NEXT_ACTION}")
    workspace = workspace.replace(
        "Next action(다음 행동)는 `run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design`이다. Effect(효과): 내부 feature order(피처 순서) 확인과 Adapter(어댑터) 설계 가능성을 검토한다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): 내부 feature order(피처 순서)가 확인된 Adapter(어댑터) 후보만 다음 물질화 후보로 좁힌다.",
    )
    workspace = workspace.replace(
        "is active_run267O_pool_wide_balance_timeslice_trade_quality_review_completed(267O 후보군 전체 잔액/시간구간/거래품질 검토 완료, 내부 피처 확인 대기 활성).",
        "is active_run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design_completed(267P 내부 피처 순서 확인 및 어댑터 설계 완료, 내부 피처 물질화 대기 활성).",
    )
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267P(267P 실행) internal feature order confirmation and Adapter design(내부 피처 순서 확인 및 어댑터 설계) `{STATUS}`. Effect(효과): run267O(267O 실행)의 강한 KPI(핵심 성과 지표) 단서를 run267N(267N 실행)의 feature order(피처 순서), runtime contract(런타임 계약), materialization boundary(물질화 경계)와 대조했고 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다."
    )
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_line + "\n", 1)
    workspace = append_after_contains(
        workspace,
        "run267O_pool_wide_balance_timeslice_trade_quality_review_report_path",
        f"  run267P_internal_feature_order_confirmation_adapter_design_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def review() -> dict[str, Any]:
    created_at = utc_now()
    for source in (
        SOURCE_CANDIDATE_TEST_REVIEW_PATH,
        SOURCE_NEGATIVE_SLICE_PATH,
        SOURCE_VARIANT_MANIFEST_PATH,
        SOURCE_RUNTIME_CONTRACT_PATH,
        SOURCE_FEATURE_DIAGNOSTICS_PATH,
    ):
        if not path_exists(source):
            raise FileNotFoundError(source)

    audit_rows, queue_rows, failure_rows = build_internal_audit()
    candidate_decisions = build_candidate_decisions(audit_rows)
    lineage = {
        "source_inputs": [
            rel(SOURCE_CANDIDATE_TEST_REVIEW_PATH),
            rel(SOURCE_NEGATIVE_SLICE_PATH),
            rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            rel(SOURCE_TEST_AXIS_SUMMARY_PATH),
            rel(SOURCE_REVIEW_RESULT_PATH),
            rel(SOURCE_VARIANT_MANIFEST_PATH),
            rel(SOURCE_RUNTIME_CONTRACT_PATH),
            rel(SOURCE_FEATURE_DIAGNOSTICS_PATH),
            rel(SOURCE_ATTEMPT_MANIFEST_PATH),
        ],
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": {
            "internal_feature_order_audit": rel(INTERNAL_FEATURE_ORDER_AUDIT_PATH),
            "adapter_design_queue": rel(ADAPTER_DESIGN_QUEUE_PATH),
            "candidate_axis_decision": rel(CANDIDATE_AXIS_DECISION_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "lineage_judgment": "connected_design_audit_no_candidate_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    result = {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "internal_feature_order_audit": audit_rows,
        "adapter_design_queue": queue_rows,
        "candidate_axis_decision": candidate_decisions,
        "failure_memory": failure_rows,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "outputs": lineage["artifact_paths"],
    }
    write_csv(
        INTERNAL_FEATURE_ORDER_AUDIT_PATH,
        audit_rows,
        (
            "queue_id",
            "source_run_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "test_type",
            "feature_family",
            "materialization_boundary",
            "model_materialization_type",
            "metric_read",
            "decision_class",
            "decision_priority",
            "decision_reason",
            "next_check",
            "feature_order_status",
            "manifest_contract_hash_match",
            "manifest_diagnostic_hash_match",
            "recomputed_hash_match",
            "feature_count_match",
            "added_feature_policy",
            "feature_count",
            "feature_order_hash",
            "recomputed_feature_order_hash",
            "added_feature",
            "variant_feature_index",
            "feature_order",
            "path_availability",
            "source_chart_available",
            "net_profit",
            "profit_factor",
            "report_equity_drawdown_percent",
            "trade_count",
            "recovery_factor",
            "worst_month",
            "worst_month_net",
            "negative_month_count",
            "positive_month_ratio",
            "weakest_chron_segment",
            "weakest_chron_net",
            "weakest_session_report",
            "weakest_session_net",
            "weakest_hour_report",
            "weakest_hour_net",
            "weakest_weekday",
            "weakest_weekday_net",
            "weak_flags",
            "worst_negative_slice_axis",
            "worst_negative_slice_bucket",
            "worst_negative_slice_net",
            "source_feature_file",
            "feature_file",
            "model_file",
            "runtime_contract_boundary",
            "claim_boundary",
        ),
    )
    write_csv(
        ADAPTER_DESIGN_QUEUE_PATH,
        queue_rows,
        (
            "queue_order",
            "priority",
            "queue_class",
            "source_queue_id",
            "candidate_alias",
            "candidate_id",
            "candidate_role",
            "test_id",
            "feature_family",
            "materialization_boundary",
            "hypothesis",
            "required_adapter_action",
            "required_feature_order_action",
            "risk_runtime_checks",
            "stop_rule",
            "next_materialization_candidate",
            "selected_candidate",
            "onnx_readiness",
        ),
    )
    write_csv(
        CANDIDATE_AXIS_DECISION_PATH,
        candidate_decisions,
        (
            "candidate_alias",
            "candidate_id",
            "candidate_role",
            "total_tests",
            "strong_curve_clues",
            "p0_adapter_rows",
            "p1_watch_rows",
            "direct_audit_rows",
            "failure_rows",
            "hold_rows",
            "p0_tests",
            "p1_tests",
            "audit_tests",
            "worst_month_floor",
            "worst_negative_slice_floor",
            "candidate_decision",
            "next_action",
            "selected_candidate",
            "onnx_readiness",
        ),
    )
    write_csv(
        FAILURE_MEMORY_PATH,
        failure_rows,
        (
            "candidate_alias",
            "candidate_id",
            "test_id",
            "decision_class",
            "failure_flags",
            "worst_month",
            "worst_month_net",
            "worst_negative_slice_axis",
            "worst_negative_slice_bucket",
            "worst_negative_slice_net",
            "do_not_repeat_without",
            "salvage_condition",
        ),
    )
    write_json(LINEAGE_PATH, lineage)
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_docs(result)
    return result


def main() -> None:
    result = review()
    print(
        json.dumps(
            {
                "status": result["status"],
                "run_id": result["run_id"],
                "audit_rows": len(result["internal_feature_order_audit"]),
                "adapter_queue_rows": len(result["adapter_design_queue"]),
                "failure_memory_rows": len(result["failure_memory"]),
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
