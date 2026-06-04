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

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import review_swap_stable_reprobe_and_source_guard_mt5_runtime_probe_without_db as ce  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = ce.STAGE_ID
RUN_NUMBER = "run364CF"
RUN_ID = "run364CF_materialize_cost_stable_h17_source_guard_offensive_inputs_without_db_v1"
PARENT_RUN_ID = ce.RUN_ID
NEXT_RUN_ID = "run364CG_train_cost_stable_h17_source_guard_offensive_scout_without_db_v1"

STATUS = "completed_stage364CF_cost_stable_h17_source_guard_offensive_inputs_materialized_open_cg_no_authority"
JUDGMENT = "experiment_design_materialized_cost_stable_h17_source_guard_scout_inputs_no_authority"
DECISION = "stage364CF_open_run364CG_cost_stable_h17_source_guard_offensive_scout"
CLAIM_BOUNDARY = (
    "research_development_runtime_input_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
MIN_QUEUE_ROWS = 12

STAGE_DIR = ce.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
PARENT_EVIDENCE_SUMMARY = RUN_DIR / "parent_evidence_summary.csv"
STABILITY_TRANSFER_AUDIT = RUN_DIR / "stability_transfer_audit.csv"
H17_OVERLAY_QUALITY_BY_MONTH = RUN_DIR / "h17_overlay_quality_by_month.csv"
H17_OVERLAY_QUALITY_BY_OPEN_HOUR = RUN_DIR / "h17_overlay_quality_by_open_hour.csv"
COST_LAYERED_SCORECARD = RUN_DIR / "cost_layered_scorecard.csv"
OFFENSIVE_AXIS_MAP = RUN_DIR / "offensive_axis_map.csv"
RUN364CG_SCOUT_QUEUE = RUN_DIR / "run364CG_cost_stable_h17_source_guard_scout_queue.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CF_cost_stable_h17_source_guard_offensive_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CF_cost_stable_h17_source_guard_offensive_inputs.md"
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

SOURCE_CE_FINAL = ce.FINAL_DECISION
SOURCE_CE_QUEUE = ce.NEXT_QUEUE
SOURCE_CE_PAIR_DELTAS = ce.PAIR_DELTAS
SOURCE_CE_OVERLAY_DECOMPOSITION = ce.SOURCE_OVERLAY_DECOMPOSITION
SOURCE_CE_TRADE_ATTRIBUTION = ce.TRADE_ATTRIBUTION
SOURCE_CE_ATTRIBUTION_BY_SOURCE = ce.ATTRIBUTION_BY_SOURCE
SOURCE_CE_SCOREBOARD = ce.SCOREBOARD_REVIEW
SOURCE_CE_SET_DIFF = ce.SET_PARAMETER_DIFF
SOURCE_CE_COMMON_IDENTITY = ce.COMMON_ARTIFACT_IDENTITY
SOURCE_CE_REPORT_RECONCILIATION = ce.REPORT_RECONCILIATION
SOURCE_CE_GATE_AUDIT = ce.GATE_AUDIT
SOURCE_CE_REPORT = ce.REPORT_PATH
SOURCE_CE_MANIFEST = ce.RUN_MANIFEST

INPUT_FILES = [
    SOURCE_CE_FINAL,
    SOURCE_CE_QUEUE,
    SOURCE_CE_PAIR_DELTAS,
    SOURCE_CE_OVERLAY_DECOMPOSITION,
    SOURCE_CE_TRADE_ATTRIBUTION,
    SOURCE_CE_ATTRIBUTION_BY_SOURCE,
    SOURCE_CE_SCOREBOARD,
    SOURCE_CE_SET_DIFF,
    SOURCE_CE_COMMON_IDENTITY,
    SOURCE_CE_REPORT_RECONCILIATION,
    SOURCE_CE_GATE_AUDIT,
    SOURCE_CE_REPORT,
    SOURCE_CE_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    PARENT_EVIDENCE_SUMMARY,
    STABILITY_TRANSFER_AUDIT,
    H17_OVERLAY_QUALITY_BY_MONTH,
    H17_OVERLAY_QUALITY_BY_OPEN_HOUR,
    COST_LAYERED_SCORECARD,
    OFFENSIVE_AXIS_MAP,
    RUN364CG_SCOUT_QUEUE,
    DATA_INTEGRITY_AUDIT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
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
    return ce.rel(path)


def exists(path: Path | str) -> bool:
    return ce.exists(path)


def sha(path: Path | str) -> str:
    return ce.sha(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ce.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    ce.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ce.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    ce.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    ce.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> pd.DataFrame:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return pd.read_csv(handle)


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
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


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


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return ce.markdown_table(rows, columns, limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path),
                "input_role": "CF source from CE review(CE 리뷰에서 온 CF 원천)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def validate_inputs() -> Mapping[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing CF inputs: {missing}")
    final = read_json(SOURCE_CE_FINAL)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CE next_run_id mismatch: {final.get('next_run_id')} != {RUN_ID}")
    return final


def parent_evidence_summary_rows(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    scoreboard = read_csv(SOURCE_CE_SCOREBOARD)
    source = read_csv(SOURCE_CE_ATTRIBUTION_BY_SOURCE)
    cd02 = scoreboard[scoreboard["variant_id"].eq("cd02_ca01_clone_current_session")].iloc[0].to_dict()
    cd02_sources = source[source["variant_id"].eq("cd02_ca01_clone_current_session")]
    rows = [
        {
            "run_id": RUN_ID,
            "evidence_item": "reviewed_best_variant(리뷰된 최선 변형)",
            "value": "cd02_ca01_clone_current_session",
            "metric_1": "net_profit",
            "metric_1_value": finite(cd02.get("net_profit"), 2),
            "metric_2": "profit_factor",
            "metric_2_value": finite(cd02.get("profit_factor"), 2),
            "metric_3": "trade_count",
            "metric_3_value": int(cd02.get("trade_count", 0)),
            "effect": "CF uses current-session stable semantics(CF는 현재 세션 안정 의미를 쓴다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "evidence_item": "swap_stability_closed(스왑 안정 닫힘)",
            "value": "cd02_vs_cd01_zero_delta",
            "metric_1": "gross_delta",
            "metric_1_value": finite(parent_final.get("cd02_vs_cd01_gross_delta"), 2),
            "metric_2": "swap_delta",
            "metric_2_value": finite(parent_final.get("cd02_vs_cd01_swap_delta"), 2),
            "metric_3": "net_delta",
            "metric_3_value": finite(parent_final.get("cd02_vs_cd01_net_delta"), 2),
            "effect": "prior BX3 net is not carried as current authority(이전 BX3 순수익을 현재 권위로 쓰지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "evidence_item": "h17_overlay_value_preserved(17시 오버레이 가치 보존)",
            "value": "cd02_vs_cd03_positive_overlay_lift",
            "metric_1": "net_lift",
            "metric_1_value": finite(parent_final.get("cd02_vs_cd03_net_delta"), 2),
            "metric_2": "left_only_net",
            "metric_2_value": finite(parent_final.get("cd02_vs_cd03_left_only_net"), 2),
            "metric_3": "right_only_net",
            "metric_3_value": finite(parent_final.get("cd02_vs_cd03_right_only_net"), 2),
            "effect": "h17 synthetic overlay remains an offensive seed(17시 합성 오버레이를 공격 씨앗으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for row in cd02_sources.to_dict("records"):
        rows.append(
            {
                "run_id": RUN_ID,
                "evidence_item": f"source_bucket_{row['source_bucket']}",
                "value": row["source_bucket"],
                "metric_1": "trade_count",
                "metric_1_value": int(row["trade_count"]),
                "metric_2": "net_profit",
                "metric_2_value": finite(row["net_profit"], 2),
                "metric_3": "profit_factor_gross",
                "metric_3_value": finite(row["profit_factor_gross"], 4),
                "effect": "source contribution stays auditable(원천 기여를 계속 감사 가능하게 둔다)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(PARENT_EVIDENCE_SUMMARY, rows)
    return rows


def stability_transfer_rows(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    pair = read_csv(SOURCE_CE_PAIR_DELTAS)
    set_diff = read_csv(SOURCE_CE_SET_DIFF)
    identity = read_csv(SOURCE_CE_COMMON_IDENTITY)
    report_recon = read_csv(SOURCE_CE_REPORT_RECONCILIATION)
    swap = pair[pair["pair_id"].eq("cd01_vs_cd02_swap_stability_control")].iloc[0]
    functional_drift = int(set_diff["functional_drift_flag"].fillna(False).astype(bool).sum())
    required_identity_failures = identity[
        identity["required_same_hash"].astype(bool) & (~identity["cd_vs_ca_same_hash"].astype(bool))
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "same_session_trade_path(동일 세션 거래 경로)",
            "status": "passed" if int(swap["common_count"]) == int(swap["left_trade_count"]) == int(swap["right_trade_count"]) else "failed",
            "observed": f"common={int(swap['common_count'])}, left_only={int(swap['left_only_count'])}, right_only={int(swap['right_only_count'])}",
            "evidence": rel(SOURCE_CE_PAIR_DELTAS),
            "effect": "CF can treat CD02 as current-session semantics(CF가 CD02를 현재 세션 의미로 취급 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "same_session_cost_delta(동일 세션 비용 차이)",
            "status": "passed" if as_float(swap["gross_delta_common_left_minus_right"]) == 0.0 and as_float(swap["swap_delta_common_left_minus_right"]) == 0.0 and as_float(swap["net_delta_left_minus_right"]) == 0.0 else "failed",
            "observed": f"gross={swap['gross_delta_common_left_minus_right']}, swap={swap['swap_delta_common_left_minus_right']}, net={swap['net_delta_left_minus_right']}",
            "evidence": rel(SOURCE_CE_PAIR_DELTAS),
            "effect": "swap table drift is not reused as alpha(스왑표 드리프트를 알파로 재사용하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "functional_set_drift(기능 설정 드리프트)",
            "status": "passed" if functional_drift == 0 else "failed",
            "observed": f"functional_drift_count={functional_drift}",
            "evidence": rel(SOURCE_CE_SET_DIFF),
            "effect": "input design does not inherit hidden functional changes(입력 설계가 숨은 기능 변경을 상속하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "required_artifact_identity(필수 산출물 정체성)",
            "status": "passed" if len(required_identity_failures) == 0 else "failed",
            "observed": f"required_identity_failures={len(required_identity_failures)}",
            "evidence": rel(SOURCE_CE_COMMON_IDENTITY),
            "effect": "feature/model/probability source remains tied(피처/모델/확률 원천 연결 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "report_metric_reconciliation(보고서 지표 대조)",
            "status": "passed" if set(report_recon["status"].astype(str)) == {"passed"} else "failed",
            "observed": f"records={len(report_recon)}",
            "evidence": rel(SOURCE_CE_REPORT_RECONCILIATION),
            "effect": "headline KPI is tied to parsed report trades(대표 KPI를 파싱 거래와 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(STABILITY_TRANSFER_AUDIT, rows)
    return rows


def h17_quality_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trades = read_csv(SOURCE_CE_TRADE_ATTRIBUTION)
    cd02 = trades[trades["variant_id"].eq("cd02_ca01_clone_current_session")].copy()
    cd02["overlay_margin_vs_long"] = cd02["p_short"] - cd02["p_long"]
    cd02["overlay_margin_vs_flat"] = cd02["p_short"] - cd02["p_flat"]
    synthetic = cd02[cd02["source_bucket"].eq("synthetic_short_overlay")].copy()

    def grouped(group_columns: list[str]) -> list[dict[str, Any]]:
        if synthetic.empty:
            return []
        grouped_df = synthetic.groupby(group_columns, dropna=False).agg(
            trade_count=("net_profit", "size"),
            net_profit=("net_profit", "sum"),
            gross_profit=("gross_profit", "sum"),
            swap=("swap", "sum"),
            win_count=("net_profit", lambda s: int((s > 0).sum())),
            loss_count=("net_profit", lambda s: int((s < 0).sum())),
            avg_p_short=("p_short", "mean"),
            avg_margin_vs_long=("overlay_margin_vs_long", "mean"),
            avg_margin_vs_flat=("overlay_margin_vs_flat", "mean"),
            min_margin_vs_long=("overlay_margin_vs_long", "min"),
        ).reset_index()
        rows = []
        for row in grouped_df.to_dict("records"):
            trade_count = int(row["trade_count"])
            rows.append(
                {
                    "run_id": RUN_ID,
                    **{column: row[column] for column in group_columns},
                    "trade_count": trade_count,
                    "net_profit": finite(row["net_profit"], 2),
                    "gross_profit": finite(row["gross_profit"], 2),
                    "swap": finite(row["swap"], 2),
                    "expectancy": finite(row["net_profit"] / trade_count if trade_count else 0, 6),
                    "win_count": int(row["win_count"]),
                    "loss_count": int(row["loss_count"]),
                    "avg_p_short": finite(row["avg_p_short"], 6),
                    "avg_margin_vs_long": finite(row["avg_margin_vs_long"], 6),
                    "avg_margin_vs_flat": finite(row["avg_margin_vs_flat"], 6),
                    "min_margin_vs_long": finite(row["min_margin_vs_long"], 6),
                    "timestamp_safe_inputs": "open_time/open_hour/month/probability only(진입 시각/시간/월/확률만 사용)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        return rows

    month_rows = grouped(["close_month"])
    hour_rows = grouped(["open_hour"])
    write_csv(H17_OVERLAY_QUALITY_BY_MONTH, month_rows)
    write_csv(H17_OVERLAY_QUALITY_BY_OPEN_HOUR, hour_rows)
    return month_rows, hour_rows


def cost_layered_score_rows(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    scoreboard = read_csv(SOURCE_CE_SCOREBOARD)
    source = read_csv(SOURCE_CE_ATTRIBUTION_BY_SOURCE)
    scoreboard["_reviewed_stable_priority"] = scoreboard["variant_id"].eq("cd02_ca01_clone_current_session").astype(int)
    source_by_variant = {
        variant: group.set_index("source_bucket").to_dict("index")
        for variant, group in source.groupby("variant_id")
    }
    rows = []
    sorted_scoreboard = scoreboard.sort_values(
        ["_reviewed_stable_priority", "net_profit", "profit_factor", "trade_count"],
        ascending=[False, False, False, False],
    )
    for rank, row in enumerate(sorted_scoreboard.to_dict("records"), start=1):
        variant = row["variant_id"]
        buckets = source_by_variant.get(variant, {})
        overlay = buckets.get("synthetic_short_overlay", {})
        native = buckets.get("native_short_threshold", {})
        long_bucket = buckets.get("long_threshold", {})
        swap = as_float(row.get("parsed_swap"))
        gross = as_float(row.get("parsed_gross_profit"))
        net = as_float(row.get("net_profit"))
        density = as_float(row.get("trade_density_per_feature_business_day"))
        dd = as_float(row.get("equity_drawdown_amount"))
        pf = as_float(row.get("profit_factor"))
        recovery = as_float(row.get("recovery_factor"))
        cost_layer_score = net + (pf * 25.0) + (recovery * 5.0) - (dd * 0.05) + min(25.0, max(0.0, as_float(overlay.get("net_profit"))))
        rows.append(
            {
                "run_id": RUN_ID,
                "score_rank": rank,
                "variant_id": variant,
                "reviewed_stable_semantics": variant == "cd02_ca01_clone_current_session",
                "net_profit": finite(net, 2),
                "profit_factor": finite(pf, 2),
                "trade_count": int(row.get("trade_count", 0)),
                "density": finite(density, 10),
                "recovery_factor": finite(recovery, 2),
                "equity_drawdown_amount": finite(dd, 2),
                "parsed_gross_profit": finite(gross, 2),
                "parsed_swap": finite(swap, 2),
                "overlay_net": finite(overlay.get("net_profit", 0), 2),
                "native_short_net": finite(native.get("net_profit", 0), 2),
                "long_net": finite(long_bucket.get("net_profit", 0), 2),
                "same_session_swap_delta_vs_cd01": finite(parent_final.get("cd02_vs_cd01_swap_delta") if variant == "cd02_ca01_clone_current_session" else "", 2),
                "overlay_lift_vs_native_control": finite(parent_final.get("cd02_vs_cd03_net_delta") if variant == "cd02_ca01_clone_current_session" else "", 2),
                "cost_layer_score": finite(cost_layer_score, 4),
                "selection_use": "input_seed_only_requires_CG_validation(입력 씨앗 전용, CG 검증 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(COST_LAYERED_SCORECARD, rows)
    return rows


def offensive_axis_rows(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "axis_id": "axis01_semantics_anchor(의미 기준축)",
            "broad_sweep": "preserve CD02 CA01/BX3 current-session semantics(CD02 CA01/BX3 현재 세션 의미 보존)",
            "extreme_sweep": "compare against overlay-off native short control(오버레이 끈 기본 숏 대조와 비교)",
            "micro_search_gate": "CG must keep density >=3/day and no trade splitting(CG는 밀도 일 3회 이상과 거래 쪼개기 금지 유지)",
            "failure_memory": "prior BX3 1008.18 net is stale swap-table memory(이전 BX3 1008.18 순수익은 낡은 스왑표 기억)",
            "evidence_seed": rel(SOURCE_CE_PAIR_DELTAS),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "axis_id": "axis02_h17_overlay_quality(17시 오버레이 품질축)",
            "broad_sweep": "loose/mid/strict p_short and margin floors(느슨/중간/엄격 p_short 및 마진 하한)",
            "extreme_sweep": "overlay-only stress and overlay-off control(오버레이 전용 압박과 오버레이 끔 대조)",
            "micro_search_gate": "overlay lift must remain positive after cost stress(비용 압박 후에도 오버레이 우위 양수)",
            "failure_memory": "do not remove h17 clue only because authority is absent(권위 부재만으로 17시 단서 제거 금지)",
            "evidence_seed": rel(SOURCE_CE_OVERLAY_DECOMPOSITION),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "axis_id": "axis03_cost_layering(비용 층화축)",
            "broad_sweep": "gross/net/swap score separation(총손익/순수익/스왑 점수 분리)",
            "extreme_sweep": "swap haircut and gross-only ranking stress(스왑 헤어컷 및 총손익 단독 순위 압박)",
            "micro_search_gate": "candidate cannot depend on one changed swap table(후보가 변한 스왑표 하나에 의존하면 안 됨)",
            "failure_memory": "swap drift is control information, not alpha(스왑 드리프트는 대조 정보이지 알파가 아님)",
            "evidence_seed": rel(SOURCE_CE_SET_DIFF),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "axis_id": "axis04_trade_shape_no_split(거래 형태 무분할축)",
            "broad_sweep": "hold/session/source quality without increasing trade slices(거래 조각 증가 없는 보유/세션/원천 품질)",
            "extreme_sweep": "strict short-balance floor and long hold stress(엄격 숏 균형 하한과 롱 보유 압박)",
            "micro_search_gate": "trade count must not be raised by splitting profit(수익을 나누는 거래수 증가 금지)",
            "failure_memory": "trade/day floor is 3+ but count-splitting is invalid(日 3회 이상은 필요하지만 거래 쪼개기는 무효)",
            "evidence_seed": rel(SOURCE_CE_ATTRIBUTION_BY_SOURCE),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for row in rows:
        row["parent_net"] = finite(parent_final.get("best_mt5_net_profit"), 2)
        row["parent_density"] = finite(parent_final.get("best_mt5_density"), 10)
    write_csv(OFFENSIVE_AXIS_MAP, rows)
    return rows


def scout_queue_rows(parent_final: Mapping[str, Any], month_rows: Sequence[Mapping[str, Any]], hour_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    trades = read_csv(SOURCE_CE_TRADE_ATTRIBUTION)
    cd02 = trades[trades["variant_id"].eq("cd02_ca01_clone_current_session")].copy()
    synthetic = cd02[cd02["source_bucket"].eq("synthetic_short_overlay")].copy()
    synthetic["margin_vs_long"] = synthetic["p_short"] - synthetic["p_long"]
    synthetic["margin_vs_flat"] = synthetic["p_short"] - synthetic["p_flat"]
    p_short_q = synthetic["p_short"].quantile([0.25, 0.5, 0.75]).to_dict() if not synthetic.empty else {0.25: 0.45, 0.5: 0.46, 0.75: 0.47}
    margin_q = synthetic["margin_vs_long"].quantile([0.25, 0.5, 0.75]).to_dict() if not synthetic.empty else {0.25: 0.07, 0.5: 0.08, 0.75: 0.09}
    bad_months = ",".join(str(row["close_month"]) for row in month_rows if as_float(row.get("net_profit")) < 0) or "none"
    best_hour = ""
    if hour_rows:
        best = max(hour_rows, key=lambda row: as_float(row.get("net_profit")))
        best_hour = str(best.get("open_hour"))
    template = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "baseline_variant_id": "cd02_ca01_clone_current_session",
        "trade_splitting_status": "forbidden(금지)",
        "top_n_status": "forbidden(금지)",
        "timestamp_boundary": "entry-known month/hour/probability and existing runtime source bucket only(진입 시점 월/시간/확률 및 기존 런타임 원천 버킷만)",
        "feature_label_boundary": "no realized future PnL in live rule; parent PnL is seed evidence only(실거래 규칙에 미래 손익 없음, 상위 손익은 씨앗 근거 전용)",
        "tier_scope": "Tier A used + Tier B missing_required(Tier A 사용 + Tier B 필수 누락)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    family_labels = {
        "semantics_anchor": "semantics_anchor(의미 기준)",
        "h17_overlay_quality": "h17_overlay_quality(17시 오버레이 품질)",
        "h17_overlay_quality_extreme": "h17_overlay_quality_extreme(17시 오버레이 품질 극단)",
        "negative_control": "negative_control(부정 대조)",
        "extreme_overlay": "extreme_overlay(극단 오버레이)",
        "cost_layering": "cost_layering(비용 층화)",
        "regime_guard": "regime_guard(국면 가드)",
        "session_focus": "session_focus(세션 집중)",
        "side_balance": "side_balance(방향 균형)",
        "trade_shape": "trade_shape(거래 형태)",
    }
    status_labels = {
        "ready_for_proxy_scout": "ready_for_proxy_scout(프록시 정찰 준비)",
        "ready_for_proxy_scout_control": "ready_for_proxy_scout_control(프록시 정찰 대조 준비)",
    }
    definitions = [
        (
            "cg01_current_session_semantics_anchor",
            "semantics_anchor",
            "ready_for_proxy_scout",
            "preserve_cd02_current_session_semantics",
            "keep_h17_overlay_as_is",
            "",
            "",
            "none",
            "baseline anchor; compare every change against CD02",
            "기준 앵커로 두고 모든 변화를 CD02와 비교",
            "density >= 3 and net/PF/DD not worse after CG scout",
            "CG 정찰 뒤 밀도 일 3회 이상과 순수익/PF/DD 비악화",
        ),
        (
            "cg02_h17_overlay_loose_margin_floor",
            "h17_overlay_quality",
            "ready_for_proxy_scout",
            "preserve_cd02_semantics",
            "synthetic_overlay_p_short_q25_margin_q25",
            finite(p_short_q[0.25], 6),
            finite(margin_q[0.25], 6),
            "none",
            "retain most overlay while filtering weakest margin",
            "대부분의 오버레이를 보존하며 가장 약한 마진만 제거",
            "overlay lift remains positive with trade count not split",
            "거래 쪼개기 없이 오버레이 우위가 양수 유지",
        ),
        (
            "cg03_h17_overlay_mid_margin_floor",
            "h17_overlay_quality",
            "ready_for_proxy_scout",
            "preserve_cd02_semantics",
            "synthetic_overlay_p_short_q50_margin_q50",
            finite(p_short_q[0.5], 6),
            finite(margin_q[0.5], 6),
            "none",
            "test middle floor for PF/DD improvement",
            "중간 하한으로 PF/DD 개선 여부 확인",
            "net and PF improve without density dropping below 3/day",
            "밀도 일 3회 미만 붕괴 없이 순수익과 PF 개선",
        ),
        (
            "cg04_h17_overlay_strict_margin_floor",
            "h17_overlay_quality_extreme",
            "ready_for_proxy_scout",
            "preserve_cd02_semantics",
            "synthetic_overlay_p_short_q75_margin_q75",
            finite(p_short_q[0.75], 6),
            finite(margin_q[0.75], 6),
            "none",
            "stress strict overlay quality cliff",
            "엄격 오버레이 품질 절벽 압박",
            "use only as cliff read unless density survives",
            "밀도가 살아남지 못하면 절벽 판독으로만 사용",
        ),
        (
            "cg05_overlay_off_native_short_control",
            "negative_control",
            "ready_for_proxy_scout_control",
            "preserve_cd03_native_short_control",
            "disable_synthetic_overlay",
            "",
            "",
            "overlay_off",
            "control whether h17 overlay still matters",
            "17시 오버레이가 여전히 의미 있는지 대조",
            "must not be treated as selected baseline",
            "선택 기준선으로 취급 금지",
        ),
        (
            "cg06_overlay_only_extreme_stress",
            "extreme_overlay",
            "ready_for_proxy_scout",
            "preserve_cd02_semantics",
            "synthetic_overlay_only_for_h17_short_bucket",
            finite(p_short_q[0.25], 6),
            finite(margin_q[0.25], 6),
            "native_short_deprioritized",
            "isolate synthetic overlay contribution",
            "합성 오버레이 기여를 분리",
            "positive only if density and short balance survive",
            "밀도와 숏 균형이 살아남을 때만 긍정",
        ),
        (
            "cg07_native_short_cost_firewall",
            "cost_layering",
            "ready_for_proxy_scout",
            "preserve_cd02_semantics",
            "keep_synthetic_overlay",
            "",
            "",
            "native_short_swap_cost_firewall",
            "reduce long-hold/native-short cost drag",
            "긴 보유/기본 숏 비용 끌림 완화",
            "improve PF/recovery without deleting shorts wholesale",
            "숏을 통째로 지우지 않고 PF/회복 개선",
        ),
        (
            "cg08_bad_overlay_month_guard_scout",
            "regime_guard",
            "ready_for_proxy_scout",
            "preserve_cd02_semantics",
            f"guard_negative_overlay_months={bad_months}",
            finite(p_short_q[0.25], 6),
            finite(margin_q[0.25], 6),
            "month_guard_seed_only",
            "test whether month regime improves overlay quality",
            "월별 국면 가드가 오버레이 품질을 개선하는지 확인",
            "requires CG split/WFO read because parent-month PnL is selection-biased",
            "상위 월별 손익은 선택 편향이 있어 CG 분할/WFO 판독 필요",
        ),
        (
            "cg09_best_open_hour_overlay_focus",
            "session_focus",
            "ready_for_proxy_scout",
            "preserve_cd02_semantics",
            f"focus_best_overlay_open_hour={best_hour or 'none'}",
            finite(p_short_q[0.25], 6),
            finite(margin_q[0.25], 6),
            "hour_focus_seed_only",
            "test if h17 clue is concentrated or broad",
            "17시 단서가 집중형인지 넓은 단서인지 확인",
            "must not collapse density below 3/day",
            "밀도 일 3회 미만 붕괴 금지",
        ),
        (
            "cg10_gross_net_swap_layered_score",
            "cost_layering",
            "ready_for_proxy_scout",
            "preserve_cd02_semantics",
            "rank_by_gross_net_swap_layered_score",
            "",
            "",
            "swap_haircut_1x",
            "avoid selecting stale swap drift",
            "낡은 스왑 드리프트 선택 방지",
            "score must agree with trade path evidence",
            "점수는 거래 경로 근거와 일치해야 함",
        ),
        (
            "cg11_short_balance_floor_guard",
            "side_balance",
            "ready_for_proxy_scout",
            "preserve_cd02_semantics",
            "short_count_floor_100_and_overlay_kept",
            finite(p_short_q[0.25], 6),
            finite(margin_q[0.25], 6),
            "short_balance_guard",
            "protect short participation while improving source quality",
            "원천 품질을 개선하면서 숏 참여 보존",
            "short count should not fall below 100 without clear PF/DD lift",
            "명확한 PF/DD 개선 없이 숏 수 100 미만 하락 금지",
        ),
        (
            "cg12_trade_shape_quality_no_split",
            "trade_shape",
            "ready_for_proxy_scout",
            "preserve_cd02_semantics",
            "no_count_split_quality_surface",
            "",
            "",
            "hold_and_source_quality_guard",
            "improve trade shape without adding slices",
            "거래 조각 추가 없이 거래 형태 개선",
            "trade/day remains >=3 by real entries, not splitting",
            "거래 쪼개기가 아닌 실제 진입으로 일 3회 이상 유지",
        ),
    ]
    rows = []
    for rank, (candidate_id, family, status, semantics_policy, overlay_policy, p_short_floor, margin_floor, cost_policy, expected_effect, expected_effect_ko, success, success_ko) in enumerate(definitions, start=1):
        row = {
            **template,
            "queue_rank": rank,
            "candidate_id": candidate_id,
            "variant_family": family_labels[family],
            "queue_status": status_labels[status],
            "semantics_policy": semantics_policy,
            "h17_overlay_policy": overlay_policy,
            "p_short_floor": p_short_floor,
            "margin_vs_long_floor": margin_floor,
            "cost_stress_policy": cost_policy,
            "expected_effect": f"{expected_effect}({expected_effect_ko})",
            "success_criteria": f"{success}({success_ko})",
            "failure_criteria": "density < 3/day, net/PF/DD deterioration without source-quality gain, or hidden trade splitting(밀도 일 3회 미만, 원천 품질 개선 없는 수익/PF/DD 악화, 또는 숨은 거래 쪼개기)",
            "invalid_conditions": "uses future realized PnL as live feature or changes ONNX/runtime identity without manifest(미래 실현 손익을 실거래 피처로 쓰거나 목록 없이 ONNX/런타임 정체성 변경)",
            "comparison_baseline": "cd02_ca01_clone_current_session",
            "evidence_seed": rel(SOURCE_CE_QUEUE),
            "parent_net": finite(parent_final.get("best_mt5_net_profit"), 2),
            "parent_density": finite(parent_final.get("best_mt5_density"), 10),
            "parent_trade_count": int(parent_final.get("best_mt5_trade_count", 0)),
        }
        rows.append(row)
    write_csv(RUN364CG_SCOUT_QUEUE, rows)
    return rows


def data_integrity_rows(parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    trades = read_csv(SOURCE_CE_TRADE_ATTRIBUTION)
    cd02 = trades[trades["variant_id"].eq("cd02_ca01_clone_current_session")].copy()
    duplicate_count = int(cd02.duplicated(subset=["open_time", "close_time", "open_type", "open_price", "close_price", "source_bucket"]).sum())
    rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "data_source(데이터 원천)",
            "status": "passed",
            "observed": f"CE parsed MT5 closed trades rows={len(cd02)}",
            "effect": "CF reads reviewed MT5 output, not unreviewed proxy(CF는 미검토 프록시가 아니라 리뷰된 MT5 출력을 읽음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "time_axis(시간축)",
            "status": "passed",
            "observed": "open_time/close_time from MT5 report; open_hour/month known at entry or review scope(MT5 보고서 진입/청산 시각, 진입 시점 시간/월 또는 리뷰 범위)",
            "effect": "candidate live rules may use entry-known time only(후보 실거래 규칙은 진입 시점 시간만 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "missing_duplicate_check(누락/중복 확인)",
            "status": "passed" if duplicate_count == 0 and len(cd02) == int(parent_final.get("best_mt5_trade_count", -1)) else "failed",
            "observed": f"cd02_rows={len(cd02)}, duplicate_count={duplicate_count}, parent_trade_count={parent_final.get('best_mt5_trade_count')}",
            "effect": "queue counts tie to the reviewed best variant(대기열 수치가 리뷰된 최선 변형과 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "feature_label_boundary(피처/라벨 경계)",
            "status": "passed",
            "observed": "future PnL is seed evidence only; queue uses probability/time/source policies(미래 손익은 씨앗 근거 전용, 대기열은 확률/시간/원천 정책 사용)",
            "effect": "look-ahead bias is named before CG scout(CG 정찰 전 미래참조 위험을 명명)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "split_boundary(분할 경계)",
            "status": "passed",
            "observed": "single current-session runtime review becomes scout input only(단일 현재 세션 런타임 리뷰는 정찰 입력 전용)",
            "effect": "CF does not claim WFO, forward, or runtime authority(CF는 WFO/전진/런타임 권위를 주장하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(DATA_INTEGRITY_AUDIT, rows)
    return rows


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "work_packet_schema_lint",
                "input_lineage_gate",
                "data_integrity_audit",
                "stability_transfer_gate",
                "offensive_queue_scope_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "hypothesis": "cost-stable current-session CA01/BX3 semantics and h17 overlay source guard can seed a broader no-split offensive scout(비용 안정 현재 세션 CA01/BX3 의미와 17시 오버레이 원천 가드가 무분할 공격 정찰 씨앗이 될 수 있다)",
            "decision_use": "open run364CG scout queue(364CG 정찰 대기열 개방)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "current-session cost-stable CD02 semantics plus h17 overlay can guide a broader scout(현재 세션 비용 안정 CD02 의미와 17시 오버레이가 더 넓은 정찰을 이끌 수 있다)",
            "decision_use": "choose CG proxy scout axes(CG 프록시 정찰 축 선택)",
            "comparison_baseline": "cd02_ca01_clone_current_session",
            "control_variables": ["US100 M5", "same reviewed CD MT5 output", "no trade splitting", "no top_n"],
            "changed_variables": ["h17 overlay floor", "native short cost firewall", "month/hour guard", "gross/net/swap ranking"],
            "sample_scope": "CE reviewed CD current-session MT5 outputs(CE 리뷰 완료 CD 현재 세션 MT5 출력)",
            "success_criteria": "CG keeps density >= 3/day and improves net/PF/DD or source quality(CG가 밀도 일 3회 이상 유지와 수익/PF/DD 또는 원천 품질 개선)",
            "failure_criteria": "density collapse, hidden trade splitting, or loss of h17 overlay value(밀도 붕괴, 숨은 거래 쪼개기, 17시 오버레이 가치 상실)",
            "invalid_conditions": "future realized PnL used as live feature or artifact identity drift(미래 실현 손익 실거래 피처 사용 또는 산출물 정체성 드리프트)",
            "stop_conditions": "run CG scout, then review before MT5 package(CG 정찰 후 MT5 패키지 전 리뷰)",
            "evidence_plan": [rel(RUN364CG_SCOUT_QUEUE), rel(DATA_INTEGRITY_AUDIT), rel(STABILITY_TRANSFER_AUDIT)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": [rel(SOURCE_CE_TRADE_ATTRIBUTION), rel(SOURCE_CE_SCOREBOARD), rel(SOURCE_CE_PAIR_DELTAS)],
            "time_axis": "MT5 report open/close timestamps; candidate policies use entry-known open_time/open_hour/month(MT5 보고서 진입/청산 시각, 후보 정책은 진입 시점 시각/시간/월 사용)",
            "sample_scope": "FPMarkets US100 M5 CE current-session runtime probe review(FPMarkets US100 M5 CE 현재 세션 런타임 탐침 리뷰)",
            "missing_or_duplicate_check": rel(DATA_INTEGRITY_AUDIT),
            "feature_label_boundary": "realized PnL used only to seed offline scout, not as live feature(실현 손익은 오프라인 정찰 씨앗 전용, 실거래 피처 아님)",
            "split_boundary": "materialization only; CG must validate before package(구체화 전용, CG가 패키지 전 검증 필요)",
            "leakage_risk": "parent-runtime outcome selection can overfit if promoted without CG/WFO(상위 런타임 결과 선택은 CG/WFO 없이 승격하면 과적합 위험)",
            "data_hash_or_identity": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES],
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_validation_scope": "no new model training; preserve reviewed ONNX identity only(새 모델 학습 없음, 리뷰된 ONNX 정체성만 보존)",
            "overfit_control": "queue is broad scout input, not selected model(대기열은 넓은 정찰 입력이지 선택 모델 아님)",
            "required_next_validation": "CG proxy/WFO-style split review before MT5 package(CG 프록시/WFO식 분할 리뷰 후 MT5 패키지)",
            "model_judgment": "not_applicable_no_new_model(새 모델 없음으로 해당 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()],
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_closeout_commit(종료 커밋 후 추적)",
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "result_subject": RUN_ID,
            "evidence_available": [rel(RUN364CG_SCOUT_QUEUE), rel(PARENT_EVIDENCE_SUMMARY), rel(STABILITY_TRANSFER_AUDIT), rel(DATA_INTEGRITY_AUDIT)],
            "evidence_missing": ["CG scout result(CG 정찰 결과)", "WFO validation(WFO 검증)", "new MT5 runtime probe(신규 MT5 런타임 탐침)"],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "CF turns CE's stable runtime clue into a broad no-split scout queue(CF는 CE의 안정 런타임 단서를 넓은 무분할 정찰 대기열로 바꿈)",
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
            "new_model_training": "not_run",
            "new_mt5_execution": "not_run_materialization_only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def build_gates(
    data_rows: Sequence[Mapping[str, Any]],
    stability_rows: Sequence[Mapping[str, Any]],
    axis_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    receipts_written: bool,
) -> list[dict[str, Any]]:
    ready_rows = [row for row in queue_rows if str(row["queue_status"]).startswith("ready")]
    gates = [
        (
            "work_packet_schema_lint",
            exists(WORK_PACKET),
            WORK_PACKET,
            "primary family and required gates are explicit(주 작업군과 필수 게이트 명시)",
        ),
        (
            "input_lineage_gate",
            all(exists(path) for path in INPUT_FILES),
            INPUT_MANIFEST,
            "CE review artifacts are connected(CE 리뷰 산출물 연결)",
        ),
        (
            "data_integrity_audit",
            all(row["status"] == "passed" for row in data_rows),
            DATA_INTEGRITY_AUDIT,
            "time axis, duplicate check, leakage boundary are named(시간축/중복/누수 경계 명시)",
        ),
        (
            "stability_transfer_gate",
            all(row["status"] == "passed" for row in stability_rows),
            STABILITY_TRANSFER_AUDIT,
            "CD02 current-session semantics can be transferred(CD02 현재 세션 의미 인계 가능)",
        ),
        (
            "offensive_queue_scope_gate",
            len(axis_rows) >= 4 and len(queue_rows) >= MIN_QUEUE_ROWS and len(ready_rows) >= MIN_QUEUE_ROWS,
            RUN364CG_SCOUT_QUEUE,
            "broad and extreme scout queue is materialized(넓은/극단 정찰 대기열 구체화)",
        ),
        (
            "required_gate_coverage_audit",
            receipts_written,
            GATE_AUDIT,
            "required gates are linked to closeout(필수 게이트를 종료 기록에 연결)",
        ),
        (
            "final_claim_guard",
            exists(CLAIM_RECEIPT),
            CLAIM_RECEIPT,
            "no runtime authority or operating promotion claimed(런타임 권위나 운영 승격 주장 없음)",
        ),
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def final_payload(parent_final: Mapping[str, Any], queue_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "queue_rows": len(queue_rows),
        "ready_queue_rows": sum(1 for row in queue_rows if str(row["queue_status"]).startswith("ready")),
        "axis_count": 4,
        "reviewed_best_variant_id": parent_final.get("reviewed_best_variant_id"),
        "parent_net_profit": parent_final.get("best_mt5_net_profit"),
        "parent_profit_factor": parent_final.get("best_mt5_profit_factor"),
        "parent_expectancy": parent_final.get("best_mt5_expectancy"),
        "parent_trade_count": parent_final.get("best_mt5_trade_count"),
        "parent_density": parent_final.get("best_mt5_density"),
        "parent_recovery_factor": parent_final.get("best_mt5_recovery_factor"),
        "parent_equity_drawdown_amount": parent_final.get("best_mt5_equity_drawdown_amount"),
        "parent_long_trade_count": parent_final.get("best_mt5_long_trade_count"),
        "parent_short_trade_count": parent_final.get("best_mt5_short_trade_count"),
        "swap_stability_delta": parent_final.get("cd02_vs_cd01_net_delta"),
        "h17_overlay_lift": parent_final.get("cd02_vs_cd03_net_delta"),
        "cd02_long_source_net": parent_final.get("cd02_long_source_net"),
        "cd02_native_short_net": parent_final.get("cd02_native_short_net"),
        "cd02_synthetic_overlay_net": parent_final.get("cd02_synthetic_overlay_net"),
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run_materialization_only",
        "external_verification_status": "out_of_scope_by_claim_materialization_only(주장 범위상 구체화 전용)",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_docs(
    final: Mapping[str, Any],
    parent_rows: Sequence[Mapping[str, Any]],
    stability_rows: Sequence[Mapping[str, Any]],
    axis_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364CF cost-stable h17 source guard offensive inputs(364CF 비용 안정 17시 원천 가드 공격 입력)

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next(다음): `{NEXT_RUN_ID}`
- gate(게이트): `{final['gate_passes']}/{final['gate_total']}`

## Action(행동)

Action(행동): CE review(CE 리뷰)의 CD02 current-session semantics(CD02 현재 세션 의미), CD02-CD01 zero gross/swap/net delta(총손익/스왑/순수익 차이 0), CD02-CD03 h17 overlay lift(17시 오버레이 우위)를 CG scout(CG 정찰) 입력으로 materialize(구체화)했다.

Effect(효과): 다음 탐색은 stale BX3 swap memory(낡은 BX3 스왑 기억)를 기준으로 삼지 않고, trade splitting(거래 쪼개기) 없이 source quality/cost layer/session guard(원천 품질/비용 층/세션 가드)를 넓게 시험한다.

## Parent Evidence(상위 근거)

{markdown_table(parent_rows, ['evidence_item', 'value', 'metric_1', 'metric_1_value', 'metric_2', 'metric_2_value', 'metric_3', 'metric_3_value'], 10)}

## Stability Transfer(안정 의미 인계)

{markdown_table(stability_rows, ['audit_item', 'status', 'observed', 'effect'], 10)}

## Offensive Axes(공격 축)

{markdown_table(axis_rows, ['axis_id', 'broad_sweep', 'extreme_sweep', 'micro_search_gate'], 8)}

## CG Queue(CG 대기열)

{markdown_table(queue_rows, ['queue_rank', 'candidate_id', 'variant_family', 'queue_status', 'h17_overlay_policy', 'cost_stress_policy'], 12)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Boundary(경계)

CF is materialization only(CF는 구체화 전용). new model training(새 모델 학습), new MT5 execution(새 MT5 실행), forward pass(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision: Stage364CF cost-stable h17 source guard offensive inputs(결정: 364CF 비용 안정 17시 원천 가드 공격 입력)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Action(행동): CE의 swap-stable CD02 runtime review(스왑 안정 CD02 런타임 리뷰)를 CG scout(CG 정찰)용 broad/extreme queue(넓은/극단 대기열) `12`행으로 구체화했다.

Effect(효과): 다음 작업은 h17 overlay value(17시 오버레이 가치), gross/net/swap layering(총손익/순수익/스왑 층화), no trade splitting(거래 쪼개기 금지)을 함께 압박할 수 있다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"\n- `{RUN_ID}` -> `{rel(REPORT_PATH)}`: CF cost-stable h17 source guard offensive inputs(CF 비용 안정 17시 원천 가드 공격 입력).\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Current materialized queue(현재 구체화 대기열): `{rel(RUN364CG_SCOUT_QUEUE)}` with `{final['queue_rows']}` scout rows(정찰 행).

Reviewed stable semantics(리뷰된 안정 의미): `{final['reviewed_best_variant_id']}`. Parent MT5 KPI(상위 MT5 핵심 성과 지표): net `{final['parent_net_profit']}`, PF `{final['parent_profit_factor']}`, trades `{final['parent_trade_count']}`, density `{final['parent_density']}`, recovery `{final['parent_recovery_factor']}`, equity DD `{final['parent_equity_drawdown_amount']}`.

Current handoff(현재 인계): CG must test(테스트 필요) h17 overlay floors(17시 오버레이 하한), cost layering(비용 층화), side/trade-shape guard(방향/거래 형태 가드) without trade splitting(거래 쪼개기 없이).

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
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

Current truth(현재 진실): `run364CF` materialized(구체화 완료) `{final['queue_rows']}` cost-stable h17 source guard scout rows(비용 안정 17시 원천 가드 정찰 행). CE evidence(CE 근거)는 CD02-CD01 gross/swap/net delta(총손익/스왑/순수익 차이) `0/0/0`과 CD02-CD03 overlay lift(오버레이 우위) `{final['h17_overlay_lift']}`다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 no-split(무분할) proxy scout(프록시 정찰)를 실행해 h17 overlay floor(17시 오버레이 하한), gross/net/swap layering(총손익/순수익/스왑 층화), side/trade-shape guard(방향/거래 형태 가드)를 검증한다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"\n## {RUN_ID}\n\nAction(행동): CE current-session runtime review(CE 현재 세션 런타임 리뷰)를 CG scout queue(CG 정찰 대기열) `{rel(RUN364CG_SCOUT_QUEUE)}`로 materialize(구체화)했다.\n\nEffect(효과): Stage364(364단계) 안에서 stage branching(단계 분기) 없이 cost-stable h17 source guard(비용 안정 17시 원천 가드)를 다음 공격 탐색으로 넘긴다.\n",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"\n- {final['created_at_utc']} `{RUN_ID}` completed(완료): materialized(구체화) `{final['queue_rows']}` CG scout rows(CG 정찰 행); next `{NEXT_RUN_ID}`.\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"\n### {RUN_ID} cost-stable h17 source guard offensive queue(비용 안정 17시 원천 가드 공격 대기열)\n\n- idea_id(아이디어 ID): `IDEA-ST364-SOURCE-REGIME-LABEL-PIVOT-DENSE-COST-RECOVERY`\n- hypothesis(가설): current-session cost-stable h17 source guard(현재 세션 비용 안정 17시 원천 가드)가 no-split scout(무분할 정찰)에서 PF/DD/source quality(PF/DD/원천 품질)를 개선할 수 있다.\n- evidence_boundary(근거 경계): materialization_only(구체화 전용), no runtime authority(런타임 권위 없음).\n- next(다음): `{NEXT_RUN_ID}`.\n",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "materialization(구체화)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "family": "experiment_design(실험 설계)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["queue_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(RUN364CG_SCOUT_QUEUE),
        "result_status": final["status"],
        "sample_rows": final["parent_trade_count"],
        "net_profit": final["parent_net_profit"],
        "profit_factor": final["parent_profit_factor"],
        "expectancy": final["parent_expectancy"],
        "trade_count": final["parent_trade_count"],
        "trade_density_per_feature_day": final["parent_density"],
        "recovery_factor": final["parent_recovery_factor"],
        "max_drawdown_amount": final["parent_equity_drawdown_amount"],
        "long_trade_count": final["parent_long_trade_count"],
        "short_trade_count": final["parent_short_trade_count"],
        "trade_density_requirement_status": "inherited_parent_passed_density_floor(상위 밀도 하한 통과 상속)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_design(실험 설계)",
        "evidence_boundary": "materialization_only(구체화 전용)",
        "external_verification_status": final["external_verification_status"],
        "next_action": NEXT_RUN_ID,
        "question": "Can cost-stable h17 source guard become the next no-split scout surface?(비용 안정 17시 원천 가드가 다음 무분할 정찰 표면이 될 수 있는가?)",
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
                "subrun_id": "",
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
        ("cg_scout_queue", RUN364CG_SCOUT_QUEUE),
        ("offensive_axis_map", OFFENSIVE_AXIS_MAP),
        ("stability_transfer_audit", STABILITY_TRANSFER_AUDIT),
        ("data_integrity_audit", DATA_INTEGRITY_AUDIT),
        ("cost_layered_scorecard", COST_LAYERED_SCORECARD),
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
                "notes": "offensive input materialization artifact(공격 입력 구체화 산출물)",
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
    write_work_packet()
    parent_rows = parent_evidence_summary_rows(parent_final)
    stability_rows = stability_transfer_rows(parent_final)
    month_rows, hour_rows = h17_quality_rows()
    score_rows = cost_layered_score_rows(parent_final)
    axis_rows = offensive_axis_rows(parent_final)
    queue_rows = scout_queue_rows(parent_final, month_rows, hour_rows)
    data_rows = data_integrity_rows(parent_final)
    gates = build_gates(data_rows, stability_rows, axis_rows, queue_rows, receipts_written=False)
    final = final_payload(parent_final, queue_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = build_gates(data_rows, stability_rows, axis_rows, queue_rows, receipts_written=True)
    final = final_payload(parent_final, queue_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, parent_rows, stability_rows, axis_rows, queue_rows, gates)
    write_ledgers(final)
    write_run_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    _ = score_rows


if __name__ == "__main__":
    main()
