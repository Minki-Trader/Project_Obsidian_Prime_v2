from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337 import execute_lifecycle_aware_mt5_runtime_probe_without_db as ce  # noqa: E402
from stage_pipelines.stage337 import train_lifecycle_aware_guarded_scouts_without_db as cd  # noqa: E402


aw = cd.aw
bg = cd.bg

TODAY = "2026-05-28"
STAGE_ID = cd.STAGE_ID
RUN_NUMBER = "run337CF"
RUN_ID = "run337CF_review_lifecycle_aware_runtime_probe_and_failure_attribution_without_db_v1"
PARENT_RUN_ID = ce.RUN_ID
NEXT_RUN_ID = "run337CG_design_directional_label_action_policy_repair_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CF_lifecycle_runtime_failure_attribution_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = cd.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = cd.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337CF_lifecycle_runtime_failure_attribution.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CF_lifecycle_runtime_failure_attribution.md"
SELECTED_STATUS = cd.SELECTED_STATUS
STAGE_BRIEF = cd.STAGE_BRIEF
WORKSPACE_STATE = cd.WORKSPACE_STATE
CURRENT_STATE = cd.CURRENT_STATE
CHANGELOG = cd.CHANGELOG
RUN_REGISTRY = cd.RUN_REGISTRY
ALPHA_LEDGER = cd.ALPHA_LEDGER
ARTIFACT_REGISTRY = cd.ARTIFACT_REGISTRY
STAGE_LEDGER = cd.STAGE_LEDGER

PARENT_FINAL = ce.FINAL_DECISION
CE_SUMMARY = ce.EXECUTION_SUMMARY
CE_DIFF = ce.PROXY_MT5_DIFF
CD_FINAL = cd.FINAL_DECISION
CD_LIFECYCLE = cd.LIFECYCLE_SCORECARD
CD_NEGATIVE = cd.NEGATIVE_CONTROL_RESULTS
CD_METRICS = cd.MODEL_METRICS
CD_SCORECARD = cd.DECISION_SCORECARD

RUNTIME_ATTRIBUTION = RUN_DIR / "runtime_parity_attribution.csv"
COST_FAILURE_ATTRIBUTION = RUN_DIR / "cost_direction_failure_attribution.csv"
SIGNAL_QUALITY_ATTRIBUTION = RUN_DIR / "signal_quality_attribution.csv"
NEXT_RESEARCH_QUEUE = RUN_DIR / "run337CG_directional_label_action_policy_repair_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    PARENT_FINAL,
    CE_SUMMARY,
    CE_DIFF,
    CD_FINAL,
    CD_LIFECYCLE,
    CD_NEGATIVE,
    CD_METRICS,
    CD_SCORECARD,
)
OUTPUT_FILES = (
    RUNTIME_ATTRIBUTION,
    COST_FAILURE_ATTRIBUTION,
    SIGNAL_QUALITY_ATTRIBUTION,
    NEXT_RESEARCH_QUEUE,
    EXPERIMENT_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    JUDGMENT_RECEIPT,
    ARTIFACT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

RUNTIME_COLUMNS = (
    "model_id",
    "feature_set_id",
    "runtime_completed",
    "matched_rows",
    "mismatch_rows",
    "max_abs_probability_diff",
    "feature_last_reached",
    "tester_gap_status",
    "mt5_trade_count",
    "mt5_net_profit",
    "mt5_profit_factor",
    "parity_attribution",
    "claim_boundary",
)
COST_COLUMNS = (
    "model_id",
    "feature_set_id",
    "model_family",
    "mt5_trade_count",
    "mt5_net_profit",
    "mt5_profit_factor",
    "lifecycle_closed_events",
    "lifecycle_net_cost1",
    "lifecycle_pf_cost1",
    "lifecycle_net_cost2",
    "cost2_guard_status",
    "direction_control_status",
    "oos_balanced_accuracy",
    "oos_macro_f1",
    "failure_driver",
    "attribution",
    "claim_boundary",
)
SIGNAL_COLUMNS = (
    "model_id",
    "split",
    "balanced_accuracy",
    "macro_f1",
    "log_loss",
    "pred_short",
    "pred_flat",
    "pred_long",
    "signal_quality_status",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "lane",
    "priority",
    "reason",
    "required_evidence",
    "forbidden_shortcut",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = cd.GATE_COLUMNS


def rel(path: Path | str) -> str:
    value = Path(path)
    try:
        return value.resolve().relative_to(ROOT.resolve()).as_posix()
    except (ValueError, RuntimeError):
        return value.as_posix()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_preserving(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_bytes(text.encode(encoding))
    return path


def as_float(value: Any) -> float:
    try:
        if value in (None, ""):
            return float("nan")
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def model_metrics_index(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    return {(row["model_id"], row["split"]): row for row in rows}


def control_index(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {row["model_id"]: row for row in rows if row.get("control_type") == "directionality_probe"}


def build_attribution_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    ce_summary = read_csv(CE_SUMMARY)
    lifecycle = {row["model_id"]: row for row in read_csv(CD_LIFECYCLE)}
    controls = control_index(read_csv(CD_NEGATIVE))
    metrics = model_metrics_index(read_csv(CD_METRICS))

    runtime_rows: list[dict[str, Any]] = []
    cost_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []

    for row in ce_summary:
        model_id = row["model_id"]
        mismatch_count = int(row.get("expected_missing_rows") or 0) + int(row.get("hash_mismatch_rows") or 0) + int(row.get("probability_mismatch_rows") or 0) + int(row.get("decision_mismatch_rows") or 0)
        feature_last = str(row.get("feature_last_reached", "")).lower() == "true"
        runtime_rows.append(
            {
                "model_id": model_id,
                "feature_set_id": row.get("feature_set_id", ""),
                "runtime_completed": str(row.get("runtime_status", "")) == "completed",
                "matched_rows": row.get("matched_rows", ""),
                "mismatch_rows": mismatch_count,
                "max_abs_probability_diff": row.get("max_abs_probability_diff", ""),
                "feature_last_reached": feature_last,
                "tester_gap_status": "tester_gap_remains" if not feature_last else "feature_last_reached",
                "mt5_trade_count": row.get("trade_count", ""),
                "mt5_net_profit": row.get("net_profit", ""),
                "mt5_profit_factor": row.get("profit_factor", ""),
                "parity_attribution": "runtime_parity_cleared_on_overlap_not_forward_authority" if mismatch_count == 0 else "runtime_mismatch_requires_repair",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        life = lifecycle.get(model_id, {})
        direction = controls.get(model_id, {})
        oos = metrics.get((model_id, "oos"), {})
        mt5_pf = as_float(row.get("profit_factor"))
        mt5_trades = as_float(row.get("trade_count"))
        model_family = "extratrees" if "extratrees" in model_id else "logreg"
        if direction.get("status") == "failed":
            driver = "directionality_inverted_or_non_signal"
        elif str(life.get("cost2_guard_status", "")).endswith("failed_guard"):
            driver = "cost_buffer_edge_missing"
        elif mt5_trades < 30:
            driver = "sparse_trade_shape_fragile"
        else:
            driver = "weak_edge_unexplained"
        if model_family == "extratrees" and mt5_trades < 30:
            driver = f"{driver}+sparse_nonlinear_shape"
        attribution = (
            "MT5 parity(런타임 동등성)는 맞지만 cost2 guard(비용2 가드), direction control(방향 대조), "
            "OOS score(OOS 점수)가 함께 약해 모델 신호 문제로 귀속한다."
        )
        cost_rows.append(
            {
                "model_id": model_id,
                "feature_set_id": row.get("feature_set_id", ""),
                "model_family": model_family,
                "mt5_trade_count": row.get("trade_count", ""),
                "mt5_net_profit": row.get("net_profit", ""),
                "mt5_profit_factor": mt5_pf,
                "lifecycle_closed_events": life.get("closed_trade_events", ""),
                "lifecycle_net_cost1": life.get("net_log_return_cost1", ""),
                "lifecycle_pf_cost1": life.get("profit_factor_cost1", ""),
                "lifecycle_net_cost2": life.get("net_log_return_cost2", ""),
                "cost2_guard_status": life.get("cost2_guard_status", ""),
                "direction_control_status": direction.get("status", "missing"),
                "oos_balanced_accuracy": oos.get("balanced_accuracy", ""),
                "oos_macro_f1": oos.get("macro_f1", ""),
                "failure_driver": driver,
                "attribution": attribution,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for row in read_csv(CD_METRICS):
        if row.get("split") not in {"validation", "oos"}:
            continue
        bal = as_float(row.get("balanced_accuracy"))
        status = "weak_signal_quality_below_random_like_threshold" if math.isfinite(bal) and bal < 0.50 else "signal_quality_watch"
        signal_rows.append(
            {
                "model_id": row.get("model_id", ""),
                "split": row.get("split", ""),
                "balanced_accuracy": row.get("balanced_accuracy", ""),
                "macro_f1": row.get("macro_f1", ""),
                "log_loss": row.get("log_loss", ""),
                "pred_short": row.get("pred_short", ""),
                "pred_flat": row.get("pred_flat", ""),
                "pred_long": row.get("pred_long", ""),
                "signal_quality_status": status,
                "effect": "score quality(점수 품질)가 약하면 fixed threshold(고정 임계값) 아래에서도 방향/비용 버퍼가 살아남기 어렵다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return runtime_rows, cost_rows, signal_rows


def build_next_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337CG_directional_label_action_policy_repair_design",
            "next_run_id": NEXT_RUN_ID,
            "lane": "no_overfit_repair_design",
            "priority": "P0",
            "reason": "runtime parity cleared on overlap, but all CD models failed cost2 guard and direction controls",
            "required_evidence": "historical-only label/action design, negative controls, WFO or rolling split plan, proxy-MT5 parity requirement",
            "forbidden_shortcut": "no forward threshold tuning, no lot optimization, no candidate selection from failed proxy",
            "effect": "다음 수리는 방향 라벨/행동 정책을 고치되 전진 데이터 과적합을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CG_tester_gap_boundary_kept",
            "next_run_id": NEXT_RUN_ID,
            "lane": "runtime_boundary_guard",
            "priority": "P1",
            "reason": "feature_last_reached_rows stayed 0/6, so forward pass/fail remains unavailable",
            "required_evidence": "completed-day or shifted custom visibility policy before any forward decision",
            "forbidden_shortcut": "do not call overlap parity runtime authority",
            "effect": "테스터 공백을 성공으로 포장하지 않고 claim boundary(주장 경계)에 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def classify(parent: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    if parent.get("next_action") != RUN_ID:
        return (
            "blocked_stage337CF_parent_transition_mismatch",
            "parent_does_not_open_cf",
            "stage337CF_blocked_parent_transition_repair",
            RUN_ID,
        )
    mismatches = sum(int(row.get("mismatch_rows") or 0) for row in runtime_rows)
    all_cost_failed = all(str(row.get("cost2_guard_status", "")).endswith("failed_guard") for row in cost_rows)
    direction_failed = sum(1 for row in cost_rows if row.get("direction_control_status") == "failed")
    if mismatches == 0 and all_cost_failed and direction_failed >= len(cost_rows):
        return (
            "completed_stage337CF_runtime_parity_cleared_cost_direction_failure_attributed_no_selection",
            "runtime_parity_cleared_cost2_and_direction_signal_failure_confirmed_repair_design_next",
            "stage337CF_open_run337CG_directional_label_action_policy_repair_design",
            NEXT_RUN_ID,
        )
    return (
        "completed_stage337CF_runtime_failure_attribution_inconclusive_no_selection",
        "runtime_cost_direction_failure_partially_attributed_more_diagnostics_required",
        "stage337CF_open_run337CG_repair_design_with_extra_diagnostics",
        NEXT_RUN_ID,
    )


def build_gates(parent: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]], signal_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    def row(gate_id: str, passed: bool, observed: str, expected: str, effect: str) -> dict[str, Any]:
        return {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    mismatches = sum(int(item.get("mismatch_rows") or 0) for item in runtime_rows)
    cost_failed = sum(1 for item in cost_rows if str(item.get("cost2_guard_status", "")).endswith("failed_guard"))
    direction_failed = sum(1 for item in cost_rows if item.get("direction_control_status") == "failed")
    return [
        row("cf_gate_parent_ce_loaded", parent.get("next_action") == RUN_ID, str(parent.get("next_action")), RUN_ID, "CE가 CF 리뷰를 열었는지 확인한다."),
        row("cf_gate_runtime_rows_loaded", len(runtime_rows) == 6, f"runtime_rows={len(runtime_rows)}", "6 runtime rows", "6개 CD ONNX(온엑스)의 런타임 결과가 모두 있는지 확인한다."),
        row("cf_gate_runtime_mismatch_zero", mismatches == 0, f"mismatches={mismatches}", "zero mismatches", "실패 원인이 런타임 불일치가 아님을 분리한다."),
        row("cf_gate_cost2_failure_named", cost_failed == len(cost_rows) and bool(cost_rows), f"failed={cost_failed}/{len(cost_rows)}", "all cost2 guards failed", "비용2 실패를 숨기지 않고 다음 수리 원인으로 기록한다."),
        row("cf_gate_direction_failure_named", direction_failed == len(cost_rows) and bool(cost_rows), f"failed={direction_failed}/{len(cost_rows)}", "all direction controls failed", "방향 신호가 뒤집히거나 약한 문제를 명시한다."),
        row("cf_gate_signal_quality_rows_loaded", len(signal_rows) == 12, f"signal_rows={len(signal_rows)}", "validation/oos rows for 6 models", "모델 점수 품질을 비용/방향 실패와 연결한다."),
        row("cf_gate_next_queue_created", True, NEXT_RUN_ID, "next repair design queued", "다음 실험을 수리 설계로 제한한다."),
        row("cf_gate_no_forward_or_goal_claim", True, "Forward/Goal not_claimed", "no forbidden claim", "리뷰 결과를 운영 주장으로 키우지 않는다."),
    ]


def write_report(final: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]]) -> Path:
    runtime_lines = "\n".join(
        f"| `{row['model_id']}` | {row['matched_rows']} | {row['mismatch_rows']} | `{row['tester_gap_status']}` | {row['mt5_trade_count']} | {row['mt5_net_profit']} | {row['mt5_profit_factor']} |"
        for row in runtime_rows
    )
    cost_lines = "\n".join(
        f"| `{row['model_id']}` | `{row['model_family']}` | {row['lifecycle_net_cost1']} | {row['lifecycle_pf_cost1']} | `{row['direction_control_status']}` | `{row['failure_driver']}` |"
        for row in cost_rows
    )
    return write_md(
        REPORT_PATH,
        f"""# Stage337 run337CF Lifecycle Runtime Failure Attribution(생애주기 런타임 실패 귀속)

## Conclusion(결론)

run337CF(337CF 실행)는 run337CE(337CE 실행)의 proxy-MT5 parity(프록시-MT5 동등성) 성공과 run337CD(337CD 실행)의 cost2/direction failure(비용2/방향 실패)를 분리했다.

Effect(효과): 런타임이 틀려서 진 것이 아니라, fixed threshold(고정 임계값) 아래에서 label/action signal(라벨/행동 신호)이 비용과 방향을 이기지 못한 것으로 귀속한다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- runtime_mismatch_rows(런타임 불일치 행): `{final['runtime_mismatch_rows']}`
- cost2_failed_models(비용2 실패 모델): `{final['cost2_failed_models']}/{final['model_rows']}`
- direction_failed_models(방향 실패 모델): `{final['direction_failed_models']}/{final['model_rows']}`
- feature_last_reached_rows(피처 끝 도달 행): `{final['feature_last_reached_rows']}`

## Runtime Attribution(런타임 귀속)

| model(모델) | matched(일치) | mismatch(불일치) | tester gap(테스터 공백) | MT5 trades(MT5 거래) | MT5 net(MT5 순익) | MT5 PF(MT5 수익 팩터) |
|---|---:|---:|---|---:|---:|---:|
{runtime_lines}

## Cost/Direction Attribution(비용/방향 귀속)

| model(모델) | family(계열) | lifecycle net cost1(생애주기 비용1 순익) | PF cost1(PF 비용1) | direction control(방향 대조) | driver(원인) |
|---|---|---:|---:|---|---|
{cost_lines}

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    return write_md(
        DECISION_DOC,
        f"""# Decision: Stage337 run337CF Failure Attribution(결정: 실패 귀속)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`

Effect(효과): 다음 run337CG(337CG 실행)는 directional label/action policy repair design(방향 라벨/행동 정책 수리 설계)로 제한한다. 전진 데이터 threshold tuning(전진 데이터 임계값 조정), lot optimization(로트 최적화), candidate selection(후보 선택)은 금지 상태다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "hypothesis": "CE cleared runtime parity on overlap, so CD failure should be attributed to signal/cost/action shape before repair design.",
                "controls": "no model training, no threshold tuning, no candidate selection",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "observed_change": "CD cost2-aware models matched MT5 telemetry but stayed net negative and PF below 1.",
                "comparison_baseline": "run337CD lifecycle proxy and run337CE MT5 runtime probe",
                "likely_drivers": ["directionality control failed", "cost buffer edge missing", "OOS balanced accuracy below 0.5", "sparse ExtraTrees trade shape"],
                "segment_checks": "runtime overlap, feature family, model family, direction negative control, validation/oos score rows",
                "trade_shape": rel(COST_FAILURE_ATTRIBUTION),
                "alternative_explanations": "tester feature-last gap still blocks forward pass/fail; account PnL units differ from proxy log returns",
                "attribution_confidence": "medium",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": rel(CD_FINAL),
                "runtime_path": rel(PARENT_FINAL),
                "shared_contract": "CE proxy-MT5 exact row comparison",
                "known_differences": "feature_last gap remains",
                "parity_check": rel(RUNTIME_ATTRIBUTION),
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            FORENSICS_RECEIPT,
            {
                "tester_identity": "inherited from run337CE",
                "trade_evidence": rel(CE_SUMMARY),
                "cost_assumptions": "MT5 broker tester native costs plus CD proxy cost stress",
                "backtest_judgment": "usable_with_boundary_for_attribution_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(REPORT_PATH), rel(RUNTIME_ATTRIBUTION), rel(COST_FAILURE_ATTRIBUTION), rel(SIGNAL_QUALITY_ATTRIBUTION)],
                "evidence_missing": "valid forward pass/fail, operating review, runtime authority",
                "judgment_label": final["judgment"],
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": final["next_action"],
                "user_explanation_hook": "동등성 문제는 줄었고, 이제 신호/방향/비용 구조를 고쳐야 한다.",
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "artifact_paths": [rel(path) for path in OUTPUT_FILES if path_exists(path)],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", final["next_action"])
    workspace = bg.replace_top_value(workspace, "updated_on: ", f"'{TODAY}'")
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337CF focus complete: lifecycle runtime failure attribution(생애주기 런타임 실패 귀속)을 `{final['status']}`로 닫았다. "
        "Effect(효과): directional label/action policy repair design(방향 라벨/행동 정책 수리 설계)을 run337CG(337CG 실행)로 연다.\n"
    )
    if "Stage337 run337CF focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current = current_text
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = cd.replace_bullet_value(current, field_name, value)
    entry = f"""
## Stage337 run337CF(337CF 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): runtime parity(런타임 동등성)는 겹친 구간에서 통과했고, cost/direction failure(비용/방향 실패)를 모델 신호 문제로 귀속했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337CF(337CF 실행)" not in current:
        marker = "## Stage337 run337CE(337CE"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(write_text_preserving(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- actual_mt5_execution(실제 MT5 실행): `reviewed_run337CE_attempted_strategy_tester`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): 다음은 directional label/action policy repair design(방향 라벨/행동 정책 수리 설계)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337CF(337CF 실행) reviewed lifecycle runtime failure attribution(생애주기 런타임 실패 귀속). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337CF reviewed lifecycle runtime failure attribution(생애주기 런타임 실패 귀속) and opened `{final['next_action']}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(write_text_preserving(CHANGELOG, changelog_bom and changelog_text or changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "lifecycle_runtime_failure_attribution_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_parity_performance_attribution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__lifecycle_runtime_failure_attribution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "lifecycle_runtime_failure_attribution",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_cost_direction_attribution",
        "tier_scope": "Tier A runtime probe attribution; no forward decision",
        "kpi_scope": "runtime_parity_cost2_direction_signal_quality",
        "scoreboard_lane": "failure_attribution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"runtime_mismatch_rows={final['runtime_mismatch_rows']};cost2_failed={final['cost2_failed_models']}",
        "guardrail_kpi": "Forward/Goal not_claimed; tester gap remains",
        "external_verification_status": "completed_run337CE_runtime_probe_reviewed_with_boundary",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__lifecycle_runtime_failure_attribution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_performance_attribution",
        "evidence_scope": "CE MT5 runtime probe, CD lifecycle scorecard, CD negative controls, CD metrics",
        "kpi_scope": "runtime_parity_cost_direction_failure",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"direction_failed={final['direction_failed_models']};signal_quality_rows={final['signal_quality_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__lifecycle_runtime_failure_attribution",
        "family": "runtime_parity_performance_attribution",
        "question": "what explains CD lifecycle-aware ONNX failure after MT5 parity cleared",
        "metric_scope": "runtime_parity_cost_direction_signal_quality",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    artifacts = [
        aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]
    artifact_columns, existing_rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    generated = now_utc()
    new_rows: list[dict[str, Any]] = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": mt5.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    merged = [row for row in existing_rows if row.get("artifact_id") not in keys]
    merged.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, merged))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    parent = read_json(PARENT_FINAL)
    runtime_rows, cost_rows, signal_rows = build_attribution_rows()
    status, judgment, decision, next_action = classify(parent, runtime_rows, cost_rows)
    queue_rows = build_next_queue()
    gates = build_gates(parent, runtime_rows, cost_rows, signal_rows)
    runtime_mismatches = sum(int(row.get("mismatch_rows") or 0) for row in runtime_rows)
    cost2_failed = sum(1 for row in cost_rows if str(row.get("cost2_guard_status", "")).endswith("failed_guard"))
    direction_failed = sum(1 for row in cost_rows if row.get("direction_control_status") == "failed")
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "model_rows": len(cost_rows),
        "runtime_rows": len(runtime_rows),
        "runtime_mismatch_rows": runtime_mismatches,
        "cost2_failed_models": cost2_failed,
        "direction_failed_models": direction_failed,
        "signal_quality_rows": len(signal_rows),
        "feature_last_reached_rows": sum(1 for row in runtime_rows if str(row.get("feature_last_reached")).lower() == "true"),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_rows": len(gates),
        "passed_gates": sum(1 for row in gates if row["status"] == "passed"),
        "failed_gates": [row["gate_id"] for row in gates if row["status"] != "passed"],
    }
    artifacts: list[Path] = [
        write_csv(RUNTIME_ATTRIBUTION, RUNTIME_COLUMNS, runtime_rows),
        write_csv(COST_FAILURE_ATTRIBUTION, COST_COLUMNS, cost_rows),
        write_csv(SIGNAL_QUALITY_ATTRIBUTION, SIGNAL_COLUMNS, signal_rows),
        write_csv(NEXT_RESEARCH_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(build_receipts(final))
    artifacts.append(write_report(final, runtime_rows, cost_rows))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final, artifacts))

    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
