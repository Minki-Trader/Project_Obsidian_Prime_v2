from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import review_h17_focus_month_cost_stress_repair_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import train_h17_focus_month_cost_stress_repair_scout_without_db as cj  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CL"
RUN_ID = "run364CL_materialize_h17_bad_month_source_balance_repair_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_SCOUT_RUN_ID = cj.RUN_ID
NEXT_RUN_ID = "run364CM_train_h17_bad_month_source_balance_repair_scout_without_db_v1"

STATUS = "completed_stage364CL_h17_bad_month_source_balance_repair_inputs_materialized_open_cm_no_authority"
JUDGMENT = "experiment_design_materialized_bad_month_source_balance_repair_inputs_no_authority"
DECISION = "stage364CL_open_run364CM_h17_bad_month_source_balance_repair_scout"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = parent.DENSITY_FLOOR
SHORT_FLOOR = parent.SHORT_FLOOR
MIN_QUEUE_ROWS = 16

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
CK_FAILURE_MEMORY = RUN_DIR / "ck_failure_memory_summary.csv"
REPAIR_AXIS_MAP = RUN_DIR / "repair_axis_map.csv"
CANDIDATE_SEED_MATRIX = RUN_DIR / "candidate_seed_matrix.csv"
SOURCE_BALANCE_MATRIX = RUN_DIR / "source_balance_matrix.csv"
BAD_MONTH_CLASS_MATRIX = RUN_DIR / "bad_month_class_matrix.csv"
RUN364CM_QUEUE = RUN_DIR / "run364CM_h17_bad_month_source_balance_repair_scout_queue.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CL_h17_bad_month_source_balance_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CL_h17_bad_month_source_balance_repair_inputs.md"
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

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.NEXT_REPAIR_QUEUE,
    parent.MONTH_FAILURE_ATTRIBUTION,
    parent.SOURCE_BALANCE_REVIEW,
    parent.POSITIVE_CLUE_REGISTER,
    parent.PACKAGE_GATE_DECISION,
    parent.PROXY_MT5_DIFF_REVIEW,
    parent.RUN_MANIFEST,
    cj.FINAL_DECISION,
    cj.PROXY_REPAIR_SURFACE,
    cj.CANDIDATE_MONTH_STABILITY,
    cj.CANDIDATE_SOURCE_ATTRIBUTION,
    cj.CANDIDATE_FILTER_AUDIT,
    cj.COST_STRESS_DIAGNOSTIC,
    cj.RUN_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    CK_FAILURE_MEMORY,
    REPAIR_AXIS_MAP,
    CANDIDATE_SEED_MATRIX,
    SOURCE_BALANCE_MATRIX,
    BAD_MONTH_CLASS_MATRIX,
    RUN364CM_QUEUE,
    DATA_INTEGRITY_AUDIT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
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
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_RESULT_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def json_ready(value: Any) -> Any:
    return parent.json_ready(value)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return parent.markdown_table(rows, columns, limit=limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig")
    lines: list[str] = []
    for line in text.splitlines():
        lines.append(next((value for prefix, value in replacements.items() if line.startswith(prefix)), line))
    write_text(path, "\n".join(lines) + "\n", bom=bom)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CL inputs(CL 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CK next_run_id mismatch(CK 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("CK has forbidden authority claim(CK 금지 권위 주장 존재)")
    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CK gate audit(CK 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    queue = read_csv(parent.NEXT_REPAIR_QUEUE)
    if len(queue) != 8:
        raise RuntimeError(f"CK to CL queue mismatch(CK-CL 대기열 불일치): {len(queue)} != 8")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CL materialization source(CL 구체화 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def failure_memory_rows(ck_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    month_failures = read_csv(parent.MONTH_FAILURE_ATTRIBUTION)
    package = read_csv(parent.PACKAGE_GATE_DECISION)
    rows: list[dict[str, Any]] = []
    for _, raw in month_failures.iterrows():
        row = raw.to_dict()
        segment = str(row.get("segment", ""))
        month_num = segment[-2:] if len(segment) >= 2 else ""
        quarter = f"Q{((int(month_num) - 1) // 3) + 1}" if month_num.isdigit() else ""
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": PARENT_RUN_ID,
                "memory_id": row.get("failure_id", ""),
                "memory_type": "bad_month_failure(손실 월 실패)",
                "source_segment": segment,
                "class_guard": f"month_of_year={month_num};quarter={quarter}",
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "trade_count": row.get("trade_count", ""),
                "short_trade_count": row.get("short_trade_count", ""),
                "converted_constraint": "use reusable month/quarter class guard, not exact-year filter(재사용 월/분기 클래스 가드 사용, 정확 연도 필터 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for _, raw in package.iterrows():
        row = raw.to_dict()
        if "failed" in str(row.get("gate_status", "")):
            rows.append(
                {
                    "run_id": RUN_ID,
                    "source_run_id": PARENT_RUN_ID,
                    "memory_id": row.get("gate_id", ""),
                    "memory_type": "package_gate_failure(패키지 게이트 실패)",
                    "source_segment": row.get("subject", ""),
                    "class_guard": row.get("evidence", ""),
                    "net_profit": ck_final.get("reviewed_net_profit", ""),
                    "profit_factor": ck_final.get("reviewed_profit_factor", ""),
                    "trade_count": ck_final.get("reviewed_trade_count", ""),
                    "short_trade_count": ck_final.get("reviewed_short_trade_count", ""),
                    "converted_constraint": row.get("effect", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def repair_axis_rows() -> list[dict[str, Any]]:
    axes = [
        (
            "cl_axis_01_bad_month_class",
            "bad month class guard(손실 월 클래스 가드)",
            "month_of_year and quarter known at entry(진입 시점에 알려진 월/분기)",
            "bad_month_count decreases without exact-year filter(정확 연도 필터 없이 손실 월 수 감소)",
        ),
        (
            "cl_axis_02_late_year_pressure",
            "late-year pressure guard(연말 압박 가드)",
            "month_of_year=12 and Q4 class(12월 및 4분기 클래스)",
            "December-class weakness improves without deleting a calendar month(달력 월 삭제 없이 12월 계열 약점 개선)",
        ),
        (
            "cl_axis_03_source_balance",
            "native/synthetic short source balance(기본/합성 숏 원천 균형)",
            "native short floor, synthetic overlay cap, source mix(기본 숏 하한, 합성 오버레이 상한, 원천 혼합)",
            "short_count stays >=100 and edge is not one thin source(숏 100개 이상 유지 및 얇은 단일 원천 의존 회피)",
        ),
        (
            "cl_axis_04_restore_quality",
            "short-floor restore quality(숏 하한 복원 품질)",
            "restored native shorts are quality-filtered by entry-known fields(복원 기본 숏을 진입 시점 필드로 품질 필터)",
            "restored shorts preserve PF/net rather than masking collapse(복원 숏이 붕괴를 가리는 대신 PF/순수익 보존)",
        ),
        (
            "cl_axis_05_package_precheck",
            "package precheck boundary(패키지 사전점검 경계)",
            "bad_month_count==0 and stress_delta>=0 before MT5 package(MT5 패키지 전 손실 월 0 및 압박 차이 0 이상)",
            "proxy package only opens after all prechecks pass(모든 사전점검 통과 후에만 프록시 패키지 개방)",
        ),
    ]
    return [
        {
            "run_id": RUN_ID,
            "axis_id": axis_id,
            "axis_name": axis_name,
            "timestamp_safe_inputs": inputs,
            "success_criteria": success,
            "failure_criteria": "net/PF edge disappears or density/short floor breaks(순수익/PF 우위 소멸 또는 밀도/숏 하한 붕괴)",
            "forbidden_shortcut": "top_n, trade splitting, exact-year date filter(top_n, 거래 쪼개기, 정확 연도 날짜 필터)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for axis_id, axis_name, inputs, success in axes
    ]


def candidate_seed_rows(ck_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    surface = read_csv(cj.PROXY_REPAIR_SURFACE)
    seed_ids = [
        ck_final["reviewed_candidate_id"],
        "cj11_cg08_bad_overlay_month_guard_scout_short_floor_rescue",
        "cj05_month_of_year_08_overlay_soft_guard",
        "cj07_month_of_year_12_overlay_soft_guard",
        "cj06_quarter_q3_pressure_overlay_soft_guard",
        "cj08_quarter_q4_pressure_overlay_soft_guard",
        "cj10_cg12_trade_shape_quality_no_split_short_floor_rescue",
        "cj04_h17_focus_cost_anchor_control",
    ]
    rows: list[dict[str, Any]] = []
    for seed_id in seed_ids:
        match = surface[surface["candidate_id"].astype(str).eq(seed_id)]
        if match.empty:
            continue
        row = match.iloc[0].to_dict()
        rows.append(
            {
                "run_id": RUN_ID,
                "seed_candidate_id": seed_id,
                "source_run_id": SOURCE_SCOUT_RUN_ID,
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "expectancy": row.get("expectancy", ""),
                "trade_count": row.get("trade_count", ""),
                "trade_density": row.get("trade_density", ""),
                "short_trade_count": row.get("short_trade_count", ""),
                "stress_delta": row.get("stress_adjusted_net_delta_vs_parent", ""),
                "bad_month_count": row.get("bad_month_count", ""),
                "bad_months": row.get("bad_months", ""),
                "seed_use": seed_use(seed_id),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def seed_use(seed_id: str) -> str:
    if seed_id.startswith("cj11"):
        return "lower bad-month comparison seed(손실 월 감소 비교 씨앗)"
    if "month_of_year_08" in seed_id or "quarter_q3" in seed_id:
        return "August/Q3 class clue(8월/3분기 클래스 단서)"
    if "month_of_year_12" in seed_id or "quarter_q4" in seed_id:
        return "December/Q4 class clue(12월/4분기 클래스 단서)"
    if "anchor_control" in seed_id:
        return "anchor control(기준 대조)"
    return "primary CL repair seed(주 CL 수리 씨앗)"


def source_balance_rows() -> list[dict[str, Any]]:
    sources = read_csv(parent.SOURCE_BALANCE_REVIEW)
    rows: list[dict[str, Any]] = []
    total_short = sources["short_trade_count"].apply(as_float).sum()
    for _, raw in sources.iterrows():
        row = raw.to_dict()
        short_count = as_float(row.get("short_trade_count"))
        rows.append(
            {
                "run_id": RUN_ID,
                "source_bucket": row.get("source_bucket", ""),
                "trade_count": row.get("trade_count", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "short_trade_count": row.get("short_trade_count", ""),
                "short_share_of_shorts": finite(short_count / total_short if total_short else 0.0),
                "balance_issue": "thin synthetic watch(얇은 합성 원천 관찰)" if row.get("source_bucket") == "synthetic_short_overlay" else "usable source(사용 가능 원천)",
                "cm_constraint": "cap synthetic overlay and restore native short quality(합성 오버레이 상한 및 기본 숏 품질 복원)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def bad_month_class_rows() -> list[dict[str, Any]]:
    failures = read_csv(parent.MONTH_FAILURE_ATTRIBUTION)
    rows: list[dict[str, Any]] = []
    for _, raw in failures.iterrows():
        row = raw.to_dict()
        segment = str(row.get("segment", ""))
        month_num = segment[-2:] if len(segment) >= 2 else ""
        quarter = f"Q{((int(month_num) - 1) // 3) + 1}" if month_num.isdigit() else ""
        rows.append(
            {
                "run_id": RUN_ID,
                "source_bad_month": segment,
                "month_of_year_guard": f"month_of_year={month_num}",
                "quarter_guard": f"quarter={quarter}",
                "session_guard": "open_hour=17 pressure class(17시 진입 압박 클래스)",
                "exact_date_filter_status": "forbidden(금지)",
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "trade_count": row.get("trade_count", ""),
                "short_trade_count": row.get("short_trade_count", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def queue_rows(ck_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "selected_candidate_id": ck_final["reviewed_candidate_id"],
        "allowed_entry_operation": "preserve_or_remove_existing_entries_only(기존 진입 보존 또는 제거만)",
        "trade_splitting_status": "not_used_no_added_entries(미사용, 추가 진입 없음)",
        "top_n_status": "forbidden(금지)",
        "exact_date_filter_status": "forbidden(금지)",
        "timestamp_safe_inputs": "source_bucket/open_hour/month_of_year/quarter/probabilities known at entry(진입 시점 원천/시간/월/분기/확률)",
        "minimum_density": DENSITY_FLOOR,
        "minimum_short_count": SHORT_FLOOR,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    specs = [
        ("cm01_cj09_month08_class_soft_guard", "cl_axis_01_bad_month_class", ck_final["reviewed_candidate_id"], "month_of_year=08", "native_overlay_balance_keep", "restore_native_short_until_floor_100", "stress_delta_floor_ge_0", 0, "turn August class into reusable guard(8월 클래스를 재사용 가드로 전환)"),
        ("cm02_cj09_month12_class_soft_guard", "cl_axis_02_late_year_pressure", ck_final["reviewed_candidate_id"], "month_of_year=12", "native_overlay_balance_keep", "restore_native_short_until_floor_100", "stress_delta_floor_ge_0", 0, "turn December class into reusable guard(12월 클래스를 재사용 가드로 전환)"),
        ("cm03_cj09_q3_q4_combo_guard", "cl_axis_01_bad_month_class", ck_final["reviewed_candidate_id"], "quarter=Q3_or_Q4", "native_overlay_balance_keep", "restore_native_short_until_floor_100", "stress_delta_floor_ge_0", 0, "generalize weak months to quarter class(약한 월을 분기 클래스로 일반화)"),
        ("cm04_cj09_month08_12_pair_guard", "cl_axis_01_bad_month_class", ck_final["reviewed_candidate_id"], "month_of_year=08_or_12", "native_overlay_balance_keep", "restore_native_short_until_floor_100", "stress_delta_floor_ge_0", 0, "test paired month class without exact-year filter(정확 연도 필터 없이 쌍 월 클래스 시험)"),
        ("cm05_cj11_month12_salvage_guard", "cl_axis_02_late_year_pressure", "cj11_cg08_bad_overlay_month_guard_scout_short_floor_rescue", "month_of_year=12", "native_overlay_balance_keep", "restore_native_short_until_floor_100", "stress_delta_floor_ge_0", 0, "use lower bad-month seed as package bridge(손실 월 감소 씨앗을 패키지 다리로 사용)"),
        ("cm06_cj11_q4_late_year_balance", "cl_axis_02_late_year_pressure", "cj11_cg08_bad_overlay_month_guard_scout_short_floor_rescue", "quarter=Q4", "native_overlay_balance_keep", "restore_native_short_until_floor_100", "stress_delta_floor_ge_0", 0, "test late-year class on cj11 seed(cj11 씨앗에서 연말 클래스 시험)"),
        ("cm07_cj09_native_short_floor105_quality", "cl_axis_04_restore_quality", ck_final["reviewed_candidate_id"], "none", "native_short_first_quality", "restore_native_short_until_floor_105", "stress_delta_floor_ge_0", 0, "raise native short quality floor(기본 숏 품질 하한 상향)"),
        ("cm08_cj09_native_short_floor110_pressure", "cl_axis_03_source_balance", ck_final["reviewed_candidate_id"], "none", "native_short_first_quality", "restore_native_short_until_floor_110", "stress_delta_floor_ge_0", 0, "test whether extra native shorts improve balance(추가 기본 숏이 균형을 개선하는지 시험)"),
        ("cm09_cj09_synthetic_overlay_cap", "cl_axis_03_source_balance", ck_final["reviewed_candidate_id"], "none", "synthetic_overlay_cap_30_percent", "restore_native_short_until_floor_100", "stress_delta_floor_ge_0", 0, "reduce thin synthetic source risk(얇은 합성 원천 위험 감소)"),
        ("cm10_cj09_native_synthetic_even_mix", "cl_axis_03_source_balance", ck_final["reviewed_candidate_id"], "none", "native_synthetic_even_short_mix", "restore_native_short_until_floor_100", "stress_delta_floor_ge_0", 0, "test balanced short source mix(균형 숏 원천 혼합 시험)"),
        ("cm11_cj09_late_year_h17_pressure", "cl_axis_02_late_year_pressure", ck_final["reviewed_candidate_id"], "month_of_year=12;open_hour=17", "native_overlay_balance_keep", "restore_native_short_until_floor_100", "stress_delta_floor_ge_0", 0, "separate late-year and h17 pressure(연말과 17시 압박 분리)"),
        ("cm12_cj09_august_h17_pressure", "cl_axis_01_bad_month_class", ck_final["reviewed_candidate_id"], "month_of_year=08;open_hour=17", "native_overlay_balance_keep", "restore_native_short_until_floor_100", "stress_delta_floor_ge_0", 0, "separate August and h17 pressure(8월과 17시 압박 분리)"),
        ("cm13_cj10_trade_shape_quality_bridge", "cl_axis_04_restore_quality", "cj10_cg12_trade_shape_quality_no_split_short_floor_rescue", "none", "trade_shape_quality_bridge", "restore_native_short_until_floor_100", "stress_delta_floor_ge_0", 0, "reuse trade-shape quality without splitting(거래 쪼개기 없이 거래 형태 품질 재사용)"),
        ("cm14_cj05_august_guard_anchor", "cl_axis_01_bad_month_class", "cj05_month_of_year_08_overlay_soft_guard", "month_of_year=08", "overlay_month_pressure_sensitive", "preserve_short_floor_100", "stress_delta_floor_ge_0", 0, "anchor August guard to prior CJ row(8월 가드를 기존 CJ 행에 고정)"),
        ("cm15_cj07_december_guard_anchor", "cl_axis_02_late_year_pressure", "cj07_month_of_year_12_overlay_soft_guard", "month_of_year=12", "overlay_month_pressure_sensitive", "preserve_short_floor_100", "stress_delta_floor_ge_0", 0, "anchor December guard to prior CJ row(12월 가드를 기존 CJ 행에 고정)"),
        ("cm16_package_precheck_control", "cl_axis_05_package_precheck", ck_final["reviewed_candidate_id"], "bad_month_count_zero_required", "precheck_flags_only", "precheck_flags_only", "stress_delta_floor_ge_0", 0, "keep MT5 package boundary explicit(MT5 패키지 경계 명시 유지)"),
    ]
    rows = []
    for rank, (candidate_id, axis_id, seed_id, month_policy, source_policy, short_policy, cost_policy, target_bad_months, effect) in enumerate(specs, start=1):
        rows.append(
            {
                **base,
                "queue_rank": rank,
                "candidate_id": candidate_id,
                "axis_id": axis_id,
                "seed_candidate_id": seed_id,
                "h17_overlay_policy": "inherit_selected_h17_focus",
                "cost_stress_policy": cost_policy,
                "month_guard_policy": month_policy,
                "short_floor_policy": short_policy,
                "source_mix_policy": source_policy,
                "target_bad_month_count": target_bad_months,
                "success_criteria": "bad_month_count<=target;stress_delta>=0;density>=3;shorts>=100",
                "failure_criteria": "net/PF edge disappears or exact-year filter would be required(순수익/PF 우위 소멸 또는 정확 연도 필터 필요)",
                "expected_effect": effect,
            }
        )
    return rows


def data_integrity_rows(queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    policy_columns = ["h17_overlay_policy", "cost_stress_policy", "month_guard_policy", "short_floor_policy", "source_mix_policy"]
    exact_policy_rows = sum(any("2025-" in str(row.get(col, "")) for col in policy_columns) for row in queue)
    top_n_rows = sum(any("top_n" in str(row.get(col, "")).lower() for col in policy_columns) for row in queue)
    split_rows = sum(not str(row.get("trade_splitting_status", "")).startswith("not_used") for row in queue)
    rows = [
        ("input_lineage", all(exists(path) for path in INPUT_FILES), f"inputs={len(INPUT_FILES)}"),
        ("queue_row_count", len(queue) >= MIN_QUEUE_ROWS, f"queue_rows={len(queue)};minimum={MIN_QUEUE_ROWS}"),
        ("no_exact_year_filter", exact_policy_rows == 0, f"exact_year_policy_rows={exact_policy_rows}"),
        ("no_top_n_policy", top_n_rows == 0, f"top_n_policy_rows={top_n_rows}"),
        ("no_trade_splitting", split_rows == 0, f"trade_splitting_rows={split_rows}"),
        ("density_floor_recorded", all(as_float(row.get("minimum_density")) >= DENSITY_FLOOR for row in queue), f"density_floor={DENSITY_FLOOR}"),
        ("short_floor_recorded", all(as_float(row.get("minimum_short_count")) >= SHORT_FLOOR for row in queue), f"short_floor={SHORT_FLOOR}"),
    ]
    return [
        {
            "run_id": RUN_ID,
            "audit_id": audit_id,
            "status": "passed" if passed else "failed",
            "evidence": evidence,
            "effect": "timestamp-safe materialization guard(시점 안전 구체화 가드)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for audit_id, passed, evidence in rows
    ]


def gate_rows(data_rows: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], receipts_written: bool) -> list[dict[str, Any]]:
    receipt_paths = [EXPERIMENT_RECEIPT, DATA_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT, LINEAGE_RECEIPT]
    checks = [
        ("scope_completion_gate", len(queue) >= MIN_QUEUE_ROWS, RUN364CM_QUEUE, "CM queue has materialized rows(CM 대기열 행 구체화)"),
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "CL inputs are connected(CL 입력 연결)"),
        ("data_integrity_gate", all(row["status"] == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "timestamp/top_n/split guards passed(시점/top_n/쪼개기 가드 통과)"),
        ("repair_axis_gate", exists(REPAIR_AXIS_MAP) and exists(CANDIDATE_SEED_MATRIX), REPAIR_AXIS_MAP, "repair axes and seed matrix exist(수리 축과 씨앗 행렬 존재)"),
        ("next_queue_gate", len(queue) == MIN_QUEUE_ROWS, RUN364CM_QUEUE, "next scout queue has 16 rows(다음 정찰 대기열 16행)"),
        ("receipt_coverage_gate", receipts_written and all(exists(path) for path in receipt_paths), EXPERIMENT_RECEIPT, "required receipts exist(필수 영수증 존재)"),
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, path, effect in checks
    ]
    rows.append(
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed" if all(row["status"] == "passed" for row in rows) else "failed",
            "evidence": rel(GATE_AUDIT),
            "effect": "required gates are connected to closeout(필수 게이트가 종료 기록에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def final_payload(
    ck_final: Mapping[str, Any],
    queue: Sequence[Mapping[str, Any]],
    data_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    exact_rows = sum(row["audit_id"] == "no_exact_year_filter" and row["status"] != "passed" for row in data_rows)
    top_n_rows = sum(row["audit_id"] == "no_top_n_policy" and row["status"] != "passed" for row in data_rows)
    split_rows = sum(row["audit_id"] == "no_trade_splitting" and row["status"] != "passed" for row in data_rows)
    gate_passes = sum(row["status"] == "passed" for row in gates)
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_scout_run_id": SOURCE_SCOUT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "queue_rows": len(queue),
        "minimum_queue_rows": MIN_QUEUE_ROWS,
        "reviewed_candidate_id": ck_final["reviewed_candidate_id"],
        "reviewed_net_profit": ck_final["reviewed_net_profit"],
        "reviewed_profit_factor": ck_final["reviewed_profit_factor"],
        "reviewed_expectancy": ck_final["reviewed_expectancy"],
        "reviewed_trade_count": ck_final["reviewed_trade_count"],
        "reviewed_density": ck_final["reviewed_density"],
        "reviewed_short_trade_count": ck_final["reviewed_short_trade_count"],
        "reviewed_bad_month_count": ck_final["reviewed_bad_month_count"],
        "reviewed_bad_months": ck_final["reviewed_bad_months"],
        "reviewed_stress_adjusted_net_delta_vs_parent": ck_final["reviewed_stress_adjusted_net_delta_vs_parent"],
        "target_bad_month_count": 0,
        "top_n_policy_fail_rows": top_n_rows,
        "trade_splitting_fail_rows": split_rows,
        "exact_year_filter_fail_rows": exact_rows,
        "gate_passes": gate_passes,
        "gate_total": len(gates),
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "external_verification_status": "out_of_scope_by_claim_materialization_only",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "queue_path": rel(RUN364CM_QUEUE),
        "report_path": rel(REPORT_PATH),
    }


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": ["obsidian-data-integrity", "obsidian-artifact-lineage", "obsidian-result-judgment"],
            "required_gates": [
                "scope_completion_gate",
                "input_lineage_gate",
                "data_integrity_gate",
                "repair_axis_gate",
                "next_queue_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "bad month/source balance repair can remove package blockers without trade splitting(손실 월/원천 균형 수리가 거래 쪼개기 없이 패키지 차단을 제거할 수 있다)",
            "comparison": "16 CM queue rows against CK selected proxy seed(CK 선택 프록시 씨앗 대비 CM 대기열 16행)",
            "success_criteria": "bad_month_count==0;stress_delta>=0;density>=3;shorts>=100",
            "stop_condition": "exact-year filter, top_n, trade splitting, or MT5 claim appears(정확 연도 필터/top_n/거래 쪼개기/MT5 주장 등장)",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "timestamp_safety": "entry-known source/open_hour/month_of_year/quarter/probabilities only(진입 시점 원천/시간/월/분기/확률만 사용)",
            "lookahead_status": "not_detected_in_materialized_queue(구체화 대기열에서 미탐지)",
            "forbidden_shortcuts": ["top_n(상위 N)", "trade_splitting(거래 쪼개기)", "exact-year date filter(정확 연도 날짜 필터)"],
            "audit_path": rel(DATA_INTEGRITY_AUDIT),
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "CL materialized CM repair scout queue(CL이 CM 수리 정찰 대기열을 구체화)",
            "evidence_available": [rel(RUN364CM_QUEUE), rel(DATA_INTEGRITY_AUDIT), rel(GATE_AUDIT)],
            "evidence_missing": ["new proxy replay(새 프록시 재생)", "new MT5 runtime probe(새 MT5 런타임 탐침)"],
            "judgment_label": "materialized_experiment_design(구체화된 실험 설계)",
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claims": ["CM queue materialized(CM 대기열 구체화)", "guardrails recorded(가드레일 기록)"],
            "forbidden_claims": ["model trained(모델 학습)", "MT5 execution(MT5 실행)", "runtime authority(런타임 권위)", "operating promotion(운영 승격)", "Goal Achieve(목표 달성)"],
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    artifact_paths = [path for path in OUTPUT_FILES if exists(path) and path != LINEAGE_RECEIPT and io_path(path).is_file()]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths],
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_or_regenerable_from_manifest(커밋 후 추적 또는 실행 목록으로 재생성 가능)",
            "lineage_judgment": "connected_with_boundary_CL_to_CM_queue(CL-CM 대기열 경계부 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_manifest(final: Mapping[str, Any]) -> None:
    exclusions = {RUN_MANIFEST, LINEAGE_RECEIPT, ARTIFACT_REGISTRY}
    output_paths = [path for path in OUTPUT_FILES if path not in exclusions and exists(path) and io_path(path).is_file()]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": final["created_at_utc"],
            "producer": rel(Path(__file__)),
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in output_paths],
            "final_decision": rel(FINAL_DECISION),
            "external_verification_status": final["external_verification_status"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    artifacts = [
        ("repair_queue", RUN364CM_QUEUE, "CM repair scout queue(CM 수리 정찰 대기열)."),
        ("repair_axis_map", REPAIR_AXIS_MAP, "CL repair axis map(CL 수리 축 지도)."),
        ("candidate_seed_matrix", CANDIDATE_SEED_MATRIX, "CL candidate seed matrix(CL 후보 씨앗 행렬)."),
        ("source_balance_matrix", SOURCE_BALANCE_MATRIX, "CL source balance matrix(CL 원천 균형 행렬)."),
        ("bad_month_class_matrix", BAD_MONTH_CLASS_MATRIX, "CL bad month class matrix(CL 손실 월 클래스 행렬)."),
        ("final_decision", FINAL_DECISION, "CL final decision(CL 최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "CL run manifest(CL 실행 목록)."),
        ("report", REPORT_PATH, "CL report(CL 보고서)."),
        ("gate_audit", GATE_AUDIT, "CL required gate audit(CL 필수 게이트 감사)."),
        ("lineage_receipt", LINEAGE_RECEIPT, "CL lineage receipt(CL 계보 영수증)."),
        ("script", Path(__file__), "CL producer script(CL 생산 스크립트)."),
    ]
    rows = []
    for artifact_type, path, notes in artifacts:
        if exists(path):
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_docs(
    final: Mapping[str, Any],
    failure_rows_: Sequence[Mapping[str, Any]],
    axes: Sequence[Mapping[str, Any]],
    source_rows_: Sequence[Mapping[str, Any]],
    month_rows_: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364CL h17 bad month source balance repair inputs(364CL 17시 손실 월 원천 균형 수리 입력)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- queue rows(대기열 행): `{final['queue_rows']}`
- reviewed seed(검토 씨앗): `{final['reviewed_candidate_id']}`
- reviewed KPI(검토 핵심 성과 지표): net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, density `{final['reviewed_density']}`, shorts `{final['reviewed_short_trade_count']}`
- blocker(차단 원인): bad months(손실 월) `{final['reviewed_bad_months']}`

## Action And Effect(행동과 효과)

Action(행동): CK package rejection(CK 패키지 거절)을 bad month class guard(손실 월 클래스 가드), source balance(원천 균형), short restore quality(숏 복원 품질), package precheck boundary(패키지 사전점검 경계)로 materialize(구체화)했다.

Effect(효과): CM scout(CM 정찰)가 no-split(무분할), no top_n(no top_n), no exact-year date filter(정확 연도 날짜 필터 없음) 조건으로 바로 proxy replay(프록시 재생)할 수 있다.

## Failure Memory(실패 기억)

{markdown_table(failure_rows_, ['memory_id', 'memory_type', 'source_segment', 'class_guard', 'net_profit', 'profit_factor', 'converted_constraint'], 12)}

## Repair Axes(수리 축)

{markdown_table(axes, ['axis_id', 'axis_name', 'timestamp_safe_inputs', 'success_criteria', 'forbidden_shortcut'], 10)}

## Bad Month Classes(손실 월 클래스)

{markdown_table(month_rows_, ['source_bad_month', 'month_of_year_guard', 'quarter_guard', 'session_guard', 'exact_date_filter_status'], 8)}

## Source Balance(원천 균형)

{markdown_table(source_rows_, ['source_bucket', 'trade_count', 'net_profit', 'profit_factor', 'short_trade_count', 'short_share_of_shorts', 'cm_constraint'], 8)}

## CM Queue(CM 대기열)

{markdown_table(queue, ['queue_rank', 'candidate_id', 'axis_id', 'seed_candidate_id', 'month_guard_policy', 'source_mix_policy', 'short_floor_policy', 'expected_effect'], 20)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Boundary(경계)

CL is materialization only(CL은 구체화 전용)이다. New model training(새 모델 학습), new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 없다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364CL h17 bad month source balance repair inputs(17시 손실 월 원천 균형 수리 입력)

Action(행동): `{RUN_ID}`에서 CK review(CK 검토)를 `{final['queue_rows']}`개 CM scout queue(CM 정찰 대기열)로 구체화했다.

Effect(효과): 다음 작업은 Stage364(364단계)를 분기하지 않고 bad month/source balance repair(손실 월/원천 균형 수리)를 proxy replay(프록시 재생)할 수 있다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- queue(대기열): `{rel(RUN364CM_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - h17 bad month/source balance repair inputs(17시 손실 월/원천 균형 수리 입력).")
    append_text_once(
        STAGE_BRIEF,
        f"run364CL__{RUN_ID}",
        f"""
<!-- run364CL__{RUN_ID} -->

## run364CL H17 Bad Month Source Balance Repair Inputs Closeout(364CL 17시 손실 월 원천 균형 수리 입력 종료)

Action(행동): CK package rejection(CK 패키지 거절)을 `{final['queue_rows']}`개 CM scout queue(CM 정찰 대기열)로 구체화했다.

Effect(효과): same Stage364(같은 364단계)에서 stage branch(단계 분기) 없이 `{NEXT_RUN_ID}`로 손실 월/원천 균형 수리를 공격 탐색한다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## {RUN_ID}

Action(행동): CK review(CK 검토)를 CM repair scout(CM 수리 정찰) 입력으로 구체화했다.

Effect(효과): stage branch(단계 분기) 없이 `{NEXT_RUN_ID}`로 이어간다.
""",
    )
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
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

Current truth(현재 진실): `run364CL` materialized(구체화 완료) CK package rejection(CK 패키지 거절)을 `{final['queue_rows']}`개 CM scout rows(CM 정찰 행)로 전환했다. Queue(대기열)는 no-split(무분할), no top_n(no top_n), no exact-year date filter(정확 연도 날짜 필터 없음)를 기록한다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 bad month class guard(손실 월 클래스 가드), source balance(원천 균형), short restore quality(숏 복원 품질)를 proxy replay(프록시 재생)한다.

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

Package candidate(패키지 후보): none(없음). CL is materialization only(CL은 구체화 전용).

Materialized queue(구체화 대기열): `{rel(RUN364CM_QUEUE)}` with `{final['queue_rows']}` rows(행).

Reviewed seed(검토 씨앗): `{final['reviewed_candidate_id']}`. Reviewed KPI(검토 핵심 성과 지표): net `{final['reviewed_net_profit']}`, PF `{final['reviewed_profit_factor']}`, density `{final['reviewed_density']}`, shorts `{final['reviewed_short_trade_count']}`, bad months `{final['reviewed_bad_months']}`.

Guardrails(가드레일): top_n fail rows(top_n 실패 행) `{final['top_n_policy_fail_rows']}`, trade splitting fail rows(거래 쪼개기 실패 행) `{final['trade_splitting_fail_rows']}`, exact-year filter fail rows(정확 연도 필터 실패 행) `{final['exact_year_filter_fail_rows']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"run364CL__{RUN_ID}",
        f"\n<!-- run364CL__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` materialized CK package rejection(CK 패키지 거절) into `{final['queue_rows']}` CM repair scout rows(CM 수리 정찰 행); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"run364CL__{RUN_ID}",
        f"\n<!-- run364CL__{RUN_ID} -->\n- `{RUN_ID}`: bad month/source balance repair inputs(손실 월/원천 균형 수리 입력). Effect(효과): CK positive proxy clue(CK 긍정 프록시 단서)를 exact-year filtering(정확 연도 필터링) 없이 CM offensive scout(CM 공격 정찰)로 전환.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"run364CL__{RUN_ID}",
        f"\n<!-- run364CL__{RUN_ID} -->\n- `{RUN_ID}` preserves CK package rejection(CK 패키지 거절 보존): bad months(손실 월) `{final['reviewed_bad_months']}` remain unresolved until `{NEXT_RUN_ID}` replay(재생). Reopen condition(재개 조건): bad_month_count==0 and stress_delta>=0 without top_n/trade splitting/exact-year date filter(top_n/거래 쪼개기/정확 연도 날짜 필터 없이 손실 월 0 및 압박 차이 0 이상).\n",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["queue_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_design(실험 설계)",
        "scoreboard_lane": "materialization(구체화)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "materialization_only(구체화 전용)",
        "question": "Can CK bad-month/source blockers become a no-split CM scout queue?(CK 손실 월/원천 차단을 무분할 CM 정찰 대기열로 바꿀 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["reviewed_net_profit"],
        "profit_factor": final["reviewed_profit_factor"],
        "expectancy": final["reviewed_expectancy"],
        "trade_count": final["reviewed_trade_count"],
        "trade_density_per_feature_day": final["reviewed_density"],
        "short_trade_count": final["reviewed_short_trade_count"],
        "trade_density_requirement_status": "materialized_density_floor_3_no_trade_splitting(밀도 하한 3, 거래 쪼개기 없음 구체화)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUN364CM_QUEUE),
    }
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **common,
                "lane": "materialization(구체화)",
                "family": "h17_bad_month_source_balance_repair_inputs(17시 손실 월 원천 균형 수리 입력)",
                "result_status": STATUS,
                "view": "materialization(구체화)",
                "tier": "Tier A",
                "metric_scope": "queue_materialization(대기열 구체화)",
            }
        ],
        extend_header=True,
    )
    ledger_rows = []
    for suffix, record_view, tier_scope, status, include_metrics in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS, True),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)", False),
        ("tier_a_plus_b_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)", True),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "CL materialization(CL 구체화)",
            "status": status,
            "primary_kpi": f"queue_rows={final['queue_rows']};target_bad_month_count={final['target_bad_month_count']}",
            "guardrail_kpi": f"top_n_fail={final['top_n_policy_fail_rows']};split_fail={final['trade_splitting_fail_rows']};exact_year_fail={final['exact_year_filter_fail_rows']};no_authority",
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "queue_materialization(대기열 구체화)",
        }
        if not include_metrics:
            for key in ["net_profit", "profit_factor", "expectancy", "trade_count", "trade_density_per_feature_day", "short_trade_count"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    ck_final = validate_inputs()
    failure_rows_ = failure_memory_rows(ck_final)
    axes = repair_axis_rows()
    seed_rows = candidate_seed_rows(ck_final)
    source_rows_ = source_balance_rows()
    month_rows_ = bad_month_class_rows()
    queue = queue_rows(ck_final)
    data_rows = data_integrity_rows(queue)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    write_csv(CK_FAILURE_MEMORY, failure_rows_)
    write_csv(REPAIR_AXIS_MAP, axes)
    write_csv(CANDIDATE_SEED_MATRIX, seed_rows)
    write_csv(SOURCE_BALANCE_MATRIX, source_rows_)
    write_csv(BAD_MONTH_CLASS_MATRIX, month_rows_)
    write_csv(RUN364CM_QUEUE, queue)
    write_csv(DATA_INTEGRITY_AUDIT, data_rows)

    gates = gate_rows(data_rows, queue, receipts_written=False)
    final = final_payload(ck_final, queue, data_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    refresh_lineage_receipt(final)
    gates = gate_rows(data_rows, queue, receipts_written=True)
    final = final_payload(ck_final, queue, data_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_docs(final, failure_rows_, axes, source_rows_, month_rows_, queue, gates)
    write_ledgers(final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
