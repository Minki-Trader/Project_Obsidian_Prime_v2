from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

STAGE_ID = "364_source_regime_label_pivot__dense_cost_recovery"
RUN_NUMBER = "run364C"
RUN_ID = "run364C_review_timestamp_context_cost_surface_without_db_v1"
PARENT_RUN_ID = "run364B_materialize_timestamp_context_cost_surface_without_db_v1"
NEXT_RUN_ID = "run364D_materialize_timestamp_context_training_seed_without_db_v1"

STATUS = "completed_stage364C_timestamp_context_surface_reviewed_training_seed_opened_no_selection_no_mt5"
JUDGMENT = "positive_scout_reviewed_month_fragile_training_seed_no_candidate_no_operating_claim"
DECISION = "stage364C_open_run364D_timestamp_context_training_seed_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_review_only_timestamp_context_positive_scout_month_fragility_"
    "training_seed_handoff_no_new_model_training_no_new_proxy_execution_no_mt5_execution_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "mt5_report_open_close_time_joined_to_runtime_bar_time_no_timezone_conversion"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
SOURCE_RUN_DIR = STAGE_DIR / "02_runs" / "run364B"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

SOURCE_CROSS_SPLIT = SOURCE_RUN_DIR / "timestamp_context_cross_split.csv"
SOURCE_SCORECARD = SOURCE_RUN_DIR / "timestamp_context_scorecard.csv"
SOURCE_FAILURE_ATTRIBUTION = SOURCE_RUN_DIR / "timestamp_context_failure_attribution.csv"
SOURCE_REVIEW_QUEUE = SOURCE_RUN_DIR / "run364C_review_queue.csv"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_REPORT = REVIEW_DIR / "run364B_timestamp_context_cost_surface_materialization.md"
SOURCE_SCRIPT = ROOT / "stage_pipelines" / "stage364" / "materialize_timestamp_context_cost_surface_without_db.py"
SOURCE_TRADE_TABLE = (
    ROOT
    / "stages"
    / "362_long_only_margin_grid__cost_buffer_first_branch"
    / "02_runs"
    / "run362B"
    / "q05_long_trade_probability_table.csv"
)

INPUT_FILES = [
    SOURCE_CROSS_SPLIT,
    SOURCE_SCORECARD,
    SOURCE_FAILURE_ATTRIBUTION,
    SOURCE_REVIEW_QUEUE,
    SOURCE_FINAL_DECISION,
    SOURCE_GATE_AUDIT,
    SOURCE_REPORT,
    SOURCE_SCRIPT,
    SOURCE_TRADE_TABLE,
]

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
PASS_REVIEW = RUN_DIR / "pass_candidate_review.csv"
MONTHLY_STABILITY = RUN_DIR / "monthly_stability.csv"
FAMILY_ATTRIBUTION = RUN_DIR / "family_attribution.csv"
REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
TRAINING_SEED_QUEUE = RUN_DIR / "run364D_training_seed_queue.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"

REPORT_PATH = REVIEW_DIR / "run364C_timestamp_context_cost_surface_review.md"
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
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364C_timestamp_context_surface_review.md"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ensure_parent(path)
    encoding = "utf-8-sig" if bom and path.suffix.lower() in {".md", ".txt"} else "utf-8"
    with open(fs_path(path), "w", encoding=encoding, newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    csv.field_size_limit(200_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    temp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    try:
        with open(fs_path(temp_path), "w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
            writer.writeheader()
            for row in rows_list:
                writer.writerow({key: row.get(key, "") for key in fieldnames})
        os.replace(fs_path(temp_path), fs_path(path))
    finally:
        if exists(temp_path):
            os.remove(fs_path(temp_path))


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool) -> None:
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    elif extend_header:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    replacements = {tuple(str(row.get(key, "")) for key in key_fields): dict(row) for row in rows}
    output: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set()
    for row in existing:
        key = tuple(str(row.get(field, "")) for field in key_fields)
        if key in replacements:
            output.append(replacements[key])
            seen.add(key)
        else:
            output.append(row)
    for key, row in replacements.items():
        if key not in seen:
            output.append(row)
    write_csv(path, output, fieldnames)


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


def load_stage364b_module() -> Any:
    spec = importlib.util.spec_from_file_location("stage364b_materializer", SOURCE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load Stage364B materializer module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_gate_passed() -> bool:
    _, rows = read_csv_rows(SOURCE_GATE_AUDIT)
    return bool(rows) and all(row.get("status") == "passed" for row in rows)


def cost_net(frame: pd.DataFrame) -> pd.Series:
    return frame["net_profit"].astype(float) - 0.30


def pass_reviews() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    materializer = load_stage364b_module()
    trade_frame = materializer.load_trade_table()
    variants = {variant["variant_id"]: variant for variant in materializer.build_variants(trade_frame)}

    cross = pd.read_csv(fs_path(SOURCE_CROSS_SPLIT), encoding="utf-8-sig")
    passing = cross[cross["cross_split_status"].eq("passes_split_cost_density_gate")].copy()
    passing["validation_cost_0_30_net"] = passing["validation_cost_0_30_net"].astype(float)
    passing["oos_cost_0_30_net"] = passing["oos_cost_0_30_net"].astype(float)
    passing["validation_density"] = passing["validation_density"].astype(float)
    passing["oos_density"] = passing["oos_density"].astype(float)
    passing["net_min"] = passing[["validation_cost_0_30_net", "oos_cost_0_30_net"]].min(axis=1)
    passing["net_sum"] = passing["validation_cost_0_30_net"] + passing["oos_cost_0_30_net"]
    passing["net_gap_abs"] = (passing["oos_cost_0_30_net"] - passing["validation_cost_0_30_net"]).abs()
    passing["density_min"] = passing[["validation_density", "oos_density"]].min(axis=1)
    passing["density_gap_abs"] = (passing["oos_density"] - passing["validation_density"]).abs()
    best_min_variant = str(passing.sort_values(["net_min", "net_sum"], ascending=False).iloc[0]["variant_id"])

    monthly_rows: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []
    for _, pass_row in passing.iterrows():
        variant_id = str(pass_row["variant_id"])
        variant = variants[variant_id]
        selected = trade_frame[materializer.select_mask(trade_frame, variant)].copy()
        selected["cost_0_30_net"] = cost_net(selected)
        monthly = (
            selected.groupby(["split", "year_month"], dropna=False)
            .agg(cost_0_30_net=("cost_0_30_net", "sum"), trade_count=("cost_0_30_net", "size"))
            .reset_index()
        )
        split_month_stats: dict[str, dict[str, Any]] = {}
        for split in ("validation", "oos"):
            split_month = monthly[monthly["split"].eq(split)]
            months = int(len(split_month))
            positives = int((split_month["cost_0_30_net"] > 0).sum())
            negatives = int((split_month["cost_0_30_net"] <= 0).sum())
            worst = float(split_month["cost_0_30_net"].min()) if months else 0.0
            best = float(split_month["cost_0_30_net"].max()) if months else 0.0
            median = float(split_month["cost_0_30_net"].median()) if months else 0.0
            split_month_stats[split] = {
                "months": months,
                "positive_months": positives,
                "negative_months": negatives,
                "positive_month_rate": positives / months if months else 0.0,
                "worst_month_net": worst,
                "best_month_net": best,
                "median_month_net": median,
            }
        for _, month_row in monthly.iterrows():
            monthly_rows.append({
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "variant_id": variant_id,
                "source_queue_id": pass_row["source_queue_id"],
                "split": month_row["split"],
                "year_month": month_row["year_month"],
                "cost_0_30_net": round(float(month_row["cost_0_30_net"]), 2),
                "trade_count": int(month_row["trade_count"]),
                "claim_boundary": CLAIM_BOUNDARY,
            })

        validation_rate = split_month_stats["validation"]["positive_month_rate"]
        oos_rate = split_month_stats["oos"]["positive_month_rate"]
        worst_month_net = min(
            split_month_stats["validation"]["worst_month_net"],
            split_month_stats["oos"]["worst_month_net"],
        )
        monthly_fragility = validation_rate < 0.50 or oos_rate < 0.50 or worst_month_net < -50.0
        balanced_score = (
            as_float(pass_row["net_min"])
            + 0.10 * as_float(pass_row["net_sum"])
            - 0.25 * as_float(pass_row["net_gap_abs"])
            + 25.0 * min(validation_rate, oos_rate)
            + 0.10 * worst_month_net
            - 10.0 * as_float(pass_row["density_gap_abs"])
        )
        if variant_id == best_min_variant:
            review_tier = "primary_training_seed_fragile_no_candidate"
            next_use = "run364D_primary_context_guard_seed"
        elif str(pass_row["source_queue_id"]) == "s364_r01_open_hour_context_stack":
            review_tier = "score_guard_family_seed_fragile_no_candidate"
            next_use = "run364D_score_guard_feature_family_seed"
        else:
            review_tier = "supporting_context_seed_fragile_no_candidate"
            next_use = "run364D_supporting_context_guard_seed"
        review_rows.append({
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "variant_id": variant_id,
            "source_queue_id": pass_row["source_queue_id"],
            "surface_family": pass_row["surface_family"],
            "variant_role": pass_row["variant_role"],
            "validation_cost_0_30_net": round(as_float(pass_row["validation_cost_0_30_net"]), 2),
            "oos_cost_0_30_net": round(as_float(pass_row["oos_cost_0_30_net"]), 2),
            "net_min": round(as_float(pass_row["net_min"]), 2),
            "net_sum": round(as_float(pass_row["net_sum"]), 2),
            "net_gap_abs": round(as_float(pass_row["net_gap_abs"]), 2),
            "validation_density": round(as_float(pass_row["validation_density"]), 10),
            "oos_density": round(as_float(pass_row["oos_density"]), 10),
            "density_min": round(as_float(pass_row["density_min"]), 10),
            "density_gap_abs": round(as_float(pass_row["density_gap_abs"]), 10),
            "validation_positive_months": split_month_stats["validation"]["positive_months"],
            "validation_months": split_month_stats["validation"]["months"],
            "oos_positive_months": split_month_stats["oos"]["positive_months"],
            "oos_months": split_month_stats["oos"]["months"],
            "validation_worst_month_net": round(split_month_stats["validation"]["worst_month_net"], 2),
            "oos_worst_month_net": round(split_month_stats["oos"]["worst_month_net"], 2),
            "monthly_fragility_flag": "true" if monthly_fragility else "false",
            "balanced_review_score": round(balanced_score, 4),
            "review_tier": review_tier,
            "next_use": next_use,
            "filter_expression": pass_row["filter_expression"],
            "threshold_source": pass_row["threshold_source"],
            "claim_boundary": CLAIM_BOUNDARY,
        })
    review_rows = sorted(review_rows, key=lambda row: (as_float(row["net_min"]), as_float(row["balanced_review_score"])), reverse=True)
    for index, row in enumerate(review_rows, start=1):
        row["review_rank"] = index

    family_rows: list[dict[str, Any]] = []
    family_frame = pd.DataFrame(review_rows)
    for source_queue_id, group in family_frame.groupby("source_queue_id"):
        best = group.sort_values(["net_min", "balanced_review_score"], ascending=False).iloc[0]
        family_rows.append({
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_queue_id": source_queue_id,
            "pass_rows": int(len(group)),
            "avg_validation_cost_0_30_net": round(float(group["validation_cost_0_30_net"].mean()), 2),
            "avg_oos_cost_0_30_net": round(float(group["oos_cost_0_30_net"].mean()), 2),
            "avg_net_min": round(float(group["net_min"].mean()), 2),
            "best_variant_id": best["variant_id"],
            "best_net_min": round(float(best["net_min"]), 2),
            "best_balanced_review_score": round(float(best["balanced_review_score"]), 4),
            "fragile_rows": int((group["monthly_fragility_flag"] == "true").sum()),
            "family_judgment": "positive_scout_but_month_fragile_seed_only",
            "claim_boundary": CLAIM_BOUNDARY,
        })
    family_rows = sorted(family_rows, key=lambda row: (as_float(row["best_net_min"]), as_int(row["pass_rows"])), reverse=True)
    return review_rows, monthly_rows, family_rows


def build_findings(review_rows: Sequence[Mapping[str, Any]], family_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    source_final = read_json(SOURCE_FINAL_DECISION)
    best = review_rows[0]
    score_guard = next((row for row in family_rows if row["source_queue_id"] == "s364_r01_open_hour_context_stack"), {})
    joint_context = next((row for row in family_rows if row["source_queue_id"] == "s364_r02_day_hour_joint_context"), {})
    return [
        {
            "finding_id": "stage364C_source_positive_scout_review",
            "finding": "Stage364B found 33 cross-split pass rows(364B가 교차 분할 통과 33행을 찾음)",
            "evidence": rel(SOURCE_CROSS_SPLIT),
            "metric": f"passing_cross_split_rows={source_final.get('passing_cross_split_rows')}",
            "judgment": "positive_scout_review_required_no_candidate_selection",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "stage364C_best_balanced_seed",
            "finding": "Best minimum split net is the hour-minute context guard(최선 최소 분할 순수익은 시간-분 문맥 가드)",
            "evidence": rel(PASS_REVIEW),
            "metric": f"variant={best['variant_id']};validation_net={best['validation_cost_0_30_net']};oos_net={best['oos_cost_0_30_net']};density_min={best['density_min']}",
            "judgment": "primary_training_seed_fragile_no_candidate",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "stage364C_month_fragility",
            "finding": "Passing rows remain monthly fragile(통과 행은 월별로 아직 취약함)",
            "evidence": rel(MONTHLY_STABILITY),
            "metric": f"best_validation_positive_months={best['validation_positive_months']}/{best['validation_months']};best_oos_positive_months={best['oos_positive_months']}/{best['oos_months']}",
            "judgment": "positive_but_not_promotion_candidate",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "stage364C_score_guard_family",
            "finding": "Hour17 score guard family has broad pass count(17시 점수 가드 계열은 통과 수가 넓음)",
            "evidence": rel(FAMILY_ATTRIBUTION),
            "metric": f"score_guard_pass_rows={score_guard.get('pass_rows', '')};best={score_guard.get('best_variant_id', '')};joint_context_best={joint_context.get('best_variant_id', '')}",
            "judgment": "feature_family_seed_only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "stage364C_next_packet_decision",
            "finding": "Open run364D training seed packet without candidate promotion(후보 승격 없이 364D 학습 씨앗 묶음을 연다)",
            "evidence": rel(TRAINING_SEED_QUEUE),
            "metric": f"next_run_id={NEXT_RUN_ID}",
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_training_seed_queue(review_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    top = review_rows[0]
    score_guard_rows = [row for row in review_rows if row["source_queue_id"] == "s364_r01_open_hour_context_stack"]
    best_score_guard = score_guard_rows[0] if score_guard_rows else top
    return [
        {
            "queue_id": "s364D_r01_hour_minute_context_guard_seed",
            "priority": 1,
            "source_variant_id": top["variant_id"],
            "source_artifact": rel(PASS_REVIEW),
            "action": "materialize timestamp-safe hour/minute context guard as training seed(시점 안전 시간/분 문맥 가드를 학습 씨앗으로 구체화)",
            "expected_effect": "keep density >= 3/day while reducing q05 cost drag(일 3회 이상 밀도를 유지하며 q05 비용 끌림을 줄임)",
            "guardrail": "no candidate selection until WFO and MT5 runtime probe(워크포워드와 MT5 런타임 탐침 전 후보 선택 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s364D_r02_hour17_score_guard_feature_family_seed",
            "priority": 2,
            "source_variant_id": best_score_guard["variant_id"],
            "source_artifact": rel(PASS_REVIEW),
            "action": "turn hour17 probability/margin guard into feature-family experiment(17시 확률/마진 가드를 피처 계열 실험으로 전환)",
            "expected_effect": "avoid hard-coded one-rule overfit and let model learn toxic context(하드코딩 단일 규칙 과적합을 피하고 모델이 유해 문맥을 학습)",
            "guardrail": "validation thresholds remain evidence only, not runtime authority(검증 임계값은 근거일 뿐 런타임 권위 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s364D_r03_month_fragility_control_seed",
            "priority": 3,
            "source_variant_id": top["variant_id"],
            "source_artifact": rel(MONTHLY_STABILITY),
            "action": "add monthly stability and WFO pressure control to next packet(다음 묶음에 월별 안정성과 WFO 압박 대조 추가)",
            "expected_effect": "stop positive split net from hiding month concentration(月별 집중이 양수 분할 순수익을 숨기지 못하게 함)",
            "guardrail": "do not promote if positive months remain sparse(양수 월이 희소하면 승격하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s364D_r04_dense_control_negative_anchor",
            "priority": 4,
            "source_variant_id": "s364_r00_all_long_dense_control",
            "source_artifact": rel(SOURCE_FAILURE_ATTRIBUTION),
            "action": "carry dense all-long control as negative anchor(전체 롱 고밀도 대조를 부정 앵커로 유지)",
            "expected_effect": "separate real context edge from raw split asymmetry(실제 문맥 우위와 원시 분할 비대칭을 분리)",
            "guardrail": "any model seed must beat dense control on validation and OOS(모든 모델 씨앗은 검증/표본외에서 고밀도 대조를 넘어야 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_role": path.stem,
            "path": rel(path),
            "sha256": sha256_file(path) if exists(path) and path.is_file() else "",
            "availability": "tracked_or_ignored_with_manifest",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_receipts(review_rows: Sequence[Mapping[str, Any]], monthly_rows: Sequence[Mapping[str, Any]], seed_rows: Sequence[Mapping[str, Any]]) -> None:
    write_json(WORK_PACKET, {
        "run_id": RUN_ID,
        "primary_family": "result_review(결과 검토)",
        "primary_skill": "obsidian-result-judgment(결과 판정)",
        "support_skills": [
            "obsidian-data-integrity(데이터 무결성)",
            "obsidian-artifact-lineage(산출물 계보)",
            "obsidian-exploration-mandate(탐색 명령)",
        ],
        "required_gates": [
            "input_presence",
            "source_gate_passed",
            "pass_review_materialized",
            "monthly_stability_materialized",
            "claim_boundary_enforced",
            "ledger_synced",
        ],
        "status": STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(DATA_INTEGRITY_RECEIPT, {
        "data_source": [rel(SOURCE_TRADE_TABLE), rel(SOURCE_CROSS_SPLIT)],
        "time_axis": TIME_AXIS,
        "sample_scope": "US100 M5 q05 long-only report-derived trades; validation and OOS only(US100 M5 q05 롱 단독 보고서 파생 거래, 검증/표본외만)",
        "missing_or_duplicate_check": "not re-audited from raw bars; inherited Stage364B input gate and trade-table row identity(원시 봉 재감사는 아님, 364B 입력 게이트와 거래표 정체성 상속)",
        "feature_label_boundary": "review reconstructs Stage364B variants; validation-derived thresholds already fixed before OOS application(364B 변형 복원, 검증 파생 임계값은 표본외 적용 전 고정)",
        "split_boundary": "validation and OOS are read from source trade table split column(검증/표본외는 원천 거래표 split 컬럼 사용)",
        "leakage_risk": "review selection can overfit to OOS; therefore no candidate selection or operating claim(OOS를 본 검토 선택 과적합 위험, 그래서 후보/운영 주장 없음)",
        "data_hash_or_identity": {
            "source_trade_table_sha256": sha256_file(SOURCE_TRADE_TABLE),
            "source_cross_split_sha256": sha256_file(SOURCE_CROSS_SPLIT),
            "review_rows": len(review_rows),
            "monthly_rows": len(monthly_rows),
        },
        "integrity_judgment": "usable_with_boundary",
    })
    write_json(LINEAGE_RECEIPT, {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": "python stage_pipelines/stage364/review_timestamp_context_cost_surface_without_db.py",
        "consumer": [rel(REPORT_PATH), rel(TRAINING_SEED_QUEUE), rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER)],
        "artifact_paths": [rel(PASS_REVIEW), rel(MONTHLY_STABILITY), rel(FAMILY_ATTRIBUTION), rel(TRAINING_SEED_QUEUE), rel(FINAL_DECISION)],
        "artifact_hashes": "written to docs/registers/artifact_registry.csv after closeout(종료 후 산출물 등록부에 기록)",
        "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked reports plus ignored run artifacts with manifest(추적 보고서와 manifest가 있는 ignored 실행 산출물)",
        "lineage_judgment": "connected_with_boundary",
    })
    write_json(JUDGMENT_RECEIPT, {
        "result_subject": RUN_ID,
        "evidence_available": [rel(PASS_REVIEW), rel(MONTHLY_STABILITY), rel(FAMILY_ATTRIBUTION), rel(REPORT_PATH), rel(FINAL_DECISION)],
        "evidence_missing": "no new model training, no new proxy execution, no MT5 execution, no candidate selection, Tier B missing_required(새 모델 학습 없음, 새 프록시 실행 없음, MT5 실행 없음, 후보 선택 없음, Tier B 필수 누락)",
        "judgment_label": "positive",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "timestamp context is a useful seed, not an operating model(시점 문맥은 유용한 씨앗이지 운영 모델은 아님)",
    })
    write_json(CLAIM_RECEIPT, {
        "run_id": RUN_ID,
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(RUN_MANIFEST, {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "command": "python stage_pipelines/stage364/review_timestamp_context_cost_surface_without_db.py",
        "input_manifest": rel(INPUT_MANIFEST),
        "outputs": [rel(PASS_REVIEW), rel(MONTHLY_STABILITY), rel(FAMILY_ATTRIBUTION), rel(TRAINING_SEED_QUEUE), rel(FINAL_DECISION)],
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    })
    best = review_rows[0]
    write_json(FINAL_DECISION, {
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "reviewed_pass_rows": len(review_rows),
        "monthly_stability_rows": len(monthly_rows),
        "training_seed_rows": len(seed_rows),
        "best_review_variant_id": best["variant_id"],
        "best_review_validation_cost_0_30_net": best["validation_cost_0_30_net"],
        "best_review_oos_cost_0_30_net": best["oos_cost_0_30_net"],
        "best_review_density_min": best["density_min"],
        "best_review_month_status": f"validation {best['validation_positive_months']}/{best['validation_months']}; oos {best['oos_positive_months']}/{best['oos_months']}",
        "primary_risk": "monthly_fragility_and_oos_seen_review_selection(월별 취약성과 OOS를 본 검토 선택)",
        "candidate_selection": "not_run",
        "new_model_training": "not_run",
        "new_proxy_execution": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_judgment": "positive_scout_reviewed_training_seed_only_no_selection",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_passes": 0,
        "gate_total": 0,
    })


def write_run_artifacts(review_rows: Sequence[Mapping[str, Any]], monthly_rows: Sequence[Mapping[str, Any]], family_rows: Sequence[Mapping[str, Any]], findings: Sequence[Mapping[str, Any]], seed_rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(PASS_REVIEW, review_rows)
    write_csv(MONTHLY_STABILITY, monthly_rows)
    write_csv(FAMILY_ATTRIBUTION, family_rows)
    write_csv(REVIEW_FINDINGS, findings)
    write_csv(TRAINING_SEED_QUEUE, seed_rows)
    write_receipts(review_rows, monthly_rows, seed_rows)


def gate_rows() -> list[dict[str, Any]]:
    final = read_json(FINAL_DECISION) if exists(FINAL_DECISION) else {}
    _, project_rows = read_csv_rows(PROJECT_LEDGER)
    _, stage_rows = read_csv_rows(STAGE_LEDGER)
    gates = [
        ("input_cross_split_present", exists(SOURCE_CROSS_SPLIT), SOURCE_CROSS_SPLIT, "Stage364B cross split(364B 교차 분할) 확인"),
        ("input_trade_table_present", exists(SOURCE_TRADE_TABLE), SOURCE_TRADE_TABLE, "q05 trade table(q05 거래표) 확인"),
        ("source_gate_passed", source_gate_passed(), SOURCE_GATE_AUDIT, "Stage364B gate(364B 게이트) 통과 확인"),
        ("source_pass_rows_expected", as_int(read_json(SOURCE_FINAL_DECISION).get("passing_cross_split_rows")) == 33, SOURCE_FINAL_DECISION, "source passing rows(원천 통과 행) 33 확인"),
        ("pass_review_materialized", exists(PASS_REVIEW) and as_int(final.get("reviewed_pass_rows")) == 33, PASS_REVIEW, "pass candidate review(통과 후보 검토) 33행"),
        ("monthly_stability_materialized", exists(MONTHLY_STABILITY) and as_int(final.get("monthly_stability_rows")) > 0, MONTHLY_STABILITY, "monthly stability(월별 안정성) 생성"),
        ("training_seed_queue_materialized", exists(TRAINING_SEED_QUEUE) and as_int(final.get("training_seed_rows")) >= 3, TRAINING_SEED_QUEUE, "run364D seed queue(364D 씨앗 대기열) 생성"),
        ("no_candidate_selection", final.get("candidate_selection") == "not_run", FINAL_DECISION, "candidate selection(후보 선택) 없음"),
        ("no_mt5_execution_claim", final.get("mt5_execution") == "not_run", FINAL_DECISION, "MT5 execution(MT5 실행) 없음"),
        ("report_present", exists(REPORT_PATH), REPORT_PATH, "review report(검토 보고서) 존재"),
        ("selection_status_synced", NEXT_RUN_ID in read_text(SELECTION_STATUS), SELECTION_STATUS, "selection status(선택 상태) 다음 실행 동기화"),
        ("workspace_state_synced", NEXT_RUN_ID in read_text(WORKSPACE_STATE), WORKSPACE_STATE, "workspace state(작업공간 상태) 다음 실행 동기화"),
        ("project_ledger_synced", sum(1 for row in project_rows if row.get("run_id") == RUN_ID) == 3, PROJECT_LEDGER, "project ledger(프로젝트 장부) 3행"),
        ("stage_ledger_synced", sum(1 for row in stage_rows if row.get("run_id") == RUN_ID) == 3, STAGE_LEDGER, "stage ledger(단계 장부) 3행"),
        ("claim_boundary_receipt", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "claim receipt(주장 영수증) 존재"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": rel(path),
            "description": description,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, description in gates
    ]


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return ""
    lines = ["|" + "|".join(columns) + "|", "|" + "|".join(["---"] * len(columns)) + "|"]
    for row in rows:
        lines.append("|" + "|".join(str(row.get(column, "")) for column in columns) + "|")
    return "\n".join(lines)


def write_reports(review_rows: Sequence[Mapping[str, Any]], family_rows: Sequence[Mapping[str, Any]], seed_rows: Sequence[Mapping[str, Any]]) -> None:
    final = read_json(FINAL_DECISION)
    gates = gate_rows()
    top_rows = list(review_rows[:8])
    report = f"""# run364C Timestamp Context Cost Surface Review(run364C 시점 문맥 비용 표면 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`

Action(행동): Stage364B(364B) passing rows(통과 행) `33`개를 실제 q05 trade table(q05 거래표)로 복원해 split/month/family stability(분할/월/계열 안정성)를 검토했다.

Effect(효과): timestamp context(시점 문맥)는 학습 씨앗으로 유지하지만, month fragility(월별 취약성)와 OOS-seen selection risk(OOS를 본 선택 위험) 때문에 candidate selection(후보 선택)이나 MT5 operating claim(MT5 운영 주장)은 하지 않는다.

## Result(결과)

- reviewed_pass_rows(검토 통과 행): `{final["reviewed_pass_rows"]}`
- monthly_stability_rows(월별 안정성 행): `{final["monthly_stability_rows"]}`
- training_seed_rows(학습 씨앗 행): `{final["training_seed_rows"]}`
- best_review_variant_id(최선 검토 변형 ID): `{final["best_review_variant_id"]}`
- best_review_validation_cost_0_30_net(최선 검토 검증 +0.30 비용 순수익): `{final["best_review_validation_cost_0_30_net"]}`
- best_review_oos_cost_0_30_net(최선 검토 표본외 +0.30 비용 순수익): `{final["best_review_oos_cost_0_30_net"]}`
- best_review_density_min(최선 검토 최소 밀도): `{final["best_review_density_min"]}`
- best_review_month_status(최선 검토 월 상태): `{final["best_review_month_status"]}`

## Top Review Rows(상위 검토 행)

{markdown_table(top_rows, ["review_rank", "variant_id", "source_queue_id", "validation_cost_0_30_net", "oos_cost_0_30_net", "density_min", "validation_positive_months", "oos_positive_months", "review_tier"])}

## Family Attribution(계열 귀속)

{markdown_table(family_rows, ["source_queue_id", "pass_rows", "avg_validation_cost_0_30_net", "avg_oos_cost_0_30_net", "best_variant_id", "fragile_rows", "family_judgment"])}

## Next Seed Queue(다음 씨앗 대기열)

{markdown_table(seed_rows, ["queue_id", "priority", "source_variant_id", "action", "guardrail"])}

## Judgment Boundary(판정 경계)

Action(행동): `run364D` training seed packet(학습 씨앗 묶음)을 열었다.

Effect(효과): 다음 작업은 context guard(문맥 가드)를 hard-coded runtime rule(하드코딩 런타임 규칙)로 승격하지 않고, feature/model/WFO pressure(피처/모델/WFO 압박)로 검증한다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report)

    write_text(DECISION_DOC, f"""# {TODAY} Stage364C Timestamp Context Surface Review Decision(364C 시점 문맥 표면 검토 결정)

- decision(결정): `{DECISION}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`

Action(행동): positive scout(긍정 스카우트)를 training seed(학습 씨앗)로 낮춰 보존했다.

Effect(효과): 월별 취약성과 OOS 선택 위험 때문에 promotion candidate(승격 후보)나 operating promotion(운영 승격)으로 올리지 않는다.

Evidence(근거): `{rel(PASS_REVIEW)}`, `{rel(MONTHLY_STABILITY)}`, `{rel(TRAINING_SEED_QUEUE)}`.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")

    write_text(SELECTION_STATUS, f"""# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `reviewed_training_seed_opened_no_selection(검토 완료, 학습 씨앗 열림, 선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## run364C Review Closeout(364C 검토 종료 기록)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gate_result(게이트 결과): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`
- reviewed_pass_rows(검토 통과 행): `{final["reviewed_pass_rows"]}`
- best_review_variant_id(최선 검토 변형 ID): `{final["best_review_variant_id"]}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage364B(364B)의 timestamp context(시점 문맥) 통과 행을 검토했다.

Effect(효과): Stage364(364단계)는 후보 선택 없이 training seed packet(학습 씨앗 묶음)으로 진행한다.
""")

    append_text_once(STAGE_BRIEF, "## run364C Review Closeout", f"""## run364C Review Closeout(364C 검토 종료)

Action(행동): timestamp context pass rows(시점 문맥 통과 행) `33`개를 monthly stability(월별 안정성)와 family attribution(계열 귀속)으로 검토했다.

Effect(효과): best seed(최선 씨앗)는 `{final["best_review_variant_id"]}`이지만, candidate selection(후보 선택) 없이 `{NEXT_RUN_ID}`로 넘긴다.
""")
    append_text_once(REVIEW_INDEX, "run364C_timestamp_context_cost_surface_review", f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}` - timestamp context cost surface review(시점 문맥 비용 표면 검토).""")
    append_text_once(STAGE_README, "run364C Review", f"""## run364C Review(364C 검토)

Action(행동): Stage364B(364B) positive scout(긍정 스카우트)를 월별 안정성과 과적합 위험으로 검토했다.

Effect(효과): 다음 실행은 `{NEXT_RUN_ID}`이고, 운영 주장은 없다.
""")


def replace_stage_brief_header() -> None:
    text = read_text(STAGE_BRIEF)
    replacements = {
        "- current_run_id(": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
        "- latest_completed_run_id(": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
        "- selection_status(": "- selection_status(선택 상태): `reviewed_training_seed_opened_no_selection(검토 완료, 학습 씨앗 열림, 선택 없음)`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    next_lines = []
    for line in text.splitlines():
        replaced = False
        for prefix, value in replacements.items():
            if line.startswith(prefix):
                next_lines.append(value)
                replaced = True
                break
        if not replaced:
            next_lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(next_lines))


def registry_rows(review_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    final = read_json(FINAL_DECISION)
    gates = gate_rows()
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "timestamp_context_review(시점 문맥 검토)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "notes": "Stage364C timestamp context review(Stage364C 시점 문맥 검토).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["reviewed_pass_rows"],
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(PASS_REVIEW),
        "result_status": STATUS,
        "sample_rows": final["reviewed_pass_rows"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "result_review(결과 검토)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "lane": "timestamp_context_review(시점 문맥 검토)",
        "family": "result_review(결과 검토)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Should timestamp context become a training seed?(시점 문맥을 학습 씨앗으로 넘길 것인가?)",
        "metric_scope": "review_only_no_runtime(검토 전용, 런타임 없음)",
    }
    best = review_rows[0]
    tier_a = dict(common)
    tier_a.update({
        "subrun_id": f"{RUN_ID}__Tier_A",
        "ledger_row_id": f"{RUN_ID}__Tier_A",
        "row_id": f"{RUN_ID}__Tier_A",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A",
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "kpi_scope": "report-derived review(보고서 파생 검토)",
        "primary_kpi": f"best={best['variant_id']};validation_net={best['validation_cost_0_30_net']};oos_net={best['oos_cost_0_30_net']};density_min={best['density_min']}",
        "guardrail_kpi": f"monthly_status=validation {best['validation_positive_months']}/{best['validation_months']};oos {best['oos_positive_months']}/{best['oos_months']};candidate_selection=not_run",
    })
    tier_b = dict(tier_a)
    tier_b.update({
        "subrun_id": f"{RUN_ID}__Tier_B",
        "ledger_row_id": f"{RUN_ID}__Tier_B",
        "row_id": f"{RUN_ID}__Tier_B",
        "record_view": "Tier B separate(Tier B 분리)",
        "tier_scope": "Tier B",
        "view": "Tier B separate(Tier B 분리)",
        "tier": "Tier B",
        "status": "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)",
        "primary_kpi": "missing_required(필수 누락)",
        "guardrail_kpi": "do_not_synthesize_tier_b(Tier B 합성 금지)",
    })
    combined = dict(tier_a)
    combined.update({
        "subrun_id": f"{RUN_ID}__Tier_AplusB",
        "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
        "row_id": f"{RUN_ID}__Tier_AplusB",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier_scope": "Tier A+B",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "status": "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)",
        "primary_kpi": "combined_not_run(합산 실행 없음)",
        "guardrail_kpi": "do_not_synthesize_combined_result(합산 결과 합성 금지)",
    })
    return [tier_a], [tier_a, tier_b, combined], [tier_a, tier_b, combined]


def write_registries(review_rows: Sequence[Mapping[str, Any]]) -> None:
    run_rows, project_rows, stage_rows = registry_rows(review_rows)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], stage_rows, extend_header=True)


def write_workspace_and_notes(review_rows: Sequence[Mapping[str, Any]]) -> None:
    best = review_rows[0]
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage364C(364C 실행)가 timestamp context cost surface(시점 문맥 비용 표면)의 통과 행 `33`개를 검토했다.

Effect(효과): 다음 작업은 `{NEXT_RUN_ID}`에서 `{best["variant_id"]}`와 hour17 score guard(17시 점수 가드)를 training seed(학습 씨앗)로 구체화한다.
""")
    append_text_once(WORKSPACE_CHANGELOG, "run364C_review_timestamp_context_cost_surface_without_db_v1", f"""## {TODAY} run364C Timestamp Context Cost Surface Review(364C 시점 문맥 비용 표면 검토)

Action(행동): Stage364B(364B) passing rows(통과 행) 33개를 split/month/family stability(분할/월/계열 안정성)로 검토했다.

Effect(효과): positive scout(긍정 스카우트)는 training seed(학습 씨앗)로 보존하고, candidate selection(후보 선택)과 MT5 operating claim(MT5 운영 주장)은 하지 않았다.
""")
    append_text_once(IDEA_REGISTRY, "IDEA-ST364C-TIMESTAMP-CONTEXT-TRAINING-SEED", f"""## IDEA-ST364C-TIMESTAMP-CONTEXT-TRAINING-SEED

- idea(아이디어): Stage364B(364B)의 timestamp context pass rows(시점 문맥 통과 행)를 hard-coded rule(하드코딩 규칙)이 아니라 model feature/training seed(모델 피처/학습 씨앗)로 넘긴다.
- best_seed(최선 씨앗): `{best["variant_id"]}`.
- seed_queue(씨앗 대기열): `{rel(TRAINING_SEED_QUEUE)}`.
- fragility_memory(취약성 기억): `{rel(MONTHLY_STABILITY)}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""")
    append_text_once(NEGATIVE_RESULT_REGISTER, "FM-ST364C-TIMESTAMP-CONTEXT-MONTH-FRAGILITY", f"""## {TODAY} FM-ST364C-TIMESTAMP-CONTEXT-MONTH-FRAGILITY

- source_run(원천 실행): `{RUN_ID}`
- failure_memory(실패 기억): timestamp context pass rows(시점 문맥 통과 행)는 split net(분할 순수익)은 양수지만 monthly positive coverage(월별 양수 커버리지)가 약하다.
- best_seed_status(최선 씨앗 상태): validation positive months(검증 양수 월) `{best["validation_positive_months"]}/{best["validation_months"]}`, OOS positive months(표본외 양수 월) `{best["oos_positive_months"]}/{best["oos_months"]}`.
- do_not_repeat(반복 금지): 이 상태를 promotion candidate(승격 후보)나 runtime authority(런타임 권위)로 과장하지 않는다.
- reopen_condition(재개 조건): `{NEXT_RUN_ID}`가 WFO/month stability(WFO/월 안정성)를 개선하고 MT5 runtime probe(MT5 런타임 탐침)로 재확인한다.
- evidence(근거): `{rel(MONTHLY_STABILITY)}`.
""")
    replace_stage_brief_header()


def write_artifact_registry() -> None:
    artifacts = [
        ("script", Path("stage_pipelines/stage364/review_timestamp_context_cost_surface_without_db.py"), "tracked"),
        ("review_report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("selection_status", SELECTION_STATUS, "tracked"),
        ("input_manifest", INPUT_MANIFEST, "ignored_with_manifest"),
        ("pass_candidate_review", PASS_REVIEW, "ignored_with_manifest"),
        ("monthly_stability", MONTHLY_STABILITY, "ignored_with_manifest"),
        ("family_attribution", FAMILY_ATTRIBUTION, "ignored_with_manifest"),
        ("review_findings", REVIEW_FINDINGS, "ignored_with_manifest"),
        ("training_seed_queue", TRAINING_SEED_QUEUE, "ignored_with_manifest"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]
    rows = []
    for artifact_type, path, availability in artifacts:
        rows.append({
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file(path) if exists(path) and Path(path).is_file() else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_ID}__{artifact_type}",
            "notes": f"Stage364C timestamp context review artifact(364C 시점 문맥 검토 산출물); availability={availability}",
            "artifact_path": rel(path),
        })
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "artifact_type", "path"], rows, extend_header=False)


def refresh_gates_and_final() -> None:
    gates = gate_rows()
    write_csv(GATE_AUDIT, gates)
    final = read_json(FINAL_DECISION)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    final["required_gate_coverage_audit"] = rel(GATE_AUDIT)
    write_json(FINAL_DECISION, final)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("Missing required Stage364C inputs: " + ", ".join(missing))
    final = read_json(SOURCE_FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"Stage364B final_decision next_run_id mismatch: {final.get('next_run_id')}")
    if as_int(final.get("passing_cross_split_rows")) != 33:
        raise RuntimeError("Stage364C expects Stage364B passing_cross_split_rows == 33")
    if not source_gate_passed():
        raise RuntimeError("Stage364B source gate audit is not fully passed")


def main() -> None:
    validate_inputs()
    review_rows, monthly_rows, family_rows = pass_reviews()
    seed_rows = build_training_seed_queue(review_rows)
    findings = build_findings(review_rows, family_rows)
    write_run_artifacts(review_rows, monthly_rows, family_rows, findings, seed_rows)
    write_reports(review_rows, family_rows, seed_rows)
    write_workspace_and_notes(review_rows)
    write_registries(review_rows)
    refresh_gates_and_final()
    write_reports(review_rows, family_rows, seed_rows)
    write_workspace_and_notes(review_rows)
    write_registries(review_rows)
    write_artifact_registry()
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
