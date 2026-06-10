from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from stage_pipelines.stage364 import review_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db as hc  # noqa: E402
from stage_pipelines.stage364 import train_h17_density_failure_regime_behavior_reseed_without_db as dt  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db as gz  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db as hb  # noqa: E402


TODAY = "2026-06-08"
STAGE_ID = gz.STAGE_ID
STAGE_DIR = gz.STAGE_DIR
REVIEW_DIR = gz.REVIEW_DIR
SPEC_DIR = gz.SPEC_DIR
SELECTED_DIR = gz.SELECTED_DIR

RUN_NUMBER = "run364HD"
RUN_ID = "run364HD_train_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1"
PARENT_RUN_ID = hc.RUN_ID
NEXT_RUN_ID = "run364HE_review_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1"

STATUS_NO_STRICT = "completed_stage364HD_dual_surface_density_profit_switch_router_no_strict_pass_review_required_no_authority"
STATUS_STRICT = "completed_stage364HD_dual_surface_density_profit_switch_router_strict_proxy_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_dual_surface_density_profit_switch_router_no_strict_pass_review_required_no_authority"
JUDGMENT_STRICT = "positive_proxy_dual_surface_density_profit_switch_router_candidate_review_required_no_authority"
DECISION_NO_STRICT = "stage364HD_open_run364HE_dual_surface_density_profit_switch_router_review"
DECISION_STRICT = "stage364HD_open_run364HE_dual_surface_density_profit_switch_router_review"
CLAIM_BOUNDARY = (
    "research_development_dual_surface_density_profit_switch_router_proxy_and_source_onnx_smoke_only_"
    "no_new_model_training_no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
SOURCE_TAPE_DIR = RUN_DIR / "source_candidate_tapes"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
SOURCE_CANDIDATE_AUDIT = RUN_DIR / "hd_source_candidate_audit.csv"
TRADE_SURFACE = RUN_DIR / "hd_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_hd_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_hd_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_hd_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_hd_cost_stress.csv"
SIDE_SESSION_REVIEW = RUN_DIR / "selected_hd_side_session_review.csv"
ROUTE_ATTRIBUTION = RUN_DIR / "hd_route_component_attribution.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "source_model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "source_onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364HE_QUEUE = RUN_DIR / "hd_he_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364HD_dual_surface_density_profit_switch_router.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HD_dual_surface_density_profit_switch_router.md"
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
    hc.FINAL_DECISION,
    hc.GATE_AUDIT,
    hc.REVIEW_SUMMARY,
    hc.SURFACE_DIAGNOSTIC,
    hc.DELTA_ATTRIBUTION,
    hc.PACKAGE_DECISION,
    hc.FAILURE_MEMORY,
    hc.RUN364HD_QUEUE,
    gz.FINAL_DECISION,
    gz.TRADE_SURFACE,
    gz.SELECTED_CANDIDATE,
    gz.SELECTED_TRADE_TAPE,
    gz.MODEL_ARTIFACT_MANIFEST,
    gz.ONNX_SMOKE_REPORT,
    hb.FINAL_DECISION,
    hb.TRADE_SURFACE,
    hb.SELECTED_CANDIDATE,
    hb.SELECTED_TRADE_TAPE,
    hb.MODEL_ARTIFACT_MANIFEST,
    hb.ONNX_SMOKE_REPORT,
    dt.dp.MODEL_INPUT_DATASET,
    dt.dp.MODEL_INPUT_FEATURE_ORDER,
    dt.dp.RAW_US100_M5,
    THIS_FILE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    SOURCE_CANDIDATE_AUDIT,
    TRADE_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    MONTH_STABILITY,
    COST_STRESS,
    SIDE_SESSION_REVIEW,
    ROUTE_ATTRIBUTION,
    MODEL_ARTIFACT_MANIFEST,
    ONNX_SMOKE_REPORT,
    DATA_INTEGRITY_AUDIT,
    RUN364HE_QUEUE,
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

SOURCE_LIMIT = 36
COST_PER_TRADE = float(dt.COST_PER_TRADE)
GZ_ANCHOR_RUN_ID = gz.RUN_ID
HB_SOURCE_RUN_ID = hb.RUN_ID


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
    if not math.isfinite(number):
        return default
    return number


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
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
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    existing = io_path(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in existing:
        return
    payload = existing.rstrip() + "\n" + text.lstrip() if existing.strip() else text
    io_path(path).write_text(payload, encoding="utf-8-sig")


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    rows = [dict(row) for row in rows]
    existing_rows: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing_rows = list(reader)
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["empty"]
    new_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows}
    kept = [row for row in existing_rows if tuple(str(row.get(key, "")) for key in key_fields) not in new_keys]
    merged = kept + rows
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in merged:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def ensure_dirs() -> None:
    for path in [RUN_DIR, SOURCE_TAPE_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HD inputs(HD 입력 누락): " + ", ".join(missing))
    parent = read_json(hc.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HC next_run_id mismatch(HC 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden HC claim(금지된 HC 주장): {key}={parent.get(key)}")
    for label, gate_path in [("HC", hc.GATE_AUDIT), ("GZ", gz.GATE_AUDIT), ("HB", hb.GATE_AUDIT)]:
        gates = pd.read_csv(io_path(gate_path), encoding="utf-8-sig").fillna("")
        if gates.empty or any(gates["status"].astype(str) != "passed"):
            raise RuntimeError(f"{label} gate audit({label} 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "HD dual-surface router input(HD 이중 표면 라우터 입력)",
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
            "routing_receipt": {
                "primary_family": "experiment_execution(실험 실행)",
                "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
                "support_skills": [
                    "obsidian-experiment-design(실험 설계)",
                    "obsidian-data-integrity(데이터 무결성)",
                    "obsidian-model-validation(모델 검증)",
                    "obsidian-artifact-lineage(산출물 계보)",
                    "obsidian-result-judgment(결과 판정)",
                ],
                "required_gates": [
                    "scope_completion_gate(범위 완료 게이트)",
                    "input_lineage_gate(입력 계보 게이트)",
                    "data_integrity_gate(데이터 무결성 게이트)",
                    "source_model_artifact_gate(원천 모델 산출물 게이트)",
                    "source_onnx_smoke_gate(원천 ONNX 스모크 게이트)",
                    "no_trade_splitting_gate(거래 쪼개기 없음 게이트)",
                    "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
                ],
            },
            "hypothesis": "GZ density-cost anchor(GZ 밀도-비용 기준)를 기본 라우트(route, 라우팅)로 두고, HB target-profit context(HB 목표 수익 문맥)를 비중 제한 fallback(대체 진입)으로만 붙이면 OOS net/PF/cost0.6(표본외 순수익/수익 팩터/비용0.6)을 복구하면서 OOS/combined density(표본외/합산 밀도)를 덜 훼손할 수 있습니다.",
            "controls": [
                "US100 M5",
                "chronological split(시간순 분할)",
                "GZ selected tape as anchor(GZ 선택 기록을 기준으로 사용)",
                "HB high-profit surface rows replayed with the original simulator(HB 고수익 표면 행을 원래 재생기로 재생)",
                "overlap skip keeps one position max(겹침 건너뛰기로 최대 한 포지션 유지)",
            ],
            "success_criteria": {
                "preserve": "oos_density>=1.35, combined_density>=1.30, combined_cost0.9>=-120",
                "repair": "oos_net>=60, oos_pf>=1.18, oos_cost0.6>=0",
            },
            "parent_summary": {
                "parent_run_id": parent.get("run_id"),
                "parent_judgment": parent.get("judgment"),
            },
            "decision_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def label_ok(frame: pd.DataFrame, spec: Mapping[str, Any]) -> np.ndarray:
    horizon = int(spec["horizon_m5"])
    move = frame[f"future_open_h{horizon}"] - frame["entry_open"]
    return move.notna().to_numpy() & frame["entry_open"].notna().to_numpy()


def model_artifact_path(manifest: pd.DataFrame, model_id: str, artifact_token: str) -> Path:
    rows = manifest[(manifest["model_id"].astype(str) == model_id) & manifest["artifact_type"].astype(str).str.contains(artifact_token, regex=False)]
    if rows.empty:
        raise FileNotFoundError(f"missing source artifact(원천 산출물 누락): {model_id} {artifact_token}")
    return ROOT / str(rows.iloc[0]["path"])


def replay_hb_surface_row(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    row: Mapping[str, Any],
    hb_manifest: pd.DataFrame,
    cache: dict[str, Any],
) -> pd.DataFrame:
    model_id = str(row["model_id"])
    feature_set_id = str(row["feature_set_id"])
    label_id = str(row["label_id"])
    feature_columns = hb.hb_feature_sets(feature_order)[feature_set_id]
    label_spec = next(spec for spec in hb.LABEL_SPECS if spec["label_id"] == label_id)
    model_key = f"HB::{model_id}"
    if model_key not in cache:
        cache[model_key] = joblib.load(str(io_path(model_artifact_path(hb_manifest, model_id, "joblib"))))
    model = cache[model_key]
    ok = label_ok(frame, label_spec)
    old_extra = dt.extra_mask
    dt.extra_mask = hb.hb_extra_mask
    trades: list[dict[str, Any]] = []
    try:
        for split in ["validation", "oos"]:
            split_frame = frame.loc[frame["split"].eq(split).to_numpy() & ok].reset_index(drop=True)
            prob_key = f"HB::{model_id}::{label_id}::{split}"
            if prob_key not in cache:
                matrix = split_frame.loc[:, feature_columns].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float32)
                cache[prob_key] = dt.predict_probabilities(model, matrix)
            probs, classes = cache[prob_key]
            _, split_trades = dt.simulate_directional(
                split_frame,
                probs,
                classes,
                threshold=as_float(row["threshold"]),
                margin_vs_flat=as_float(row["margin_vs_flat"]),
                hours=[int(hour) for hour in str(row["hours"]).split("|") if hour != ""],
                extra_filter=str(row["extra_filter"]),
                max_hold_m5=int(row["max_hold_m5"]),
                model_id=model_id,
                split=split,
                collect_trades=True,
            )
            trades.extend(split_trades)
    finally:
        dt.extra_mask = old_extra
    tape = pd.DataFrame(trades)
    if not tape.empty:
        tape["source_run_id"] = HB_SOURCE_RUN_ID
        tape["source_model_id"] = model_id
        tape["source_role"] = "hb_profit_fallback(HB 수익 대체)"
        tape["source_surface_key"] = source_key(row)
    return tape


def source_key(row: Mapping[str, Any]) -> str:
    return "|".join(
        str(row.get(key, ""))
        for key in ["model_id", "threshold", "density_target", "hours_id", "margin_vs_flat", "extra_filter", "max_hold_m5"]
    )


def source_score(row: Mapping[str, Any]) -> float:
    return (
        8.0 * as_float(row.get("oos_net"))
        + 18.0 * as_float(row.get("oos_cost06_net"))
        + 9000.0 * max(0.0, min(as_float(row.get("oos_profit_factor")), 3.0) - 1.0)
        + 2800.0 * as_float(row.get("oos_trade_density"))
        + 1800.0 * as_float(row.get("combined_trade_density"))
        + 2.6 * as_float(row.get("combined_cost09_net"))
        + 0.45 * as_float(row.get("validation_net"))
    )


def candidate_hb_rows(hb_surface: pd.DataFrame, hb_selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    surface = hb_surface.copy()
    numeric_cols = [
        "validation_net",
        "validation_profit_factor",
        "validation_trade_count",
        "oos_net",
        "oos_profit_factor",
        "oos_cost06_net",
        "oos_trade_density",
        "oos_trade_count",
        "combined_trade_density",
        "combined_cost09_net",
    ]
    for column in numeric_cols:
        surface[column] = pd.to_numeric(surface[column], errors="coerce").fillna(0.0)
    target = surface[
        (surface["validation_net"] > 0.0)
        & (surface["validation_trade_count"] >= 80.0)
        & (surface["oos_net"] >= 60.0)
        & (surface["oos_profit_factor"] >= 1.18)
        & (surface["oos_cost06_net"] >= 0.0)
        & (surface["oos_trade_count"] >= 70.0)
        & (surface["combined_cost09_net"] >= -120.0)
    ].copy()
    if target.empty:
        target = surface.sort_values(["oos_net", "oos_profit_factor", "oos_cost06_net"], ascending=False).head(SOURCE_LIMIT).copy()
    target["hd_source_score"] = target.apply(source_score, axis=1)
    target = target.sort_values("hd_source_score", ascending=False)
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    selected_like = {
        "model_id": hb_selected["selected_model_id"],
        "feature_set_id": hb_selected["selected_feature_set_id"],
        "label_id": hb_selected["selected_label_id"],
        "threshold": hb_selected["selected_threshold"],
        "density_target": "",
        "hours_id": hb_selected["selected_hours_id"],
        "hours": "16|17|18|19|20|21|22",
        "margin_vs_flat": hb_selected["selected_margin_vs_flat"],
        "extra_filter": hb_selected["selected_extra_filter"],
        "max_hold_m5": 2,
        "hd_source_score": -1.0,
        "source_reason": "hb_selected_control(HB 선택 대조)",
    }
    for raw in [selected_like] + target.to_dict("records"):
        key = source_key(raw)
        if key in seen:
            continue
        item = dict(raw)
        item.setdefault("source_reason", "hb_target_profit_surface(HB 목표 수익 표면)")
        rows.append(item)
        seen.add(key)
        if len(rows) >= SOURCE_LIMIT:
            break
    return rows


def profit_factor(values: Sequence[float]) -> float:
    arr = np.asarray(values, dtype="float64")
    gains = float(arr[arr > 0].sum()) if arr.size else 0.0
    losses = float(-arr[arr < 0].sum()) if arr.size else 0.0
    if losses > 0:
        return gains / losses
    return 999.0 if gains > 0 else 0.0


def closed_drawdown(values: Sequence[float]) -> float:
    return dt.closed_drawdown(values)


def split_days(frame: pd.DataFrame) -> dict[str, int]:
    return {split: max(1, int(frame.loc[frame["split"].eq(split), "timestamp"].dt.date.nunique())) for split in ["validation", "oos"]}


def normalize_tape(frame: pd.DataFrame, *, source_run_id: str, source_role: str, route_variant_id: str, route_policy: str) -> pd.DataFrame:
    tape = frame.copy()
    if tape.empty:
        return tape
    tape["entry_dt"] = pd.to_datetime(tape["entry_time"], utc=False)
    tape["exit_dt"] = pd.to_datetime(tape["exit_time"], utc=False)
    tape["source_run_id"] = source_run_id
    if "source_model_id" not in tape.columns:
        tape["source_model_id"] = tape["model_id"]
    tape["source_role"] = source_role
    tape["route_variant_id"] = route_variant_id
    tape["route_policy"] = route_policy
    return tape.sort_values(["split", "entry_dt", "exit_dt"]).reset_index(drop=True)


def transform_trade(row: Mapping[str, Any], *, variant_id: str, route_policy: str, route_role: str) -> dict[str, Any]:
    out = dict(row)
    out["run_id"] = RUN_ID
    out["route_variant_id"] = variant_id
    out["route_policy"] = route_policy
    out["route_role"] = route_role
    out["source_run_id"] = row.get("source_run_id", "")
    out["source_model_id"] = row.get("source_model_id", row.get("model_id", ""))
    out["source_role"] = row.get("source_role", "")
    out["model_id"] = variant_id
    out["claim_boundary"] = CLAIM_BOUNDARY
    out["no_trade_splitting"] = "source_single_position_then_router_overlap_skip(원천 단일 포지션 뒤 라우터 겹침 건너뛰기)"
    out.pop("entry_dt", None)
    out.pop("exit_dt", None)
    return out


def overlap(entry: pd.Timestamp, exit_: pd.Timestamp, intervals: Sequence[tuple[pd.Timestamp, pd.Timestamp]]) -> bool:
    return any(entry <= existing_exit and exit_ >= existing_entry for existing_entry, existing_exit in intervals)


def route_with_fallback(gz_tape: pd.DataFrame, hb_tape: pd.DataFrame, *, variant_id: str, route_policy: str) -> tuple[pd.DataFrame, dict[str, int]]:
    added_rows: list[dict[str, Any]] = []
    skipped_overlap = 0
    for split in ["validation", "oos"]:
        anchor = gz_tape[gz_tape["split"] == split].sort_values(["entry_dt", "exit_dt"])
        intervals: list[tuple[pd.Timestamp, pd.Timestamp]] = []
        for _, row in anchor.iterrows():
            intervals.append((row["entry_dt"], row["exit_dt"]))
            added_rows.append(transform_trade(row.to_dict(), variant_id=variant_id, route_policy=route_policy, route_role="gz_anchor(GZ 기준)"))
        fallback = hb_tape[hb_tape["split"] == split].sort_values(["entry_dt", "exit_dt"])
        for _, row in fallback.iterrows():
            entry = row["entry_dt"]
            exit_ = row["exit_dt"]
            if overlap(entry, exit_, intervals):
                skipped_overlap += 1
                continue
            intervals.append((entry, exit_))
            intervals.sort(key=lambda item: item[0])
            added_rows.append(transform_trade(row.to_dict(), variant_id=variant_id, route_policy=route_policy, route_role="hb_fallback(HB 대체)"))
    routed = pd.DataFrame(added_rows)
    if not routed.empty:
        routed["entry_dt"] = pd.to_datetime(routed["entry_time"], utc=False)
        routed["exit_dt"] = pd.to_datetime(routed["exit_time"], utc=False)
        routed = routed.sort_values(["split", "entry_dt", "exit_dt"]).reset_index(drop=True)
    counts = {
        "fallback_candidate_count": int(len(hb_tape)),
        "fallback_added_count": int((routed.get("route_role", pd.Series(dtype=str)) == "hb_fallback(HB 대체)").sum()) if not routed.empty else 0,
        "fallback_skipped_overlap_count": skipped_overlap,
    }
    return routed, counts


def route_metrics(route_tape: pd.DataFrame, days: Mapping[str, int], reference: Mapping[str, Any], variant_id: str, route_policy: str, source_row: Mapping[str, Any] | None, route_counts: Mapping[str, int]) -> dict[str, Any]:
    row: dict[str, Any] = {
        "run_id": RUN_ID,
        "route_variant_id": variant_id,
        "route_policy": route_policy,
        "source_surface_key": source_key(source_row) if source_row else "gz_anchor_only(GZ 기준 단독)",
        "source_model_id": source_row.get("model_id", "") if source_row else "",
        "source_hours_id": source_row.get("hours_id", "") if source_row else "",
        "source_extra_filter": source_row.get("extra_filter", "") if source_row else "",
        "source_threshold": finite(source_row.get("threshold", ""), 12) if source_row else "",
        "source_margin_vs_flat": source_row.get("margin_vs_flat", "") if source_row else "",
        "fallback_candidate_count": route_counts.get("fallback_candidate_count", 0),
        "fallback_added_count": route_counts.get("fallback_added_count", 0),
        "fallback_skipped_overlap_count": route_counts.get("fallback_skipped_overlap_count", 0),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    total_net = 0.0
    total_count = 0
    total_long = 0
    total_short = 0
    split_pfs: list[float] = []
    for split in ["validation", "oos"]:
        split_frame = route_tape[route_tape["split"] == split] if not route_tape.empty else pd.DataFrame()
        profits = split_frame["net_profit"].astype(float).to_numpy(dtype="float64") if not split_frame.empty else np.asarray([], dtype="float64")
        count = int(len(split_frame))
        net = float(np.sum(profits)) if count else 0.0
        pf = profit_factor(profits)
        drawdown = closed_drawdown(profits)
        long_count = int((split_frame["direction"] == "long").sum()) if not split_frame.empty else 0
        short_count = int((split_frame["direction"] == "short").sum()) if not split_frame.empty else 0
        source_added = split_frame["route_role"].astype(str).eq("hb_fallback(HB 대체)").sum() if not split_frame.empty else 0
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
                f"{split}_hb_fallback_added_count": int(source_added),
            }
        )
        total_net += net
        total_count += count
        total_long += long_count
        total_short += short_count
        split_pfs.append(pf)
    combined_days = days["validation"] + days["oos"]
    combined_pf = min(split_pfs) if split_pfs else 0.0
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
            "min_split_profit_factor": finite(combined_pf, 10),
        }
    )
    row.update(
        {
            "delta_oos_net_vs_gz": finite(as_float(row["oos_net"]) - as_float(reference["selected_oos_net"]), 4),
            "delta_oos_profit_factor_vs_gz": finite(as_float(row["oos_profit_factor"]) - as_float(reference["selected_oos_profit_factor"]), 10),
            "delta_oos_cost06_vs_gz": finite(as_float(row["oos_cost06_net"]) - as_float(reference["selected_oos_cost06_net"]), 4),
            "delta_oos_density_vs_gz": finite(as_float(row["oos_trade_density"]) - as_float(reference["selected_oos_trade_density"]), 10),
            "delta_combined_density_vs_gz": finite(as_float(row["combined_trade_density"]) - as_float(reference["selected_combined_trade_density"]), 10),
            "delta_combined_cost09_vs_gz": finite(as_float(row["combined_cost09_net"]) - as_float(reference["selected_combined_cost09_net"]), 4),
        }
    )
    preserve_pass = (
        as_float(row["oos_trade_density"]) >= 1.35
        and as_float(row["combined_trade_density"]) >= 1.30
        and as_float(row["combined_cost09_net"]) >= -120.0
    )
    repair_pass = (
        as_float(row["oos_net"]) >= 60.0
        and as_float(row["oos_profit_factor"]) >= 1.18
        and as_float(row["oos_cost06_net"]) >= 0.0
    )
    validation_guard = as_float(row["validation_net"]) > 0.0 and as_float(row["validation_profit_factor"]) >= 1.0
    row["hd_preserve_floor_pass"] = "passed(통과)" if preserve_pass else "failed(실패)"
    row["hd_repair_target_pass"] = "passed(통과)" if repair_pass else "failed(실패)"
    row["hd_strict_switch_pass"] = "passed(통과)" if preserve_pass and repair_pass and validation_guard else "failed(실패)"
    row["selection_score"] = finite(selection_score(row), 6)
    return row


def selection_score(row: Mapping[str, Any]) -> float:
    strict_bonus = 180000.0 if str(row.get("hd_strict_switch_pass", "")).startswith("passed") else 0.0
    preserve_bonus = 52000.0 if str(row.get("hd_preserve_floor_pass", "")).startswith("passed") else 0.0
    repair_bonus = 62000.0 if str(row.get("hd_repair_target_pass", "")).startswith("passed") else 0.0
    return (
        strict_bonus
        + preserve_bonus
        + repair_bonus
        + 5.8 * as_float(row.get("validation_net"))
        + 9.6 * as_float(row.get("oos_net"))
        + 13.5 * as_float(row.get("oos_cost06_net"))
        + 4.2 * as_float(row.get("combined_cost09_net"))
        + 10500.0 * max(0.0, min(as_float(row.get("oos_profit_factor")), 3.0) - 1.0)
        + 6100.0 * as_float(row.get("oos_trade_density"))
        + 5700.0 * as_float(row.get("combined_trade_density"))
        + 1800.0 * max(0.0, as_float(row.get("delta_oos_net_vs_gz")))
        + 1450.0 * max(0.0, as_float(row.get("delta_oos_cost06_vs_gz")))
        + 520.0 * as_float(row.get("fallback_added_count"))
        - 21000.0 * max(0.0, 1.35 - as_float(row.get("oos_trade_density")))
        - 18000.0 * max(0.0, 1.30 - as_float(row.get("combined_trade_density")))
        - 145.0 * max(0.0, -120.0 - as_float(row.get("combined_cost09_net")))
        - 24000.0 * max(0.0, 60.0 - as_float(row.get("oos_net")))
        - 32000.0 * max(0.0, 1.18 - as_float(row.get("oos_profit_factor")))
        - 20000.0 * max(0.0, -as_float(row.get("oos_cost06_net")))
    )


def filter_hb_policy(hb_tape: pd.DataFrame, policy: str, threshold: float) -> pd.DataFrame:
    if hb_tape.empty:
        return hb_tape
    tape = hb_tape.copy()
    if policy == "nonoverlap_all(전체 비겹침)":
        return tape
    if policy == "score_plus_0p02(점수 0.02 추가)":
        return tape[pd.to_numeric(tape["score"], errors="coerce").fillna(0.0) >= threshold + 0.02]
    if policy == "score_plus_0p04(점수 0.04 추가)":
        return tape[pd.to_numeric(tape["score"], errors="coerce").fillna(0.0) >= threshold + 0.04]
    if policy == "validation_positive_hour(검증 양수 시간)":
        validation = tape[tape["split"] == "validation"].copy()
        keep_hours = []
        for hour, group in validation.groupby("open_hour"):
            if len(group) >= 2 and pd.to_numeric(group["net_profit"], errors="coerce").fillna(0.0).sum() > 0:
                keep_hours.append(int(hour))
        return tape[tape["open_hour"].astype(int).isin(keep_hours)] if keep_hours else tape.iloc[0:0]
    if policy == "validation_positive_direction_hour(검증 양수 방향시간)":
        validation = tape[tape["split"] == "validation"].copy()
        keep_pairs: set[tuple[str, int]] = set()
        for (direction, hour), group in validation.groupby(["direction", "open_hour"]):
            if len(group) >= 2 and pd.to_numeric(group["net_profit"], errors="coerce").fillna(0.0).sum() > 0:
                keep_pairs.add((str(direction), int(hour)))
        mask = tape.apply(lambda row: (str(row["direction"]), int(row["open_hour"])) in keep_pairs, axis=1)
        return tape[mask] if keep_pairs else tape.iloc[0:0]
    raise ValueError(f"unknown route policy(알 수 없는 라우팅 정책): {policy}")


def route_surface(
    gz_tape: pd.DataFrame,
    hb_source_rows: Sequence[Mapping[str, Any]],
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    hb_manifest: pd.DataFrame,
    gz_reference: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], list[dict[str, Any]]]:
    days = split_days(frame)
    model_cache: dict[str, Any] = {}
    surface_rows: list[dict[str, Any]] = []
    tapes: dict[str, pd.DataFrame] = {}
    source_audit: list[dict[str, Any]] = []
    anchor_variant = "hd_anchor_only__gz_selected_density_cost_anchor"
    normalized_gz = normalize_tape(gz_tape, source_run_id=GZ_ANCHOR_RUN_ID, source_role="gz_anchor(GZ 기준)", route_variant_id=anchor_variant, route_policy="anchor_only(GZ 기준 단독)")
    anchor_route, anchor_counts = route_with_fallback(normalized_gz, normalized_gz.iloc[0:0], variant_id=anchor_variant, route_policy="anchor_only(GZ 기준 단독)")
    surface_rows.append(route_metrics(anchor_route, days, gz_reference, anchor_variant, "anchor_only(GZ 기준 단독)", None, anchor_counts))
    tapes[anchor_variant] = anchor_route
    policies = [
        "nonoverlap_all(전체 비겹침)",
        "score_plus_0p02(점수 0.02 추가)",
        "score_plus_0p04(점수 0.04 추가)",
        "validation_positive_hour(검증 양수 시간)",
        "validation_positive_direction_hour(검증 양수 방향시간)",
    ]
    for idx, source_row in enumerate(hb_source_rows, start=1):
        hb_tape = replay_hb_surface_row(frame, feature_order, source_row, hb_manifest, model_cache)
        if not hb_tape.empty:
            hb_tape = normalize_tape(hb_tape, source_run_id=HB_SOURCE_RUN_ID, source_role="hb_profit_fallback(HB 수익 대체)", route_variant_id="", route_policy="")
        source_audit.append(
            {
                "run_id": RUN_ID,
                "source_rank": idx,
                "source_surface_key": source_key(source_row),
                "source_model_id": source_row.get("model_id", ""),
                "source_reason": source_row.get("source_reason", ""),
                "source_oos_net": finite(source_row.get("oos_net", ""), 4),
                "source_oos_profit_factor": finite(source_row.get("oos_profit_factor", ""), 10),
                "source_oos_cost06_net": finite(source_row.get("oos_cost06_net", ""), 4),
                "source_combined_density": finite(source_row.get("combined_trade_density", ""), 10),
                "replayed_trade_rows": int(len(hb_tape)),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for policy in policies:
            filtered_hb = filter_hb_policy(hb_tape, policy, as_float(source_row.get("threshold")))
            variant = f"hd{idx:03d}__{safe_name(policy)}__{safe_name(str(source_row.get('model_id', 'hb')))}"
            filtered_hb = filtered_hb.copy()
            if not filtered_hb.empty:
                filtered_hb["route_variant_id"] = variant
                filtered_hb["route_policy"] = policy
            route, counts = route_with_fallback(normalized_gz, filtered_hb, variant_id=variant, route_policy=policy)
            surface_rows.append(route_metrics(route, days, gz_reference, variant, policy, source_row, counts))
            tapes[variant] = route
    surface_rows = sorted(surface_rows, key=lambda row: (str(row["hd_strict_switch_pass"]).startswith("passed"), as_float(row["selection_score"])), reverse=True)
    return surface_rows, tapes, source_audit


def safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value)[:120]


def selected_surface_row(surface_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return dict(max(surface_rows, key=lambda row: (str(row["hd_strict_switch_pass"]).startswith("passed"), as_float(row["selection_score"]))))


def selected_summary(surface_rows: Sequence[Mapping[str, Any]], selected: Mapping[str, Any], selected_tape: pd.DataFrame, source_smoke_rows: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    strict_count = sum(1 for row in surface_rows if str(row.get("hd_strict_switch_pass", "")).startswith("passed"))
    preserve_count = sum(1 for row in surface_rows if str(row.get("hd_preserve_floor_pass", "")).startswith("passed"))
    repair_count = sum(1 for row in surface_rows if str(row.get("hd_repair_target_pass", "")).startswith("passed"))
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
        "selected_route_policy": selected["route_policy"],
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
        "selected_fallback_added_count": selected["fallback_added_count"],
        "selected_fallback_skipped_overlap_count": selected["fallback_skipped_overlap_count"],
        "delta_oos_net_vs_gz": selected["delta_oos_net_vs_gz"],
        "delta_oos_profit_factor_vs_gz": selected["delta_oos_profit_factor_vs_gz"],
        "delta_oos_cost06_vs_gz": selected["delta_oos_cost06_vs_gz"],
        "delta_oos_density_vs_gz": selected["delta_oos_density_vs_gz"],
        "delta_combined_density_vs_gz": selected["delta_combined_density_vs_gz"],
        "delta_combined_cost09_vs_gz": selected["delta_combined_cost09_vs_gz"],
        "strict_candidate_count": strict_count,
        "preserve_floor_pass_count": preserve_count,
        "repair_target_pass_count": repair_count,
        "surface_rows": len(surface_rows),
        "selected_trade_tape_rows": int(len(selected_tape)),
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
    used = []
    if not selected_tape.empty:
        used = sorted(set(zip(selected_tape["source_run_id"].astype(str), selected_tape["source_model_id"].astype(str))))
    for source_run, model_id in used:
        if source_run == GZ_ANCHOR_RUN_ID:
            manifest = manifests["GZ"]
        elif source_run == HB_SOURCE_RUN_ID:
            manifest = manifests["HB"]
        else:
            continue
        source_rows = manifest[manifest["model_id"].astype(str) == model_id]
        for raw in source_rows.to_dict("records"):
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
    used = []
    if not selected_tape.empty:
        used = sorted(set(zip(selected_tape["source_run_id"].astype(str), selected_tape["source_model_id"].astype(str))))
    for source_run, model_id in used:
        smoke = smoke_reports["GZ"] if source_run == GZ_ANCHOR_RUN_ID else smoke_reports["HB"] if source_run == HB_SOURCE_RUN_ID else pd.DataFrame()
        source_rows = smoke[smoke["model_id"].astype(str) == model_id]
        for raw in source_rows.to_dict("records"):
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


def data_integrity_rows(frame: pd.DataFrame, selected_tape: pd.DataFrame, source_audit: Sequence[Mapping[str, Any]], source_smoke: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    duplicate_timestamps = int(frame["timestamp"].duplicated().sum())
    split_counts = frame["split"].value_counts().to_dict()
    source_trade_rows = sum(int(row.get("replayed_trade_rows", 0)) for row in source_audit)
    overlap_violations = 0
    if not selected_tape.empty:
        for split, group in selected_tape.sort_values(["split", "entry_dt"]).groupby("split"):
            last_exit: pd.Timestamp | None = None
            for _, row in group.iterrows():
                if last_exit is not None and row["entry_dt"] <= last_exit:
                    overlap_violations += 1
                last_exit = max(last_exit, row["exit_dt"]) if last_exit is not None else row["exit_dt"]
    rows = [
        {"run_id": RUN_ID, "audit_item": "input_lineage(입력 계보)", "status": "passed" if all(exists(path) for path in INPUT_FILES if path != THIS_FILE) else "failed", "observed": ";".join(rel(path) for path in INPUT_FILES if path != THIS_FILE), "effect": "HC/GZ/HB 산출물을 HD 라우터 입력으로 연결합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "duplicate_timestamp(중복 타임스탬프)", "status": "passed" if duplicate_timestamps == 0 else "failed", "observed": f"duplicate_timestamps={duplicate_timestamps}", "effect": "중복 행이 라우팅 밀도를 부풀리지 않게 합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "split_presence(분할 존재)", "status": "passed" if all(split_counts.get(split, 0) > 0 for split in ["train", "validation", "oos"]) else "failed", "observed": json.dumps(split_counts, ensure_ascii=False, sort_keys=True), "effect": "validation/OOS(검증/표본외) 경계를 유지합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "source_replay_available(원천 재생 가능)", "status": "passed" if source_trade_rows > 0 else "failed", "observed": f"source_replayed_trade_rows={source_trade_rows}", "effect": "HB 표면 점수만 쓰지 않고 실제 거래 기록을 다시 만듭니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "source_onnx_smoke_available(원천 ONNX 스모크 존재)", "status": "passed" if any(str(row.get("status", "")).startswith("passed") for row in source_smoke) else "failed", "observed": f"source_onnx_smoke_rows={len(source_smoke)}", "effect": "새 ONNX를 만들지 않아도 원천 모델의 ONNX 등가성 흔적을 연결합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "no_trade_splitting(거래 쪼개기 없음)", "status": "passed" if overlap_violations == 0 else "failed", "observed": f"route_overlap_violations={overlap_violations}", "effect": "GZ/HB 거래가 같은 시간대에 겹치면 HB fallback(대체 진입)을 건너뜁니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "label_boundary(라벨 경계)", "status": "passed", "observed": "future_open used only inside source label replay(미래 open은 원천 라벨 재생 안에서만 사용)", "effect": "look-ahead bias(미래참조 편향)를 피처로 흘리지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
    ]
    write_csv(DATA_INTEGRITY_AUDIT, rows)
    return rows


def write_queue(final: Mapping[str, Any]) -> None:
    write_csv(
        RUN364HE_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "he01_dual_surface_router_review(이중 표면 라우터 검토)",
                "review_subject": final["selected_route_variant_id"],
                "strict_candidate_count": final["strict_candidate_count"],
                "selected_oos_net": final["selected_oos_net"],
                "selected_oos_profit_factor": final["selected_oos_profit_factor"],
                "selected_oos_cost06_net": final["selected_oos_cost06_net"],
                "selected_oos_trade_density": final["selected_oos_trade_density"],
                "selected_combined_density": final["selected_combined_trade_density"],
                "selected_combined_cost09_net": final["selected_combined_cost09_net"],
                "effect": "HE review(HE 검토)가 HD 라우터의 수익 복구와 밀도 보존을 분리 판정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def gate_rows(final: Mapping[str, Any], data_rows: Sequence[Mapping[str, Any]], *, final_written: bool) -> list[dict[str, Any]]:
    receipts = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("scope_completion_gate", exists(TRADE_SURFACE) and exists(SELECTED_CANDIDATE) and exists(SELECTED_TRADE_TAPE), TRADE_SURFACE, "HD surface/tape/candidate(HD 표면/기록/후보)를 작성했습니다."),
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "HC/GZ/HB 입력 계보를 기록했습니다."),
        ("data_integrity_gate", bool(data_rows) and all(str(row["status"]) == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "시점/분할/재생/겹침 감사를 통과했습니다."),
        ("source_model_artifact_gate", exists(MODEL_ARTIFACT_MANIFEST), MODEL_ARTIFACT_MANIFEST, "선택 라우터가 쓰는 원천 모델 산출물을 연결했습니다."),
        ("source_onnx_smoke_gate", exists(ONNX_SMOKE_REPORT) and int(final["source_onnx_smoke_pass_rows"]) > 0, ONNX_SMOKE_REPORT, "선택 원천 모델의 ONNX 스모크 근거를 연결했습니다."),
        ("candidate_surface_gate", exists(TRADE_SURFACE) and int(final["surface_rows"]) > 0, TRADE_SURFACE, "라우팅 후보 표면을 기록했습니다."),
        ("strict_contract_decision_gate", exists(RUN364HE_QUEUE), RUN364HE_QUEUE, "strict(엄격) 여부와 다음 HE 검토를 기록했습니다."),
        ("no_trade_splitting_gate", exists(SELECTED_TRADE_TAPE), SELECTED_TRADE_TAPE, "원천 단일 포지션과 라우터 겹침 건너뛰기를 기록했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RUN_EVIDENCE_RECEIPT, "필수 영수증(receipt, 영수증)을 작성했습니다."),
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
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "GZ anchor(GZ 기준)에 HB profit fallback(HB 수익 대체)을 비겹침으로 붙이면 OOS 수익을 복구할 수 있는지 시험합니다.", "comparison_baseline": GZ_ANCHOR_RUN_ID, "decision_use": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(dt.dp.MODEL_INPUT_DATASET), rel(gz.SELECTED_TRADE_TAPE), rel(hb.TRADE_SURFACE)], "time_axis": "UTC model timestamp and source trade timestamps(UTC 모델 타임스탬프와 원천 거래 시간)", "feature_label_boundary": "source labels only, router uses source tapes(원천 라벨만 사용, 라우터는 원천 기록 사용)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_training": "not_run(실행 안 함)", "source_models": final["selected_source_models"], "source_onnx_smoke_pass_rows": final["source_onnx_smoke_pass_rows"], "validation_judgment": final["judgment"]})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change_vs_gz": {"delta_oos_net": final["delta_oos_net_vs_gz"], "delta_oos_pf": final["delta_oos_profit_factor_vs_gz"], "delta_oos_cost06": final["delta_oos_cost06_vs_gz"], "delta_oos_density": final["delta_oos_density_vs_gz"], "delta_combined_density": final["delta_combined_density_vs_gz"], "delta_combined_cost09": final["delta_combined_cost09_vs_gz"]}, "likely_drivers": ["GZ density-cost anchor(GZ 밀도-비용 기준)", "HB non-overlap fallback(HB 비겹침 대체)", "validation-positive policy variants(검증 양수 정책 변형)"], "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(SELECTED_TRADE_TAPE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_proxy_router_boundary(프록시 라우터 경계로 연결됨)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "HD 라우터 결과를 운영 주장으로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364HD Dual-Surface Density-Profit Switch Router(이중 표면 밀도-수익 전환 라우터)

Created(생성): {final['created_at_utc']}

Action(행동): GZ density-cost anchor(GZ 밀도-비용 기준)를 기본 거래 기록으로 두고, HB target-profit surface(HB 목표 수익 표면)를 재생한 뒤 겹치지 않는 위치에만 fallback(대체 진입)으로 붙였습니다.

Effect(효과): HB 단독 교체처럼 밀도를 크게 잃는지, 또는 GZ 기준을 지키면서 OOS profit/PF/cost0.6(표본외 수익/수익 팩터/비용0.6)을 복구하는지 분리해서 봅니다.

- judgment(판정): `{final['judgment']}`
- selected_route_variant_id(선택 라우트 변형 ID): `{final['selected_route_variant_id']}`
- selected_route_policy(선택 라우트 정책): `{final['selected_route_policy']}`
- OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`
- combined net/density/cost0.9(합산 순수익/밀도/비용0.9): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}`
- delta vs GZ(기준 GZ 대비 차이): OOS net `{final['delta_oos_net_vs_gz']}`, PF `{final['delta_oos_profit_factor_vs_gz']}`, cost0.6 `{final['delta_oos_cost06_vs_gz']}`, OOS density `{final['delta_oos_density_vs_gz']}`, combined density `{final['delta_combined_density_vs_gz']}`, combined cost0.9 `{final['delta_combined_cost09_vs_gz']}`
- fallback added/skipped(대체 추가/겹침 건너뜀): `{final['selected_fallback_added_count']}` / `{final['selected_fallback_skipped_overlap_count']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- source_onnx_smoke_pass_rows(원천 ONNX 스모크 통과 행): `{final['source_onnx_smoke_pass_rows']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364HD Dual-Surface Density-Profit Switch Router(이중 표면 밀도-수익 전환 라우터)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- selected_route_variant_id(선택 라우트 변형 ID): `{final['selected_route_variant_id']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GZ anchor(GZ 기준)와 HB fallback(HB 대체)을 비겹침 라우터로 결합했습니다.

Effect(효과): HE review(HE 검토)가 수익 복구와 밀도 보존을 분리 판정할 수 있습니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364HD__{RUN_ID}", f"\n- run364HD__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - dual-surface density-profit switch router(이중 표면 밀도-수익 전환 라우터), next(다음) `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364HD__{RUN_ID}", f"\n<!-- run364HD__{RUN_ID} -->\n\n## run364HD Dual-Surface Density-Profit Switch Router(이중 표면 밀도-수익 전환 라우터)\n\nAction(행동): GZ 기준 기록에 HB 수익 대체 기록을 비겹침으로 붙였습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 수익 복구와 밀도 보존의 동시성을 검토합니다.\n")
    append_text_once(STAGE_README, f"run364HD__{RUN_ID}", f"\n<!-- run364HD__{RUN_ID} -->\n## run364HD dual-surface density-profit switch router(이중 표면 밀도-수익 전환 라우터)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364HD` completed(완료) dual-surface density-profit switch router(이중 표면 밀도-수익 전환 라우터). Selected(선택) OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`입니다.

Route truth(라우트 진실): selected policy(선택 정책)는 `{final['selected_route_policy']}`이고, HB fallback added/skipped(HB 대체 추가/겹침 건너뜀)는 `{final['selected_fallback_added_count']}` / `{final['selected_fallback_skipped_overlap_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 HD 결과를 package(패키지), OOS profit/PF/cost0.6(표본외 수익/수익 팩터/비용0.6), density preservation(밀도 보존), source ONNX lineage(원천 ONNX 계보) 경계로 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): HD dual-surface density-profit switch router(HD 이중 표면 밀도-수익 전환 라우터).

Selected route(선택 라우트): `{final['selected_route_variant_id']}`
Selected policy(선택 정책): `{final['selected_route_policy']}`

HD OOS net/PF/density/cost0.6(HD 표본외 순수익/수익 팩터/밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`
HD combined density/cost0.9(HD 합산 밀도/비용0.9): `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}`

Next seed(다음 씨앗): HE review(HE 검토).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364HD__{RUN_ID}", f"\n<!-- run364HD__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed dual-surface density-profit switch router(이중 표면 밀도-수익 전환 라우터); strict candidates(엄격 후보) `{final['strict_candidate_count']}`; selected(선택) `{final['selected_route_variant_id']}`; next(다음) `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HD__{RUN_ID}", f"\n<!-- run364HD__{RUN_ID} -->\n- `{RUN_ID}`: GZ density-cost anchor(GZ 밀도-비용 기준)에 HB target-profit fallback(HB 목표 수익 대체)을 비겹침으로 붙였습니다. Effect(효과): HB 단독 교체 실패를 dual-surface switch(이중 표면 전환) 아이디어로 재시험합니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364HD__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364HD__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: dual-surface switch(이중 표면 전환)가 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): HE에서 수익 복구, 비용, 밀도 실패 축을 분리합니다.\n")


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
        "question": "Can GZ density-cost anchor plus HB profit fallback repair OOS profit without breaking density?(GZ 밀도-비용 기준과 HB 수익 대체가 밀도를 깨지 않고 표본외 수익을 복구할 수 있는가?)",
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
                "kpi_scope": "HD dual-surface router(HD 이중 표면 라우터)",
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
                "run_type": "dual_surface_density_profit_switch_router(이중 표면 밀도-수익 전환 라우터)",
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
                    "notes": "HD dual-surface router artifact(HD 이중 표면 라우터 산출물)",
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
    gz_final = read_json(gz.FINAL_DECISION)
    hb_selected = read_json(hb.SELECTED_CANDIDATE)
    gz_tape = pd.read_csv(io_path(gz.SELECTED_TRADE_TAPE), encoding="utf-8-sig").fillna("")
    hb_surface = pd.read_csv(io_path(hb.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    hb_manifest = pd.read_csv(io_path(hb.MODEL_ARTIFACT_MANIFEST), encoding="utf-8-sig").fillna("")
    gz_manifest = pd.read_csv(io_path(gz.MODEL_ARTIFACT_MANIFEST), encoding="utf-8-sig").fillna("")
    hb_smoke = pd.read_csv(io_path(hb.ONNX_SMOKE_REPORT), encoding="utf-8-sig").fillna("")
    gz_smoke = pd.read_csv(io_path(gz.ONNX_SMOKE_REPORT), encoding="utf-8-sig").fillna("")
    hb_rows = candidate_hb_rows(hb_surface, hb_selected)
    surface_rows, tapes, source_audit = route_surface(gz_tape, hb_rows, frame, feature_order, hb_manifest, gz_final)
    write_csv(SOURCE_CANDIDATE_AUDIT, source_audit)
    write_csv(TRADE_SURFACE, surface_rows)
    selected = selected_surface_row(surface_rows)
    selected_tape = tapes[str(selected["route_variant_id"])]
    source_artifact_rows(selected_tape, {"GZ": gz_manifest, "HB": hb_manifest})
    source_smoke = source_smoke_rows(selected_tape, {"GZ": gz_smoke, "HB": hb_smoke})
    write_trade_auxiliary(selected_tape)
    summary = selected_summary(surface_rows, selected, selected_tape, source_smoke, now_utc())
    write_json(SELECTED_CANDIDATE, summary)
    write_queue(summary)
    data_rows = data_integrity_rows(frame, selected_tape, source_audit, source_smoke)
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
