from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

SOURCE_STAGE_ID = "362_long_only_margin_grid__cost_buffer_first_branch"
NEXT_STAGE_ID = "363_lower_floor_rank_surface__q05_long_density_recovery"

RUN_NUMBER = "run362C"
RUN_ID = "run362C_review_q05_long_only_margin_grid_without_db_v1"
PARENT_RUN_ID = "run362B_materialize_q05_long_only_margin_grid_without_db_v1"
NEXT_RUN_NUMBER = "run363A"
NEXT_RUN_ID = "run363A_branch_stage362_to_lower_floor_rank_surface_without_db_v1"
NEXT_STAGE_RUN_ID = "run363B_materialize_q05_lower_floor_rank_surface_without_db_v1"

STATUS = "completed_stage362C_q05_margin_grid_reviewed_no_selection_stage363_branch"
JUDGMENT = "negative_margin_grid_density_collapse_preserved_lower_floor_rank_seed_no_operating_claim"
DECISION = "stage362C_close_no_selection_open_stage363_lower_floor_rank_surface"
CLAIM_BOUNDARY = (
    "research_development_review_only_q05_margin_grid_negative_memory_and_stage363_handoff_"
    "no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

BRANCH_STATUS = "completed_stage363A_lower_floor_rank_surface_branch_opened_no_selection"
BRANCH_JUDGMENT = "stage363_lower_floor_rank_surface_opened_from_stage362_density_collapse_no_operating_claim"
BRANCH_DECISION = "stage363A_open_run363B_materialize_q05_lower_floor_rank_surface_without_db_v1"
BRANCH_CLAIM_BOUNDARY = (
    "state_sync_stage_branch_lower_floor_rank_surface_handoff_only_no_new_model_training_"
    "no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "mt5_report_open_close_time_joined_to_runtime_bar_time_no_timezone_conversion"

STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
STAGE_SPEC_DIR = STAGE_DIR / "00_spec"
STAGE_REVIEW_DIR = STAGE_DIR / "03_reviews"
STAGE_SELECTED_DIR = STAGE_DIR / "04_selected"

SOURCE_RUN_DIR = STAGE_DIR / "02_runs" / "run362B"
SOURCE_Q05_TABLE = SOURCE_RUN_DIR / "q05_long_trade_probability_table.csv"
SOURCE_CROSS_SPLIT = SOURCE_RUN_DIR / "margin_grid_cross_split.csv"
SOURCE_FAILURE_ATTRIBUTION = SOURCE_RUN_DIR / "margin_grid_failure_attribution.csv"
SOURCE_REVIEW_QUEUE = SOURCE_RUN_DIR / "run362C_review_queue.csv"
SOURCE_FINAL = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_REPORT = STAGE_REVIEW_DIR / "run362B_q05_long_only_margin_grid_materialization.md"
SOURCE_SCRIPT = ROOT / "stage_pipelines" / "stage362" / "materialize_q05_long_only_margin_grid_without_db.py"

INPUT_FILES = [
    SOURCE_Q05_TABLE,
    SOURCE_CROSS_SPLIT,
    SOURCE_FAILURE_ATTRIBUTION,
    SOURCE_REVIEW_QUEUE,
    SOURCE_FINAL,
    SOURCE_REPORT,
    SOURCE_SCRIPT,
]

REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
BRANCH_DECISION_TABLE = RUN_DIR / "stage363_branch_decision.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_DESIGN_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"

REPORT_PATH = STAGE_REVIEW_DIR / "run362C_q05_long_only_margin_grid_review.md"
STAGE_BRIEF = STAGE_SPEC_DIR / "stage_brief.md"
REVIEW_INDEX = STAGE_REVIEW_DIR / "review_index.md"
STAGE_LEDGER = STAGE_REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = STAGE_SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
NEXT_RUN_DIR = NEXT_STAGE_DIR / "02_runs" / NEXT_RUN_NUMBER
NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUT_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_REVIEW_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"

NEXT_STAGE_BRIEF = NEXT_SPEC_DIR / "stage_brief.md"
NEXT_INPUT_REFS = NEXT_INPUT_DIR / "input_refs.md"
NEXT_INPUT_MANIFEST = NEXT_INPUT_DIR / "stage363_input_manifest.csv"
NEXT_REPORT_PATH = NEXT_REVIEW_DIR / "run363A_stage_branch.md"
NEXT_REVIEW_INDEX = NEXT_REVIEW_DIR / "review_index.md"
NEXT_STAGE_LEDGER = NEXT_REVIEW_DIR / "stage_run_ledger.csv"
NEXT_SELECTION_STATUS = NEXT_SELECTED_DIR / "selection_status.md"
NEXT_STAGE_README = NEXT_STAGE_DIR / "README.md"
NEXT_BRANCH_HANDOFF = NEXT_RUN_DIR / "stage363_branch_handoff.csv"
NEXT_DESIGN_QUEUE = NEXT_RUN_DIR / "run363B_design_queue.csv"
NEXT_FINAL_DECISION = NEXT_RUN_DIR / "final_decision.json"
NEXT_GATE_AUDIT = NEXT_RUN_DIR / "required_gate_coverage_audit.csv"
NEXT_RUN_MANIFEST = NEXT_RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage362C_margin_grid_review_and_stage363_branch.md"


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


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Iterable[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    had_header = bool(fieldnames)
    for row in rows_list:
        for key in row:
            if key not in fieldnames and (extend_header or not had_header):
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys
    ]
    write_csv(path, [*kept, *rows_list], fieldnames)


def require_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {missing}")


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value == "" or value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def score_frame(frame: pd.DataFrame, feature_day_count: float, drag: float = 0.30) -> dict[str, Any]:
    trade_count = int(len(frame))
    density = trade_count / feature_day_count if feature_day_count else 0.0
    if trade_count == 0:
        return {
            "trade_count": 0,
            "density": round(density, 10),
            "net": 0.0,
            "profit_factor": "",
            "expectancy": "",
            "win_rate_percent": "",
        }
    adjusted = pd.to_numeric(frame["net_profit"], errors="coerce").fillna(0.0) - drag
    wins = adjusted[adjusted > 0]
    losses = adjusted[adjusted < 0]
    gross_profit = float(wins.sum())
    gross_loss = float(losses.sum())
    pf = gross_profit / abs(gross_loss) if gross_loss < 0 else None
    return {
        "trade_count": trade_count,
        "density": round(density, 10),
        "net": round(float(adjusted.sum()), 10),
        "profit_factor": round(pf, 10) if pf is not None else "",
        "expectancy": round(float(adjusted.mean()), 10),
        "win_rate_percent": round(float(len(wins) / trade_count * 100.0), 10),
    }


def load_trade_table() -> pd.DataFrame:
    frame = pd.read_csv(fs_path(SOURCE_Q05_TABLE))
    for column in [
        "net_profit",
        "p_short",
        "p_flat",
        "p_long",
        "margin_gap_actual",
        "p_long_minus_p_short",
        "p_long_minus_p_flat",
        "feature_day_count",
    ]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["open_time_dt"] = pd.to_datetime(frame["open_time"], errors="coerce")
    frame["open_hour"] = frame["open_time_dt"].dt.hour
    return frame


def feature_days(frame: pd.DataFrame, split: str) -> float:
    subset = frame.loc[frame["split"].eq(split)]
    if subset.empty:
        return 0.0
    return float(subset["feature_day_count"].dropna().max())


def build_review_findings(frame: pd.DataFrame) -> list[dict[str, Any]]:
    validation = frame.loc[frame["split"].eq("validation")]
    val_days = feature_days(frame, "validation")
    oos_days = feature_days(frame, "oos")

    findings: list[dict[str, Any]] = []

    def add_filter_row(finding_id: str, description: str, selected: Mapping[str, pd.DataFrame]) -> None:
        val_metrics = score_frame(selected["validation"], val_days)
        oos_metrics = score_frame(selected["oos"], oos_days)
        findings.append(
            {
                "finding_id": finding_id,
                "description": description,
                "validation_trades": val_metrics["trade_count"],
                "validation_density": val_metrics["density"],
                "validation_cost_0_30_net": val_metrics["net"],
                "validation_cost_0_30_pf": val_metrics["profit_factor"],
                "oos_trades": oos_metrics["trade_count"],
                "oos_density": oos_metrics["density"],
                "oos_cost_0_30_net": oos_metrics["net"],
                "oos_cost_0_30_pf": oos_metrics["profit_factor"],
                "review_judgment": (
                    "passes_review_gate"
                    if val_metrics["net"] > 0
                    and oos_metrics["net"] > 0
                    and val_metrics["density"] >= 3.0
                    and oos_metrics["density"] >= 3.0
                    else "fails_review_gate"
                ),
                "time_axis": TIME_AXIS,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    add_filter_row(
        "q05_all_long_cost_control",
        "all q05 long trades(q05 전체 롱 거래) keep density(밀도 유지) but fail validation cost(검증 비용 실패)",
        {
            "validation": frame.loc[frame["split"].eq("validation")],
            "oos": frame.loc[frame["split"].eq("oos")],
        },
    )

    for quantile in [0.20, 0.35, 0.40]:
        threshold = float(validation["margin_gap_actual"].quantile(quantile))
        add_filter_row(
            f"validation_margin_gap_q{int(quantile * 100):02d}",
            f"validation-derived margin_gap_actual quantile(검증 파생 마진 분위수) {quantile:.2f} threshold={threshold:.6f}",
            {
                "validation": frame.loc[
                    frame["split"].eq("validation") & (frame["margin_gap_actual"] >= threshold)
                ],
                "oos": frame.loc[frame["split"].eq("oos") & (frame["margin_gap_actual"] >= threshold)],
            },
        )

    for quantile in [0.15, 0.20, 0.35]:
        threshold = float(validation["p_long_minus_p_short"].quantile(quantile))
        add_filter_row(
            f"validation_long_minus_short_q{int(quantile * 100):02d}",
            f"validation-derived p_long_minus_p_short quantile(검증 파생 롱-숏 분위수) {quantile:.2f} threshold={threshold:.6f}",
            {
                "validation": frame.loc[
                    frame["split"].eq("validation") & (frame["p_long_minus_p_short"] >= threshold)
                ],
                "oos": frame.loc[frame["split"].eq("oos") & (frame["p_long_minus_p_short"] >= threshold)],
            },
        )

    return findings


def build_failure_memory(findings: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    all_long = next(row for row in findings if row["finding_id"] == "q05_all_long_cost_control")
    margin_q20 = next(row for row in findings if row["finding_id"] == "validation_margin_gap_q20")
    margin_q35 = next(row for row in findings if row["finding_id"] == "validation_margin_gap_q35")
    return [
        {
            "memory_id": "FM-ST362C-Q05-MARGIN-GRID-DENSITY-COLLAPSE",
            "hypothesis": "q05 long-only margin grid(q05 롱 단독 마진 격자)가 비용 버퍼를 회복한다",
            "variants_tried": "35 designed grid rows + validation-derived rank probes(35개 설계 격자 + 검증 파생 순위 탐침)",
            "failed_boundary": "report-derived materialization review(보고서 파생 구체화 검토)",
            "why_failed": (
                f"all_long validation_cost_0_30_net={all_long['validation_cost_0_30_net']} and "
                f"margin_q35 validation_density={margin_q35['validation_density']}"
            ),
            "salvage_value": (
                f"margin_q20 near miss(근접 실패) validation_net={margin_q20['validation_cost_0_30_net']} "
                f"oos_net={margin_q20['oos_cost_0_30_net']}"
            ),
            "reopen_condition": "Stage363 lower-floor/rank surface(363단계 낮은 하한/순위 표면)가 density>=3 and validation/OOS cost positive(밀도 3 이상 및 검증/표본외 비용 양수)를 회복할 때",
            "do_not_repeat": "p_long_floor>=0.40 margin-only tightening(p_long 하한 0.40 이상 마진 단독 조임)을 후보 선택처럼 반복하지 않는다",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_stage363_design_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "s363_r01_no_filter_cost_control",
            "priority": 1,
            "surface_family": "dense_control(고밀도 대조)",
            "hypothesis": "all q05 long-only(q05 전체 롱 단독)는 density(밀도)를 유지하지만 validation cost(검증 비용)가 깨지는 기준선이다",
            "changed_variables": "none_control(변경 없음 대조)",
            "planned_grid": "single all-long control(전체 롱 단일 대조)",
            "success_criteria": "documents baseline loss before lower-floor search(낮은 하한 탐색 전 기준 손실 기록)",
            "failure_criteria": "missing q05 trade table(q05 거래 표 누락)",
            "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s363_r02_lower_absolute_floor_dense_margin",
            "priority": 2,
            "surface_family": "lower_floor_margin(낮은 하한 마진)",
            "hypothesis": "p_long floor(p_long 하한)를 0.33-0.36으로 낮추면 validation density(검증 밀도)를 살린 채 cost drag(비용 끌림)를 줄일 수 있다",
            "changed_variables": "p_long_floor=[0.330,0.335,0.340,0.345,0.350,0.355,0.360]; margin_gap=[-0.010,-0.005,0.000,0.002,0.004,0.006,0.008]",
            "planned_grid": "49 absolute threshold rows(49개 절대 임계값 행)",
            "success_criteria": "validation/OOS cost_0_30_net > 0 and density >= 3(검증/표본외 비용 후 순수익 양수 및 밀도 3 이상)",
            "failure_criteria": "cost positive only below density 3(비용 양수가 밀도 3 미만에만 존재)",
            "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s363_r03_validation_quantile_margin_rank",
            "priority": 3,
            "surface_family": "validation_rank_margin(검증 순위 마진)",
            "hypothesis": "validation-derived margin quantile(검증 파생 마진 분위수)를 OOS(표본외)에 고정 적용하면 OOS tuning(표본외 튜닝) 없이 cliff(절벽)를 볼 수 있다",
            "changed_variables": "margin_gap_actual validation quantile q=[0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40]",
            "planned_grid": "8 rank rows(8개 순위 행)",
            "success_criteria": "q threshold from validation only(검증에서만 분위수 산출), OOS applied unchanged(표본외 고정 적용)",
            "failure_criteria": "validation threshold becomes split-local OOS tuned(검증 임계값이 표본외 튜닝으로 바뀜)",
            "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s363_r04_target_density_margin_boundary",
            "priority": 4,
            "surface_family": "target_density_boundary(목표 밀도 경계)",
            "hypothesis": "minimum margin threshold that keeps validation density >=3(검증 밀도 3 이상 유지 최소 마진 임계값)가 cost near-miss(비용 근접 실패)를 드러낸다",
            "changed_variables": "target_density=[3.0,3.2,3.5]; score=margin_gap_actual",
            "planned_grid": "3 target-density rows(3개 목표 밀도 행)",
            "success_criteria": "validation density target met and validation cost loss narrows(검증 밀도 충족 및 검증 비용 손실 축소)",
            "failure_criteria": "density target preserves negative validation cost(밀도 목표가 검증 비용 손실을 보존)",
            "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s363_r05_long_minus_short_rank",
            "priority": 5,
            "surface_family": "long_short_rank(롱-숏 순위)",
            "hypothesis": "p_long_minus_p_short(롱-숏 차이)는 p_flat(관망) 과민 반응보다 안정적인 cost filter(비용 필터)일 수 있다",
            "changed_variables": "p_long_minus_p_short validation quantile q=[0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40]",
            "planned_grid": "8 rank rows(8개 순위 행)",
            "success_criteria": "both splits cost positive while density >=3(양쪽 분할 비용 양수 및 밀도 3 이상)",
            "failure_criteria": "same density collapse as Stage362B(362B와 같은 밀도 붕괴)",
            "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s363_r06_two_axis_soft_rank",
            "priority": 6,
            "surface_family": "two_axis_rank(두 축 순위)",
            "hypothesis": "margin rank + long-short rank(마진 순위 + 롱-숏 순위)를 부드럽게 합치면 단일 마진 필터보다 loss hour(손실 시간)를 덜 자른다",
            "changed_variables": "score=rank(margin_gap_actual)+rank(p_long_minus_p_short); cutoff quantile q=[0.05..0.40]",
            "planned_grid": "8 combined-rank rows(8개 합성 순위 행)",
            "success_criteria": "validation cost improves without OOS cliff(표본외 절벽 없이 검증 비용 개선)",
            "failure_criteria": "validation/OOS split disagreement widens(검증/표본외 괴리 확대)",
            "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s363_r07_hour_loss_attribution_only",
            "priority": 7,
            "surface_family": "session_attribution_only(세션 귀속 전용)",
            "hypothesis": "hour-level loss concentration(시간별 손실 집중)은 rank surface(순위 표면)의 보조 설명으로만 쓴다",
            "changed_variables": "open_hour attribution, no candidate selection(진입 시간 귀속, 후보 선택 없음)",
            "planned_grid": "hour summary only(시간 요약 전용)",
            "success_criteria": "explains validation cost drag(검증 비용 끌림 설명)",
            "failure_criteria": "session pruning used as candidate shortcut(세션 절단을 후보 지름길로 사용)",
            "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s363_r08_extreme_sparse_upper_bound",
            "priority": 8,
            "surface_family": "sparse_upper_bound(희소 상한)",
            "hypothesis": "positive but sparse pocket(양수지만 희소한 구간)을 upper bound(상한)로 보존해 density cliff(밀도 절벽)를 계량한다",
            "changed_variables": "margin/p_long quantile q=[0.45,0.50,0.60]",
            "planned_grid": "6 sparse rows(6개 희소 행)",
            "success_criteria": "records cliff boundary(절벽 경계 기록)",
            "failure_criteria": "sparse result promoted despite density fail(밀도 실패 희소 결과를 승격)",
            "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("stage362b_artifacts_visible", exists(SOURCE_FINAL), SOURCE_FINAL, "Stage362B final decision(362B 최종 결정) 확인"),
        ("q05_trade_table_visible", exists(SOURCE_Q05_TABLE), SOURCE_Q05_TABLE, "q05 trade probability table(q05 거래 확률 표) 확인"),
        ("review_queue_consumed", exists(SOURCE_REVIEW_QUEUE), SOURCE_REVIEW_QUEUE, "run362C review queue(검토 대기열) 소비"),
        ("review_findings_recorded", exists(REVIEW_FINDINGS), REVIEW_FINDINGS, "review findings(검토 결과) 기록"),
        ("failure_memory_recorded", exists(FAILURE_MEMORY), FAILURE_MEMORY, "failure memory(실패 기억) 기록"),
        ("stage363_design_queue_created", exists(NEXT_DESIGN_QUEUE), NEXT_DESIGN_QUEUE, "Stage363 design queue(설계 대기열) 생성"),
        ("next_stage_docs_created", exists(NEXT_STAGE_BRIEF), NEXT_STAGE_BRIEF, "Stage363 docs(문서) 생성"),
        ("tier_records_recorded", exists(STAGE_LEDGER), STAGE_LEDGER, "Tier A/B/A+B records(티어 기록) 기록"),
        ("state_sync_audit", exists(WORKSPACE_STATE), WORKSPACE_STATE, "current truth(현재 진실) Stage363으로 동기화"),
        ("artifact_lineage_audit", exists(LINEAGE_RECEIPT), LINEAGE_RECEIPT, "artifact lineage(산출물 계보) 연결"),
        ("result_judgment_boundary", exists(JUDGMENT_RECEIPT), JUDGMENT_RECEIPT, "negative/no-selection judgment(부정/선택 없음 판정) 경계"),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "operating claim(운영 주장) 차단"),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "required gates(필수 게이트) 자체 기록"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "path": rel(path),
            "notes": notes,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, notes in gates
    ]


def branch_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("stage363_structure_created", exists(NEXT_STAGE_DIR), NEXT_STAGE_DIR, "Stage363 structure(363단계 구조) 생성"),
        ("stage363_design_queue_created", exists(NEXT_DESIGN_QUEUE), NEXT_DESIGN_QUEUE, "Stage363 design queue(설계 대기열) 생성"),
        ("stage363_selection_status_sync", exists(NEXT_SELECTION_STATUS), NEXT_SELECTION_STATUS, "Stage363 selection status(선택 상태) 동기화"),
        ("stage363_ledger_sync", exists(NEXT_STAGE_LEDGER), NEXT_STAGE_LEDGER, "Stage363 ledger(장부) 동기화"),
        ("state_sync_audit", exists(WORKSPACE_STATE), WORKSPACE_STATE, "current truth(현재 진실) 동기화"),
        ("final_claim_guard", True, NEXT_FINAL_DECISION, "operating claim(운영 주장) 없음"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "path": rel(path),
            "notes": notes,
            "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, notes in gates
    ]


def write_run_artifacts(
    findings: Sequence[Mapping[str, Any]],
    failure_memory: Sequence[Mapping[str, Any]],
    design_queue: Sequence[Mapping[str, Any]],
) -> None:
    write_csv(REVIEW_FINDINGS, findings)
    write_csv(FAILURE_MEMORY, failure_memory)
    write_csv(
        BRANCH_DECISION_TABLE,
        [
            {
                "run_id": RUN_ID,
                "decision": DECISION,
                "next_stage_id": NEXT_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "next_materialization_run_id": NEXT_STAGE_RUN_ID,
                "reason": "Stage362B margin-only filter collapsed density(362B 마진 단독 필터가 밀도를 붕괴)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(NEXT_BRANCH_HANDOFF, [
        {
            "source_run_id": RUN_ID,
            "next_stage_id": NEXT_STAGE_ID,
            "next_run_id": NEXT_RUN_ID,
            "design_queue": rel(NEXT_DESIGN_QUEUE),
            "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        }
    ])
    write_csv(NEXT_DESIGN_QUEUE, design_queue)

    gates = gate_rows()
    branch_gates = branch_gate_rows()
    write_csv(GATE_AUDIT, gates)
    write_csv(NEXT_GATE_AUDIT, branch_gates)

    write_json(WORK_PACKET, {
        "run_id": RUN_ID,
        "primary_family": "experiment_design(실험 설계)",
        "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
        "support_skills": [
            "obsidian-reentry-read(재진입 확인)",
            "obsidian-data-integrity(데이터 무결성)",
            "obsidian-result-judgment(결과 판정)",
            "obsidian-artifact-lineage(산출물 계보)",
        ],
        "required_gates": [row["gate_id"] for row in gates],
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(DATA_INTEGRITY_RECEIPT, {
        "data_source": [rel(SOURCE_Q05_TABLE), rel(SOURCE_CROSS_SPLIT), rel(SOURCE_FAILURE_ATTRIBUTION)],
        "time_axis": TIME_AXIS,
        "sample_scope": "US100 M5 q05 long-only MT5 report-derived validation/OOS closed trades(US100 M5 q05 롱 단독 MT5 보고서 파생 검증/표본외 종료 거래)",
        "missing_or_duplicate_check": "source run362B already matched 1114 long trades; run362C reviews derived rows only(원천 362B가 1114개 롱 거래를 매칭했고 362C는 파생 행만 검토)",
        "feature_label_boundary": "no new features or labels; open-time probabilities only(새 피처/라벨 없음, 진입 시점 확률만 사용)",
        "split_boundary": "validation and OOS remain separate; validation-derived rank thresholds proposed for Stage363(검증/표본외 분리 유지, 363단계는 검증 파생 순위 임계값 제안)",
        "leakage_risk": "OOS-tuned threshold selection if Stage363 derives quantiles from OOS(363단계가 표본외 분위수를 만들면 누수 위험)",
        "data_hash_or_identity": {"q05_table_sha256": sha256_file(SOURCE_Q05_TABLE)},
        "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)",
    })
    write_json(EXPERIMENT_DESIGN_RECEIPT, {
        "hypothesis": "lower-floor/rank surface(낮은 하한/순위 표면)가 q05 long-only cost drag(비용 끌림)를 줄이면서 density(밀도)를 보존한다",
        "decision_use": "Stage363B materialization queue(363B 구체화 대기열) 선택",
        "comparison_baseline": "Stage362B 35-row margin grid and q05 all-long cost control(362B 35개 마진 격자와 q05 전체 롱 비용 대조)",
        "control_variables": ["US100", "M5", "q05 runtime probabilities", "+0.30 cost drag", "validation/OOS split"],
        "changed_variables": ["p_long floor", "margin rank", "long-short rank", "target density boundary", "hour attribution only"],
        "sample_scope": "Tier A report-derived validation/OOS; Tier B missing_required(티어 A 보고서 파생 검증/표본외, 티어 B 필수 누락)",
        "success_criteria": "validation/OOS cost_0_30_net > 0, density >= 3, no candidate selection without MT5(검증/표본외 비용 후 양수, 밀도 3 이상, MT5 없이 후보 선택 없음)",
        "failure_criteria": "positive cost only below density 3 or split-specific cliff(비용 양수가 밀도 3 미만 또는 분할 절벽에만 존재)",
        "invalid_conditions": "OOS-derived thresholds, missing q05 table, altered time axis(표본외 파생 임계값, q05 표 누락, 시간축 변경)",
        "stop_conditions": "all Stage363 queue rows fail density/cost; then pivot to regime/label source(363 대기열 전부 밀도/비용 실패 시 국면/라벨 원천으로 전환)",
        "evidence_plan": [rel(NEXT_DESIGN_QUEUE), rel(NEXT_GATE_AUDIT), rel(NEXT_REPORT_PATH)],
    })
    write_json(LINEAGE_RECEIPT, {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path("stage_pipelines/stage362/review_q05_long_only_margin_grid_and_branch_stage363_without_db.py")),
        "consumer": [rel(REPORT_PATH), rel(NEXT_DESIGN_QUEUE), rel(NEXT_STAGE_BRIEF)],
        "artifact_paths": [rel(REVIEW_FINDINGS), rel(FAILURE_MEMORY), rel(NEXT_DESIGN_QUEUE), rel(REPORT_PATH), rel(NEXT_REPORT_PATH)],
        "artifact_hashes": {
            rel(SOURCE_Q05_TABLE): sha256_file(SOURCE_Q05_TABLE),
            rel(SOURCE_FINAL): sha256_file(SOURCE_FINAL),
        },
        "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(NEXT_STAGE_LEDGER)],
        "availability": "tracked_docs_with_ignored_run_artifacts(추적 문서와 무시 실행 산출물)",
        "lineage_judgment": "connected_with_boundary(경계 내 연결됨)",
    })
    write_json(JUDGMENT_RECEIPT, {
        "result_subject": RUN_ID,
        "evidence_available": [rel(SOURCE_FINAL), rel(REVIEW_FINDINGS), rel(FAILURE_MEMORY), rel(NEXT_DESIGN_QUEUE)],
        "evidence_missing": "no new MT5 execution, no candidate selection, Tier B missing_required(새 MT5 실행 없음, 후보 선택 없음, 티어 B 필수 누락)",
        "judgment_label": "negative(부정)",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_STAGE_RUN_ID,
        "user_explanation_hook": "margin-only filter was too sparse; next surface lowers floor and uses validation-derived rank(마진 단독 필터가 너무 희소했고 다음 표면은 하한을 낮추고 검증 파생 순위를 쓴다)",
    })
    write_json(CLAIM_RECEIPT, {
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "operating_promotion": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    })
    final = {
        "stage_id": SOURCE_STAGE_ID,
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "next_materialization_run_id": NEXT_STAGE_RUN_ID,
        "review_findings_rows": len(findings),
        "failure_memory_rows": len(failure_memory),
        "stage363_design_queue_rows": len(design_queue),
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "operating_promotion": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FINAL_DECISION, final)
    write_json(RUN_MANIFEST, {
        "run_id": RUN_ID,
        "created_at_utc": now_utc(),
        "command": "python stage_pipelines/stage362/review_q05_long_only_margin_grid_and_branch_stage363_without_db.py",
        "inputs": [rel(path) for path in INPUT_FILES],
        "outputs": [rel(REVIEW_FINDINGS), rel(FAILURE_MEMORY), rel(NEXT_DESIGN_QUEUE), rel(REPORT_PATH), rel(NEXT_REPORT_PATH)],
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(NEXT_FINAL_DECISION, {
        "stage_id": NEXT_STAGE_ID,
        "run_number": NEXT_RUN_NUMBER,
        "run_id": NEXT_RUN_ID,
        "parent_run_id": RUN_ID,
        "status": BRANCH_STATUS,
        "judgment": BRANCH_JUDGMENT,
        "decision": BRANCH_DECISION,
        "next_run_id": NEXT_STAGE_RUN_ID,
        "design_queue_rows": len(design_queue),
        "gate_passes": sum(1 for row in branch_gates if row["status"] == "passed"),
        "gate_total": len(branch_gates),
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "operating_promotion": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BRANCH_CLAIM_BOUNDARY,
    })
    write_json(NEXT_RUN_MANIFEST, {
        "run_id": NEXT_RUN_ID,
        "created_at_utc": now_utc(),
        "producer": rel(Path("stage_pipelines/stage362/review_q05_long_only_margin_grid_and_branch_stage363_without_db.py")),
        "inputs": [rel(FINAL_DECISION), rel(REVIEW_FINDINGS), rel(FAILURE_MEMORY)],
        "outputs": [rel(NEXT_DESIGN_QUEUE), rel(NEXT_BRANCH_HANDOFF), rel(NEXT_REPORT_PATH)],
        "claim_boundary": BRANCH_CLAIM_BOUNDARY,
    })


def best_finding(findings: Sequence[Mapping[str, Any]], key: str) -> Mapping[str, Any]:
    return max(findings, key=lambda row: as_float(row[key]))


def write_reports(findings: Sequence[Mapping[str, Any]], failure_memory: Sequence[Mapping[str, Any]], design_queue: Sequence[Mapping[str, Any]]) -> None:
    best_validation = best_finding(findings, "validation_cost_0_30_net")
    best_oos = best_finding(findings, "oos_cost_0_30_net")
    margin_q20 = next(row for row in findings if row["finding_id"] == "validation_margin_gap_q20")
    gates = gate_rows()
    branch_gates = branch_gate_rows()

    write_text(REPORT_PATH, f"""# run362C Q05 Long-Only Margin Grid Review(run362C q05 롱 단독 마진 격자 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_stage_id(다음 단계 ID): `{NEXT_STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`

Action(행동): Stage362B(362B 실행)의 margin grid(마진 격자)를 검토하고 lower-floor/rank surface(낮은 하한/순위 표면) 분기를 열었다.

Effect(효과): Stage362(362단계)는 candidate selection(후보 선택) 없이 닫고, Stage363(363단계)는 density recovery(밀도 회복) 질문만 가볍게 받는다.

## Review Result(검토 결과)

- review_findings_rows(검토 결과 행): `{len(findings)}`
- stage363_design_queue_rows(363단계 설계 대기열 행): `{len(design_queue)}`
- best_validation_finding(최선 검증 항목): `{best_validation["finding_id"]}`
- best_validation_cost_0_30_net(최선 검증 +0.30 비용 순수익): `{best_validation["validation_cost_0_30_net"]}`
- best_validation_density(최선 검증 밀도): `{best_validation["validation_density"]}`
- best_oos_finding(최선 표본외 항목): `{best_oos["finding_id"]}`
- best_oos_cost_0_30_net(최선 표본외 +0.30 비용 순수익): `{best_oos["oos_cost_0_30_net"]}`
- margin_q20_validation_near_miss(q20 검증 근접 실패): net `{margin_q20["validation_cost_0_30_net"]}`, density `{margin_q20["validation_density"]}`

## Judgment Boundary(판정 경계)

Action(행동): margin-only tightening(마진 단독 조임)을 no-selection negative memory(선택 없음 부정 기억)로 닫았다.

Effect(효과): sparse positive pockets(희소 양수 구간)는 운영 의미가 아니라 Stage363(363단계)의 lower-floor/rank seed(낮은 하한/순위 씨앗)로만 보존한다.

## Artifacts(산출물)

- review_findings(검토 결과): `{rel(REVIEW_FINDINGS)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY)}`
- branch_decision(분기 결정): `{rel(BRANCH_DECISION_TABLE)}`
- stage363_design_queue(363단계 설계 대기열): `{rel(NEXT_DESIGN_QUEUE)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")

    write_text(SELECTION_STATUS, f"""# Stage362 Selection Status(362단계 선택 상태)

- selection_status(선택 상태): `reviewed_no_selection_branched_to_stage363(검토 완료, 선택 없음, 363단계 분기)`
- active_stage_id(활성 단계 ID): `{SOURCE_STAGE_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- next_stage_id(다음 단계 ID): `{NEXT_STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## run362C Review Closeout(362C 검토 종료 기록)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gate_result(게이트 결과): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`
- stage363_design_queue_rows(363단계 설계 대기열 행): `{len(design_queue)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): margin grid(마진 격자)를 no-selection(선택 없음)으로 닫았다.

Effect(효과): 다음 작업은 Stage363B(363B 실행) lower-floor/rank materialization(낮은 하한/순위 구체화)이다.
""")

    append_text_once(STAGE_BRIEF, "## run362C Review Closeout", f"""## run362C Review Closeout(362C 검토 종료)

Action(행동): Stage362B(362B 실행)의 35-row margin grid(35행 마진 격자)와 rank near-miss(순위 근접 실패)를 검토했다.

Effect(효과): validation/OOS(검증/표본외) cost positive(비용 양수)와 density >= 3(밀도 3 이상)를 동시에 만족한 행이 없어 Stage362(362단계)는 후보 선택 없이 Stage363(363단계) lower-floor/rank surface(낮은 하한/순위 표면)로 분기한다.
""")
    append_text_once(REVIEW_INDEX, "run362C_q05_long_only_margin_grid_review", f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}` - q05 long-only margin grid review(q05 롱 단독 마진 격자 검토) and Stage363 branch(363단계 분기).""")
    append_text_once(STAGE_README, "run362C Review", f"""## run362C Review(362C 검토)

Action(행동): margin-only surface(마진 단독 표면)를 no-selection negative memory(선택 없음 부정 기억)로 닫았다.

Effect(효과): Stage363(363단계)은 lower-floor/rank surface(낮은 하한/순위 표면)만 작게 탐색한다.
""")

    write_text(NEXT_STAGE_BRIEF, f"""# Stage363 Brief(363단계 개요): Lower-Floor Rank Surface(낮은 하한 순위 표면)

- canonical_stage_id(정식 단계 ID): `{NEXT_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_STAGE_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{NEXT_RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_run_id(원천 실행 ID): `{RUN_ID}`
- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- claim_boundary(주장 경계): `{BRANCH_CLAIM_BOUNDARY}`

## Question(질문)

Can lower p_long floor and validation-derived rank/quantile surface(낮은 p_long 하한 및 검증 파생 순위/분위수 표면) recover +0.30 cost buffer(+0.30 비용 버퍼) without density collapse(밀도 붕괴 없이 회복할 수 있는가)?

## Source Truth(원천 진실)

- source_failure(원천 실패): Stage362B margin-only filter(362B 마진 단독 필터)는 passing_cross_split_rows(교차 분할 통과 행) `0`.
- preserved_clue(보존 단서): margin_q20 near miss(q20 마진 근접 실패)는 validation loss(검증 손실)를 크게 줄였지만 아직 cost positive(비용 양수)가 아니다.
- no_selection_boundary(선택 없음 경계): candidate selection(후보 선택), MT5 execution(MT5 실행), operating promotion(운영 승격) 없음.

## Scope(범위)

Action(행동): Stage363(363단계)는 Stage362C(362C 실행)의 design queue(설계 대기열)만 먼저 구체화한다.

Effect(효과): regime/label/router(국면/라벨/라우터)를 아직 붙이지 않고 lower-floor/rank(낮은 하한/순위) 질문만 작게 확인한다.

## Exploration Boundary(탐색 경계)

- idea_id(아이디어 ID): `IDEA-ST363-Q05-LOWER-FLOOR-RANK-SURFACE`
- hypothesis(가설): absolute p_long floor(절대 p_long 하한)를 낮추고 validation-derived rank(검증 파생 순위)를 쓰면 density(밀도)를 보존하면서 cost drag(비용 끌림)를 줄일 수 있다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): lower p_long floor(낮은 p_long 하한), margin rank(마진 순위), long-short rank(롱-숏 순위), target density boundary(목표 밀도 경계)
- extreme_sweep(극단 탐색): all-long dense control(전체 롱 고밀도 대조), sparse upper bound(희소 상한), hour attribution only(시간 귀속 전용)
- micro_search_gate(미세 탐색 게이트): validation/OOS +0.30 net positive(검증/표본외 +0.30 순수익 양수) 그리고 density >= 3(밀도 3 이상)
- wfo_plan(WFO 계획): Stage363B(363B 실행)가 positive scout(긍정 탐색)를 만들 때만 WFO(walk-forward optimization, 워크포워드 최적화)로 강화한다.
- failure_memory(실패 기억): Stage362C(362C 실행)는 p_long_floor>=0.40 margin-only tightening(마진 단독 조임)을 반복 금지로 기록했다.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`
""")
    write_text(NEXT_INPUT_REFS, f"""# Stage363 Input References(363단계 입력 참조)

Action(행동): Stage363(363단계)의 입력 참조를 Stage362C(362C 실행) 산출물에 고정한다.

Effect(효과): 다음 materialization(구체화)이 다른 표본이나 OOS-tuned threshold(표본외 튜닝 임계값)를 몰래 쓰지 못하게 한다.

- source_review_report(원천 검토 보고서): `{rel(REPORT_PATH)}`
- source_review_findings(원천 검토 결과): `{rel(REVIEW_FINDINGS)}`
- source_failure_memory(원천 실패 기억): `{rel(FAILURE_MEMORY)}`
- design_queue(설계 대기열): `{rel(NEXT_DESIGN_QUEUE)}`
- q05_trade_probability_table(q05 거래 확률 표): `{rel(SOURCE_Q05_TABLE)}`
""")
    write_csv(NEXT_INPUT_MANIFEST, [
        {"input_id": "source_review_report", "path": rel(REPORT_PATH), "sha256": sha256_file(REPORT_PATH), "availability": "tracked"},
        {"input_id": "source_review_findings", "path": rel(REVIEW_FINDINGS), "sha256": sha256_file(REVIEW_FINDINGS), "availability": "ignored_with_manifest"},
        {"input_id": "source_failure_memory", "path": rel(FAILURE_MEMORY), "sha256": sha256_file(FAILURE_MEMORY), "availability": "ignored_with_manifest"},
        {"input_id": "design_queue", "path": rel(NEXT_DESIGN_QUEUE), "sha256": sha256_file(NEXT_DESIGN_QUEUE), "availability": "ignored_with_manifest"},
        {"input_id": "q05_trade_probability_table", "path": rel(SOURCE_Q05_TABLE), "sha256": sha256_file(SOURCE_Q05_TABLE), "availability": "ignored_with_manifest"},
    ])
    write_text(NEXT_REPORT_PATH, f"""# run363A Stage Branch(run363A 단계 분기): Lower-Floor Rank Surface(낮은 하한 순위 표면)

- run_id(실행 ID): `{NEXT_RUN_ID}`
- parent_run_id(부모 실행 ID): `{RUN_ID}`
- status(상태): `{BRANCH_STATUS}`
- judgment(판정): `{BRANCH_JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_STAGE_RUN_ID}`
- gate_result(게이트 결과): `{sum(1 for row in branch_gates if row["status"] == "passed")}/{len(branch_gates)}`

Action(행동): Stage362C(362C 실행)의 no-selection review(선택 없음 검토)를 Stage363(363단계) lower-floor/rank surface(낮은 하한/순위 표면)로 분기했다.

Effect(효과): 다음 작업은 run363B(363B 실행)에서 design queue(설계 대기열) `8`개를 구체화하는 것이다.

Claim Boundary(주장 경계): `{BRANCH_CLAIM_BOUNDARY}`
""")
    write_text(NEXT_REVIEW_INDEX, f"""# Stage363 Review Index(363단계 검토 색인)

- `{NEXT_RUN_ID}`: `{rel(NEXT_REPORT_PATH)}` - Stage363 branch(363단계 분기) and design queue handoff(설계 대기열 인계).
""")
    write_text(NEXT_SELECTION_STATUS, f"""# Stage363 Selection Status(363단계 선택 상태)

- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- active_stage_id(활성 단계 ID): `{NEXT_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_STAGE_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{NEXT_RUN_ID}`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): lower-floor/rank surface(낮은 하한/순위 표면) 탐색 stage(단계)를 열었다.

Effect(효과): Stage363B(363B 실행)는 MT5 execution(MT5 실행)이나 candidate selection(후보 선택) 없이 report-derived materialization(보고서 파생 구체화)만 수행한다.
""")
    write_text(NEXT_STAGE_README, f"""# Stage363(363단계): Lower-Floor Rank Surface(낮은 하한 순위 표면)

Action(행동): Stage362C(362C 실행)의 density collapse(밀도 붕괴) 실패 기억에서 lower-floor/rank surface(낮은 하한/순위 표면)를 분기했다.

Effect(효과): q05 long-only edge(q05 롱 단독 우위)를 더 낮은 하한과 검증 파생 순위로 다시 확인하되, 운영 주장(operating claim, 운영 주장)은 만들지 않는다.
""")
    write_text(DECISION_DOC, f"""# Decision(결정): Stage362C Review and Stage363 Branch(362C 검토 및 363단계 분기)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_stage_id(다음 단계 ID): `{NEXT_STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- next_materialization_run_id(다음 구체화 실행 ID): `{NEXT_STAGE_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage362B(362B 실행)의 margin-only grid(마진 단독 격자)를 no-selection negative memory(선택 없음 부정 기억)로 닫고 Stage363(363단계)을 열었다.

Effect(효과): 다음 탐색은 lower-floor/rank/target-density surface(낮은 하한/순위/목표 밀도 표면)에 한정되어 가벼워진다.
""")


def registry_rows(findings: Sequence[Mapping[str, Any]], design_queue: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    gates = gate_rows()
    branch_gates = branch_gate_rows()
    best_validation = best_finding(findings, "validation_cost_0_30_net")
    best_oos = best_finding(findings, "oos_cost_0_30_net")

    common_review = {
        "stage_id": SOURCE_STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "margin_grid_review(마진 격자 검토)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "notes": "Stage362C reviews q05 margin grid and branches Stage363(Stage362C q05 마진 격자를 검토하고 Stage363을 분기).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(findings),
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(REVIEW_FINDINGS),
        "result_status": STATUS,
        "sample_rows": len(findings),
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_design(실험 설계)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
        "lane": "margin_grid_review(마진 격자 검토)",
        "family": "experiment_design(실험 설계)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Should q05 margin grid branch to lower-floor rank surface?(q05 마진 격자를 낮은 하한 순위 표면으로 분기해야 하는가?)",
        "metric_scope": "review_only(검토 전용)",
    }
    tier_a = dict(common_review)
    tier_a.update({
        "subrun_id": f"{RUN_ID}__Tier_A",
        "ledger_row_id": f"{RUN_ID}__Tier_A",
        "row_id": f"{RUN_ID}__Tier_A",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A",
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "kpi_scope": "report-derived review(보고서 파생 검토)",
        "primary_kpi": f"best_validation={best_validation['finding_id']};validation_net={best_validation['validation_cost_0_30_net']};best_oos={best_oos['finding_id']};oos_net={best_oos['oos_cost_0_30_net']}",
        "guardrail_kpi": f"stage363_design_queue_rows={len(design_queue)};candidate_selection=not_run",
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

    run_review = dict(common_review)
    run_review.update({"subrun_id": f"{RUN_ID}__Tier_A", "ledger_row_id": f"{RUN_ID}__Tier_A", "row_id": f"{RUN_ID}__Tier_A"})

    branch_row = {
        "stage_id": NEXT_STAGE_ID,
        "run_id": NEXT_RUN_ID,
        "subrun_id": f"{NEXT_RUN_ID}__Tier_AplusB",
        "parent_run_id": RUN_ID,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "status": BRANCH_STATUS,
        "judgment": BRANCH_JUDGMENT,
        "path": rel(NEXT_REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "notes": "Stage363 lower-floor rank surface branch(Stage363 낮은 하한 순위 표면 분기).",
        "run_number": NEXT_RUN_NUMBER,
        "date": TODAY,
        "decision": BRANCH_DECISION,
        "next_run_id": NEXT_STAGE_RUN_ID,
        "rows": len(design_queue),
        "gate_passes": sum(1 for row in branch_gates if row["status"] == "passed"),
        "gate_total": len(branch_gates),
        "claim_boundary": BRANCH_CLAIM_BOUNDARY,
        "report_path": rel(NEXT_REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(NEXT_DESIGN_QUEUE),
        "result_status": BRANCH_STATUS,
        "sample_rows": len(design_queue),
        "source_package_run_id": RUN_ID,
        "work_family": "state_sync(상태 동기화)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": BRANCH_JUDGMENT,
        "final_decision_path": rel(NEXT_FINAL_DECISION),
        "created_at": TODAY,
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "primary_report": rel(NEXT_REPORT_PATH),
        "evidence_boundary": BRANCH_CLAIM_BOUNDARY,
        "next_action": NEXT_STAGE_RUN_ID,
        "question": "Can lower-floor rank surface recover q05 long density and cost?(낮은 하한 순위 표면이 q05 롱 밀도와 비용을 회복할 수 있는가?)",
        "ledger_row_id": f"{NEXT_RUN_ID}__Tier_AplusB",
        "row_id": f"{NEXT_RUN_ID}__Tier_AplusB",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage_branch_no_new_runtime(단계 분기, 새 런타임 없음)",
        "primary_kpi": f"design_queue_rows={len(design_queue)}",
        "guardrail_kpi": "no_candidate_selection(후보 선택 없음)",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "metric_scope": "out_of_scope_by_claim(주장 범위 밖)",
    }
    return [run_review, branch_row], [tier_a, tier_b, combined, branch_row], [tier_a, tier_b, combined], [branch_row]


def write_registries(findings: Sequence[Mapping[str, Any]], design_queue: Sequence[Mapping[str, Any]]) -> None:
    run_rows, project_rows, stage_rows, next_stage_rows = registry_rows(findings, design_queue)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], stage_rows, extend_header=True)
    write_csv(NEXT_STAGE_LEDGER, next_stage_rows)


def write_artifact_registry() -> None:
    artifacts = [
        ("script", Path("stage_pipelines/stage362/review_q05_long_only_margin_grid_and_branch_stage363_without_db.py"), "tracked"),
        ("review_report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("stage363_report", NEXT_REPORT_PATH, "tracked"),
        ("stage363_stage_brief", NEXT_STAGE_BRIEF, "tracked"),
        ("stage363_selection_status", NEXT_SELECTION_STATUS, "tracked"),
        ("review_findings", REVIEW_FINDINGS, "ignored_with_manifest"),
        ("failure_memory", FAILURE_MEMORY, "ignored_with_manifest"),
        ("stage363_design_queue", NEXT_DESIGN_QUEUE, "ignored_with_manifest"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("stage363_final_decision", NEXT_FINAL_DECISION, "ignored_with_manifest"),
    ]
    rows = []
    for artifact_type, path, availability in artifacts:
        rows.append(
            {
                "stage_id": NEXT_STAGE_ID if "stage363" in artifact_type else SOURCE_STAGE_ID,
                "run_id": NEXT_RUN_ID if "stage363" in artifact_type else RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file(path) if exists(path) and Path(path).is_file() else "",
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": BRANCH_CLAIM_BOUNDARY if "stage363" in artifact_type else CLAIM_BOUNDARY,
                "notes": f"Stage362C review and Stage363 branch artifact(362C 검토 및 363단계 분기 산출물); availability={availability}",
            }
        )
    if exists(ARTIFACT_REGISTRY):
        fieldnames, existing = read_csv_rows(ARTIFACT_REGISTRY)
    else:
        fieldnames, existing = [], []
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    existing_keys = {
        (row.get("stage_id", ""), row.get("run_id", ""), row.get("artifact_type", ""), row.get("path", ""))
        for row in existing
    }
    rows_to_append = [
        row
        for row in rows
        if (row.get("stage_id", ""), row.get("run_id", ""), row.get("artifact_type", ""), row.get("path", ""))
        not in existing_keys
    ]
    if not rows_to_append:
        return
    ensure_parent(ARTIFACT_REGISTRY)
    mode = "a" if exists(ARTIFACT_REGISTRY) else "w"
    encoding = "utf-8" if exists(ARTIFACT_REGISTRY) else "utf-8-sig"
    with open(fs_path(ARTIFACT_REGISTRY), mode, encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        if mode == "w":
            writer.writeheader()
        for row in rows_to_append:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_workspace_state() -> None:
    write_text(WORKSPACE_STATE, f"""current_stage_id: {NEXT_STAGE_ID}
current_run_id: {NEXT_STAGE_RUN_ID}
latest_completed_run_id: {NEXT_RUN_ID}
current_status: {BRANCH_STATUS}
current_judgment: {BRANCH_JUDGMENT}
current_decision: {BRANCH_DECISION}
next_run_id: {NEXT_STAGE_RUN_ID}
claim_boundary: {BRANCH_CLAIM_BOUNDARY}
updated_at: {TODAY}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{NEXT_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_STAGE_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{NEXT_RUN_ID}`
- current_status(현재 상태): `{BRANCH_STATUS}`
- current_judgment(현재 판정): `{BRANCH_JUDGMENT}`
- current_decision(현재 결정): `{BRANCH_DECISION}`
- claim_boundary(주장 경계): `{BRANCH_CLAIM_BOUNDARY}`

Action(행동): Stage362C(362C 실행)가 q05 margin grid(q05 마진 격자)를 no-selection negative memory(선택 없음 부정 기억)로 닫고 Stage363(363단계)을 열었다.

Effect(효과): 다음 작업은 `{NEXT_STAGE_RUN_ID}`에서 lower-floor/rank design queue(낮은 하한/순위 설계 대기열)를 구체화한다.
""")
    append_text_once(WORKSPACE_CHANGELOG, "run362C_review_q05_long_only_margin_grid_without_db_v1", f"""## {TODAY} run362C Review and Stage363 Branch(362C 검토 및 363단계 분기)

Action(행동): q05 long-only margin grid(q05 롱 단독 마진 격자)를 no-selection(선택 없음)으로 닫고 lower-floor/rank surface(낮은 하한/순위 표면)를 열었다.

Effect(효과): current truth(현재 진실)는 Stage363B(363B 실행) materialization(구체화) 대기 상태다.
""")


def write_idea_and_negative_registers() -> None:
    append_text_once(IDEA_REGISTRY, "IDEA-ST362C-Q05-MARGIN-GRID-REVIEW", f"""## IDEA-ST362C-Q05-MARGIN-GRID-REVIEW

- idea(아이디어): q05 margin grid(q05 마진 격자)를 no-selection negative memory(선택 없음 부정 기억)로 검토한다.
- hypothesis(가설): Stage362B(362B 실행)의 sparse cost-positive pockets(희소 비용 양수 구간)는 candidate selection(후보 선택)이 아니라 lower-floor/rank seed(낮은 하한/순위 씨앗)이다.
- evidence_boundary(근거 경계): `review_only_no_new_mt5(검토 전용, 새 MT5 없음)`.
- next_action(다음 행동): `{NEXT_RUN_ID}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## IDEA-ST363-Q05-LOWER-FLOOR-RANK-SURFACE

- idea(아이디어): lower p_long floor and validation-derived rank/quantile surface(낮은 p_long 하한 및 검증 파생 순위/분위수 표면).
- hypothesis(가설): density(밀도)를 보존하면서 validation cost drag(검증 비용 끌림)를 줄이는 표면이 absolute margin tightening(절대 마진 조임)보다 낫다.
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`.
- next_action(다음 행동): `{NEXT_STAGE_RUN_ID}`.
""")
    append_text_once(NEGATIVE_RESULT_REGISTER, "FM-ST362C-Q05-MARGIN-GRID-DENSITY-COLLAPSE", f"""## {TODAY} FM-ST362C-Q05-MARGIN-GRID-DENSITY-COLLAPSE

- source_run(원천 실행): `{RUN_ID}`
- failure(실패): p_long_floor>=0.40 margin-only tightening(p_long 하한 0.40 이상 마진 단독 조임)은 validation/OOS cost positive(검증/표본외 비용 양수)와 density >= 3(밀도 3 이상)를 동시에 회복하지 못했다.
- salvage_value(회수 가치): validation-derived margin rank near miss(검증 파생 마진 순위 근접 실패)는 Stage363(363단계) lower-floor/rank surface(낮은 하한/순위 표면)의 씨앗이다.
- do_not_repeat(반복 금지): sparse cost-positive pocket(희소 비용 양수 구간)을 candidate selection(후보 선택)으로 올리지 않는다.
- reopen_condition(재개 조건): Stage363B(363B 실행)가 validation/OOS cost positive(검증/표본외 비용 양수)와 density >= 3(밀도 3 이상)를 동시에 만들 때.
- evidence(근거): `{rel(REVIEW_FINDINGS)}`
""")


def refresh_gate_artifacts() -> None:
    gates = gate_rows()
    branch_gates = branch_gate_rows()
    write_csv(GATE_AUDIT, gates)
    write_csv(NEXT_GATE_AUDIT, branch_gates)

    final = read_json(FINAL_DECISION)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_json(FINAL_DECISION, final)

    next_final = read_json(NEXT_FINAL_DECISION)
    next_final["gate_passes"] = sum(1 for row in branch_gates if row["status"] == "passed")
    next_final["gate_total"] = len(branch_gates)
    write_json(NEXT_FINAL_DECISION, next_final)


def main() -> None:
    require_inputs()
    frame = load_trade_table()
    findings = build_review_findings(frame)
    failure_memory = build_failure_memory(findings)
    design_queue = build_stage363_design_queue()
    write_run_artifacts(findings, failure_memory, design_queue)
    write_reports(findings, failure_memory, design_queue)
    write_workspace_state()
    write_idea_and_negative_registers()
    write_reports(findings, failure_memory, design_queue)
    refresh_gate_artifacts()
    write_registries(findings, design_queue)
    write_artifact_registry()
    refresh_gate_artifacts()
    result = read_json(FINAL_DECISION)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
