from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "267_adapter_research__baseline_candidate_racing_protocol"
RUN_NUMBER = "run267M"
RUN_ID = "run267M_stage267_pool_wide_ablation_replacement_design_v1"
STATUS = "run267M_pool_wide_ablation_replacement_design_completed"
NEXT_ACTION = "run267N_materialize_pool_wide_ablation_replacement_p0"
CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_"
    "no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate"
)

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
DESIGN_ROOT = RUN_ROOT / "pool_wide_ablation_replacement_design"

POOL_PATH = STAGE_ROOT / "01_inputs" / "baseline_candidate_pool.csv"
INITIAL_SCOREBOARD_PATH = REVIEWS_ROOT / "stage267_initial_scoreboard.csv"
MONTHLY_WEAKNESS_PATH = REVIEWS_ROOT / "stage267_monthly_weakness_matrix.csv"
SEGMENT_WEAKNESS_PATH = REVIEWS_ROOT / "stage267_segment_weakness_matrix.csv"
ABLATION_MAP_PATH = STAGE_ROOT / "02_runs" / "run267B" / "feature_ablation_map.csv"
REPLACEMENT_MAP_PATH = STAGE_ROOT / "02_runs" / "run267B" / "similar_feature_replacement_map.csv"
HISTORICAL_2024_WEAKNESS_PATH = STAGE_ROOT / "02_runs" / "run267B" / "historical_2024" / "candidate_weakness_summary.csv"
RUN267K_CANDIDATE_REVIEW_PATH = (
    STAGE_ROOT / "02_runs" / "run267K" / "retrained_soft_context_adapter_materialization" / "candidate_retrained_soft_context_review.csv"
)
RUN267L_DECISION_PATH = (
    STAGE_ROOT / "02_runs" / "run267L" / "retrained_soft_context_followup_or_prune" / "followup_or_prune_decision_matrix.csv"
)
RUN267L_NEXT_DESIGN_PATH = (
    STAGE_ROOT / "02_runs" / "run267L" / "retrained_soft_context_followup_or_prune" / "next_pool_wide_experiment_design.csv"
)

CANDIDATE_CONTEXT_PATH = DESIGN_ROOT / "candidate_context_matrix.csv"
WEAK_SLICE_MATRIX_PATH = DESIGN_ROOT / "pool_wide_weak_slice_matrix.csv"
ABLATION_REPLACEMENT_MATRIX_PATH = DESIGN_ROOT / "ablation_replacement_matrix.csv"
MATERIALIZATION_QUEUE_PATH = DESIGN_ROOT / "p0_materialization_queue.csv"
VALIDATION_RECEIPT_PATH = DESIGN_ROOT / "design_validation_receipt.csv"
LINEAGE_PATH = DESIGN_ROOT / "lineage.json"
RESULT_PATH = DESIGN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267M_pool_wide_ablation_replacement_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267M_pool_wide_ablation_replacement_design.py")

STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

ID_TO_ALIAS = {
    "s264_allow_inner_high_quarter": "s264_aih",
    "s264_lowrank_control": "s264_lc",
    "s262_lowrank_inner_half_filter": "s262_lih",
    "s264_allow_inner_all_oos_anchor": "s264_aia",
    "s258_short_tight_control": "s258_stc",
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def replace_tail_from_marker(text: str, marker: str, replacement: str) -> str:
    start = text.find(marker)
    if start == -1:
        return text.rstrip() + "\n" + replacement.rstrip() + "\n"
    return text[:start].rstrip() + "\n" + replacement.rstrip() + "\n"


def by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {str(row.get(key)): dict(row) for row in rows if row.get(key)}


def alias_for(candidate_id: str) -> str:
    return ID_TO_ALIAS.get(candidate_id, candidate_id)


def derive_priority(candidate_id: str, family: str, row_id: str) -> str:
    role_sensitive = {
        "s264_allow_inner_high_quarter": {"trend_strength_direction", "volatility_bandwidth", "trend_strength(추세 강도)", "volatility_risk(변동성 위험)"},
        "s264_lowrank_control": {"source_feature_rank_bucket", "source_feature_gate", "compressed_gate(압축 게이트)", "trend_strength(추세 강도)"},
        "s262_lowrank_inner_half_filter": {"source_feature_rank_bucket", "moving_average_trend", "trend_spread(추세 간격)", "compressed_gate(압축 게이트)"},
        "s264_allow_inner_all_oos_anchor": {"session_timing", "volatility_bandwidth", "volatility_risk(변동성 위험)", "trend_strength(추세 강도)"},
        "s258_short_tight_control": {"volatility_bandwidth", "price_return_range", "session_timing", "volatility_risk(변동성 위험)"},
    }
    if family in role_sensitive.get(candidate_id, set()) or row_id in {"abl_trend_strength_direction", "rep_trend_strength_adx", "rep_volatility_atr"}:
        return "P0(우선순위 0)"
    if family in {"moving_average_trend", "oscillator_momentum", "compressed_gate(압축 게이트)", "trend_spread(추세 간격)"}:
        return "P1(우선순위 1)"
    return "P2(우선순위 2)"


def build_candidate_context(
    pool_rows: Sequence[Mapping[str, str]],
    initial_rows: Sequence[Mapping[str, str]],
    historical_rows: Sequence[Mapping[str, str]],
    run267k_rows: Sequence[Mapping[str, str]],
    run267l_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    initial_by_id = by_key(initial_rows, "candidate_id")
    historical_by_id = by_key(historical_rows, "candidate_id")
    run267k_by_id = by_key(run267k_rows, "candidate_id")
    run267l_by_id = by_key(run267l_rows, "candidate_id")
    rows: list[dict[str, Any]] = []
    for pool in pool_rows:
        candidate_id = str(pool.get("candidate_id"))
        initial = initial_by_id.get(candidate_id, {})
        historical = historical_by_id.get(candidate_id, {})
        run267k = run267k_by_id.get(candidate_id, {})
        run267l = run267l_by_id.get(candidate_id, {})
        rows.append(
            {
                "candidate_id": candidate_id,
                "candidate_alias": alias_for(candidate_id),
                "role_ko": pool.get("role_ko"),
                "role_en": pool.get("role_en"),
                "source_stage": pool.get("source_stage"),
                "initial_validation_pf": as_float(initial.get("validation_pf")),
                "initial_validation_net": as_float(initial.get("validation_net")),
                "initial_validation_dd_percent": as_float(initial.get("validation_dd_percent")),
                "initial_oos_pf": as_float(initial.get("oos_pf")),
                "initial_oos_net": as_float(initial.get("oos_net")),
                "initial_oos_dd_percent": as_float(initial.get("oos_dd_percent")),
                "historical_2024_net": as_float(historical.get("net_profit")),
                "historical_2024_pf": as_float(historical.get("profit_factor")),
                "historical_2024_trade_count": as_int(historical.get("trade_count")),
                "historical_2024_dd_percent": as_float(historical.get("report_equity_drawdown_percent")),
                "historical_2024_worst_month": historical.get("worst_month"),
                "historical_2024_worst_month_net": as_float(historical.get("worst_month_net")),
                "historical_2024_curve_grade": historical.get("curve_grade"),
                "run267k_net": as_float(run267k.get("net_profit"), default=""),
                "run267k_pf": as_float(run267k.get("profit_factor"), default=""),
                "run267k_trade_count": as_int(run267k.get("trade_count"), default=0),
                "run267k_dd_percent": as_float(run267k.get("report_equity_drawdown_percent"), default=""),
                "run267l_decision": run267l.get("decision") or "not_in_retrain_branch(재학습 분기 밖)",
                "racing_role": pool.get("initial_racing_use"),
                "known_strength": pool.get("known_strength"),
                "known_risk": pool.get("known_risk"),
            }
        )
    return rows


def build_weak_slice_matrix(
    monthly_rows: Sequence[Mapping[str, str]],
    segment_rows: Sequence[Mapping[str, str]],
    historical_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in monthly_rows:
        rows.append(
            {
                "candidate_id": row.get("candidate_id"),
                "candidate_alias": alias_for(str(row.get("candidate_id"))),
                "source": "stage267_regular_window(정규 구간)",
                "axis": "month(월)",
                "split": row.get("split"),
                "bucket": row.get("month"),
                "trade_count": as_int(row.get("trade_count")),
                "net_profit": as_float(row.get("net_profit")),
                "profit_factor": as_float(row.get("profit_factor")),
                "quality_flag": row.get("quality_flag"),
                "weakness_read": row.get("weakness_read_ko"),
                "priority": "P0(우선순위 0)" if row.get("quality_flag") == "negative_month" else "P1(우선순위 1)",
            }
        )
    for row in segment_rows:
        rows.append(
            {
                "candidate_id": row.get("candidate_id"),
                "candidate_alias": alias_for(str(row.get("candidate_id"))),
                "source": "stage267_regular_window(정규 구간)",
                "axis": "chron_segment(순서 구간)",
                "split": row.get("split"),
                "bucket": row.get("segment"),
                "trade_count": as_int(row.get("trade_count")),
                "net_profit": as_float(row.get("net_profit")),
                "profit_factor": as_float(row.get("profit_factor")),
                "quality_flag": row.get("quality_flag"),
                "weakness_read": row.get("weakness_read_ko"),
                "priority": "P1(우선순위 1)",
            }
        )
    for row in historical_rows:
        candidate_id = str(row.get("candidate_id"))
        weak_items = (
            ("worst_month(최악 월)", row.get("worst_month"), row.get("worst_month_net")),
            ("weakest_session(최약 세션)", row.get("weakest_session"), row.get("weakest_session_net")),
            ("weakest_hour(최약 시간)", row.get("weakest_hour_utc"), row.get("weakest_hour_net")),
            ("weakest_adx_bucket(최약 ADX 구간)", row.get("weakest_adx_bucket"), row.get("weakest_adx_net")),
            ("weakest_chron_segment(최약 순서 구간)", row.get("weakest_chron_segment"), row.get("weakest_chron_net")),
        )
        for axis, bucket, net in weak_items:
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "candidate_alias": row.get("candidate_alias") or alias_for(candidate_id),
                    "source": "historical_2024(2024 과거 압박)",
                    "axis": axis,
                    "split": "historical_2024",
                    "bucket": bucket,
                    "trade_count": as_int(row.get("trade_count")),
                    "net_profit": as_float(net),
                    "profit_factor": as_float(row.get("profit_factor")),
                    "quality_flag": row.get("curve_grade"),
                    "weakness_read": row.get("candidate_read"),
                    "priority": "P0(우선순위 0)" if as_float(net) < -100 else "P1(우선순위 1)",
                }
            )
    return rows


def build_ablation_replacement_matrix(
    candidate_rows: Sequence[Mapping[str, Any]],
    ablation_rows: Sequence[Mapping[str, str]],
    replacement_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in candidate_rows:
        candidate_id = str(candidate["candidate_id"])
        role = str(candidate.get("role_en") or "")
        for source in ablation_rows:
            feature_group = str(source.get("feature_group"))
            priority = derive_priority(candidate_id, feature_group, str(source.get("ablation_id")))
            rows.append(
                {
                    "matrix_id": f"{candidate['candidate_alias']}__{source.get('ablation_id')}",
                    "candidate_id": candidate_id,
                    "candidate_alias": candidate.get("candidate_alias"),
                    "candidate_role": role,
                    "test_type": "feature_category_ablation(피처 범주 제거)",
                    "test_id": source.get("ablation_id"),
                    "feature_family": feature_group,
                    "features_or_replacements": source.get("features_or_columns"),
                    "reason": source.get("reason"),
                    "expected_read": source.get("expected_read"),
                    "priority": priority,
                    "execution_status": "planned_for_run267N_or_later(267N 이후 계획)",
                }
            )
        for source in replacement_rows:
            source_family = str(source.get("source_family"))
            priority = derive_priority(candidate_id, source_family, str(source.get("replacement_id")))
            rows.append(
                {
                    "matrix_id": f"{candidate['candidate_alias']}__{source.get('replacement_id')}",
                    "candidate_id": candidate_id,
                    "candidate_alias": candidate.get("candidate_alias"),
                    "candidate_role": role,
                    "test_type": "similar_feature_replacement(유사 피처 대체)",
                    "test_id": source.get("replacement_id"),
                    "feature_family": source_family,
                    "features_or_replacements": f"{source.get('source_feature')} -> {source.get('replacement_candidates')}",
                    "reason": source.get("reason"),
                    "expected_read": (
                        "candidate_should_degrade_gracefully_not_collapse(후보는 완전히 무너지지 않고 완만히 약화해야 함)"
                    ),
                    "priority": priority,
                    "execution_status": "planned_for_run267N_or_later(267N 이후 계획)",
                }
            )
    return rows


def build_materialization_queue(matrix_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    p0_rows = [row for row in matrix_rows if str(row.get("priority")) == "P0(우선순위 0)"]
    queue: list[dict[str, Any]] = []
    per_candidate: dict[str, int] = {}
    for row in p0_rows:
        candidate_id = str(row.get("candidate_id"))
        count = per_candidate.get(candidate_id, 0)
        if count >= 5:
            continue
        per_candidate[candidate_id] = count + 1
        queue.append(
            {
                "queue_id": f"run267N_{len(queue) + 1:02d}_{row.get('candidate_alias')}_{row.get('test_id')}",
                "source_matrix_id": row.get("matrix_id"),
                "candidate_id": candidate_id,
                "candidate_alias": row.get("candidate_alias"),
                "test_type": row.get("test_type"),
                "test_id": row.get("test_id"),
                "feature_family": row.get("feature_family"),
                "features_or_replacements": row.get("features_or_replacements"),
                "materialization_lane": "stage_local_feature_surface_variant(단계 로컬 피처 표면 변형)",
                "required_views": "Tier A separate;Tier B required_or_out_of_scope;actual routed total(Tier A 분리;Tier B 필수 또는 범위 밖;실제 라우팅 전체)",
                "success_gate": "dd_down_or_weak_slice_less_negative_without_trade_count_collapse(손실폭 또는 약한 구간 완화, 거래 수 붕괴 없음)",
                "failure_gate": "candidate_collapses_or_only_one_slice_improves(후보 붕괴 또는 한 구간만 개선)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return queue


def build_validation_receipt() -> list[dict[str, Any]]:
    return [
        {
            "check_id": "experiment_design_receipt",
            "check_family": "obsidian-experiment-design(실험 설계)",
            "requirement": "hypothesis_comparison_controls_changed_variables_success_failure_stop_evidence_named(가설/비교/통제/변경/성공/실패/중단/근거 명명)",
            "evidence_source": rel(REPORT_PATH),
            "pass_condition": "all_five_candidates_present_and_p0_queue_exists(다섯 후보 존재, P0 큐 존재)",
            "failure_action": "do_not_materialize_run267N(267N 물질화 금지)",
            "effect": "prevents_narrow_single_candidate_followup(좁은 단일 후보 후속 방지)",
        },
        {
            "check_id": "data_integrity_receipt",
            "check_family": "obsidian-data-integrity(데이터 무결성)",
            "requirement": "source_time_axis_split_label_boundary_and_leakage_risk_named(원천/시간축/분리/라벨 경계/누수 위험 명명)",
            "evidence_source": rel(REPORT_PATH),
            "pass_condition": "2024_weakness_not_used_as_training_label(2024 약점을 학습 라벨로 쓰지 않음)",
            "failure_action": "mark_design_invalid(설계 무효)",
            "effect": "prevents_historical_stress_overfit(과거 압박 과적합 방지)",
        },
        {
            "check_id": "model_validation_receipt",
            "check_family": "obsidian-model-validation(모델 검증)",
            "requirement": "model_family_threshold_policy_calibration_risk_overfit_risk_named(모델군/문턱값 정책/보정 위험/과적합 위험 명명)",
            "evidence_source": rel(REPORT_PATH),
            "pass_condition": "no_model_or_threshold_selection_claim(모델 또는 문턱값 선택 주장 없음)",
            "failure_action": "downgrade_claim(주장 낮춤)",
            "effect": "prevents_design_from_becoming_selection(설계가 선택으로 둔갑하는 일 방지)",
        },
        {
            "check_id": "result_judgment_receipt",
            "check_family": "obsidian-result-judgment(결과 판정)",
            "requirement": "selected_candidate_onnx_goal_claim_boundary_explicit(선택 후보/ONNX/목표/주장 경계 명시)",
            "evidence_source": rel(REPORT_PATH),
            "pass_condition": "selected_candidate_none_and_goal_not_claimed(선택 후보 없음, 목표 미주장)",
            "failure_action": "block_closeout(마감 차단)",
            "effect": "keeps_research_boundary(연구 경계 유지)",
        },
    ]


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    items = [
        ("stage267_run267M_design_script", "producer_script", PRODUCER_PATH, "Builds run267M pool-wide ablation/replacement design."),
        ("stage267_run267M_candidate_context", "candidate_context_matrix", CANDIDATE_CONTEXT_PATH, "Run267M candidate context matrix."),
        ("stage267_run267M_weak_slice_matrix", "weak_slice_matrix", WEAK_SLICE_MATRIX_PATH, "Run267M pool-wide weak-slice matrix."),
        ("stage267_run267M_ablation_replacement_matrix", "ablation_replacement_matrix", ABLATION_REPLACEMENT_MATRIX_PATH, "Run267M ablation and replacement matrix."),
        ("stage267_run267M_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267M P0 materialization queue."),
        ("stage267_run267M_validation_receipt", "validation_receipt", VALIDATION_RECEIPT_PATH, "Run267M design validation receipt."),
        ("stage267_run267M_lineage", "lineage", LINEAGE_PATH, "Run267M lineage."),
        ("stage267_run267M_result", "result", RESULT_PATH, "Run267M JSON result."),
        ("stage267_run267M_report", "review_report", REPORT_PATH, "User-facing run267M report."),
    ]
    rows = []
    for artifact_id, artifact_type, path, notes in items:
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    return rows


def build_result() -> dict[str, Any]:
    created_at = utc_now()
    pool_rows = read_csv(POOL_PATH)
    initial_rows = read_csv(INITIAL_SCOREBOARD_PATH)
    monthly_rows = read_csv(MONTHLY_WEAKNESS_PATH)
    segment_rows = read_csv(SEGMENT_WEAKNESS_PATH)
    ablation_rows = read_csv(ABLATION_MAP_PATH)
    replacement_rows = read_csv(REPLACEMENT_MAP_PATH)
    historical_rows = read_csv(HISTORICAL_2024_WEAKNESS_PATH)
    run267k_rows = read_csv(RUN267K_CANDIDATE_REVIEW_PATH)
    run267l_rows = read_csv(RUN267L_DECISION_PATH)
    candidate_context = build_candidate_context(pool_rows, initial_rows, historical_rows, run267k_rows, run267l_rows)
    weak_slice_matrix = build_weak_slice_matrix(monthly_rows, segment_rows, historical_rows)
    ablation_replacement_matrix = build_ablation_replacement_matrix(candidate_context, ablation_rows, replacement_rows)
    materialization_queue = build_materialization_queue(ablation_replacement_matrix)
    validation_receipt = build_validation_receipt()
    lineage = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "inputs": {
            "baseline_candidate_pool": rel(POOL_PATH),
            "initial_scoreboard": rel(INITIAL_SCOREBOARD_PATH),
            "monthly_weakness": rel(MONTHLY_WEAKNESS_PATH),
            "segment_weakness": rel(SEGMENT_WEAKNESS_PATH),
            "feature_ablation_map": rel(ABLATION_MAP_PATH),
            "similar_replacement_map": rel(REPLACEMENT_MAP_PATH),
            "historical_2024_weakness": rel(HISTORICAL_2024_WEAKNESS_PATH),
            "run267K_candidate_review": rel(RUN267K_CANDIDATE_REVIEW_PATH),
            "run267L_decision": rel(RUN267L_DECISION_PATH),
            "run267L_next_design": rel(RUN267L_NEXT_DESIGN_PATH),
        },
        "outputs": {
            "candidate_context": rel(CANDIDATE_CONTEXT_PATH),
            "weak_slice_matrix": rel(WEAK_SLICE_MATRIX_PATH),
            "ablation_replacement_matrix": rel(ABLATION_REPLACEMENT_MATRIX_PATH),
            "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
            "validation_receipt": rel(VALIDATION_RECEIPT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    return {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_context": candidate_context,
        "weak_slice_matrix": weak_slice_matrix,
        "ablation_replacement_matrix": ablation_replacement_matrix,
        "materialization_queue": materialization_queue,
        "validation_receipt": validation_receipt,
        "lineage": lineage,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
    }


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(
        CANDIDATE_CONTEXT_PATH,
        result["candidate_context"],
        (
            "candidate_id",
            "candidate_alias",
            "role_ko",
            "role_en",
            "source_stage",
            "initial_validation_pf",
            "initial_validation_net",
            "initial_validation_dd_percent",
            "initial_oos_pf",
            "initial_oos_net",
            "initial_oos_dd_percent",
            "historical_2024_net",
            "historical_2024_pf",
            "historical_2024_trade_count",
            "historical_2024_dd_percent",
            "historical_2024_worst_month",
            "historical_2024_worst_month_net",
            "historical_2024_curve_grade",
            "run267k_net",
            "run267k_pf",
            "run267k_trade_count",
            "run267k_dd_percent",
            "run267l_decision",
            "racing_role",
            "known_strength",
            "known_risk",
        ),
    )
    write_csv(
        WEAK_SLICE_MATRIX_PATH,
        result["weak_slice_matrix"],
        (
            "candidate_id",
            "candidate_alias",
            "source",
            "axis",
            "split",
            "bucket",
            "trade_count",
            "net_profit",
            "profit_factor",
            "quality_flag",
            "weakness_read",
            "priority",
        ),
    )
    write_csv(
        ABLATION_REPLACEMENT_MATRIX_PATH,
        result["ablation_replacement_matrix"],
        (
            "matrix_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_type",
            "test_id",
            "feature_family",
            "features_or_replacements",
            "reason",
            "expected_read",
            "priority",
            "execution_status",
        ),
    )
    write_csv(
        MATERIALIZATION_QUEUE_PATH,
        result["materialization_queue"],
        (
            "queue_id",
            "source_matrix_id",
            "candidate_id",
            "candidate_alias",
            "test_type",
            "test_id",
            "feature_family",
            "features_or_replacements",
            "materialization_lane",
            "required_views",
            "success_gate",
            "failure_gate",
            "claim_boundary",
        ),
    )
    write_csv(
        VALIDATION_RECEIPT_PATH,
        result["validation_receipt"],
        ("check_id", "check_family", "requirement", "evidence_source", "pass_condition", "failure_action", "effect"),
    )
    write_json(LINEAGE_PATH, result["lineage"])
    write_json(RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def fmt(value: Any) -> str:
    text = str(value)
    if text == "":
        return ""
    return f"{as_float(value):.2f}"


def report_markdown(result: Mapping[str, Any]) -> str:
    candidates = list(result["candidate_context"])
    queue = list(result["materialization_queue"])
    weak_slices = list(result["weak_slice_matrix"])
    p0_counts: dict[str, int] = {}
    for row in queue:
        alias = str(row.get("candidate_alias"))
        p0_counts[alias] = p0_counts.get(alias, 0) + 1
    negative_slices = [row for row in weak_slices if as_float(row.get("net_profit")) < 0]
    lines = [
        "# Stage267 Run267M Pool-wide Ablation and Replacement Design(267M 후보군 전체 제거/대체 설계)",
        "",
        "## Summary(요약)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        "- primary_family(주 작업군): `experiment_design(실험 설계)`.",
        "- primary_skill(주 스킬): `obsidian-experiment-design(실험 설계)`.",
        "- support_skills(보조 스킬): `obsidian-data-integrity(데이터 무결성)`, `obsidian-model-validation(모델 검증)`, `obsidian-result-judgment(결과 판정)`.",
        "- action(행동): 다섯 Baseline candidates(기준 후보) 전체를 feature/category ablation(피처/범주 제거), similar replacement(유사 대체), weak-slice matrix(약한 구간 행렬)로 다시 설계했다.",
        "- effect(효과): run267K(267K 실행)의 soft-context retrain(부드러운 문맥 재학습) 단서를 보존하되, 다음 작업을 한 후보 미세 수리가 아니라 후보군 전체 구조 검증으로 옮긴다.",
        "",
        "## Candidate Context(후보 맥락)",
        "",
        "| candidate(후보) | role(역할) | initial val PF(초기 검증 PF) | OOS net(표본외 순수익) | 2024 net(2024 순수익) | 2024 DD%(2024 손실폭) | run267K/run267L read(267K/267L 판독) |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in candidates:
        run267_read = row.get("run267l_decision")
        if run267_read == "not_in_retrain_branch(재학습 분기 밖)":
            run267_read = "pool_only(후보군 전용)"
        lines.append(
            f"| `{row['candidate_alias']}` | {row['role_ko']} | {fmt(row['initial_validation_pf'])} | "
            f"{fmt(row['initial_oos_net'])} | {fmt(row['historical_2024_net'])} | "
            f"{fmt(row['historical_2024_dd_percent'])} | {run267_read} |"
        )
    lines.extend(
        [
            "",
            "## Design Scope(설계 범위)",
            "",
            f"- candidate_count(후보 수): `{len(candidates)}`.",
            f"- weak_slice_rows(약한 구간 행): `{len(weak_slices)}`; negative_slice_rows(음수 구간 행): `{len(negative_slices)}`.",
            f"- ablation_replacement_rows(제거/대체 행): `{len(result['ablation_replacement_matrix'])}`.",
            f"- P0 materialization queue(P0 물질화 큐): `{len(queue)}` rows(행).",
            "- sample_scope(표본 범위): US100 M5, regular validation/OOS(정규 검증/표본외) 단서와 2024 historical stress(2024 과거 압박) 단서를 함께 쓴다.",
            "- changed_variables(변경 변수): feature category removal(피처 범주 제거), trend/volatility/momentum/breadth replacement(추세/변동성/모멘텀/폭 대체), compressed gate/rank variation(압축 게이트/순위 변형).",
            "- control_variables(통제 변수): symbol/timeframe/cost/tester contract(심볼/시간봉/비용/테스터 계약), 후보 ID, 기존 stage evidence(단계 근거) 경계.",
            "",
            "## P0 Queue(P0 큐)",
            "",
            "| candidate(후보) | queued tests(큐 테스트 수) | focus(초점) |",
            "| --- | ---: | --- |",
        ]
    )
    for row in candidates:
        alias = str(row["candidate_alias"])
        lines.append(
            f"| `{alias}` | {p0_counts.get(alias, 0)} | trend/volatility/gate stress(추세/변동성/게이트 압박) |"
        )
    lines.extend(
        [
            "",
            "## Experiment Design(실험 설계)",
            "",
            "- hypothesis(가설): 강한 후보라면 특정 feature family(피처군), ADX/ATR(ADX/ATR), rank bucket(순위 구간), 특정 약한 월 하나에만 붙어 있지 않아야 한다.",
            "- decision_use(결정 사용처): 후보 유지/가지치기/회수, Adapter(어댑터) 구조 확장 가치, 다음 materialization(물질화) 우선순위를 정한다.",
            "- comparison_baseline(비교 기준): Stage267 initial scoreboard(초기 점수판), run267B 2024 historical stress(2024 과거 압박), run267K/run267L retrain salvage(재학습 회수 단서).",
            "- success_criteria(성공 기준): DD(drawdown, 손실폭)와 weak slices(약한 구간)가 완화되면서 trade count(거래 수), PF(profit factor, 수익 팩터), expectancy(기대값)가 무너지지 않는다.",
            "- failure_criteria(실패 기준): 특정 feature(피처) 제거나 유사 대체에서 후보가 완전히 무너지거나, 한 달/한 요일만 좋아지고 전체 curve(곡선)가 나빠진다.",
            "- invalid_conditions(무효 조건): 2024 결과를 학습 target(목표)으로 사용, feature order(피처 순서) 불일치, split leakage(분리 누수), Tier B(티어 B) 기록 누락을 숨기는 경우.",
            "- stop_conditions(중단 조건): P0에서 동일 후보가 feature family(피처군) 2개 이상에서 붕괴하면 그 후보는 candidate(후보)가 아니라 failure memory(실패 기억) 또는 salvage clue(회수 단서)로 낮춘다.",
            "- evidence_plan(근거 계획): materialization manifest(물질화 목록), feature/model manifest(피처/모델 목록), parity check(동등성 점검), MT5 execution report(MT5 실행 보고), trade records(거래 기록), curve diagnostics(곡선 진단), negative slice summary(음수 구간 요약), ledger rows(장부 행).",
            "",
            "## Data and Model Boundary(데이터와 모델 경계)",
            "",
            "- data_source(데이터 원천): baseline candidate pool(기준 후보군), Stage267 scoreboards(점수판), run267B 2024 outputs(2024 출력), run267K/run267L evidence(근거).",
            "- time_axis(시간축): FPMarkets US100 M5 broker time(FPMarkets US100 M5 브로커 시간), 기존 stage 계약을 따른다.",
            "- feature_label_boundary(피처/라벨 경계): run267M(267M 실행)은 설계만 만들며 새 label(라벨)이나 outcome-fitted target(결과 맞춤 목표)을 만들지 않는다.",
            "- split_boundary(분리 경계): 2024 historical stress(2024 과거 압박)는 견고성 판독이며 학습 선택으로 과장하지 않는다.",
            "- leakage_risk(누수 위험): 약한 월을 직접 학습 target(목표)으로 쓰거나, replacement feature(대체 피처)가 미래 bar(봉)를 참조하는 경우.",
            "- integrity_judgment(무결성 판정): `usable_with_boundary(경계付き 사용 가능)`.",
            "- model_family(모델군): current candidate surfaces(현재 후보 표면)와 stage-local feature variants(단계 로컬 피처 변형)를 비교 설계한다.",
            "- threshold_policy(문턱값 정책): 이번 run(실행)은 새 threshold search(문턱값 탐색)를 하지 않는다.",
            "- overfit_risk(과적합 위험): feature family(피처군)를 많이 시험하므로, 단일 최고값보다 깨짐 정도를 우선 판독한다.",
            "- validation_judgment(검증 판정): `design_ready_for_materialization_no_candidate_selection(물질화 설계 준비, 선택 후보 없음)`.",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(판정 대상): run267M pool-wide ablation/replacement design(267M 후보군 전체 제거/대체 설계).",
            "- evidence_available(있는 근거): candidate context(후보 맥락), weak slice matrix(약한 구간 행렬), ablation/replacement matrix(제거/대체 행렬), P0 queue(P0 큐).",
            "- evidence_missing(없는 근거): run267N materialization/execution(267N 물질화/실행), MT5 results(MT5 결과), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `design_ready_no_candidate_selection(설계 준비, 선택 후보 없음)`.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- candidate_context_matrix(후보 맥락 행렬): `{rel(CANDIDATE_CONTEXT_PATH)}`",
            f"- weak_slice_matrix(약한 구간 행렬): `{rel(WEAK_SLICE_MATRIX_PATH)}`",
            f"- ablation_replacement_matrix(제거/대체 행렬): `{rel(ABLATION_REPLACEMENT_MATRIX_PATH)}`",
            f"- materialization_queue(물질화 큐): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- validation_receipt(검증 영수증): `{rel(VALIDATION_RECEIPT_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- result(결과): `{rel(RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def update_ledgers(result: Mapping[str, Any]) -> None:
    created_at = str(result["created_at_utc"])
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267M_pool_wide_ablation_replacement_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "pool_wide_ablation_replacement_design",
            "tier_scope": "all five baseline candidates design",
            "scoreboard": "experiment_design",
            "status": STATUS,
            "judgment": "design_ready_no_candidate_selection",
            "evidence_boundary": "design_matrix_only_no_mt5_execution_no_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"candidate_count={len(result['candidate_context'])};matrix_rows={len(result['ablation_replacement_matrix'])};queue_rows={len(result['materialization_queue'])};next_action={NEXT_ACTION}.",
        },
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__pool_wide_ablation_replacement_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "pool_wide_ablation_replacement_design",
            "parent_run_id": RUN_ID,
            "record_view": "pool_wide_ablation_replacement_design",
            "tier_scope": "all five baseline candidates design",
            "kpi_scope": "design_matrix_and_materialization_queue",
            "scoreboard_lane": "experiment_design",
            "status": STATUS,
            "judgment": "design_ready_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"candidate_count={len(result['candidate_context'])};matrix_rows={len(result['ablation_replacement_matrix'])};queue_rows={len(result['materialization_queue'])}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "not_applicable_design_only",
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
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_pool_wide_ablation_replacement_design",
            "status": STATUS,
            "judgment": "design_ready_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"Run267M pool-wide ablation/replacement design; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    for row in artifact_rows(created_at):
        upsert_csv(
            ARTIFACT_REGISTRY_PATH,
            "artifact_id",
            row,
            ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        )


def update_current_working_state() -> None:
    text = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_ablation_replacement_design`")
    text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
    evidence_line = f"- Stage267(267단계) run267M pool-wide ablation/replacement design(후보군 전체 제거/대체 설계): `{rel(REPORT_PATH)}`"
    text = append_after_contains(text, "stage267_run267L_retrained_soft_context_followup_or_prune.md", evidence_line)
    latest_line = f"- latest_design(최신 설계): run267M(267M 실행) pool-wide ablation/replacement design(후보군 전체 제거/대체 설계) `{rel(REPORT_PATH)}`."
    text = append_after_contains(text, "latest_design(최신 설계): run267L", latest_line)
    text = text.replace("- next_run(다음 실행): `run267M_design_pool_wide_ablation_replacement_and_weak_slice_matrix`", f"- next_run(다음 실행): `{NEXT_ACTION}`")
    text = replace_line_prefix(
        text,
        "- action(행동):",
        "- action(행동): run267M(267M 실행)는 다섯 Baseline candidates(기준 후보) 전체의 feature/category ablation(피처/범주 제거), similar replacement(유사 대체), weak-slice matrix(약한 구간 행렬), P0 materialization queue(P0 물질화 큐)를 만들었다.",
    )
    text = replace_line_prefix(
        text,
        "- effect(효과):",
        "- effect(효과): 다음 작업은 후보별 강점/약점을 같은 조건으로 물질화해 누가 덜 깨지는지 볼 수 있다.",
    )
    text = replace_line_prefix(
        text,
        "- next_action(다음 행동):",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): P0 ablation/replacement(우선 제거/대체) 변형을 물질화해 MT5(MetaTrader 5, 메타트레이더5) 실행 준비로 넘긴다.",
    )
    text = replace_tail_from_marker(
        text,
        "Run267I(267I 실행)는",
        (
            "Run267I(267I 실행)는 P0 soft non-calendar Adapter MT5 review(P0 부드러운 비달력 어댑터 MT5 검토)를 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭)가 여전히 불편해 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
            "Run267K(267K 실행)는 retrained soft-context Adapter MT5 review(재학습 부드러운 문맥 어댑터 MT5 검토)를 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 좋아졌지만 Monday(월요일), 2024-12 약점과 거래 수 축소가 남았다.\n\n"
            "Run267L(267L 실행)는 retrained soft-context branch(재학습 부드러운 문맥 분기)를 salvage clue(회수 단서)로 가지치기했다.\n"
            "Effect(효과): 한 후보 수리 루프를 끊고 후보군 전체 검증으로 되돌렸다.\n\n"
            "Run267M(267M 실행)는 다섯 Baseline candidates(기준 후보) 전체의 ablation/replacement(제거/대체), weak-slice matrix(약한 구간 행렬), P0 materialization queue(P0 물질화 큐)를 설계했다.\n"
            f"Effect(효과): 다음 행동(next action, 다음 행동)은 `{NEXT_ACTION}`이고, 아직 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 없다.\n"
        ),
    )
    write_md(CURRENT_WORKING_STATE_PATH, text)


def update_selection_status() -> None:
    text = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    text = append_after_contains(
        text,
        "run267L_retrained_soft_context_followup_or_prune",
        f"- run267M_pool_wide_ablation_replacement_design(267M 후보군 전체 제거/대체 설계): `{rel(REPORT_PATH)}`",
    )
    text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    text = replace_tail_from_marker(
        text,
        "Run267I(267I 실행)는",
        (
            "Run267I(267I 실행)는 P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화), MT5 execution(MT5 실행), MT5 review(MT5 검토)까지 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭), Monday(월요일), July(7월), chron_mid(중간 순서 구간) 약점이 남아 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
            "Run267L(267L 실행)는 retrained soft-context branch(재학습 부드러운 문맥 분기)를 standalone candidate(독립 후보)가 아니라 salvage clue(회수 단서)로 가지치기했다.\n"
            "Effect(효과): selected candidate(선택 후보)는 없고, 후보군 전체 설계로 되돌아갔다.\n\n"
            "Run267M(267M 실행)는 다섯 Baseline candidates(기준 후보) 전체의 ablation/replacement(제거/대체), weak-slice matrix(약한 구간 행렬), P0 materialization queue(P0 물질화 큐)를 설계했다.\n"
            f"Effect(효과): selected candidate(선택 후보)는 여전히 없고, next_action(다음 행동)은 `{NEXT_ACTION}`이다.\n"
        ),
    )
    write_md(SELECTION_STATUS_PATH, text)


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    text = append_after_contains(
        text,
        "run267L_retrained_soft_context_followup_or_prune",
        f"- run267M_pool_wide_ablation_replacement_design(267M 후보군 전체 제거/대체 설계): `{rel(REPORT_PATH)}`",
    )
    text = replace_tail_from_marker(
        text,
        "Run267I(267I 실행)는",
        (
            "Run267I(267I 실행)는 P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화), MT5 execution(MT5 실행), MT5 review(MT5 검토)까지 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭), Monday(월요일), July(7월), chron_mid(중간 순서 구간) 약점이 남아 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
            "Run267L(267L 실행)는 retrained soft-context branch(재학습 부드러운 문맥 분기)를 standalone candidate(독립 후보)가 아니라 salvage clue(회수 단서)로 가지치기했다.\n"
            "Effect(효과): selected candidate(선택 후보)는 없고, 후보군 전체 설계로 되돌아갔다.\n\n"
            "Run267M(267M 실행)는 다섯 Baseline candidates(기준 후보) 전체의 ablation/replacement(제거/대체), weak-slice matrix(약한 구간 행렬), P0 materialization queue(P0 물질화 큐)를 설계했다.\n"
            f"Effect(효과): selected candidate(선택 후보)는 여전히 없고, next_action(다음 행동)은 `{NEXT_ACTION}`이다.\n"
        ),
    )
    write_md(REVIEW_INDEX_PATH, text)


def update_workspace_state() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = text.replace("current_run_id: run267L_stage267_retrained_soft_context_followup_or_prune_v1", f"current_run_id: {RUN_ID}", 1)
    new_focus = (
        "current_focus:\n"
        "- >-\n"
        f"  Stage267(267단계) run267M(267M 실행) pool-wide ablation/replacement design(후보군 전체 제거/대체 설계) `{STATUS}`. Effect(효과): 다섯 Baseline candidates(기준 후보) 전체의 weak-slice matrix(약한 구간 행렬), ablation/replacement matrix(제거/대체 행렬), P0 materialization queue(P0 물질화 큐)를 만들었고 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다."
    )
    if f"`{STATUS}`" not in text:
        text = text.replace("current_focus:", new_focus, 1)
    text = text.replace(
        "  Next action(다음 행동)는 `run267M_design_pool_wide_ablation_replacement_and_weak_slice_matrix`이다. Effect(효과): 다섯 Baseline candidates(기준 후보) 전체의 ablation/replacement(제거/대체)와 weak-slice matrix(약한 구간 행렬)로 되돌아간다.",
        f"  Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): P0 ablation/replacement(우선 제거/대체) 변형을 물질화해 MT5(MetaTrader 5, 메타트레이더5) 실행 준비로 넘긴다.",
        1,
    )
    text = text.replace(
        "is active_run267L_retrained_soft_context_followup_or_prune_completed(267L 재학습 부드러운 문맥 후속/가지치기 완료 활성).",
        "is active_run267M_pool_wide_ablation_replacement_design_completed(267M 후보군 전체 제거/대체 설계 완료 활성).",
        1,
    )
    text = text.replace(f"  status: run267L_retrained_soft_context_followup_or_prune_completed", f"  status: {STATUS}", 1)
    text = text.replace("  current_run_id: run267L_stage267_retrained_soft_context_followup_or_prune_v1", f"  current_run_id: {RUN_ID}", 1)
    text = text.replace("  last_completed_run_id: run267L_stage267_retrained_soft_context_followup_or_prune_v1", f"  last_completed_run_id: {RUN_ID}", 1)
    text = append_after_contains(
        text,
        "run267L_retrained_soft_context_followup_or_prune_path",
        f"  run267M_pool_wide_ablation_replacement_design_path: {rel(REPORT_PATH)}",
    )
    text = text.replace("  next_action: run267M_design_pool_wide_ablation_replacement_and_weak_slice_matrix", f"  next_action: {NEXT_ACTION}", 1)
    write_md(WORKSPACE_STATE_PATH, text)


def update_docs() -> None:
    update_current_working_state()
    update_selection_status()
    update_review_index()
    update_workspace_state()


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_docs()
    print(
        json.dumps(
            {
                "status": STATUS,
                "candidate_count": len(result["candidate_context"]),
                "weak_slice_rows": len(result["weak_slice_matrix"]),
                "matrix_rows": len(result["ablation_replacement_matrix"]),
                "queue_rows": len(result["materialization_queue"]),
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
