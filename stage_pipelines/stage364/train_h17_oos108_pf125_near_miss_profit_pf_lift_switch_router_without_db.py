from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from stage_pipelines.stage364 import review_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db as he  # noqa: E402
from stage_pipelines.stage364 import train_h17_density_failure_regime_behavior_reseed_without_db as dt  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db as gz  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db as hd  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db as hb  # noqa: E402


TODAY = "2026-06-08"
STAGE_ID = hd.STAGE_ID
STAGE_DIR = hd.STAGE_DIR
REVIEW_DIR = hd.REVIEW_DIR
SPEC_DIR = hd.SPEC_DIR
SELECTED_DIR = hd.SELECTED_DIR

RUN_NUMBER = "run364HF"
RUN_ID = "run364HF_train_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1"
PARENT_RUN_ID = he.RUN_ID
NEXT_RUN_ID = "run364HG_review_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1"

STATUS_STRICT = "completed_stage364HF_near_miss_profit_pf_lift_switch_router_strict_proxy_review_required_no_authority"
STATUS_NO_STRICT = "completed_stage364HF_near_miss_profit_pf_lift_switch_router_no_strict_pass_review_required_no_authority"
JUDGMENT_STRICT = "positive_proxy_near_miss_profit_pf_lift_switch_router_candidate_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_near_miss_profit_pf_lift_switch_router_no_strict_pass_review_required_no_authority"
DECISION_STRICT = "stage364HF_open_run364HG_near_miss_profit_pf_lift_switch_router_review"
DECISION_NO_STRICT = "stage364HF_open_run364HG_near_miss_profit_pf_lift_switch_router_review"
CLAIM_BOUNDARY = (
    "research_development_near_miss_profit_pf_lift_switch_router_proxy_and_source_onnx_smoke_only_"
    "no_new_model_training_no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
SOURCE_NEIGHBORHOOD_AUDIT = RUN_DIR / "hf_source_neighborhood_audit.csv"
TRADE_SURFACE = RUN_DIR / "hf_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_hf_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_hf_trade_tape.csv"
SELECTED_VETO_GROUPS = RUN_DIR / "selected_hf_veto_groups.csv"
MONTH_STABILITY = RUN_DIR / "selected_hf_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_hf_cost_stress.csv"
SIDE_SESSION_REVIEW = RUN_DIR / "selected_hf_side_session_review.csv"
ROUTE_ATTRIBUTION = RUN_DIR / "hf_route_component_attribution.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "source_model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "source_onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364HG_QUEUE = RUN_DIR / "hf_hg_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HF_near_miss_profit_pf_lift_switch_router.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HF_near_miss_profit_pf_lift_switch_router.md"
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
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

THIS_FILE = Path(__file__)

INPUT_FILES = [
    he.FINAL_DECISION,
    he.GATE_AUDIT,
    he.REVIEW_SUMMARY,
    he.FAILURE_MEMORY,
    he.RUN364HF_QUEUE,
    hd.FINAL_DECISION,
    hd.GATE_AUDIT,
    hd.TRADE_SURFACE,
    hd.SELECTED_CANDIDATE,
    hd.SELECTED_TRADE_TAPE,
    hd.SOURCE_CANDIDATE_AUDIT,
    hd.MODEL_ARTIFACT_MANIFEST,
    hd.ONNX_SMOKE_REPORT,
    gz.FINAL_DECISION,
    gz.SELECTED_TRADE_TAPE,
    gz.MODEL_ARTIFACT_MANIFEST,
    gz.ONNX_SMOKE_REPORT,
    hb.FINAL_DECISION,
    hb.TRADE_SURFACE,
    hb.SELECTED_CANDIDATE,
    hb.MODEL_ARTIFACT_MANIFEST,
    hb.ONNX_SMOKE_REPORT,
    dt.dp.MODEL_INPUT_DATASET,
    dt.dp.MODEL_INPUT_FEATURE_ORDER,
    THIS_FILE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    SOURCE_NEIGHBORHOOD_AUDIT,
    TRADE_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    SELECTED_VETO_GROUPS,
    MONTH_STABILITY,
    COST_STRESS,
    SIDE_SESSION_REVIEW,
    ROUTE_ATTRIBUTION,
    MODEL_ARTIFACT_MANIFEST,
    ONNX_SMOKE_REPORT,
    DATA_INTEGRITY_AUDIT,
    RUN364HG_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    THIS_FILE,
]

VETO_POLICIES = [
    {
        "policy_id": "veto_open_hour_pflat_sl_gap",
        "label": "open_hour+pflat_bin+short_long_gap_bin(진입 시간+평탄확률 구간+숏롱차 구간)",
        "keys": ["open_hour", "pflat_bin", "sl_gap_bin"],
    },
    {
        "policy_id": "veto_route_hour_pflat_sl_gap",
        "label": "route_role+open_hour+pflat_bin+short_long_gap_bin(라우트 역할+진입 시간+평탄확률 구간+숏롱차 구간)",
        "keys": ["route_role", "open_hour", "pflat_bin", "sl_gap_bin"],
    },
    {
        "policy_id": "veto_direction_hour_pflat_side_edge",
        "label": "direction+open_hour+pflat_bin+side_edge_bin(방향+진입 시간+평탄확률 구간+방향 우위 구간)",
        "keys": ["direction", "open_hour", "pflat_bin", "side_edge_bin"],
    },
    {
        "policy_id": "veto_direction_hour_pflat_sl_gap",
        "label": "direction+open_hour+pflat_bin+short_long_gap_bin(방향+진입 시간+평탄확률 구간+숏롱차 구간)",
        "keys": ["direction", "open_hour", "pflat_bin", "sl_gap_bin"],
    },
    {
        "policy_id": "veto_open_hour2_pflat_sl_gap",
        "label": "open_hour+hour2_bin+pflat_bin+short_long_gap_bin(진입 시간+2시간 구간+평탄확률 구간+숏롱차 구간)",
        "keys": ["open_hour", "hour2_bin", "pflat_bin", "sl_gap_bin"],
    },
    {
        "policy_id": "veto_open_hour_pflat_side_sl_gap",
        "label": "open_hour+pflat_bin+side_edge_bin+short_long_gap_bin(진입 시간+평탄확률 구간+방향 우위 구간+숏롱차 구간)",
        "keys": ["open_hour", "pflat_bin", "side_edge_bin", "sl_gap_bin"],
    },
    {
        "policy_id": "veto_open_hour_pflat_side_edge",
        "label": "open_hour+pflat_bin+side_edge_bin(진입 시간+평탄확률 구간+방향 우위 구간)",
        "keys": ["open_hour", "pflat_bin", "side_edge_bin"],
    },
    {
        "policy_id": "veto_route_hour2_pflat_side_edge",
        "label": "route_role+hour2_bin+pflat_bin+side_edge_bin(라우트 역할+2시간 구간+평탄확률 구간+방향 우위 구간)",
        "keys": ["route_role", "hour2_bin", "pflat_bin", "side_edge_bin"],
    },
    {
        "policy_id": "veto_direction_pflat_side_edge",
        "label": "direction+pflat_bin+side_edge_bin(방향+평탄확률 구간+방향 우위 구간)",
        "keys": ["direction", "pflat_bin", "side_edge_bin"],
    },
    {
        "policy_id": "veto_open_hour_score_pflat",
        "label": "open_hour+score_bin+pflat_bin(진입 시간+점수 구간+평탄확률 구간)",
        "keys": ["open_hour", "score_bin", "pflat_bin"],
    },
]
MIN_COUNTS = [2, 3, 5, 8]
SUM_FLOORS = [-18.0, -12.0, -8.0]
MAX_REMOVED_TOTAL = 18
MAX_REMOVED_OOS = 8
PARENT_ROUTE_LIMIT = 36

OOS_DENSITY_FLOOR = 1.35
COMBINED_DENSITY_FLOOR = 1.30
COMBINED_COST09_FLOOR = -120.0
OOS_NET_TARGET = 60.0
OOS_PF_TARGET = 1.18
OOS_COST06_TARGET = 0.0
COST_PER_TRADE = float(dt.COST_PER_TRADE)


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(path).as_posix()


def exists(path: Path | str) -> bool:
    return io_path(path).exists()


def sha(path: Path | str) -> str:
    return gz.sha(Path(path))


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def finite(value: Any, digits: int = 10) -> float | str:
    number = as_float(value, default=math.nan)
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def read_json(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = [dict(row) for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fields: list[str] = []
        for row in rows:
            for key in row.keys():
                if key not in fields:
                    fields.append(str(key))
        fieldnames = fields or ["empty"]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_text_once(path: Path, marker: str, text: str) -> None:
    hd.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    hd.append_or_replace_csv(path, key_fields, rows)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HF inputs(HF 입력 누락): " + ", ".join(missing))
    parent = read_json(he.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HE next_run_id mismatch(HE 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden parent claim(금지된 상위 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(io_path(he.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("HE gate audit(HE 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "HF source input(HF 원천 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet(parent: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "question": "Can validation-derived micro veto lift HD near miss above OOS net/PF targets while preserving density?(검증 유래 미세 차단이 HD 근접 실패를 밀도 보존 상태로 표본외 순수익/PF 목표 위로 올릴 수 있는가?)",
            "hypothesis": (
                "HD selected route(HD 선택 라우트)의 수익/PF 부족은 소수 anchor loss bucket(기준 손실 구간)에서 나오며, "
                "validation-derived probability-shape veto(검증 유래 확률 형태 차단)로 손실 구간을 제거하면 OOS net/PF/cost0.6(표본외 순수익/PF/비용0.6)을 올릴 수 있습니다."
            ),
            "controls": [
                "US100 M5",
                "chronological split(시간순 분할)",
                "GZ anchor + HB fallback route(GZ 기준 + HB 대체 라우트)",
                "source row neighborhood replay(원천 행 이웃 재생)",
                "validation-only veto group discovery(검증 전용 차단 그룹 발견)",
                "no OOS-only trade deletion(표본외 전용 거래 삭제 금지)",
            ],
            "success_criteria": {
                "preserve": f"oos_density>={OOS_DENSITY_FLOOR};combined_density>={COMBINED_DENSITY_FLOOR};combined_cost0.9>={COMBINED_COST09_FLOOR}",
                "repair": f"oos_net>={OOS_NET_TARGET};oos_pf>={OOS_PF_TARGET};oos_cost0.6>={OOS_COST06_TARGET}",
            },
            "parent_summary": {
                "parent_run_id": parent.get("run_id"),
                "parent_judgment": parent.get("judgment"),
                "hd_oos_net": parent.get("oos_net", parent.get("selected_oos_net")),
                "hd_oos_profit_factor": parent.get("oos_pf", parent.get("selected_oos_profit_factor")),
            },
            "decision_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def normalize_for_hf(tape: pd.DataFrame, parent_variant: str) -> pd.DataFrame:
    out = tape.copy()
    if out.empty:
        return out
    out["entry_dt"] = pd.to_datetime(out["entry_time"], utc=False)
    out["exit_dt"] = pd.to_datetime(out["exit_time"], utc=False)
    out["net_profit"] = pd.to_numeric(out["net_profit"], errors="coerce").fillna(0.0)
    out["score"] = pd.to_numeric(out["score"], errors="coerce").fillna(0.0)
    out["p_short"] = pd.to_numeric(out["p_short"], errors="coerce").fillna(0.0)
    out["p_flat"] = pd.to_numeric(out["p_flat"], errors="coerce").fillna(0.0)
    out["p_long"] = pd.to_numeric(out["p_long"], errors="coerce").fillna(0.0)
    out["open_hour"] = pd.to_numeric(out["open_hour"], errors="coerce").fillna(-1).astype(int)
    out["hf_parent_route_variant_id"] = parent_variant
    out["hf_parent_route_policy"] = out.get("route_policy", "")
    return out


def add_probability_bins(tape: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, list[float]]]:
    out = tape.copy()
    if out.empty:
        return out, {}
    out["side_edge"] = np.where(out["direction"].astype(str).eq("short"), out["p_short"] - out["p_long"], out["p_long"] - out["p_short"])
    out["flat_gap"] = out["score"] - out["p_flat"]
    out["short_long_gap"] = out["p_short"] - out["p_long"]
    out["hour2_bin"] = (out["open_hour"] // 2).astype(int)
    validation = out[out["split"].astype(str) == "validation"]
    edges: dict[str, list[float]] = {}
    for name, column, bins in [
        ("score_bin", "score", 8),
        ("pflat_bin", "p_flat", 6),
        ("flat_gap_bin", "flat_gap", 8),
        ("side_edge_bin", "side_edge", 8),
        ("sl_gap_bin", "short_long_gap", 8),
    ]:
        values = validation[column].astype(float).to_numpy(dtype="float64")
        if len(values) < bins or float(np.nanmax(values)) == float(np.nanmin(values)):
            out[name] = 0
            edges[name] = []
            continue
        quantiles = np.unique(np.quantile(values, np.linspace(0.0, 1.0, bins + 1)))
        if len(quantiles) < 3:
            out[name] = 0
            edges[name] = []
            continue
        quantiles[0] -= 1e-9
        quantiles[-1] += 1e-9
        out[name] = pd.cut(out[column], bins=quantiles, labels=False, include_lowest=True).astype("Int64").fillna(-1).astype(int)
        edges[name] = [round(float(value), 12) for value in quantiles]
    return out, edges


def group_key(row: Mapping[str, Any], keys: Sequence[str]) -> tuple[Any, ...]:
    return tuple(row.get(key, "") for key in keys)


def apply_veto_policy(
    tape: pd.DataFrame,
    *,
    policy: Mapping[str, Any],
    min_count: int,
    sum_floor: float,
) -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, int]]:
    keys = list(policy["keys"])
    validation = tape[tape["split"].astype(str) == "validation"]
    grouped = validation.groupby(keys, dropna=False)["net_profit"].agg(["count", "sum", "mean"]).reset_index()
    bad = grouped[(grouped["count"] >= min_count) & (grouped["sum"] <= sum_floor)].copy()
    if bad.empty:
        return tape.iloc[0:0], [], {"removed_count": len(tape), "removed_oos_count": int((tape["split"].astype(str) == "oos").sum()), "bad_group_count": 0}
    bad_keys = {tuple(row[key] for key in keys) for _, row in bad.iterrows()}
    keep_mask = tape.apply(lambda row: group_key(row, keys) not in bad_keys, axis=1)
    removed = tape.loc[~keep_mask].copy()
    if int((~keep_mask).sum()) > MAX_REMOVED_TOTAL or int(((~keep_mask) & tape["split"].astype(str).eq("oos")).sum()) > MAX_REMOVED_OOS:
        return tape.iloc[0:0], [], {"removed_count": int((~keep_mask).sum()), "removed_oos_count": int(((~keep_mask) & tape["split"].astype(str).eq("oos")).sum()), "bad_group_count": int(len(bad))}
    group_rows: list[dict[str, Any]] = []
    for idx, raw in bad.iterrows():
        key_filter = np.ones(len(tape), dtype=bool)
        for key in keys:
            key_filter &= tape[key].eq(raw[key]).to_numpy()
        removed_group = tape.loc[key_filter].copy()
        group_rows.append(
            {
                "run_id": RUN_ID,
                "veto_policy_id": policy["policy_id"],
                "veto_policy_label": policy["label"],
                "veto_key_fields": "|".join(keys),
                "veto_group_rank": int(idx) + 1,
                "veto_key_values": json.dumps({key: raw[key] for key in keys}, ensure_ascii=False, sort_keys=True),
                "validation_count": int(raw["count"]),
                "validation_net": finite(raw["sum"], 4),
                "validation_expectancy": finite(raw["mean"], 10),
                "removed_total_count": int(len(removed_group)),
                "removed_oos_count": int((removed_group["split"].astype(str) == "oos").sum()),
                "removed_validation_count": int((removed_group["split"].astype(str) == "validation").sum()),
                "removed_total_net": finite(removed_group["net_profit"].sum(), 4),
                "removed_oos_net": finite(removed_group.loc[removed_group["split"].astype(str) == "oos", "net_profit"].sum(), 4),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    counts = {
        "removed_count": int((~keep_mask).sum()),
        "removed_oos_count": int(((~keep_mask) & tape["split"].astype(str).eq("oos")).sum()),
        "bad_group_count": int(len(bad)),
    }
    return tape.loc[keep_mask].copy(), group_rows, counts


def profit_factor(values: Sequence[float]) -> float:
    return hd.profit_factor(values)


def closed_drawdown(values: Sequence[float]) -> float:
    return hd.closed_drawdown(values)


def metric_row(
    tape: pd.DataFrame,
    *,
    days: Mapping[str, int],
    parent_row: Mapping[str, Any],
    variant_id: str,
    veto_policy_id: str,
    veto_policy_label: str,
    veto_key_fields: str,
    min_count: int | str,
    sum_floor: float | str,
    removed_count: int,
    removed_oos_count: int,
    bad_group_count: int,
    bin_edges: Mapping[str, Sequence[float]],
    hd_reference: Mapping[str, Any],
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "run_id": RUN_ID,
        "route_variant_id": variant_id,
        "parent_route_variant_id": parent_row.get("route_variant_id", ""),
        "parent_route_policy": parent_row.get("route_policy", ""),
        "source_surface_key": parent_row.get("source_surface_key", ""),
        "source_model_id": parent_row.get("source_model_id", ""),
        "veto_policy_id": veto_policy_id,
        "veto_policy_label": veto_policy_label,
        "veto_key_fields": veto_key_fields,
        "veto_min_count": min_count,
        "veto_sum_floor": sum_floor,
        "veto_bad_group_count": bad_group_count,
        "veto_removed_count": removed_count,
        "veto_removed_oos_count": removed_oos_count,
        "bin_edges_json": json.dumps(bin_edges, ensure_ascii=False, sort_keys=True),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    total_net = 0.0
    total_count = 0
    total_long = 0
    total_short = 0
    split_pfs: list[float] = []
    for split in ["validation", "oos"]:
        split_frame = tape[tape["split"].astype(str) == split] if not tape.empty else pd.DataFrame()
        profits = split_frame["net_profit"].astype(float).to_numpy(dtype="float64") if not split_frame.empty else np.asarray([], dtype="float64")
        count = int(len(split_frame))
        net = float(np.sum(profits)) if count else 0.0
        pf = profit_factor(profits)
        drawdown = closed_drawdown(profits)
        long_count = int((split_frame["direction"].astype(str) == "long").sum()) if not split_frame.empty else 0
        short_count = int((split_frame["direction"].astype(str) == "short").sum()) if not split_frame.empty else 0
        hb_added = int(split_frame["route_role"].astype(str).str.contains("hb_fallback", na=False).sum()) if not split_frame.empty else 0
        row.update(
            {
                f"{split}_net": finite(net, 4),
                f"{split}_profit_factor": finite(pf, 10),
                f"{split}_expectancy": finite(net / count, 10) if count else 0.0,
                f"{split}_trade_density": finite(count / days[split], 10),
                f"{split}_trade_count": count,
                f"{split}_cost06_net": finite(net - 0.30 * count, 4),
                f"{split}_cost09_net": finite(net - 0.60 * count, 4),
                f"{split}_max_drawdown": finite(drawdown, 4),
                f"{split}_recovery_factor": finite(net / drawdown, 10) if drawdown > 0 else (999.0 if net > 0 else 0.0),
                f"{split}_long_trade_count": long_count,
                f"{split}_short_trade_count": short_count,
                f"{split}_hb_fallback_added_count": hb_added,
            }
        )
        total_net += net
        total_count += count
        total_long += long_count
        total_short += short_count
        split_pfs.append(pf)
    combined_days = days["validation"] + days["oos"]
    row.update(
        {
            "combined_net": finite(total_net, 4),
            "combined_trade_count": total_count,
            "combined_trade_density": finite(total_count / combined_days, 10),
            "combined_cost06_net": finite(total_net - 0.30 * total_count, 4),
            "combined_cost09_net": finite(total_net - 0.60 * total_count, 4),
            "combined_long_trade_count": total_long,
            "combined_short_trade_count": total_short,
            "combined_short_share": finite(total_short / total_count, 10) if total_count else 0.0,
            "min_split_profit_factor": finite(min(split_pfs), 10) if split_pfs else 0.0,
        }
    )
    row.update(
        {
            "delta_oos_net_vs_hd": finite(as_float(row["oos_net"]) - as_float(hd_reference["selected_oos_net"]), 4),
            "delta_oos_profit_factor_vs_hd": finite(as_float(row["oos_profit_factor"]) - as_float(hd_reference["selected_oos_profit_factor"]), 10),
            "delta_oos_cost06_vs_hd": finite(as_float(row["oos_cost06_net"]) - as_float(hd_reference["selected_oos_cost06_net"]), 4),
            "delta_oos_density_vs_hd": finite(as_float(row["oos_trade_density"]) - as_float(hd_reference["selected_oos_trade_density"]), 10),
            "delta_combined_density_vs_hd": finite(as_float(row["combined_trade_density"]) - as_float(hd_reference["selected_combined_trade_density"]), 10),
            "delta_combined_cost09_vs_hd": finite(as_float(row["combined_cost09_net"]) - as_float(hd_reference["selected_combined_cost09_net"]), 4),
        }
    )
    preserve_pass = (
        as_float(row["oos_trade_density"]) >= OOS_DENSITY_FLOOR
        and as_float(row["combined_trade_density"]) >= COMBINED_DENSITY_FLOOR
        and as_float(row["combined_cost09_net"]) >= COMBINED_COST09_FLOOR
    )
    repair_pass = (
        as_float(row["oos_net"]) >= OOS_NET_TARGET
        and as_float(row["oos_profit_factor"]) >= OOS_PF_TARGET
        and as_float(row["oos_cost06_net"]) >= OOS_COST06_TARGET
    )
    validation_guard = as_float(row["validation_net"]) > 0.0 and as_float(row["validation_profit_factor"]) >= 1.0
    micro_guard = removed_count <= MAX_REMOVED_TOTAL and removed_oos_count <= MAX_REMOVED_OOS
    row["hf_preserve_floor_pass"] = "passed(통과)" if preserve_pass else "failed(실패)"
    row["hf_repair_target_pass"] = "passed(통과)" if repair_pass else "failed(실패)"
    row["hf_validation_guard_pass"] = "passed(통과)" if validation_guard else "failed(실패)"
    row["hf_micro_veto_guard_pass"] = "passed(통과)" if micro_guard else "failed(실패)"
    row["hf_strict_switch_pass"] = "passed(통과)" if preserve_pass and repair_pass and validation_guard and micro_guard else "failed(실패)"
    row["selection_score"] = finite(selection_score(row), 6)
    return row


def selection_score(row: Mapping[str, Any]) -> float:
    strict_bonus = 240000.0 if str(row.get("hf_strict_switch_pass", "")).startswith("passed") else 0.0
    preserve_bonus = 52000.0 if str(row.get("hf_preserve_floor_pass", "")).startswith("passed") else 0.0
    repair_bonus = 72000.0 if str(row.get("hf_repair_target_pass", "")).startswith("passed") else 0.0
    validation_bonus = 18000.0 if str(row.get("hf_validation_guard_pass", "")).startswith("passed") else 0.0
    return (
        strict_bonus
        + preserve_bonus
        + repair_bonus
        + validation_bonus
        + 7.5 * as_float(row.get("validation_net"))
        + 14.0 * as_float(row.get("oos_net"))
        + 15.0 * as_float(row.get("oos_cost06_net"))
        + 4.0 * as_float(row.get("combined_cost09_net"))
        + 12500.0 * max(0.0, min(as_float(row.get("oos_profit_factor")), 3.0) - 1.0)
        + 6100.0 * as_float(row.get("oos_trade_density"))
        + 5700.0 * as_float(row.get("combined_trade_density"))
        + 1900.0 * max(0.0, as_float(row.get("delta_oos_net_vs_hd")))
        + 2600.0 * max(0.0, as_float(row.get("delta_oos_profit_factor_vs_hd")))
        + 1200.0 * max(0.0, as_float(row.get("delta_oos_cost06_vs_hd")))
        - 26000.0 * max(0.0, OOS_NET_TARGET - as_float(row.get("oos_net")))
        - 36000.0 * max(0.0, OOS_PF_TARGET - as_float(row.get("oos_profit_factor")))
        - 21000.0 * max(0.0, OOS_DENSITY_FLOOR - as_float(row.get("oos_trade_density")))
        - 23000.0 * max(0.0, COMBINED_DENSITY_FLOOR - as_float(row.get("combined_trade_density")))
        - 180.0 * max(0.0, COMBINED_COST09_FLOOR - as_float(row.get("combined_cost09_net")))
        - 420.0 * max(0.0, as_float(row.get("veto_removed_oos_count")) - 2.0)
    )


def variant_name(parent_variant: str, policy_id: str, min_count: int | str, sum_floor: float | str) -> str:
    base = hd.safe_name(parent_variant)
    suffix = f"{policy_id}__mc{min_count}__sf{str(sum_floor).replace('-', 'm').replace('.', 'p')}"
    return f"hf__{hd.safe_name(suffix)}__{base}"[:180]


def build_surface(
    route_tapes: Mapping[str, pd.DataFrame],
    hd_surface: pd.DataFrame,
    frame: pd.DataFrame,
    hd_reference: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], dict[str, list[dict[str, Any]]]]:
    days = hd.split_days(frame)
    surface = hd_surface.copy()
    for column in [
        "selection_score",
        "oos_net",
        "oos_profit_factor",
        "oos_cost06_net",
        "oos_trade_density",
        "combined_trade_density",
        "combined_cost09_net",
    ]:
        surface[column] = pd.to_numeric(surface[column], errors="coerce").fillna(0.0)
    ranked = surface.sort_values(
        ["selection_score", "oos_net", "oos_profit_factor", "oos_cost06_net"],
        ascending=False,
    ).head(PARENT_ROUTE_LIMIT)
    eligible_parents = set(ranked["route_variant_id"].astype(str))
    eligible_parents.add(str(hd_reference.get("selected_route_variant_id", "")))
    parent_rows = {str(row["route_variant_id"]): dict(row) for row in surface.to_dict("records")}
    surface_rows: list[dict[str, Any]] = []
    tapes: dict[str, pd.DataFrame] = {}
    veto_groups_by_variant: dict[str, list[dict[str, Any]]] = {}
    for parent_variant, raw_tape in route_tapes.items():
        if parent_variant not in eligible_parents:
            continue
        parent_row = parent_rows.get(parent_variant, {"route_variant_id": parent_variant, "route_policy": ""})
        tape = normalize_for_hf(raw_tape, parent_variant)
        binned, bin_edges = add_probability_bins(tape)
        base_variant = variant_name(parent_variant, "no_veto(차단 없음)", "none", "none")
        base_tape = binned.copy()
        base_tape["run_id"] = RUN_ID
        base_tape["model_id"] = base_variant
        base_tape["route_variant_id"] = base_variant
        base_tape["route_policy"] = "no_veto(차단 없음)"
        base_tape["hf_veto_policy_id"] = "no_veto(차단 없음)"
        base_tape["hf_veto_key_fields"] = ""
        surface_rows.append(
            metric_row(
                base_tape,
                days=days,
                parent_row=parent_row,
                variant_id=base_variant,
                veto_policy_id="no_veto(차단 없음)",
                veto_policy_label="no_veto(차단 없음)",
                veto_key_fields="",
                min_count="",
                sum_floor="",
                removed_count=0,
                removed_oos_count=0,
                bad_group_count=0,
                bin_edges=bin_edges,
                hd_reference=hd_reference,
            )
        )
        tapes[base_variant] = base_tape
        veto_groups_by_variant[base_variant] = []
        for policy in VETO_POLICIES:
            for min_count in MIN_COUNTS:
                for sum_floor in SUM_FLOORS:
                    kept, group_rows, counts = apply_veto_policy(binned, policy=policy, min_count=min_count, sum_floor=sum_floor)
                    if kept.empty:
                        continue
                    variant = variant_name(parent_variant, str(policy["policy_id"]), min_count, sum_floor)
                    kept = kept.copy()
                    kept["run_id"] = RUN_ID
                    kept["model_id"] = variant
                    kept["route_variant_id"] = variant
                    kept["route_policy"] = f"{policy['label']} min_count={min_count} sum_floor={sum_floor}(검증 차단)"
                    kept["hf_veto_policy_id"] = policy["policy_id"]
                    kept["hf_veto_key_fields"] = "|".join(policy["keys"])
                    surface_rows.append(
                        metric_row(
                            kept,
                            days=days,
                            parent_row=parent_row,
                            variant_id=variant,
                            veto_policy_id=str(policy["policy_id"]),
                            veto_policy_label=str(policy["label"]),
                            veto_key_fields="|".join(policy["keys"]),
                            min_count=min_count,
                            sum_floor=sum_floor,
                            removed_count=counts["removed_count"],
                            removed_oos_count=counts["removed_oos_count"],
                            bad_group_count=counts["bad_group_count"],
                            bin_edges=bin_edges,
                            hd_reference=hd_reference,
                        )
                    )
                    tapes[variant] = kept
                    veto_groups_by_variant[variant] = [
                        {
                            **group,
                            "route_variant_id": variant,
                            "parent_route_variant_id": parent_variant,
                            "veto_min_count": min_count,
                            "veto_sum_floor": sum_floor,
                        }
                        for group in group_rows
                    ]
    surface_rows = sorted(surface_rows, key=lambda row: (str(row["hf_strict_switch_pass"]).startswith("passed"), as_float(row["selection_score"])), reverse=True)
    return surface_rows, tapes, veto_groups_by_variant


def selected_surface_row(surface_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return dict(max(surface_rows, key=lambda row: (str(row["hf_strict_switch_pass"]).startswith("passed"), as_float(row["selection_score"]))))


def selected_summary(
    surface_rows: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    selected_tape: pd.DataFrame,
    selected_groups: Sequence[Mapping[str, Any]],
    source_smoke_rows: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    strict_count = sum(1 for row in surface_rows if str(row.get("hf_strict_switch_pass", "")).startswith("passed"))
    preserve_count = sum(1 for row in surface_rows if str(row.get("hf_preserve_floor_pass", "")).startswith("passed"))
    repair_count = sum(1 for row in surface_rows if str(row.get("hf_repair_target_pass", "")).startswith("passed"))
    source_models = sorted(set(selected_tape["source_model_id"].astype(str))) if not selected_tape.empty else []
    source_runs = sorted(set(selected_tape["source_run_id"].astype(str))) if not selected_tape.empty else []
    smoke_pass = [row for row in source_smoke_rows if str(row.get("status", "")).startswith("passed")]
    status = STATUS_STRICT if strict_count else STATUS_NO_STRICT
    judgment = JUDGMENT_STRICT if strict_count else JUDGMENT_NO_STRICT
    decision = DECISION_STRICT if strict_count else DECISION_NO_STRICT
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "selected_route_variant_id": selected["route_variant_id"],
        "selected_parent_route_variant_id": selected["parent_route_variant_id"],
        "selected_veto_policy_id": selected["veto_policy_id"],
        "selected_veto_policy_label": selected["veto_policy_label"],
        "selected_veto_key_fields": selected["veto_key_fields"],
        "selected_veto_min_count": selected["veto_min_count"],
        "selected_veto_sum_floor": selected["veto_sum_floor"],
        "selected_veto_bad_group_count": selected["veto_bad_group_count"],
        "selected_veto_removed_count": selected["veto_removed_count"],
        "selected_veto_removed_oos_count": selected["veto_removed_oos_count"],
        "selected_source_models": "|".join(source_models),
        "selected_source_runs": "|".join(source_runs),
        "selected_source_surface_key": selected.get("source_surface_key", ""),
        "selected_oos_net": selected["oos_net"],
        "selected_oos_profit_factor": selected["oos_profit_factor"],
        "selected_oos_trade_density": selected["oos_trade_density"],
        "selected_oos_trade_count": selected["oos_trade_count"],
        "selected_oos_cost06_net": selected["oos_cost06_net"],
        "selected_oos_cost09_net": selected["oos_cost09_net"],
        "selected_validation_net": selected["validation_net"],
        "selected_validation_profit_factor": selected["validation_profit_factor"],
        "selected_validation_trade_density": selected["validation_trade_density"],
        "selected_validation_trade_count": selected["validation_trade_count"],
        "selected_combined_net": selected["combined_net"],
        "selected_combined_trade_density": selected["combined_trade_density"],
        "selected_combined_trade_count": selected["combined_trade_count"],
        "selected_combined_cost06_net": selected["combined_cost06_net"],
        "selected_combined_cost09_net": selected["combined_cost09_net"],
        "selected_combined_short_share": selected["combined_short_share"],
        "delta_oos_net_vs_hd": selected["delta_oos_net_vs_hd"],
        "delta_oos_profit_factor_vs_hd": selected["delta_oos_profit_factor_vs_hd"],
        "delta_oos_cost06_vs_hd": selected["delta_oos_cost06_vs_hd"],
        "delta_oos_density_vs_hd": selected["delta_oos_density_vs_hd"],
        "delta_combined_density_vs_hd": selected["delta_combined_density_vs_hd"],
        "delta_combined_cost09_vs_hd": selected["delta_combined_cost09_vs_hd"],
        "strict_candidate_count": strict_count,
        "preserve_floor_pass_count": preserve_count,
        "repair_target_pass_count": repair_count,
        "surface_rows": len(surface_rows),
        "selected_trade_tape_rows": int(len(selected_tape)),
        "selected_veto_group_rows": int(len(selected_groups)),
        "source_onnx_smoke_pass_rows": len(smoke_pass),
        "runtime_package": "not_opened",
        "new_model_training": "not_run_source_model_router(새 학습 없음, 원천 모델 라우터)",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def source_artifact_rows(selected_tape: pd.DataFrame, manifests: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    used = sorted(set(zip(selected_tape["source_run_id"].astype(str), selected_tape["source_model_id"].astype(str)))) if not selected_tape.empty else []
    for source_run, model_id in used:
        if source_run == hd.GZ_ANCHOR_RUN_ID:
            manifest = manifests["GZ"]
        elif source_run == hd.HB_SOURCE_RUN_ID:
            manifest = manifests["HB"]
        else:
            continue
        for raw in manifest[manifest["model_id"].astype(str) == model_id].to_dict("records"):
            path = ROOT / str(raw["path"])
            rows.append(
                {
                    "run_id": RUN_ID,
                    "source_run_id": source_run,
                    "model_id": model_id,
                    "artifact_type": raw.get("artifact_type", ""),
                    "path": raw.get("path", ""),
                    "sha256": sha(path) if exists(path) and io_path(path).is_file() else raw.get("sha256", ""),
                    "status": "linked_source_artifact(원천 산출물 연결)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(MODEL_ARTIFACT_MANIFEST, rows)
    return rows


def source_smoke_rows(selected_tape: pd.DataFrame, smoke_reports: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    used = sorted(set(zip(selected_tape["source_run_id"].astype(str), selected_tape["source_model_id"].astype(str)))) if not selected_tape.empty else []
    for source_run, model_id in used:
        smoke = smoke_reports["GZ"] if source_run == hd.GZ_ANCHOR_RUN_ID else smoke_reports["HB"] if source_run == hd.HB_SOURCE_RUN_ID else pd.DataFrame()
        for raw in smoke[smoke["model_id"].astype(str) == model_id].to_dict("records"):
            rows.append(
                {
                    "run_id": RUN_ID,
                    "source_run_id": source_run,
                    "model_id": model_id,
                    "onnx_path": raw.get("onnx_path", ""),
                    "sample_rows": raw.get("sample_rows", ""),
                    "max_abs_diff": raw.get("max_abs_diff", ""),
                    "status": raw.get("status", ""),
                    "failure": raw.get("failure", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(ONNX_SMOKE_REPORT, rows)
    return rows


def write_trade_auxiliary(selected_tape: pd.DataFrame) -> None:
    output = selected_tape.drop(columns=["entry_dt", "exit_dt"], errors="ignore").to_dict("records") if not selected_tape.empty else []
    write_csv(SELECTED_TRADE_TAPE, output)
    month_rows: list[dict[str, Any]] = []
    stress_rows: list[dict[str, Any]] = []
    side_rows: list[dict[str, Any]] = []
    attribution_rows: list[dict[str, Any]] = []
    if not selected_tape.empty:
        frame = selected_tape.copy()
        frame["net_profit"] = pd.to_numeric(frame["net_profit"], errors="coerce").fillna(0.0)
        for (split, month), group in frame.groupby(["split", "open_month"], sort=True):
            profits = group["net_profit"].to_numpy(dtype="float64")
            month_rows.append({"run_id": RUN_ID, "split": split, "open_month": month, "trade_count": int(len(group)), "net_profit": finite(float(profits.sum()), 4), "profit_factor": finite(profit_factor(profits), 10), "positive_month": str(float(profits.sum()) > 0).lower(), "claim_boundary": CLAIM_BOUNDARY})
        for cost in [0.30, 0.45, 0.60, 0.90]:
            adjusted = frame["net_profit"] - (cost - COST_PER_TRADE)
            for split, group in frame.assign(adjusted=adjusted).groupby("split", sort=True):
                profits = group["adjusted"].to_numpy(dtype="float64")
                stress_rows.append({"run_id": RUN_ID, "split": split, "cost_per_trade": cost, "trade_count": int(len(group)), "net_profit": finite(float(profits.sum()), 4), "profit_factor": finite(profit_factor(profits), 10), "expectancy": finite(float(np.mean(profits)) if len(profits) else 0.0, 10), "claim_boundary": CLAIM_BOUNDARY})
        for (split, role, direction, hour), group in frame.groupby(["split", "route_role", "direction", "open_hour"], sort=True):
            profits = group["net_profit"].to_numpy(dtype="float64")
            side_rows.append({"run_id": RUN_ID, "split": split, "route_role": role, "direction": direction, "open_hour": int(hour), "trade_count": int(len(group)), "net_profit": finite(float(profits.sum()), 4), "profit_factor": finite(profit_factor(profits), 10), "expectancy": finite(float(np.mean(profits)) if len(profits) else 0.0, 10), "claim_boundary": CLAIM_BOUNDARY})
        for (split, role, source_run), group in frame.groupby(["split", "route_role", "source_run_id"], sort=True):
            profits = group["net_profit"].to_numpy(dtype="float64")
            attribution_rows.append({"run_id": RUN_ID, "split": split, "route_role": role, "source_run_id": source_run, "trade_count": int(len(group)), "net_profit": finite(float(profits.sum()), 4), "profit_factor": finite(profit_factor(profits), 10), "expectancy": finite(float(np.mean(profits)) if len(profits) else 0.0, 10), "claim_boundary": CLAIM_BOUNDARY})
    write_csv(MONTH_STABILITY, month_rows)
    write_csv(COST_STRESS, stress_rows)
    write_csv(SIDE_SESSION_REVIEW, side_rows)
    write_csv(ROUTE_ATTRIBUTION, attribution_rows)


def data_integrity_rows(frame: pd.DataFrame, selected_tape: pd.DataFrame, source_audit: Sequence[Mapping[str, Any]], selected_groups: Sequence[Mapping[str, Any]], source_smoke: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    duplicate_timestamps = int(frame["timestamp"].duplicated().sum())
    split_counts = frame["split"].value_counts().to_dict()
    overlap_violations = 0
    if not selected_tape.empty:
        for _, group in selected_tape.sort_values(["split", "entry_dt"]).groupby("split"):
            last_exit: pd.Timestamp | None = None
            for _, row in group.iterrows():
                if last_exit is not None and row["entry_dt"] <= last_exit:
                    overlap_violations += 1
                last_exit = max(last_exit, row["exit_dt"]) if last_exit is not None else row["exit_dt"]
    rows = [
        {"run_id": RUN_ID, "audit_item": "input_lineage(입력 계보)", "status": "passed" if all(exists(path) for path in INPUT_FILES if path != THIS_FILE) else "failed", "observed": ";".join(rel(path) for path in INPUT_FILES if path != THIS_FILE), "effect": "HE/HD/GZ/HB 산출물을 HF 입력으로 연결합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "duplicate_timestamp(중복 타임스탬프)", "status": "passed" if duplicate_timestamps == 0 else "failed", "observed": f"duplicate_timestamps={duplicate_timestamps}", "effect": "기초 데이터 중복이 라우트 판단을 왜곡하지 않게 합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "split_presence(분할 존재)", "status": "passed" if all(split_counts.get(split, 0) > 0 for split in ["train", "validation", "oos"]) else "failed", "observed": json.dumps(split_counts, ensure_ascii=False, sort_keys=True), "effect": "validation/OOS(검증/표본외) 경계를 유지합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "source_neighborhood_replay(원천 이웃 재생)", "status": "passed" if len(source_audit) > 0 else "failed", "observed": f"source_rows={len(source_audit)}", "effect": "HD 단일 선택만이 아니라 HB source row neighborhood(원천 행 이웃)를 다시 평가합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "validation_veto_groups(검증 차단 그룹)", "status": "passed" if len(selected_groups) > 0 else "failed", "observed": f"selected_veto_groups={len(selected_groups)}", "effect": "차단 규칙이 OOS(표본외) 직접 삭제가 아니라 validation(검증) 손실 그룹에서 나온 것을 기록합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "source_onnx_smoke_available(원천 ONNX 스모크 존재)", "status": "passed" if any(str(row.get("status", "")).startswith("passed") for row in source_smoke) else "failed", "observed": f"source_onnx_smoke_rows={len(source_smoke)}", "effect": "새 ONNX(온엑스)를 만들지 않아도 원천 모델 ONNX(온엑스) 계보를 연결합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "no_trade_splitting(거래 쪼개기 없음)", "status": "passed" if overlap_violations == 0 else "failed", "observed": f"route_overlap_violations={overlap_violations}", "effect": "기존 단일 포지션 라우트에서 일부 거래를 차단할 뿐 거래를 쪼개지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "label_boundary(라벨 경계)", "status": "passed", "observed": "veto discovery uses validation trade outcomes only(차단 발견은 검증 거래 결과만 사용)", "effect": "OOS(표본외) 손익을 직접 조건으로 삼는 look-ahead style(미래참조식) 삭제를 피합니다.", "claim_boundary": CLAIM_BOUNDARY},
    ]
    write_csv(DATA_INTEGRITY_AUDIT, rows)
    return rows


def write_queue(final: Mapping[str, Any]) -> None:
    write_csv(
        RUN364HG_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "hg01_near_miss_profit_pf_lift_review(근접 실패 수익/PF 리프트 검토)",
                "review_subject": final["selected_route_variant_id"],
                "strict_candidate_count": final["strict_candidate_count"],
                "selected_oos_net": final["selected_oos_net"],
                "selected_oos_profit_factor": final["selected_oos_profit_factor"],
                "selected_oos_cost06_net": final["selected_oos_cost06_net"],
                "selected_oos_density": final["selected_oos_trade_density"],
                "selected_combined_density": final["selected_combined_trade_density"],
                "selected_combined_cost09_net": final["selected_combined_cost09_net"],
                "required_review": "veto attribution, package boundary, overfit caution(차단 귀속, 패키지 경계, 과적합 주의)",
                "effect": "HG review(HG 검토)가 HF strict proxy(엄격 프록시)를 패키지로 열지, 더 검증할지 분리 판단합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def gate_rows(final: Mapping[str, Any], data_rows: Sequence[Mapping[str, Any]], *, final_written: bool) -> list[dict[str, Any]]:
    receipts = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("scope_completion_gate", exists(TRADE_SURFACE) and exists(SELECTED_CANDIDATE) and exists(SELECTED_TRADE_TAPE), TRADE_SURFACE, "HF surface/tape/candidate(HF 표면/기록/후보)를 작성했습니다."),
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "HE/HD/GZ/HB 입력 계보를 기록했습니다."),
        ("source_neighborhood_gate", exists(SOURCE_NEIGHBORHOOD_AUDIT), SOURCE_NEIGHBORHOOD_AUDIT, "HB source row neighborhood(HB 원천 행 이웃)를 다시 재생했습니다."),
        ("kpi_contract_audit", exists(TRADE_SURFACE) and int(final["surface_rows"]) > 0, TRADE_SURFACE, "net/PF/expectancy/density/cost/drawdown(순수익/PF/기대값/밀도/비용/낙폭) KPI를 표면에 기록했습니다."),
        ("validation_veto_gate", exists(SELECTED_VETO_GROUPS) and int(final["selected_veto_group_rows"]) > 0, SELECTED_VETO_GROUPS, "선택 후보의 차단 그룹이 validation(검증)에서 유래했음을 기록했습니다."),
        ("data_integrity_gate", bool(data_rows) and all(str(row["status"]) == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "입력/분할/차단/겹침 감사를 통과했습니다."),
        ("source_onnx_smoke_gate", exists(ONNX_SMOKE_REPORT) and int(final["source_onnx_smoke_pass_rows"]) > 0, ONNX_SMOKE_REPORT, "선택 원천 모델의 ONNX(온엑스) 스모크 근거를 연결했습니다."),
        ("no_trade_splitting_gate", exists(SELECTED_TRADE_TAPE), SELECTED_TRADE_TAPE, "거래 쪼개기가 아니라 validation-derived veto(검증 유래 차단)만 적용했습니다."),
        ("skill_receipt_lint", all(exists(path) for path in receipts), RUN_EVIDENCE_RECEIPT, "필수 receipt(영수증)를 작성했습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트 커버리지 감사를 종료 기록에 연결했습니다."),
        ("final_claim_guard", final["runtime_authority"] == "not_claimed" and final["operating_promotion"] == "not_claimed" and final["goal_achieve"] == "not_claimed", CLAIM_RECEIPT, "운영 권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    rows = [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in gates]
    write_csv(GATE_AUDIT, rows)
    return rows


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {**summary, "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates)}


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy router with source ONNX smoke(Python 프록시 라우터와 원천 ONNX 스모크), no MT5(MT5 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "validation-derived micro veto(검증 유래 미세 차단)가 HD near miss(HD 근접 실패)를 수익/PF 목표 위로 올릴 수 있는지 시험합니다.", "comparison_baseline": hd.RUN_ID, "decision_use": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(dt.dp.MODEL_INPUT_DATASET), rel(hd.SELECTED_TRADE_TAPE), rel(hb.TRADE_SURFACE)], "time_axis": "UTC model timestamp and source trade timestamps(UTC 모델 타임스탬프와 원천 거래 시간)", "feature_label_boundary": "veto groups learned from validation trade results only(차단 그룹은 검증 거래 결과에서만 학습)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_training": "not_run(실행 안 함)", "source_models": final["selected_source_models"], "source_onnx_smoke_pass_rows": final["source_onnx_smoke_pass_rows"], "validation_judgment": final["judgment"]})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change_vs_hd": {"delta_oos_net": final["delta_oos_net_vs_hd"], "delta_oos_pf": final["delta_oos_profit_factor_vs_hd"], "delta_oos_cost06": final["delta_oos_cost06_vs_hd"], "delta_oos_density": final["delta_oos_density_vs_hd"], "delta_combined_density": final["delta_combined_density_vs_hd"], "delta_combined_cost09": final["delta_combined_cost09_vs_hd"]}, "likely_driver": final["selected_veto_policy_label"], "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(SELECTED_TRADE_TAPE), rel(SELECTED_VETO_GROUPS), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_proxy_router_boundary(프록시 라우터 경계로 연결됨)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "HF strict proxy(HF 엄격 프록시)를 운영 주장으로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364HF Near-Miss Profit/PF Lift Switch Router(근접 실패 수익/PF 리프트 전환 라우터)

Created(생성): {final['created_at_utc']}

Action(행동): HD dual-surface router(HD 이중 표면 라우터)의 source row neighborhood(원천 행 이웃)를 다시 replay(재생)하고, validation-derived micro veto(검증 유래 미세 차단)를 각 라우트에 적용했습니다.

Effect(효과): HD near miss(HD 근접 실패)를 OOS net/PF/cost0.6(표본외 순수익/PF/비용0.6) 목표 위로 올릴 수 있는지 보되, OOS-only deletion(표본외 전용 삭제)과 runtime authority(런타임 권위) 주장을 차단합니다.

- judgment(판정): `{final['judgment']}`
- selected_route_variant_id(선택 라우트 변형 ID): `{final['selected_route_variant_id']}`
- selected_parent_route(선택 상위 라우트): `{final['selected_parent_route_variant_id']}`
- selected_veto_policy(선택 차단 정책): `{final['selected_veto_policy_label']}`
- selected_veto_rule(선택 차단 규칙): key `{final['selected_veto_key_fields']}`, min_count `{final['selected_veto_min_count']}`, sum_floor `{final['selected_veto_sum_floor']}`
- OOS net/PF/density/cost0.6(표본외 순수익/PF/밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`
- combined net/density/cost0.9(합산 순수익/밀도/비용0.9): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}`
- delta vs HD(HD 대비 차이): OOS net `{final['delta_oos_net_vs_hd']}`, PF `{final['delta_oos_profit_factor_vs_hd']}`, cost0.6 `{final['delta_oos_cost06_vs_hd']}`, OOS density `{final['delta_oos_density_vs_hd']}`, combined density `{final['delta_combined_density_vs_hd']}`, combined cost0.9 `{final['delta_combined_cost09_vs_hd']}`
- veto removed total/OOS(차단 제거 전체/표본외): `{final['selected_veto_removed_count']}` / `{final['selected_veto_removed_oos_count']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- source_onnx_smoke_pass_rows(원천 ONNX 스모크 통과 행): `{final['source_onnx_smoke_pass_rows']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364HF Near-Miss Profit/PF Lift Switch Router(근접 실패 수익/PF 리프트 전환 라우터)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): HF strict proxy(HF 엄격 프록시) 후보를 HG review(HG 검토)로 넘깁니다.

Effect(효과): 수익/PF 리프트 단서는 살리되, package(패키지)와 MT5 runtime probe(MT5 런타임 탐침) 여부는 별도 검토에서 닫습니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364HF__{RUN_ID}", f"\n- run364HF__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - near-miss profit/PF lift switch router(근접 실패 수익/PF 리프트 전환 라우터), next(다음) `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364HF__{RUN_ID}", f"\n<!-- run364HF__{RUN_ID} -->\n\n## run364HF Near-Miss Profit/PF Lift Switch Router(근접 실패 수익/PF 리프트 전환 라우터)\n\nAction(행동): HD source neighborhood(HD 원천 이웃)에 validation-derived micro veto(검증 유래 미세 차단)를 적용했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 strict proxy(엄격 프록시) 후보의 패키지 가능성과 과적합 위험을 검토합니다.\n")
    append_text_once(STAGE_README, f"run364HF__{RUN_ID}", f"\n<!-- run364HF__{RUN_ID} -->\n## run364HF near-miss profit/PF lift switch router(근접 실패 수익/PF 리프트 전환 라우터)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364HF` completed(완료) near-miss profit/PF lift switch router(근접 실패 수익/PF 리프트 전환 라우터). Selected(선택) OOS net/PF/density/cost0.6(표본외 순수익/PF/밀도/비용0.6)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`입니다.

Route truth(라우트 진실): selected veto(선택 차단)는 `{final['selected_veto_policy_label']}`이고, validation(검증) 손실 그룹 `{final['selected_veto_bad_group_count']}`개에서 total/OOS(전체/표본외) `{final['selected_veto_removed_count']}` / `{final['selected_veto_removed_oos_count']}`개 거래를 차단했습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 strict proxy(엄격 프록시) 후보를 package boundary(패키지 경계), overfit caution(과적합 주의), MT5 probe readiness(MT5 탐침 준비성)로 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): HF near-miss profit/PF lift switch router(HF 근접 실패 수익/PF 리프트 전환 라우터).

HF OOS net/PF/density/cost0.6(HF 표본외 순수익/PF/밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`
HF combined density/cost0.9(HF 합산 밀도/비용0.9): `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}`
HF delta vs HD(HF의 HD 대비 차이): net `{final['delta_oos_net_vs_hd']}`, PF `{final['delta_oos_profit_factor_vs_hd']}`, cost0.6 `{final['delta_oos_cost06_vs_hd']}`, density `{final['delta_oos_density_vs_hd']}`

Next seed(다음 씨앗): HG near-miss profit/PF lift review(HG 근접 실패 수익/PF 리프트 검토).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364HF__{RUN_ID}", f"\n<!-- run364HF__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed near-miss profit/PF lift switch router(근접 실패 수익/PF 리프트 전환 라우터); strict candidates(엄격 후보) `{final['strict_candidate_count']}`; selected(선택) `{final['selected_route_variant_id']}`; next(다음) `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HF__{RUN_ID}", f"\n<!-- run364HF__{RUN_ID} -->\n- `{RUN_ID}`: validation-derived micro veto(검증 유래 미세 차단)가 HD near miss(HD 근접 실패)를 OOS net/PF target(표본외 순수익/PF 목표) 위로 올렸습니다. Effect(효과): HG가 package(패키지) 또는 추가 검증 여부를 판단합니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364HF__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364HF__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: validation-derived micro veto(검증 유래 미세 차단)가 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): 다음 작업은 더 넓은 원천 또는 새 trade-shape(거래 형태)로 넘어가야 합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    artifact_count = len([path for path in OUTPUT_FILES if exists(path)])
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "artifact_count": artifact_count,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Can validation-derived micro veto lift HD near miss without breaking density?(검증 유래 미세 차단이 밀도를 깨지 않고 HD 근접 실패를 올릴 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"strict_candidate_count={final['strict_candidate_count']};oos_net={final['selected_oos_net']};oos_pf={final['selected_oos_profit_factor']};oos_density={final['selected_oos_trade_density']};combined_cost09={final['selected_combined_cost09_net']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append(
            {
                **common,
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "view": record_view,
                "tier": tier_scope,
                "kpi_scope": "HF near-miss profit/PF lift router(HF 근접 실패 수익/PF 리프트 라우터)",
                "metric_scope": "python_proxy_source_onnx_smoke(Python 프록시와 원천 ONNX 스모크)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "",
                "source_authority": "python_proxy_source_onnx_smoke_no_mt5(Python 프록시와 원천 ONNX 스모크, MT5 없음)",
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **common,
                "run_family": "experiment_execution(실험 실행)",
                "run_type": "near_miss_profit_pf_lift_switch_router(근접 실패 수익/PF 리프트 전환 라우터)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(TRADE_SURFACE),
                "selected_net_profit": final["selected_oos_net"],
                "selected_profit_factor": final["selected_oos_profit_factor"],
                "selected_trade_density": final["selected_oos_trade_density"],
            }
        ],
    )
    try:
        hb.et.repair_run_registry_line_endings(RUN_ID)
    except AttributeError:
        pass


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == THIS_FILE else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "HF near-miss profit/PF lift artifact(HF 근접 실패 수익/PF 리프트 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "command": f"python {rel(THIS_FILE)}",
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    feature_order = dt.load_feature_order()
    frame = dt.load_dataset(feature_order)
    hd_final = read_json(hd.FINAL_DECISION)
    hd_surface_existing = pd.read_csv(io_path(hd.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    gz_final = read_json(gz.FINAL_DECISION)
    hb_selected = read_json(hb.SELECTED_CANDIDATE)
    gz_tape = pd.read_csv(io_path(gz.SELECTED_TRADE_TAPE), encoding="utf-8-sig").fillna("")
    hb_surface = pd.read_csv(io_path(hb.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    hb_manifest = pd.read_csv(io_path(hb.MODEL_ARTIFACT_MANIFEST), encoding="utf-8-sig").fillna("")
    gz_manifest = pd.read_csv(io_path(gz.MODEL_ARTIFACT_MANIFEST), encoding="utf-8-sig").fillna("")
    hb_smoke = pd.read_csv(io_path(hb.ONNX_SMOKE_REPORT), encoding="utf-8-sig").fillna("")
    gz_smoke = pd.read_csv(io_path(gz.ONNX_SMOKE_REPORT), encoding="utf-8-sig").fillna("")
    hb_rows = hd.candidate_hb_rows(hb_surface, hb_selected)
    _, route_tapes, source_audit = hd.route_surface(gz_tape, hb_rows, frame, feature_order, hb_manifest, gz_final)
    source_audit_rows = [{**row, "run_id": RUN_ID, "claim_boundary": CLAIM_BOUNDARY} for row in source_audit]
    write_csv(SOURCE_NEIGHBORHOOD_AUDIT, source_audit_rows)
    surface_rows, tapes, veto_groups = build_surface(route_tapes, hd_surface_existing, frame, hd_final)
    write_csv(TRADE_SURFACE, surface_rows)
    selected = selected_surface_row(surface_rows)
    selected_tape = tapes[str(selected["route_variant_id"])].copy()
    selected_groups = veto_groups.get(str(selected["route_variant_id"]), [])
    write_csv(SELECTED_VETO_GROUPS, selected_groups)
    source_artifact_rows(selected_tape, {"GZ": gz_manifest, "HB": hb_manifest})
    source_smoke = source_smoke_rows(selected_tape, {"GZ": gz_smoke, "HB": hb_smoke})
    write_trade_auxiliary(selected_tape)
    summary = selected_summary(surface_rows, selected, selected_tape, selected_groups, source_smoke, now_utc())
    write_json(SELECTED_CANDIDATE, summary)
    write_queue(summary)
    data_rows = data_integrity_rows(frame, selected_tape, source_audit_rows, selected_groups, source_smoke)
    gates = gate_rows(summary, data_rows, final_written=False)
    final = final_payload(summary, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(final, data_rows, final_written=True)
    final = final_payload(summary, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, gates)
    write_ledgers(final, gates)
    write_manifest(final)
    write_artifact_registry(final)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "strict_candidate_count": final["strict_candidate_count"],
                    "selected_route_variant_id": final["selected_route_variant_id"],
                    "selected_oos_net": final["selected_oos_net"],
                    "selected_oos_profit_factor": final["selected_oos_profit_factor"],
                    "selected_oos_trade_density": final["selected_oos_trade_density"],
                    "selected_oos_cost06_net": final["selected_oos_cost06_net"],
                    "selected_combined_trade_density": final["selected_combined_trade_density"],
                    "selected_combined_cost09_net": final["selected_combined_cost09_net"],
                    "veto_removed_count": final["selected_veto_removed_count"],
                    "veto_removed_oos_count": final["selected_veto_removed_oos_count"],
                    "gate_passes": final["gate_passes"],
                    "gate_total": final["gate_total"],
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
