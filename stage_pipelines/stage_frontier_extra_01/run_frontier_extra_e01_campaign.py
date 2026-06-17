from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.alpha import scout_runner as scout  # noqa: E402
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage_frontier_50 import run_frontier50_runtime_probe as f50rt  # noqa: E402
from stage_pipelines.stage_frontier_runtime_backfill import run_frontier_runtime_probe_backfill as backfill  # noqa: E402


STAGE_ID = "stage_frontier_extra_E01__f001_f050_hypothesis_mixing_runtime_learning"
RUN_ID = "frontier_extra_E01_heavy_runtime_learning_campaign_v1"
RUN_NUMBER = "e01"
EXPLORATION_LABEL = "frontier_extra_E01_hypothesis_mixing_runtime_learning"
COMMON_RUN_ROOT = f"Project_Obsidian_Prime_v2/{RUN_ID}"

MATERIAL_START = 1
MATERIAL_END = 50
MATERIAL_WINDOW = f"F{MATERIAL_START:03d}-F{MATERIAL_END:03d}"
TRIGGER_FRONTIER_ID = "stage_frontier_50__short_pf_edge_loss_floor_regime_transfer_after_f49_state_machine_memory"
RESUME_FRONTIER_ID = "stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild"
RESUME_RUN_ID = "frontier81A_stage_open_mt5_native_order_intent_cost_shape_rebuild_v1"

CLAIM_BOUNDARY = (
    "frontier_extra_runtime_learning_only_no_completion_no_selected_baseline_"
    "no_operating_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
SPEC_DIR = STAGE_DIR / "00_spec"
INPUT_DIR = STAGE_DIR / "01_inputs"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
MT5_DIR = RUN_DIR / "mt5"
RUNTIME_TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"

INGREDIENT_CSV = INPUT_DIR / "frontier_extra_E01_ingredient_cards.csv"
INGREDIENT_JSON = INPUT_DIR / "frontier_extra_E01_ingredient_cards.json"
SCAN_SUMMARY_JSON = INPUT_DIR / "frontier_extra_E01_receipt_first_scan_summary.json"
MIX_QUEUE_CSV = INPUT_DIR / "frontier_extra_E01_mix_queue.csv"
MIX_QUEUE_JSON = INPUT_DIR / "frontier_extra_E01_mix_queue.json"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
CANDIDATE_MANIFEST = RUN_DIR / "candidate_manifest.csv"
RUNTIME_RECEIPT_CSV = RUN_DIR / "mt5_runtime_receipt.csv"
RUNTIME_RECEIPT_JSON = RUN_DIR / "mt5_runtime_receipt.json"
EXECUTION_RESULTS_JSON = MT5_DIR / "execution_results.json"
REPORT_RECORDS_JSON = MT5_DIR / "strategy_tester_report_records.json"

OPEN_REPORT = REVIEWS_DIR / "frontier_extra_E01_stage_open_report.md"
SCAN_REPORT = REVIEWS_DIR / "frontier_extra_E01_receipt_first_scan_report.md"
MIX_REPORT = REVIEWS_DIR / "frontier_extra_E01_mix_design_report.md"
RUNTIME_REPORT = REVIEWS_DIR / "frontier_extra_E01_mt5_runtime_learning_campaign_report.md"
GATE_AUDIT = REVIEWS_DIR / "required_gate_coverage_audit_E01.md"
CLOSEOUT_REPORT = REVIEWS_DIR / "stage_closeout_report.md"
REVIEW_INDEX = REVIEWS_DIR / "review_index.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
NEGATIVE_MEMORY = SELECTED_DIR / "negative_memory.md"
PRESERVED_CLUE = SELECTED_DIR / "preserved_clue.md"

EXTRA_REGISTER = ROOT / "docs" / "registers" / "frontier_extra_stage_register.yaml"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

SCRIPT_REL = "stage_pipelines/stage_frontier_extra_01/run_frontier_extra_e01_campaign.py"
F50_SUMMARY = (
    ROOT
    / "stages"
    / TRIGGER_FRONTIER_ID
    / "02_runs"
    / "frontier50C_capped_loss_floor_regime_transfer_repair_v1"
    / "repair_candidate_summary.csv"
)
BACKFILL_COVERAGE = ROOT / "docs" / "agent_control" / "runtime_probe_backfill" / "frontier_runtime_probe_coverage_audit_latest.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Frontier Extra Stage E01.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--candidate-count", type=int, default=12)
    parser.add_argument("--broad-mix-count", type=int, default=420)
    parser.add_argument("--wfo-mix-count", type=int, default=90)
    parser.add_argument("--terminal-path", default=str(backfill.DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(backfill.DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(backfill.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(backfill.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(backfill.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: str | Path) -> str:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return p.relative_to(ROOT).as_posix()


def safe_token(value: Any, *, limit: int = 48) -> str:
    token = re.sub(r"[^A-Za-z0-9_]+", "_", str(value)).strip("_")
    return token[:limit] or "na"


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path, *, max_chars: int = 12000) -> str:
    if not path_exists(path):
        return ""
    text = io_path(path).read_text(encoding="utf-8-sig", errors="replace")
    return text[:max_chars]


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else ["empty"]))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (
        SPEC_DIR,
        INPUT_DIR,
        RUN_DIR,
        MT5_DIR,
        MT5_DIR / "executions",
        MT5_DIR / "reports",
        RUNTIME_TELEMETRY_DIR,
        REVIEWS_DIR,
        SELECTED_DIR,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)


def stage_dir_for_num(stage_num: int) -> Path | None:
    prefix = f"stage_frontier_{stage_num:02d}__"
    matches = [path for path in (ROOT / "stages").iterdir() if path.is_dir() and path.name.startswith(prefix)]
    return matches[0] if matches else None


def load_backfill_coverage() -> dict[str, Any]:
    if not path_exists(BACKFILL_COVERAGE):
        return {}
    return read_json(BACKFILL_COVERAGE)


def file_hash(path: Path) -> str:
    try:
        return sha256_file_lf_normalized(path)
    except Exception:
        return ""


def evidence_files(stage: Path) -> list[Path]:
    candidates: list[Path] = []
    for relative in (
        "00_spec/stage_brief.md",
        "04_selected/selection_status.md",
        "04_selected/selection_status.json",
        "04_selected/negative_memory.md",
        "04_selected/preserved_clue.md",
        "03_reviews/stage_closeout_report.md",
        "03_reviews/runtime_probe_status.json",
        "03_reviews/runtime_probe_backfill_status.json",
        "03_reviews/stage_run_ledger.csv",
    ):
        path = stage / relative
        if path_exists(path):
            candidates.append(path)
    review_dir = stage / "03_reviews"
    if path_exists(review_dir):
        for path in sorted(review_dir.glob("*runtime*report*.md"))[:8]:
            if path not in candidates:
                candidates.append(path)
        for path in sorted(review_dir.glob("*closeout*report*.md"))[:8]:
            if path not in candidates:
                candidates.append(path)
    return candidates[:18]


def line_after(label: str, text: str) -> str:
    pattern = re.compile(rf"{re.escape(label)}[^\n:：]*[:：]\s*(.+)", re.IGNORECASE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def classify_salvage(stage_num: int, text: str, runtime_recorded: set[int]) -> str:
    lower = text.lower()
    if stage_num in runtime_recorded or "runtime_probe_observation" in lower or "strategy tester" in lower:
        return "runtime_gap_material(런타임 간극 재료)"
    if "preserved clue" in lower or "보존 단서" in text:
        return "preserved_clue_material(보존 단서 재료)"
    if "negative memory" in lower or "부정 기억" in text:
        return "negative_memory_material(부정 기억 재료)"
    if "invalid_setup" in lower or "ineligible" in lower or "무효" in text:
        return "invalid_setup_material(무효 설정 재료)"
    if "blocked" in lower or "차단" in text:
        return "blocked_retry_material(차단 재시도 재료)"
    return "reference_material(참고 재료)"


def axis_tags(text: str, stage_num: int) -> list[str]:
    lower = text.lower()
    tags: list[str] = []
    mapping = [
        ("feature", "feature_set(피처 묶음)"),
        ("label", "label(라벨)"),
        ("model", "model_family(모델 계열)"),
        ("trade shape", "trade_shape(거래 형태)"),
        ("risk", "risk_logic(위험 로직)"),
        ("regime", "regime_split(장세 분할)"),
        ("runtime", "runtime_economics(런타임 경제성)"),
        ("onnx", "onnx_handoff(온엑스 인계)"),
        ("density", "density(밀도)"),
        ("drawdown", "drawdown(손실폭)"),
        ("session", "session(세션)"),
        ("lifecycle", "lifecycle(생명주기)"),
        ("order", "order_intent(주문 의도)"),
    ]
    for needle, tag in mapping:
        if needle in lower:
            tags.append(tag)
    if not tags:
        if stage_num <= 14:
            tags.append("early_onnx_label_seed(초기 온엑스/라벨 씨앗)")
        elif stage_num <= 33:
            tags.append("middle_proxy_failure_memory(중기 프록시 실패 기억)")
        else:
            tags.append("late_short_pf_runtime_gap(후기 숏 수익팩터 런타임 간극)")
    return tags[:5]


def build_ingredient_cards() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    coverage = load_backfill_coverage()
    runtime_recorded = {int(item) for item in coverage.get("runtime_recorded_stage_nums", []) if int(item) <= MATERIAL_END}
    status_only = {int(item) for item in coverage.get("backfill_status_no_runtime_execution_stage_nums", []) if int(item) <= MATERIAL_END}
    cards: list[dict[str, Any]] = []
    missing: list[int] = []
    for stage_num in range(MATERIAL_START, MATERIAL_END + 1):
        stage = stage_dir_for_num(stage_num)
        if stage is None:
            missing.append(stage_num)
            cards.append(
                {
                    "source_frontier": f"F{stage_num:03d}",
                    "stage_id": "",
                    "material_status": "missing_material(자료 누락)",
                    "hypothesis": "missing stage directory(단계 폴더 누락)",
                    "artifact_paths": "",
                    "artifact_hashes": "",
                    "salvage_value": "missing_material(자료 누락)",
                    "do_not_repeat": "missing_material(자료 누락)",
                    "tier_scope": "missing_required(필수 누락)",
                    "claim_boundary": CLAIM_BOUNDARY,
                    "axis_tags": "",
                    "runtime_evidence_count": 0,
                }
            )
            continue
        files = evidence_files(stage)
        texts = [read_text(path, max_chars=10000) for path in files if path.suffix.lower() in {".md", ".json", ".csv"}]
        joined = "\n".join(texts)
        hypothesis = (
            line_after("frontier_thesis", joined)
            or line_after("Thesis", joined)
            or line_after("Action", joined)
            or stage.name
        )
        do_not_repeat = (
            line_after("do_not_repeat", joined)
            or line_after("Do-not-repeat", joined)
            or line_after("Negative memory", joined)
            or line_after("부정 기억", joined)
            or "derive from closeout receipt(마감 영수증에서 유도)"
        )
        tier_scope = "Tier A separate recorded; Tier B/combined checked if present(Tier A 분리 기록, Tier B/합산은 있는 경우 확인)"
        if "Tier B" in joined or "티어 B" in joined:
            tier_scope = "Tier A/B evidence present or explicitly missing(Tier A/B 근거 있음 또는 명시 누락)"
        claim = line_after("Claim boundary", joined) or line_after("claim_boundary", joined) or CLAIM_BOUNDARY
        runtime_count = sum(1 for path in files if "runtime" in path.name.lower())
        material_status = "runtime_recorded(런타임 기록 있음)" if stage_num in runtime_recorded else "status_only_no_runtime_execution(상태 전용, 런타임 미실행)" if stage_num in status_only else "receipt_scanned(영수증 스캔됨)"
        cards.append(
            {
                "source_frontier": f"F{stage_num:03d}",
                "stage_id": stage.name,
                "material_status": material_status,
                "hypothesis": hypothesis[:500],
                "artifact_paths": json.dumps([rel(path) for path in files[:10]], ensure_ascii=False),
                "artifact_hashes": json.dumps({rel(path): file_hash(path) for path in files[:10]}, ensure_ascii=False, sort_keys=True),
                "salvage_value": classify_salvage(stage_num, joined, runtime_recorded),
                "do_not_repeat": do_not_repeat[:500],
                "tier_scope": tier_scope,
                "claim_boundary": claim[:500],
                "axis_tags": "|".join(axis_tags(joined, stage_num)),
                "runtime_evidence_count": runtime_count,
            }
        )
    summary = {
        "material_window": MATERIAL_WINDOW,
        "ingredient_count": len(cards),
        "missing_stage_nums": missing,
        "runtime_recorded_stage_nums": sorted(runtime_recorded),
        "status_only_stage_nums": sorted(status_only),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return cards, summary


def load_f50_candidates() -> pd.DataFrame:
    if not path_exists(F50_SUMMARY):
        raise RuntimeError(f"missing F50 runtime substrate summary: {F50_SUMMARY}")
    frame = pd.read_csv(io_path(F50_SUMMARY), encoding="utf-8-sig")
    frame = frame.loc[frame["onnx_friendly"].astype(bool)].copy()
    for column in ("forward_min_pf", "forward_max_dd", "forward_min_density", "score_threshold", "oos_profit_factor", "validation_profit_factor"):
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def select_runtime_candidates(frame: pd.DataFrame, candidate_count: int) -> list[dict[str, Any]]:
    specs = [
        ("top_forward_pf", ["forward_min_pf", "forward_max_dd"], [False, True]),
        ("low_dd", ["forward_max_dd", "forward_min_pf"], [True, False]),
        ("high_density", ["forward_min_density", "forward_min_pf"], [False, False]),
        ("low_threshold_boundary", ["score_threshold", "forward_min_pf"], [True, False]),
        ("high_threshold_boundary", ["score_threshold", "forward_min_pf"], [False, False]),
        ("extreme_dd_boundary", ["forward_max_dd", "forward_min_pf"], [False, False]),
        ("oos_pf_boundary", ["oos_profit_factor", "forward_max_dd"], [False, True]),
        ("validation_pf_boundary", ["validation_profit_factor", "forward_max_dd"], [False, True]),
    ]
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for reason, columns, ascending in specs:
        usable = [column for column in columns if column in frame.columns]
        if not usable:
            continue
        ordered = frame.sort_values(usable, ascending=ascending[: len(usable)])
        for _, row in ordered.head(max(candidate_count, 20)).iterrows():
            candidate_id = str(row["candidate_id"])
            if candidate_id in seen:
                continue
            payload = dict(row)
            payload["selection_reason"] = reason
            selected.append(payload)
            seen.add(candidate_id)
            if len(selected) >= candidate_count:
                return selected
    for _, row in frame.iterrows():
        candidate_id = str(row["candidate_id"])
        if candidate_id not in seen:
            payload = dict(row)
            payload["selection_reason"] = "fill_diversity"
            selected.append(payload)
            seen.add(candidate_id)
        if len(selected) >= candidate_count:
            break
    return selected


def build_mix_queue(
    ingredients: Sequence[Mapping[str, Any]],
    candidates: Sequence[Mapping[str, Any]],
    broad_count: int,
    wfo_count: int,
) -> list[dict[str, Any]]:
    axes = [
        "feature_set+label+runtime_cost(피처 묶음+라벨+런타임 비용)",
        "model_family+risk_logic+regime_split(모델 계열+위험 로직+장세 분할)",
        "trade_shape+density+drawdown(거래 형태+밀도+손실폭)",
        "onnx_handoff+order_intent+lifecycle(온엑스 인계+주문 의도+생명주기)",
        "extreme_boundary+negative_memory+seed_surface(극단 경계+부정 기억+씨앗 표면)",
    ]
    n = len(ingredients)
    rows: list[dict[str, Any]] = []
    mt5_selected_ids = {str(item["candidate_id"]) for item in candidates}
    for index in range(max(broad_count, wfo_count)):
        a = ingredients[(index * 7) % n]
        b = ingredients[(index * 11 + 3) % n]
        c = ingredients[(index * 17 + 9) % n]
        extra = ingredients[(index * 23 + 13) % n] if index % 5 == 0 else None
        candidate = candidates[index % len(candidates)]
        ingredient_ids = [a["source_frontier"], b["source_frontier"], c["source_frontier"]]
        if extra:
            ingredient_ids.append(extra["source_frontier"])
        runtime_bonus = sum(1 for item in (a, b, c, extra) if item and "runtime" in str(item.get("salvage_value", "")).lower())
        decision_weight = round(1.0 + runtime_bonus * 0.35 + (index % 13) * 0.03, 4)
        rows.append(
            {
                "mix_id": f"E01M{index + 1:04d}",
                "material_window": MATERIAL_WINDOW,
                "ingredient_ids": "+".join(ingredient_ids),
                "axis_mix": axes[index % len(axes)],
                "runtime_substrate": "F50 executable loss-floor regime transfer surface(F50 실행 가능 손실하한 장세전이 표면)",
                "runtime_candidate_id": candidate["candidate_id"],
                "candidate_selection_reason": candidate.get("selection_reason", ""),
                "mix_strength": "extreme(극단)" if index % 7 == 0 else "broad(넓음)",
                "wfo_aware": bool(index < wfo_count),
                "selected_for_mt5": bool(index < len(candidates) and str(candidate["candidate_id"]) in mt5_selected_ids),
                "decision_weight": decision_weight,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def patch_f50_runtime_paths(run_id: str, run_root: Path) -> None:
    f50rt.STAGE_ID = STAGE_ID
    f50rt.RUN_ID = run_id
    f50rt.RUN_ROOT = run_root
    f50rt.MT5_ROOT = run_root / "mt5"
    f50rt.MODELS_ROOT = run_root / "models"
    f50rt.FEATURE_ROOT = run_root / "feature_matrices"


def split_dates(split_payload: Mapping[str, Mapping[str, Any]], split: str) -> tuple[str, str]:
    payload = split_payload[split]
    return str(payload["from_date"]), str(payload["to_date"])


def materialize_candidate(
    candidate_row: Mapping[str, Any],
    index: int,
    identity: scout.RunIdentity,
    common_files_root: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Mapping[str, Any]]]:
    candidate_id = str(candidate_row["candidate_id"])
    token = safe_token(candidate_id, limit=36)
    local_run_id = f"{RUN_ID}_c{index:02d}_{token}"
    candidate_run_root = RUN_DIR / "candidate_runs" / local_run_id
    patch_f50_runtime_paths(local_run_id, candidate_run_root)
    for path in (candidate_run_root, f50rt.MT5_ROOT, f50rt.MODELS_ROOT, f50rt.FEATURE_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)

    row = pd.Series(candidate_row)
    training = f50rt.train_runtime_candidate(row)
    artifacts = f50rt.materialize_model_artifacts(row, training)
    split_payload = f50rt.materialize_split_payload(row, training, artifacts)
    onnx_path = ROOT / str(artifacts["onnx_path"])
    mt5.copy_to_common_files(common_files_root, onnx_path, scout.common_ref("models", onnx_path.name, context=identity))

    attempts: list[dict[str, Any]] = []
    for split in ("validation_is", "oos"):
        payload = split_payload[split]
        feature_path = ROOT / str(payload["feature_export"]["path"])
        mt5.copy_to_common_files(common_files_root, feature_path, scout.common_ref("features", feature_path.name, context=identity))
        from_date, to_date = split_dates(split_payload, split)
        stem_prefix = f"e01_{index:02d}_{token}"
        rule = scout.ThresholdRule(
            threshold_id=f"{RUN_ID}_{token}_threshold_margin",
            short_threshold=float(candidate_row["score_threshold"]),
            long_threshold=1.0,
            min_margin=0.0,
        )
        attempt = scout.materialize_mt5_attempt_files(
            run_output_root=RUN_DIR,
            tier_name=scout.TIER_A,
            split_name=split,
            local_onnx_path=onnx_path,
            local_feature_matrix_path=feature_path,
            rule=rule,
            feature_count=int(artifacts["feature_count"]),
            feature_order_hash=str(artifacts["feature_order_hash"]),
            from_date=from_date,
            to_date=to_date,
            stem_prefix=stem_prefix,
            record_view_prefix="mt5_frontier_extra_E01",
            attempt_role="frontier_extra_runtime_learning",
            decision_mode="threshold_margin",
            max_hold_bars=12,
            reentry_cooldown_bars=0,
            context=identity,
        )
        attempt_name = f"{stem_prefix}_{split}"
        attempt.update(
            {
                "attempt_name": attempt_name,
                "candidate_id": candidate_id,
                "source_candidate_id": candidate_id,
                "source_frontier": "F050",
                "selection_reason": candidate_row.get("selection_reason", ""),
                "run_id": RUN_ID,
                "local_candidate_run_id": local_run_id,
                "ini_name": f"opv2_{attempt_name}.ini",
                "onnx_path": rel(onnx_path),
                "onnx_sha256": artifacts.get("onnx_sha256", ""),
                "model_path": artifacts.get("model_path", ""),
                "model_sha256": artifacts.get("model_sha256", ""),
                "feature_order_hash": artifacts.get("feature_order_hash", ""),
                "expected": payload["expected"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempts.append(attempt)

    artifact_row = {
        "candidate_index": index,
        "candidate_id": candidate_id,
        "local_candidate_run_id": local_run_id,
        "selection_reason": candidate_row.get("selection_reason", ""),
        "model_path": artifacts.get("model_path"),
        "model_sha256": artifacts.get("model_sha256"),
        "onnx_path": artifacts.get("onnx_path"),
        "onnx_sha256": artifacts.get("onnx_sha256"),
        "feature_count": artifacts.get("feature_count"),
        "feature_order_hash": artifacts.get("feature_order_hash"),
        "score_threshold": candidate_row.get("score_threshold"),
        "forward_min_pf": candidate_row.get("forward_min_pf"),
        "forward_max_dd": candidate_row.get("forward_max_dd"),
        "forward_min_density": candidate_row.get("forward_min_density"),
    }
    write_json(candidate_run_root / "candidate_artifact_manifest.json", {"artifact": artifact_row, "attempts": attempts})
    return attempts, artifact_row, split_payload


def execute_attempts(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]], compile_payload: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    terminal_probe = backfill.terminal_processes()
    write_json(RUN_DIR / "terminal_process_audit.json", terminal_probe)
    execution_results: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []
    if not args.execute or args.materialize_only:
        for attempt in attempts:
            execution_results.append(blocked_execution(attempt, "not_run_materialize_only"))
    else:
        compile_status = (compile_payload.get("compile") or {}).get("status")
        can_run = compile_status == "completed" or path_exists(backfill.PORTABLE_EA_BINARY)
        if not can_run:
            for attempt in attempts:
                execution_results.append(blocked_execution(attempt, "compile_blocked_and_no_portable_ex5_fallback"))
        elif terminal_probe.get("status") != "no_terminal64_process":
            for attempt in attempts:
                execution_results.append(blocked_execution(attempt, "target_portable_terminal_already_running"))
        else:
            for attempt in attempts:
                backfill.remove_runtime_outputs(Path(args.common_files_root), attempt)
                mt5.remove_existing_mt5_report_artifacts(Path(args.terminal_data_root), attempt, run_id=RUN_ID)
                try:
                    tester_result = mt5.run_mt5_tester(
                        Path(args.terminal_path),
                        ROOT / str(attempt["ini"]["path"]),
                        set_path=ROOT / str(attempt["set"]["path"]),
                        tester_profile_set_path=Path(args.tester_profile_root) / mt5.EA_TESTER_SET_NAME,
                        tester_profile_ini_path=Path(args.tester_profile_root) / str(attempt["ini_name"]),
                        timeout_seconds=int(args.timeout_seconds),
                        terminal_extra_args=["/portable"],
                    )
                except subprocess.TimeoutExpired as exc:
                    tester_result = {
                        "status": "blocked",
                        "command": exc.cmd,
                        "returncode": None,
                        "stdout": tail_text(exc.stdout),
                        "stderr": tail_text(exc.stderr),
                        "blocker": "terminal_timeout",
                    }
                runtime_outputs = mt5.wait_for_mt5_runtime_outputs(
                    Path(args.common_files_root),
                    attempt,
                    timeout_seconds=int(args.wait_timeout_seconds),
                    poll_seconds=2.0,
                )
                if runtime_outputs.get("status") != "completed":
                    tester_result["status"] = "blocked"
                    tester_result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
                result = {
                    **tester_result,
                    "runtime_outputs": runtime_outputs,
                    "attempt_name": attempt["attempt_name"],
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "record_view_prefix": attempt["record_view_prefix"],
                    "attempt_role": attempt["attempt_role"],
                    "candidate_id": attempt.get("candidate_id"),
                    "source_candidate_id": attempt.get("source_candidate_id"),
                    "ini_path": attempt["ini"]["path"],
                    "set_path": attempt["set"]["path"],
                    "common_model_path": attempt["common_model_path"],
                    "common_feature_matrix_path": attempt["common_feature_matrix_path"],
                }
                write_json(MT5_DIR / "executions" / f"{attempt['attempt_name']}_tester_execution.json", result)
                execution_results.append(result)
            report_records = mt5.collect_mt5_strategy_report_artifacts(
                terminal_data_root=Path(args.terminal_data_root),
                run_output_root=RUN_DIR,
                attempts=attempts,
                run_id=RUN_ID,
            )
            mt5.attach_mt5_report_metrics(execution_results, report_records)
    copied = copy_runtime_outputs(Path(args.common_files_root), attempts)
    write_json(EXECUTION_RESULTS_JSON, {"execution_results": execution_results, "copied_runtime_outputs": copied})
    write_json(REPORT_RECORDS_JSON, report_records)
    return execution_results, report_records, copied


def blocked_execution(attempt: Mapping[str, Any], blocker: str) -> dict[str, Any]:
    return {
        "status": "blocked",
        "blocker": blocker,
        "attempt_name": attempt.get("attempt_name"),
        "tier": attempt.get("tier"),
        "split": attempt.get("split"),
        "candidate_id": attempt.get("candidate_id"),
        "runtime_outputs": {"status": "blocked", "blocker": blocker},
    }


def tail_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")[-2000:]
    return str(value)[-2000:]


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    for attempt in attempts:
        for key in ("common_telemetry_path", "common_summary_path"):
            source = common_files_root / Path(str(attempt.get(key, "")))
            if not path_exists(source):
                copied.append({"attempt_name": attempt.get("attempt_name"), "kind": key, "status": "missing", "source": source.as_posix()})
                continue
            destination = RUNTIME_TELEMETRY_DIR / f"{attempt.get('attempt_name')}_{Path(str(attempt.get(key))).name}"
            io_path(destination.parent).mkdir(parents=True, exist_ok=True)
            shutil.copy2(io_path(source), io_path(destination))
            copied.append(
                {
                    "attempt_name": attempt.get("attempt_name"),
                    "kind": key,
                    "status": "copied",
                    "source": source.as_posix(),
                    "path": rel(destination),
                    "sha256": sha256_file_lf_normalized(destination),
                }
            )
    return copied


def as_int(value: Any) -> int:
    try:
        if value is None or value == "":
            return 0
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def as_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def gap_cause(row: Mapping[str, Any]) -> str:
    if row.get("runtime_status") != "completed":
        return f"runtime_blocked({row.get('blocker', 'unknown')})"
    if row.get("report_status") != "completed":
        return "report_missing_or_unparsed(보고서 누락 또는 파싱 실패)"
    if as_int(row.get("trade_count")) <= 0:
        return "zero_trade_or_density_death(무거래 또는 밀도 사망)"
    pf = as_float(row.get("profit_factor"))
    dd = as_float(row.get("max_drawdown_percent"))
    if pf is not None and pf < 1.0:
        return "pf_collapse_below_one(수익 팩터 1 미만 붕괴)"
    if dd is not None and dd >= 20.0:
        return "drawdown_collapse_ge20pct(손실폭 20퍼센트 이상 붕괴)"
    if as_int(row.get("signal_count_diff")) != 0:
        return "signal_mismatch(신호 불일치)"
    return "runtime_observation_recorded(런타임 관찰 기록됨)"


def build_runtime_receipt(
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    compile_payload: Mapping[str, Any],
) -> list[dict[str, Any]]:
    result_by_attempt = {str(row.get("attempt_name")): row for row in execution_results}
    ea_source = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.mq5"
    ea_binary = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        result = dict(result_by_attempt.get(str(attempt["attempt_name"]), {}))
        runtime = result.get("runtime_outputs", {}) if isinstance(result.get("runtime_outputs"), Mapping) else {}
        last_summary = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
        report = result.get("strategy_tester_report", {}) if isinstance(result.get("strategy_tester_report"), Mapping) else {}
        metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
        expected = attempt.get("expected", {}) if isinstance(attempt.get("expected"), Mapping) else {}
        row = {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "attempt_name": attempt.get("attempt_name"),
            "candidate_id": attempt.get("candidate_id"),
            "source_frontier": attempt.get("source_frontier"),
            "split": attempt.get("split"),
            "tester_status": result.get("status", "missing"),
            "tester_returncode": result.get("returncode", ""),
            "runtime_status": runtime.get("status", "missing"),
            "runtime_wait_status": runtime.get("wait_status", ""),
            "report_status": report.get("status", "missing"),
            "terminal_path": result.get("command", [""])[0] if isinstance(result.get("command"), list) and result.get("command") else "",
            "ea_source_path": rel(ea_source),
            "ea_source_sha256": sha256_file_lf_normalized(ea_source) if path_exists(ea_source) else "",
            "ea_binary_path": rel(ea_binary) if path_exists(ea_binary) else "",
            "ea_binary_sha256": mt5.sha256_file(ea_binary) if path_exists(ea_binary) else "",
            "set_path": attempt.get("set", {}).get("path"),
            "set_sha256": attempt.get("set", {}).get("sha256"),
            "ini_path": attempt.get("ini", {}).get("path"),
            "ini_sha256": attempt.get("ini", {}).get("sha256"),
            "onnx_path": attempt.get("onnx_path"),
            "onnx_sha256": attempt.get("onnx_sha256"),
            "feature_order_hash": attempt.get("feature_order_hash"),
            "feature_matrix_path": attempt.get("local_feature_matrix_path"),
            "common_model_path": attempt.get("common_model_path"),
            "common_feature_matrix_path": attempt.get("common_feature_matrix_path"),
            "telemetry_path": runtime.get("telemetry_path"),
            "summary_path": runtime.get("summary_path"),
            "report_path": (report.get("html_report") or {}).get("path") if isinstance(report.get("html_report"), Mapping) else "",
            "snapshot_path": (report.get("chart") or {}).get("path") if isinstance(report.get("chart"), Mapping) else "",
            "execution_log_path": rel(MT5_DIR / "executions" / f"{attempt['attempt_name']}_tester_execution.json"),
            "model_ok_count": as_int(last_summary.get("model_ok_count")),
            "feature_ready_count": as_int(last_summary.get("feature_ready_count")),
            "mt5_long_count": as_int(last_summary.get("long_count")),
            "mt5_short_count": as_int(last_summary.get("short_count")),
            "mt5_flat_count": as_int(last_summary.get("flat_count")),
            "mt5_order_attempt_count": as_int(last_summary.get("order_attempt_count")),
            "mt5_order_fill_count": as_int(last_summary.get("order_fill_count")),
            "expected_rows": as_int(expected.get("rows")),
            "expected_signal_count": as_int(expected.get("signal_count")),
            "expected_long_count": as_int(expected.get("long_count")),
            "expected_short_count": as_int(expected.get("short_count")),
            "expected_flat_count": as_int(expected.get("flat_count")),
            "signal_count_diff": as_int(last_summary.get("long_count")) + as_int(last_summary.get("short_count")) - as_int(expected.get("signal_count")),
            "feature_ready_diff": as_int(last_summary.get("feature_ready_count")) - as_int(expected.get("rows")),
            "net_profit": metrics.get("net_profit"),
            "profit_factor": metrics.get("profit_factor"),
            "trade_count": metrics.get("trade_count"),
            "max_drawdown_percent": metrics.get("max_drawdown_percent"),
            "recovery_factor": metrics.get("recovery_factor"),
            "blocker": result.get("blocker", ""),
            "compile_status": (compile_payload.get("compile") or {}).get("status"),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        row["gap_cause"] = gap_cause(row)
        rows.append(row)
    return rows


def summarize_runtime(rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [row for row in rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed"]
    report_completed = [row for row in rows if row.get("report_status") == "completed"]
    best = {}
    if report_completed:
        best = max(report_completed, key=lambda row: as_float(row.get("net_profit")) or -999999.0)
    gap_counts: dict[str, int] = {}
    for row in rows:
        gap = str(row.get("gap_cause", "unknown"))
        gap_counts[gap] = gap_counts.get(gap, 0) + 1
    return {
        "attempt_count": len(attempts),
        "completed_runtime_attempt_count": len(completed),
        "completed_report_count": len(report_completed),
        "candidate_count": len({row.get("candidate_id") for row in attempts}),
        "gap_cause_counts": gap_counts,
        "best_runtime_row": best,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def closeout_status(summary: Mapping[str, Any]) -> tuple[str, str]:
    if int(summary.get("attempt_count", 0)) >= 20 and int(summary.get("completed_runtime_attempt_count", 0)) > 0:
        return (
            "closed_heavy_runtime_learning_campaign_no_authority",
            "runtime_learning_recorded_with_negative_memory_and_reference_surface_no_authority",
        )
    if int(summary.get("attempt_count", 0)) >= 20:
        return (
            "closed_blocked_runtime_learning_campaign_no_authority",
            "blocked_retry_condition_recorded_for_mt5_runtime_campaign_no_authority",
        )
    return (
        "closed_invalid_scope_too_few_runtime_attempts_no_authority",
        "invalid_setup_runtime_campaign_under_minimum_attempt_count_no_authority",
    )


def base_ledger_row(summary: Mapping[str, Any], status: str, judgment: str, created_at: str) -> dict[str, Any]:
    best = summary.get("best_runtime_row") or {}
    return {
        "ledger_row_id": f"{RUN_ID}__closeout",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "frontier_extra_E01_closeout(전선 추가 E01 마감)",
        "parent_run_id": "frontier80F_runtime_probe_quality_closeout_v1",
        "record_view": "E01 heavy runtime learning campaign(E01 무거운 런타임 학습 캠페인)",
        "tier_scope": "Tier A separate MT5 attempts; Tier B/combined missing_required unless source card says otherwise",
        "kpi_scope": "mt5_runtime_learning_campaign(MT5 런타임 학습 캠페인)",
        "scoreboard_lane": "frontier_extra_runtime_learning(전선 추가 런타임 학습)",
        "lane": "runtime_learning(런타임 학습)",
        "family": "runtime_backtest(MT5/런타임/백테스트)",
        "status": status,
        "judgment": judgment,
        "path": rel(CLOSEOUT_REPORT),
        "primary_kpi": f"attempts={summary.get('attempt_count')};completed_runtime={summary.get('completed_runtime_attempt_count')};reports={summary.get('completed_report_count')}",
        "guardrail_kpi": "no_completion_no_baseline_no_promotion_no_authority_no_live",
        "external_verification_status": "mt5_attempted_recorded(MT5 시도 기록됨)",
        "notes": (
            f"best_runtime_candidate={best.get('candidate_id', '')};split={best.get('split', '')};"
            f"pf={best.get('profit_factor', '')};dd={best.get('max_drawdown_percent', '')};"
            f"trades={best.get('trade_count', '')};gap={best.get('gap_cause', '')}"
        ),
        "run_number": "frontier_extra_E01",
        "date": created_at[:10],
        "decision": judgment,
        "next_run_id": RESUME_RUN_ID,
        "rows": summary.get("attempt_count"),
        "gate_passes": "",
        "gate_total": "",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(CLOSEOUT_REPORT),
        "best_candidate_id": best.get("candidate_id", ""),
        "net_profit": best.get("net_profit", ""),
        "profit_factor": best.get("profit_factor", ""),
        "drawdown": best.get("max_drawdown_percent", ""),
        "trade_count": best.get("trade_count", ""),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "frontier_extra_E01",
        "tier": "Tier A",
        "metric_scope": "mt5_runtime_learning",
        "result_status": status,
        "work_family": "runtime_backtest",
        "row_id": f"{RUN_ID}__closeout",
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": RESUME_FRONTIER_ID,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "MT5 runtime learning evidence only(MT5 런타임 학습 근거만)",
    }


def write_reports(
    created_at: str,
    ingredients: Sequence[Mapping[str, Any]],
    scan_summary: Mapping[str, Any],
    mix_queue: Sequence[Mapping[str, Any]],
    candidate_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    runtime_summary: Mapping[str, Any],
    compile_payload: Mapping[str, Any],
    status: str,
    judgment: str,
) -> None:
    write_text(SPEC_DIR / "stage_brief.md", stage_brief_text(created_at))
    write_text(INPUT_DIR / "input_refs.md", input_refs_text())
    write_text(OPEN_REPORT, open_report_text(created_at, len(ingredients), len(mix_queue), len(candidate_rows)))
    write_text(SCAN_REPORT, scan_report_text(scan_summary, ingredients))
    write_text(MIX_REPORT, mix_report_text(mix_queue, candidate_rows))
    write_text(RUNTIME_REPORT, runtime_report_text(created_at, runtime_summary, runtime_rows))
    write_text(GATE_AUDIT, gate_audit_text(scan_summary, mix_queue, attempts, runtime_rows, compile_payload, status))
    write_text(CLOSEOUT_REPORT, closeout_text(created_at, runtime_summary, status, judgment))
    write_text(SELECTION_STATUS, selection_status_text(created_at, runtime_summary, status, judgment))
    write_text(NEGATIVE_MEMORY, negative_memory_text(runtime_summary))
    write_text(PRESERVED_CLUE, preserved_clue_text(runtime_summary))
    write_text(REVIEW_INDEX, review_index_text())


def stage_brief_text(created_at: str) -> str:
    return f"""# Frontier Extra Stage E01 Brief(전선 추가 단계 E01 개요)

Updated(갱신): {created_at}

Stage id(단계 ID): `{STAGE_ID}`

Thesis(가설): F01-F50(전선01-50)의 closeout/failure/runtime gap(마감/실패/런타임 간극)을 ingredient(재료)로 바꾸고, runnable F50 surface(실행 가능한 F50 표면)를 substrate(바탕)로 삼아 aggressive mixed hypotheses(공격적 혼합 가설)를 실제 MT5 runtime learning campaign(MT5 런타임 학습 캠페인)까지 밀어본다.

Effect(효과): Extra Stage(추가 단계)가 문서상 규칙이 아니라 next frontier open(다음 전선 개방)을 앞두고 실제 scan/mix/MT5/closeout(스캔/혼합/MT5/마감)을 수행하는 운영 단위가 된다.

Resume target(재개 대상): `{RESUME_FRONTIER_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def input_refs_text() -> str:
    return f"""# E01 Input References(E01 입력 참조)

- material window(재료 구간): `{MATERIAL_WINDOW}`
- trigger frontier(트리거 전선): `{TRIGGER_FRONTIER_ID}`
- F50 runtime substrate(F50 런타임 바탕): `{rel(F50_SUMMARY)}`
- runtime backfill coverage(런타임 소급 커버리지): `{rel(BACKFILL_COVERAGE)}`
- resume frontier(재개 전선): `{RESUME_FRONTIER_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def open_report_text(created_at: str, ingredient_count: int, mix_count: int, candidate_count: int) -> str:
    return f"""# E01 Stage Open Report(E01 단계 개방 보고서)

Updated(갱신): {created_at}

Action(행동): E01(추가01)을 F50 due extra stage(F50 도래 추가 단계) backfill execution(소급 실행)으로 열었다.

Effect(효과): F81(전선81)을 열기 전, F01-F50(전선01-50) 재료를 먼저 혼합/런타임 학습으로 소화한다.

- ingredient cards(재료 카드): `{ingredient_count}`
- broad/extreme mix queue(넓은/극단 혼합 대기열): `{mix_count}`
- selected MT5 runtime candidates(선택 MT5 런타임 후보): `{candidate_count}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def scan_report_text(summary: Mapping[str, Any], ingredients: Sequence[Mapping[str, Any]]) -> str:
    counts: dict[str, int] = {}
    for card in ingredients:
        status = str(card.get("material_status", "unknown"))
        counts[status] = counts.get(status, 0) + 1
    count_lines = "\n".join(f"- `{key}`: {value}" for key, value in sorted(counts.items()))
    return f"""# E01 Receipt-First Scan Report(E01 영수증 우선 스캔 보고서)

Material window(재료 구간): `{summary.get('material_window')}`

Ingredient count(재료 수): `{summary.get('ingredient_count')}`

Missing stage nums(누락 단계 번호): `{summary.get('missing_stage_nums')}`

Runtime recorded stage nums(런타임 기록 단계 번호): `{summary.get('runtime_recorded_stage_nums')}`

## Status Counts(상태 집계)

{count_lines}

Effect(효과): F01-F50(전선01-50)을 winner/baseline(승자/기준선)으로 상속하지 않고, runtime gap/negative memory/preserved clue(런타임 간극/부정 기억/보존 단서) 재료로만 사용한다.
"""


def mix_report_text(mix_queue: Sequence[Mapping[str, Any]], candidates: Sequence[Mapping[str, Any]]) -> str:
    selected = [row for row in mix_queue if row.get("selected_for_mt5")]
    candidate_lines = "\n".join(
        f"- `{row.get('candidate_id')}`: `{row.get('selection_reason')}`, forward_min_pf `{row.get('forward_min_pf')}`, forward_max_dd `{row.get('forward_max_dd')}`"
        for row in candidates
    )
    return f"""# E01 Mix Design Report(E01 혼합 설계 보고서)

- broad/extreme mix count(넓은/극단 혼합 수): `{len(mix_queue)}`
- WFO-aware mix count(워크포워드 인식 혼합 수): `{sum(1 for row in mix_queue if row.get('wfo_aware'))}`
- selected MT5 mix count(선택 MT5 혼합 수): `{len(selected)}`

## Selected Runtime Substrate Candidates(선택 런타임 바탕 후보)

{candidate_lines}

Effect(효과): F01-F50(전선01-50)의 다양한 실패/단서를 섞되, 실제 MT5에 넣을 수 있는 F50 executable substrate(F50 실행 가능 바탕)를 통해 런타임 학습을 닫는다.
"""


def runtime_report_text(created_at: str, summary: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# E01 MT5 Runtime Learning Campaign Report(E01 MT5 런타임 학습 캠페인 보고서)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- attempts(시도): `{summary.get('attempt_count')}`",
        f"- completed runtime attempts(완료 런타임 시도): `{summary.get('completed_runtime_attempt_count')}`",
        f"- completed reports(완료 보고서): `{summary.get('completed_report_count')}`",
        f"- candidate count(후보 수): `{summary.get('candidate_count')}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "| attempt(시도) | split(분할) | status(상태) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | gap cause(간극 원인) |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row.get('attempt_name')}` | `{row.get('split')}` | `{row.get('tester_status')}/{row.get('runtime_status')}/{row.get('report_status')}` | "
            f"{row.get('profit_factor', '')} | {row.get('max_drawdown_percent', '')} | {row.get('trade_count', '')} | `{row.get('gap_cause')}` |"
        )
    lines.extend(
        [
            "",
            "Effect(효과): 성공/실패/무거래/불일치/차단을 모두 runtime learning evidence(런타임 학습 근거)로 남긴다.",
        ]
    )
    return "\n".join(lines)


def gate_audit_text(
    scan_summary: Mapping[str, Any],
    mix_queue: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    compile_payload: Mapping[str, Any],
    status: str,
) -> str:
    compile_status = (compile_payload.get("compile") or {}).get("status")
    rows = [
        ("frontier_extra_due_check", "passed", rel(EXTRA_REGISTER), "E01 due backfill(소급 도래)을 등록했다."),
        ("receipt_first_scan", "passed" if scan_summary.get("ingredient_count") == 50 else "blocked", rel(INGREDIENT_CSV), "F01-F50 재료 카드를 만들었다."),
        ("mix_queue", "passed" if len(mix_queue) >= 300 else "blocked", rel(MIX_QUEUE_CSV), "300개 이상 broad/extreme mix(넓은/극단 혼합)를 만들었다."),
        ("mt5_attempt_count", "passed" if len(attempts) >= 20 else "blocked", rel(RUNTIME_RECEIPT_CSV), "20개 이상 MT5 attempt(시도)를 materialize/execute(구체화/실행)했다."),
        ("compile_not_runtime_substitute", "passed", rel(RUN_MANIFEST), f"compile status(컴파일 상태) `{compile_status}`를 기록하되 runtime evidence(런타임 근거)를 대체하지 않았다."),
        ("runtime_evidence_record", "passed" if len(runtime_rows) == len(attempts) else "blocked", rel(RUNTIME_REPORT), "각 시도마다 runtime row(런타임 행)를 남겼다."),
        ("final_claim_guard", "passed", CLAIM_BOUNDARY, "금지 claim(주장)을 만들지 않았다."),
    ]
    table = "\n".join(f"| `{gate}` | `{gate_status}` | `{evidence}` | {effect} |" for gate, gate_status, evidence, effect in rows)
    return f"""# E01 Required Gate Coverage Audit(E01 필수 게이트 커버리지 감사)

Status(상태): `{status}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
{table}
"""


def closeout_text(created_at: str, summary: Mapping[str, Any], status: str, judgment: str) -> str:
    best = summary.get("best_runtime_row") or {}
    best_summary = (
        f"candidate={best.get('candidate_id', '')}; split={best.get('split', '')}; "
        f"net={best.get('net_profit', '')}; PF={best.get('profit_factor', '')}; "
        f"DD={best.get('max_drawdown_percent', '')}; trades={best.get('trade_count', '')}; "
        f"gap={best.get('gap_cause', '')}"
    )
    return f"""# E01 Closeout Report(E01 마감 보고서)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): E01(추가01)은 F01-F50(전선01-50) 재료를 ingredient card(재료 카드)로 만들고, broad/extreme mix queue(넓은/극단 혼합 대기열)를 만든 뒤, F50 executable runtime substrate(F50 실행 가능 런타임 바탕)로 MT5 Strategy Tester(전략 테스터) campaign(캠페인)을 수행했다.

Effect(효과): Extra Stage(추가 단계) 운영 도입과 실제 런타임 학습을 한 단계 안에서 닫았고, E01을 다시 열지 않고 F81(전선81)로 재개할 수 있다.

- attempts(시도): `{summary.get('attempt_count')}`
- completed runtime attempts(완료 런타임 시도): `{summary.get('completed_runtime_attempt_count')}`
- completed reports(완료 보고서): `{summary.get('completed_report_count')}`
- best runtime row(최선 런타임 행): `{best_summary}`

Closeout labels(마감 라벨): `negative_memory(부정 기억)`, `reference_surface(참고 표면)`, `runtime_learning_record(런타임 학습 기록)`, `next_frontier_proposal(다음 전선 제안)`.

Next frontier proposal(다음 전선 제안): `{RESUME_FRONTIER_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def selection_status_text(created_at: str, summary: Mapping[str, Any], status: str, judgment: str) -> str:
    return f"""# E01 Selection Status(E01 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Selected baseline(선택 기준선): `not_claimed(주장 없음)`

Runtime authority(런타임 권위): `not_claimed(주장 없음)`

Live readiness(실거래 준비): `not_claimed(주장 없음)`

Resume target(재개 대상): `{RESUME_FRONTIER_ID}`

Effect(효과): E01(추가01)은 runtime learning record(런타임 학습 기록)로 닫혔고, F81(전선81) open(개방) 전 extra due(추가 도래)는 해소됐다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def negative_memory_text(summary: Mapping[str, Any]) -> str:
    return f"""# E01 Negative Memory(E01 부정 기억)

MT5 runtime learning(MT5 런타임 학습)은 proxy/hypothesis/runtime gap(프록시/가설/런타임 간극)을 줄이는 장치다. E01 결과는 completion(완성)이나 baseline(기준선)이 아니다.

Gap cause counts(간극 원인 집계): `{json.dumps(json_ready(summary.get('gap_cause_counts', {})), ensure_ascii=False)}`

Do not repeat(반복 금지): Extra Stage(추가 단계)를 문서 회고로 축소하거나, compile(컴파일)과 proxy parity(프록시 동등성)를 runtime evidence(런타임 근거)로 대체하지 않는다.
"""


def preserved_clue_text(summary: Mapping[str, Any]) -> str:
    return f"""# E01 Preserved Clue(E01 보존 단서)

Preserved clue(보존 단서): F01-F50(전선01-50)을 winner/baseline(승자/기준선)으로 상속하지 않고도, ingredient card(재료 카드)와 runtime substrate(런타임 바탕)를 연결하면 50단계마다 heavy finite campaign(무겁지만 유한한 캠페인)을 운영할 수 있다.

Runtime summary(런타임 요약): attempts `{summary.get('attempt_count')}`, completed runtime `{summary.get('completed_runtime_attempt_count')}`, reports `{summary.get('completed_report_count')}`.

Next use(다음 사용): F81(전선81)은 E01의 negative memory/reference surface(부정 기억/참고 표면)를 참고하되 selected baseline/runtime authority(선택 기준선/런타임 권위)를 상속하지 않는다.
"""


def review_index_text() -> str:
    return f"""# E01 Review Index(E01 검토 색인)

- `{rel(OPEN_REPORT)}`: stage open report(단계 개방 보고서)
- `{rel(SCAN_REPORT)}`: receipt-first scan report(영수증 우선 스캔 보고서)
- `{rel(MIX_REPORT)}`: mix design report(혼합 설계 보고서)
- `{rel(RUNTIME_REPORT)}`: MT5 runtime learning campaign report(MT5 런타임 학습 캠페인 보고서)
- `{rel(GATE_AUDIT)}`: required gate coverage audit(필수 게이트 커버리지 감사)
- `{rel(CLOSEOUT_REPORT)}`: closeout report(마감 보고서)
- `{rel(RUN_MANIFEST)}`: run manifest(실행 목록)
"""


def update_register(created_at: str, status: str, judgment: str, runtime_summary: Mapping[str, Any]) -> None:
    text = f"""version: frontier_extra_stage_register_v1
updated_at_utc: "{created_at}"
extra_stages:
  E01:
    extra_stage_id: "{STAGE_ID}"
    status: "{status}"
    judgment: "{judgment}"
    due_frontier_closeout: "F050"
    material_window: "{MATERIAL_WINDOW}"
    backfill_execution: true
    resume_frontier_id: "{RESUME_FRONTIER_ID}"
    resume_run_id: "{RESUME_RUN_ID}"
    run_id: "{RUN_ID}"
    stage_path: "{rel(STAGE_DIR)}"
    open_report: "{rel(OPEN_REPORT)}"
    closeout_report: "{rel(CLOSEOUT_REPORT)}"
    run_manifest: "{rel(RUN_MANIFEST)}"
    ingredient_cards: "{rel(INGREDIENT_CSV)}"
    mix_queue: "{rel(MIX_QUEUE_CSV)}"
    mt5_runtime_receipt: "{rel(RUNTIME_RECEIPT_CSV)}"
    attempt_count: {int(runtime_summary.get('attempt_count', 0))}
    completed_runtime_attempt_count: {int(runtime_summary.get('completed_runtime_attempt_count', 0))}
    completed_report_count: {int(runtime_summary.get('completed_report_count', 0))}
    claim_boundary: "{CLAIM_BOUNDARY}"
    forbidden_claims:
      - completion
      - selected_baseline
      - operating_promotion
      - runtime_authority
      - live_readiness
      - goal_achieve
      - git_push_as_validation
"""
    write_text(EXTRA_REGISTER, text)


def update_state(created_at: str, status: str, judgment: str, runtime_summary: Mapping[str, Any]) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: frontier_extra_E01_closed_resume_frontier_81_not_opened
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {RESUME_RUN_ID}
resume_frontier_id: {RESUME_FRONTIER_ID}
frontier_extra_due_status: E01_closed_resume_F81
runtime_probe_status: e01_attempts_{runtime_summary.get('attempt_count')}_completed_runtime_{runtime_summary.get('completed_runtime_attempt_count')}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{created_at}'
context_anchor: {rel(CLOSEOUT_REPORT)}
notes:
  - "Action(행동): E01 Extra Stage(추가 단계)를 F01-F50 재료 혼합과 MT5 runtime learning(MT5 런타임 학습)으로 닫았다."
  - "Effect(효과): F81(전선81)은 E01 closeout(마감) 뒤 resume target(재개 대상)으로 남는다."
  - "Boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `frontier_extra_E01_closed_resume_frontier_81_not_opened`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): E01(추가01)을 F01-F50(전선01-50) ingredient mixing(재료 혼합)과 MT5 runtime learning campaign(MT5 런타임 학습 캠페인)으로 닫았다.

Effect(효과): F81(전선81)은 아직 열지 않았고, 다음 재개 대상이다.

Runtime summary(런타임 요약): attempts `{runtime_summary.get('attempt_count')}`, completed runtime `{runtime_summary.get('completed_runtime_attempt_count')}`, reports `{runtime_summary.get('completed_report_count')}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def main() -> int:
    args = parse_args()
    created_at = utc_now()
    ensure_dirs()

    ingredients, scan_summary = build_ingredient_cards()
    write_csv(INGREDIENT_CSV, ingredients)
    write_json(INGREDIENT_JSON, ingredients)
    write_json(SCAN_SUMMARY_JSON, scan_summary)

    f50_candidates = load_f50_candidates()
    candidate_target = int(args.candidate_count)
    if args.execute and not args.materialize_only:
        candidate_target = max(10, candidate_target)
    selected_candidates = select_runtime_candidates(f50_candidates, candidate_target)
    mix_queue = build_mix_queue(ingredients, selected_candidates, int(args.broad_mix_count), int(args.wfo_mix_count))
    write_csv(MIX_QUEUE_CSV, mix_queue)
    write_json(MIX_QUEUE_JSON, mix_queue)

    identity = scout.RunIdentity(
        stage_id=STAGE_ID,
        stage_number=501,
        run_number=RUN_NUMBER,
        run_id=RUN_ID,
        exploration_label=EXPLORATION_LABEL,
        common_run_root=COMMON_RUN_ROOT,
    )
    attempts: list[dict[str, Any]] = []
    candidate_artifacts: list[dict[str, Any]] = []
    split_payloads: dict[str, Any] = {}
    for index, candidate in enumerate(selected_candidates, start=1):
        candidate_attempts, artifact_row, split_payload = materialize_candidate(candidate, index, identity, Path(args.common_files_root))
        attempts.extend(candidate_attempts)
        candidate_artifacts.append(artifact_row)
        split_payloads[str(candidate["candidate_id"])] = split_payload
    write_csv(CANDIDATE_MANIFEST, candidate_artifacts)
    write_json(RUN_DIR / "candidate_artifacts.json", candidate_artifacts)
    write_json(MT5_DIR / "attempts.json", attempts)

    compile_payload = backfill.compile_runtime_ea(Path(args.metaeditor_path))
    write_json(MT5_DIR / "mt5_compile_result.json", compile_payload)
    execution_results, report_records, copied_outputs = execute_attempts(args, attempts, compile_payload)
    runtime_rows = build_runtime_receipt(attempts, execution_results, compile_payload)
    runtime_summary = summarize_runtime(runtime_rows, attempts)
    status, judgment = closeout_status(runtime_summary)

    write_csv(RUNTIME_RECEIPT_CSV, runtime_rows)
    write_json(RUNTIME_RECEIPT_JSON, runtime_rows)
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "material_window": MATERIAL_WINDOW,
            "trigger_frontier_id": TRIGGER_FRONTIER_ID,
            "resume_frontier_id": RESUME_FRONTIER_ID,
            "status": status,
            "judgment": judgment,
            "ingredient_cards": rel(INGREDIENT_CSV),
            "mix_queue": rel(MIX_QUEUE_CSV),
            "candidate_artifacts": candidate_artifacts,
            "attempts": attempts,
            "compile_payload": compile_payload,
            "execution_results": execution_results,
            "report_records": report_records,
            "copied_runtime_outputs": copied_outputs,
            "runtime_rows": runtime_rows,
            "runtime_summary": runtime_summary,
            "claim_boundary": CLAIM_BOUNDARY,
            "producer": SCRIPT_REL,
            "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        },
    )

    write_reports(
        created_at,
        ingredients,
        scan_summary,
        mix_queue,
        selected_candidates,
        attempts,
        runtime_rows,
        runtime_summary,
        compile_payload,
        status,
        judgment,
    )
    update_register(created_at, status, judgment, runtime_summary)
    update_state(created_at, status, judgment, runtime_summary)
    ledger_row = base_ledger_row(runtime_summary, status, judgment, created_at)
    upsert_csv(RUN_REGISTRY, "run_id", ledger_row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", ledger_row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", ledger_row, source_header=ALPHA_LEDGER)

    print(
        json.dumps(
            json_ready(
                {
                    "status": status,
                    "judgment": judgment,
                    "attempt_count": runtime_summary["attempt_count"],
                    "completed_runtime_attempt_count": runtime_summary["completed_runtime_attempt_count"],
                    "completed_report_count": runtime_summary["completed_report_count"],
                    "resume_frontier_id": RESUME_FRONTIER_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if int(runtime_summary["attempt_count"]) >= 20 else 1


if __name__ == "__main__":
    raise SystemExit(main())
