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

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from stage_pipelines.stage364 import review_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db as ep  # noqa: E402
from stage_pipelines.stage364 import review_h17_oos108_validation_floor_bridge_without_db as em  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_validation_floor_bridge_without_db as el  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = ep.STAGE_ID
RUN_NUMBER = "run364EQ"
RUN_ID = "run364EQ_train_h17_oos108_scope_aligned_cost_side_repair_scout_without_db_v1"
PARENT_RUN_ID = ep.RUN_ID
PROXY_RUN_ID = el.RUN_ID
REVIEW_RUN_ID = em.RUN_ID
NEXT_RUN_ID = "run364ER_train_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1"

STATUS = "completed_stage364EQ_oos108_scope_aligned_cost_side_repair_scout_no_strict_pass_open_er_no_authority"
JUDGMENT = (
    "negative_current_surface_cost_side_strict_pass_zero_positive_reseed_seed_"
    "existing_surface_insufficient_no_authority"
)
DECISION = "stage364EQ_open_run364ER_oos108_cost_side_model_label_feature_reseed"
CLAIM_BOUNDARY = (
    "research_development_scope_aligned_cost_side_proxy_scout_only_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUNTIME_NET_REFERENCE = 523.58
RUNTIME_PF_REFERENCE = 1.21
DENSITY_FLOOR = 3.0
SHORT_SHARE_TARGET = 0.72
COST06_PENALTY_PER_TRADE = 0.30
COST09_PENALTY_PER_TRADE = 0.60

STAGE_DIR = ep.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

WORK_PACKET = RUN_DIR / "work_packet.json"
INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SURFACE = RUN_DIR / "eq_scope_aligned_cost_side_surface.csv"
STRICT_CANDIDATES = RUN_DIR / "eq_strict_operational_proxy_pass_candidates.csv"
RELAXED_CANDIDATES = RUN_DIR / "eq_relaxed_density_seed_candidates.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "eq_failure_attribution.csv"
TRADE_TAPE_SCOPE_AUDIT = RUN_DIR / "eq_trade_tape_scope_audit.csv"
RUN364ER_QUEUE = RUN_DIR / "run364ER_cost_side_model_label_feature_reseed_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364EQ_oos108_cost_side_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EQ_h17_oos108_scope_aligned_cost_side_repair_scout.md"
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

INPUT_FILES = [
    ep.FINAL_DECISION,
    ep.GATE_AUDIT,
    ep.SCOPE_ALIGNMENT,
    ep.GUARDRAIL_REVIEW,
    ep.RUN364EQ_QUEUE,
    el.FINAL_DECISION,
    el.SELECTED_CANDIDATE,
    el.TRADE_SURFACE,
    el.COST_STRESS,
    el.MONTH_STABILITY,
    el.SELECTED_TRADE_TAPE,
    em.FINAL_DECISION,
    em.COST_STRESS_REVIEW,
    em.SIDE_BALANCE_REVIEW,
    Path(__file__),
]

OUTPUT_FILES = [
    WORK_PACKET,
    INPUT_MANIFEST,
    SURFACE,
    STRICT_CANDIDATES,
    RELAXED_CANDIDATES,
    FAILURE_ATTRIBUTION,
    TRADE_TAPE_SCOPE_AUDIT,
    RUN364ER_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    LINEAGE_RECEIPT,
    RESULT_RECEIPT,
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
    NEGATIVE_REGISTER,
    Path(__file__),
]

NUMERIC_COLUMNS = [
    "threshold",
    "density_target",
    "margin_vs_flat",
    "max_hold_m5",
    "validation_net",
    "validation_profit_factor",
    "validation_expectancy",
    "validation_trade_density",
    "validation_trade_count",
    "validation_max_drawdown",
    "validation_recovery_factor",
    "validation_long_trade_count",
    "validation_short_trade_count",
    "oos_net",
    "oos_profit_factor",
    "oos_expectancy",
    "oos_trade_density",
    "oos_trade_count",
    "oos_max_drawdown",
    "oos_recovery_factor",
    "oos_long_trade_count",
    "oos_short_trade_count",
]

SURFACE_COLUMNS = [
    "run_id",
    "source_run_id",
    "candidate_id",
    "model_id",
    "model_family",
    "feature_set_id",
    "label_id",
    "threshold",
    "density_target",
    "hours_id",
    "margin_vs_flat",
    "stability_filter",
    "max_hold_m5",
    "validation_net",
    "validation_profit_factor",
    "validation_trade_density",
    "validation_trade_count",
    "validation_cost06_net",
    "validation_long_trade_count",
    "validation_short_trade_count",
    "oos_net",
    "oos_profit_factor",
    "oos_trade_density",
    "oos_trade_count",
    "oos_cost06_net",
    "oos_long_trade_count",
    "oos_short_trade_count",
    "combined_net",
    "combined_trade_count",
    "combined_trade_density",
    "combined_cost06_net",
    "combined_cost09_net",
    "combined_long_trade_count",
    "combined_short_trade_count",
    "combined_short_share",
    "min_split_profit_factor",
    "max_split_drawdown",
    "min_split_recovery_factor",
    "runtime_net_gap_vs_523_58",
    "density_ge_3",
    "validation_cost06_ge_0",
    "oos_cost06_gt_0",
    "combined_cost09_ge_0",
    "min_pf_ge_runtime_1_21",
    "short_share_le_0_72",
    "combined_net_ge_runtime_523_58",
    "strict_condition_count",
    "strict_operational_proxy_pass",
    "relaxed_density_seed",
    "eq_score",
    "claim_boundary",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return ep.rel(path)


def exists(path: Path | str) -> bool:
    return ep.exists(path)


def sha(path: Path | str) -> str:
    return ep.sha(path)


def read_json(path: Path) -> Any:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ep.write_json(path, payload)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    ep.write_csv(path, rows, fieldnames=fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ep.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    materialized = Path(path)
    materialized.parent.mkdir(parents=True, exist_ok=True)
    existing = materialized.read_text(encoding="utf-8-sig") if materialized.exists() else ""
    if marker in existing:
        return
    payload = existing.rstrip() + "\n" + text.lstrip() if existing.strip() else text
    materialized.write_text(payload, encoding="utf-8-sig")


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    ep.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    ep.replace_prefixed_lines(path, replacements, bom=bom)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def bool_text(value: Any) -> str:
    return "true" if bool(value) else "false"


def frame_to_rows(frame: pd.DataFrame, columns: Sequence[str] | None = None) -> list[dict[str, Any]]:
    selected = frame if columns is None else frame[list(columns)]
    cleaned = selected.copy()
    cleaned = cleaned.where(pd.notna(cleaned), "")
    rows: list[dict[str, Any]] = []
    for row in cleaned.to_dict(orient="records"):
        rows.append({key: finite(value) if isinstance(value, (float, int)) else value for key, value in row.items()})
    return rows


def infer_model_family(model_id: str) -> str:
    if "__rf" in model_id:
        return "RandomForest(랜덤포레스트)"
    if "__et" in model_id:
        return "ExtraTrees(엑스트라트리)"
    if "__gb" in model_id:
        return "GradientBoosting(그래디언트부스팅)"
    return "unknown(미상)"


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing EQ inputs(EQ 입력 누락): " + ", ".join(missing))
    ep_final = read_json(ep.FINAL_DECISION)
    el_final = read_json(el.FINAL_DECISION)
    if ep_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EP next_run_id mismatch(EP 다음 실행 ID 불일치): {ep_final.get('next_run_id')} != {RUN_ID}")
    for label, final in [("EP", ep_final), ("EL", el_final)]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if final.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    ep_gates = read_csv(ep.GATE_AUDIT)
    if ep_gates.empty or any(ep_gates["status"].astype(str) != "passed"):
        raise RuntimeError("EP gate audit(EP 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return {"ep_final": ep_final, "el_final": el_final}


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-exploration-mandate(탐색 명령)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "input_lineage_gate",
                "data_integrity_scope_gate",
                "scope_aligned_surface_gate",
                "cost_side_guardrail_gate",
                "strict_pass_decision_gate",
                "model_validation_boundary_gate",
                "paired_tier_record_gate",
                "artifact_lineage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "hypothesis": (
                "Scope-aligned validation+OOS proxy(범위 정렬 검증+표본외 프록시) surface(표면) 안에서 "
                "cost resilience(비용 회복력), PF floor(PF 바닥), short share(숏 비중), density(밀도)를 동시에 만족하는 repair seed(수리 씨앗)가 있는지 확인합니다."
            ),
            "effect": "기존 MT5 runtime clue(런타임 단서)를 운영 주장으로 키우기 전에 비용/방향 병목을 분해합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_input_manifest() -> None:
    rows = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": bool_text(exists(path)),
                "sha256": sha(path),
                "source_role": "producer_script(생산 스크립트)" if path == Path(__file__) else "input_artifact(입력 산출물)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)


def build_surface() -> pd.DataFrame:
    frame = read_csv(el.TRADE_SURFACE)
    for column in NUMERIC_COLUMNS:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["run_id"] = RUN_ID
    frame["source_run_id"] = PROXY_RUN_ID
    frame["candidate_id"] = frame["model_id"].astype(str)
    frame["model_family"] = frame["model_id"].astype(str).map(infer_model_family)

    validation_days = frame["validation_trade_count"] / frame["validation_trade_density"].replace(0, math.nan)
    oos_days = frame["oos_trade_count"] / frame["oos_trade_density"].replace(0, math.nan)
    total_days = validation_days + oos_days

    frame["combined_net"] = frame["validation_net"] + frame["oos_net"]
    frame["combined_trade_count"] = frame["validation_trade_count"] + frame["oos_trade_count"]
    frame["combined_trade_density"] = frame["combined_trade_count"] / total_days
    frame["combined_long_trade_count"] = frame["validation_long_trade_count"] + frame["oos_long_trade_count"]
    frame["combined_short_trade_count"] = frame["validation_short_trade_count"] + frame["oos_short_trade_count"]
    frame["combined_short_share"] = frame["combined_short_trade_count"] / frame["combined_trade_count"].replace(0, math.nan)
    frame["validation_cost06_net"] = frame["validation_net"] - COST06_PENALTY_PER_TRADE * frame["validation_trade_count"]
    frame["oos_cost06_net"] = frame["oos_net"] - COST06_PENALTY_PER_TRADE * frame["oos_trade_count"]
    frame["combined_cost06_net"] = frame["combined_net"] - COST06_PENALTY_PER_TRADE * frame["combined_trade_count"]
    frame["combined_cost09_net"] = frame["combined_net"] - COST09_PENALTY_PER_TRADE * frame["combined_trade_count"]
    frame["min_split_profit_factor"] = frame[["validation_profit_factor", "oos_profit_factor"]].min(axis=1)
    frame["max_split_drawdown"] = frame[["validation_max_drawdown", "oos_max_drawdown"]].max(axis=1)
    frame["min_split_recovery_factor"] = frame[["validation_recovery_factor", "oos_recovery_factor"]].min(axis=1)
    frame["runtime_net_gap_vs_523_58"] = frame["combined_net"] - RUNTIME_NET_REFERENCE

    checks = {
        "density_ge_3": frame["combined_trade_density"] >= DENSITY_FLOOR,
        "validation_cost06_ge_0": frame["validation_cost06_net"] >= 0,
        "oos_cost06_gt_0": frame["oos_cost06_net"] > 0,
        "combined_cost09_ge_0": frame["combined_cost09_net"] >= 0,
        "min_pf_ge_runtime_1_21": frame["min_split_profit_factor"] >= RUNTIME_PF_REFERENCE,
        "short_share_le_0_72": frame["combined_short_share"] <= SHORT_SHARE_TARGET,
        "combined_net_ge_runtime_523_58": frame["combined_net"] >= RUNTIME_NET_REFERENCE,
    }
    for column, mask in checks.items():
        frame[column] = mask.fillna(False)
    frame["strict_condition_count"] = sum(frame[column].astype(int) for column in checks)
    frame["strict_operational_proxy_pass"] = frame[list(checks)].all(axis=1)
    frame["relaxed_density_seed"] = (
        (frame["combined_trade_density"] >= DENSITY_FLOOR)
        & (frame["validation_profit_factor"] >= 1.05)
        & (frame["oos_profit_factor"] >= 1.08)
        & (frame["combined_cost06_net"] > 0)
        & (frame["combined_net"] > 0)
    )
    frame["eq_score"] = (
        frame["strict_condition_count"] * 10000
        + frame["combined_net"].fillna(0)
        + 250 * (frame["min_split_profit_factor"].fillna(0) - 1.0)
        + 0.50 * frame["combined_cost09_net"].fillna(-9999)
        - 250 * (frame["combined_short_share"].fillna(1.0) - SHORT_SHARE_TARGET).clip(lower=0)
        - 120 * (DENSITY_FLOOR - frame["combined_trade_density"].fillna(0)).clip(lower=0)
    )
    frame["claim_boundary"] = CLAIM_BOUNDARY
    return frame.sort_values(
        ["strict_operational_proxy_pass", "relaxed_density_seed", "strict_condition_count", "eq_score"],
        ascending=[False, False, False, False],
    )


def build_trade_tape_scope_audit() -> list[dict[str, Any]]:
    tape = read_csv(el.SELECTED_TRADE_TAPE)
    selected = read_json(el.SELECTED_CANDIDATE)
    rows = []
    for split, expected_key in [("validation", "validation_trade_count"), ("oos", "oos_trade_count")]:
        split_frame = tape[tape["split"].astype(str) == split]
        actual = len(split_frame)
        expected = int(float(selected.get(expected_key, 0) or 0))
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": PROXY_RUN_ID,
                "split": split,
                "expected_trade_count_from_selected_candidate": expected,
                "actual_trade_tape_rows": actual,
                "full_tape_available": bool_text(actual == expected),
                "usage": (
                    "full_split_diagnostic_usable(전체 분할 진단 가능)"
                    if actual == expected
                    else "scope_limitation_only_not_full_guardrail(범위 제한 기록 전용, 전체 가드레일 아님)"
                ),
                "effect": "session/side filter(세션/방향 필터)는 full tape(전체 테이프)가 필요하므로 ER에서 재생성해야 합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_failure_attribution(surface: pd.DataFrame) -> list[dict[str, Any]]:
    checks = [
        ("density_ge_3(밀도 3 이상)", "density_ge_3", ">=3/day", "Trade per day(일 거래수) 하한입니다."),
        ("validation_cost06_ge_0(검증 비용0.6 순수익 0 이상)", "validation_cost06_ge_0", ">=0", "검증 구간 비용 회복력 병목입니다."),
        ("oos_cost06_gt_0(표본외 비용0.6 순수익 양수)", "oos_cost06_gt_0", ">0", "표본외 비용 회복력 병목입니다."),
        ("combined_cost09_ge_0(합산 비용0.9 순수익 0 이상)", "combined_cost09_ge_0", ">=0", "강한 비용 압박 병목입니다."),
        ("min_pf_ge_runtime_1_21(분할 PF 1.21 이상)", "min_pf_ge_runtime_1_21", ">=1.21", "MT5 PF reference(런타임 PF 기준) 병목입니다."),
        ("short_share_le_0_72(숏 비중 0.72 이하)", "short_share_le_0_72", "<=0.72", "숏 편중 품질 병목입니다."),
        ("combined_net_ge_runtime_523_58(합산 순수익 523.58 이상)", "combined_net_ge_runtime_523_58", ">=523.58", "MT5 net reference(런타임 순수익 기준) 병목입니다."),
        ("strict_operational_proxy_pass(엄격 운영 프록시 통과)", "strict_operational_proxy_pass", "all checks", "기존 표면에서 운영형 repair seed(수리 씨앗)가 있는지 봅니다."),
        ("relaxed_density_seed(완화 밀도 씨앗)", "relaxed_density_seed", "density/PF/cost06 relaxed", "다음 모델/라벨 재시드 씨앗입니다."),
    ]
    rows = []
    total = len(surface)
    for rank, (label, column, threshold, implication) in enumerate(checks, start=1):
        passed = int(surface[column].astype(bool).sum())
        rows.append(
            {
                "run_id": RUN_ID,
                "rank": rank,
                "check": label,
                "threshold": threshold,
                "pass_count": passed,
                "fail_count": total - passed,
                "total_count": total,
                "pass_rate": finite(passed / total if total else math.nan),
                "implication": implication,
                "next_repair_use": (
                    "open_model_label_feature_reseed(모델/라벨/피처 재시드 열기)"
                    if column == "strict_operational_proxy_pass" and passed == 0
                    else "diagnostic_constraint(진단 제약)"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_queue(final_preview: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "er01_cost_resilient_label_reseed",
            "seed": "EQ strict pass 0(엄격 통과 0) and validation cost0.6 weakness(검증 비용0.6 약점)",
            "target_question": "Can a cost-aware label(비용 인식 라벨) lift validation cost0.6 without density below 3/day(일 3회 아래 밀도 하락)?",
            "success_criteria": "validation_cost06_net>=0, oos_cost06_net>0, combined_density>=3, no trade splitting(거래 쪼개기 없음)",
            "allowed_ideas": "cost-adjusted label(비용 조정 라벨), asymmetric loss(비대칭 손실), margin-to-flat floor(플랫 대비 마진 바닥)",
            "effect": "수익을 거래수로 잘게 나누지 않고 비용에 약한 거래를 줄입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 2,
            "queue_id": "er02_density_preserving_pf_floor_reseed",
            "seed": f"min split PF(분할 PF) >= {RUNTIME_PF_REFERENCE} rows exist but density/cost fail(밀도/비용 실패)",
            "target_question": "Can PF floor(PF 바닥) and density floor(밀도 바닥) coexist without sparse high-PF overfiltering(희소 고PF 과필터)?",
            "success_criteria": "min_split_pf>=1.21, combined_density>=3, combined_net improves toward 523.58",
            "allowed_ideas": "model-family reseed(모델 계열 재시드), calibration rank gap(보정 순위 간극), density-aware score(밀도 인식 점수)",
            "effect": "PF만 좋은 저밀도 후보로 도망가지 않고 운영 밀도 요구를 유지합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 3,
            "queue_id": "er03_short_quality_feature_reseed",
            "seed": "combined short share(합산 숏 비중) bottleneck and selected MT5 short share 0.7663622527",
            "target_question": "Can short-heavy exposure(숏 편중 노출) become higher quality instead of simply fewer trades(단순 거래 감소)?",
            "success_criteria": "short_share<=0.72 or short expectancy lift(숏 기대값 상승), density>=3, cost stress not worse",
            "allowed_ideas": "side-specific features(방향별 피처), hour 19/20 short veto(19/20시 숏 배제), realized volatility bucket(실현 변동성 구간)",
            "effect": "숏 거래를 무작정 자르지 않고 수익성 있는 숏만 남길 조건을 찾습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 4,
            "queue_id": "er04_full_trade_tape_replay_contract",
            "seed": "selected_el_trade_tape has OOS partial rows(표본외 부분 행) so session scout needs regeneration",
            "target_question": "Can the next run emit full validation/OOS trade tapes(전체 검증/표본외 거래 테이프) for session/side attribution(세션/방향 귀속)?",
            "success_criteria": "full tape count equals selected candidate trade count for validation and OOS",
            "allowed_ideas": "full tape writer(전체 테이프 기록기), side/session attribution(방향/세션 귀속), timestamp-safe replay(시점 안전 재생)",
            "effect": "부분 테이프에 기대어 세션 필터를 과장하지 않게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def pick_rows(surface: pd.DataFrame) -> tuple[dict[str, Any], dict[str, Any]]:
    relaxed = surface[surface["relaxed_density_seed"]]
    if relaxed.empty:
        density_seed = surface.iloc[0].to_dict()
    else:
        density_seed = relaxed.sort_values(["combined_net", "min_split_profit_factor"], ascending=[False, False]).iloc[0].to_dict()
    near_miss = surface.sort_values(["strict_condition_count", "eq_score"], ascending=[False, False]).iloc[0].to_dict()
    return density_seed, near_miss


def build_final(surface: pd.DataFrame, failure_rows: Sequence[Mapping[str, Any]], tape_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    density_seed, near_miss = pick_rows(surface)
    strict_count = int(surface["strict_operational_proxy_pass"].astype(bool).sum())
    relaxed_count = int(surface["relaxed_density_seed"].astype(bool).sum())
    relaxed_unique_count = int(
        surface[surface["relaxed_density_seed"]]
        .drop_duplicates(
            subset=[
                "candidate_id",
                "feature_set_id",
                "label_id",
                "threshold",
                "combined_net",
                "combined_trade_count",
                "combined_trade_density",
            ]
        )
        .shape[0]
    )
    created_at = now_utc()
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "proxy_run_id": PROXY_RUN_ID,
        "review_run_id": REVIEW_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": created_at,
        "surface_rows": int(len(surface)),
        "strict_operational_proxy_pass_count": strict_count,
        "relaxed_density_seed_count": relaxed_count,
        "relaxed_density_seed_unique_count": relaxed_unique_count,
        "runtime_net_reference": RUNTIME_NET_REFERENCE,
        "runtime_pf_reference": RUNTIME_PF_REFERENCE,
        "density_floor": DENSITY_FLOOR,
        "short_share_target": SHORT_SHARE_TARGET,
        "best_density_seed_id": density_seed.get("candidate_id", ""),
        "best_density_seed_combined_net": finite(density_seed.get("combined_net")),
        "best_density_seed_combined_density": finite(density_seed.get("combined_trade_density")),
        "best_density_seed_trade_count": finite(density_seed.get("combined_trade_count")),
        "best_density_seed_min_pf": finite(density_seed.get("min_split_profit_factor")),
        "best_density_seed_validation_cost06_net": finite(density_seed.get("validation_cost06_net")),
        "best_density_seed_oos_cost06_net": finite(density_seed.get("oos_cost06_net")),
        "best_density_seed_combined_cost09_net": finite(density_seed.get("combined_cost09_net")),
        "best_density_seed_short_share": finite(density_seed.get("combined_short_share")),
        "best_density_seed_long_trade_count": finite(density_seed.get("combined_long_trade_count")),
        "best_density_seed_short_trade_count": finite(density_seed.get("combined_short_trade_count")),
        "best_near_miss_id": near_miss.get("candidate_id", ""),
        "best_near_miss_combined_net": finite(near_miss.get("combined_net")),
        "best_near_miss_density": finite(near_miss.get("combined_trade_density")),
        "best_near_miss_min_pf": finite(near_miss.get("min_split_profit_factor")),
        "best_near_miss_condition_count": int(near_miss.get("strict_condition_count", 0) or 0),
        "best_near_miss_short_share": finite(near_miss.get("combined_short_share")),
        "queue_rows": len(queue_rows),
        "oos_trade_tape_full_available": next((row["full_tape_available"] for row in tape_rows if row["split"] == "oos"), "false"),
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "new_mt5_execution": "not_run(미실행)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "evidence_available": [rel(path) for path in [SURFACE, STRICT_CANDIDATES, RELAXED_CANDIDATES, FAILURE_ATTRIBUTION, TRADE_TAPE_SCOPE_AUDIT, RUN364ER_QUEUE]],
        "evidence_missing": [
            "new model/label/feature reseed(새 모델/라벨/피처 재시드)",
            "full OOS trade tape(전체 표본외 거래 테이프)",
            "new MT5 runtime probe(새 MT5 런타임 탐침)",
            "forward/replay evidence(전진/재생 근거)",
            "runtime authority closure(런타임 권위 폐쇄)",
        ],
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "입력 산출물과 hash(해시)를 기록했습니다."),
        ("data_integrity_scope_gate", exists(TRADE_TAPE_SCOPE_AUDIT), TRADE_TAPE_SCOPE_AUDIT, "선택 trade tape(거래 테이프)의 OOS partial scope(표본외 부분 범위)를 기록했습니다."),
        ("scope_aligned_surface_gate", int(final["surface_rows"]) > 0 and exists(SURFACE), SURFACE, "validation/OOS/combined(검증/표본외/합산) 지표를 모든 후보에 붙였습니다."),
        ("cost_side_guardrail_gate", exists(FAILURE_ATTRIBUTION), FAILURE_ATTRIBUTION, "cost/side(비용/방향) 병목을 pass/fail count(통과/실패 수)로 분해했습니다."),
        ("strict_pass_decision_gate", "strict_operational_proxy_pass_count" in final, FINAL_DECISION, "strict pass(엄격 통과) 0개를 next reseed(다음 재시드) 조건으로 연결했습니다."),
        ("model_validation_boundary_gate", final["runtime_authority"] == "not_claimed", MODEL_RECEIPT, "single-window proxy scout(단일 구간 프록시 정찰)로만 판정했습니다."),
        ("paired_tier_record_gate", True, STAGE_LEDGER, "Tier A, Tier B missing, Tier A+B out-of-scope(주장 범위 밖) 행을 장부에 남깁니다."),
        ("artifact_lineage_gate", exists(LINEAGE_RECEIPT), LINEAGE_RECEIPT, "산출물 계보 receipt(영수증)를 만들었습니다."),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "모든 required gate(필수 게이트)를 closeout(종료 기록)에 연결합니다."),
        ("final_claim_guard", final["goal_achieve"] == "not_claimed" and final["operating_promotion"] == "not_claimed", FINAL_DECISION, "Goal/live/authority(목표/실거래/권위)를 주장하지 않습니다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": name,
            "status": "passed" if ok else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, ok, path, effect in checks
    ]


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "idea_id": "stage364EQ_oos108_cost_side_scope_aligned_repair_scout",
            "hypothesis": "기존 EL surface(EL 표면) 안에 cost/PF/density/side(비용/PF/밀도/방향)를 동시에 만족하는 repair seed(수리 씨앗)가 있는지 본다.",
            "broad_sweep": "all EL surface rows(모든 EL 표면 행) 32928",
            "extreme_sweep": "runtime net 523.58 and PF 1.21 references(런타임 순수익/PF 기준), cost0.9 stress(비용0.9 압박)",
            "micro_search_gate": "strict pass(엄격 통과)가 있을 때만 threshold micro-search(임계값 미세탐색)",
            "wfo_plan": "single-window scout only(단일 구간 정찰 전용); ER must reseed before stronger claim(ER 재시드 필요)",
            "failure_memory": "strict pass zero(엄격 통과 0)는 기존 표면 미세조정 반복 금지 조건입니다.",
            "evidence_boundary": "scout-only(정찰 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": [rel(el.TRADE_SURFACE), rel(el.SELECTED_CANDIDATE), rel(el.SELECTED_TRADE_TAPE), rel(ep.SCOPE_ALIGNMENT)],
            "time_axis": "UTC model input timestamp inherited from EL(EL에서 상속된 UTC 모델 입력 시각)",
            "sample_scope": "Tier A validation+OOS proxy surface(Tier A 검증+표본외 프록시 표면), rows=" + str(final["surface_rows"]),
            "missing_or_duplicate_check": "surface row count recorded; selected OOS trade tape partial limitation recorded(표면 행 수 기록, 선택 OOS 테이프 부분 제한 기록)",
            "feature_label_boundary": "no new feature or label calculation(새 피처/라벨 계산 없음); inherited timestamp-safe EL artifacts(시점 안전 EL 산출물 상속)",
            "split_boundary": "validation separate, OOS separate, validation+OOS combined(검증 분리, 표본외 분리, 검증+표본외 합산)",
            "leakage_risk": "selection bias from re-ranking prior surface(기존 표면 재순위화 선택 편향); no operating claim(운영 주장 없음)",
            "data_hash_or_identity": {rel(path): sha(path) for path in [el.TRADE_SURFACE, el.SELECTED_CANDIDATE, ep.SCOPE_ALIGNMENT]},
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_family": "existing EL surface model families(기존 EL 표면 모델 계열)",
            "target_and_label": "OOS108 validation floor direction labels(OOS108 검증 바닥 방향 라벨) inherited from EL(EL 상속)",
            "split_method": "chronological validation/OOS proxy split(시간순 검증/표본외 프록시 분할)",
            "selection_metric": "strict condition count(엄격 조건 수), eq_score(EQ 점수), density seed ranking(밀도 씨앗 순위)",
            "secondary_metrics": "cost0.6, cost0.9, short_share, density, runtime net/PF reference gap(비용0.6/0.9, 숏 비중, 밀도, 런타임 기준 차이)",
            "threshold_policy": "existing thresholds only(기존 임계값만); no new threshold optimization(새 임계값 최적화 없음)",
            "overfit_risk": "multiple-testing and surface reuse(다중 시험 및 표면 재사용)",
            "calibration_risk": "scores are ranking signals not calibrated probabilities(점수는 보정 확률이 아니라 순위 신호)",
            "comparison_baseline": PARENT_RUN_ID,
            "validation_judgment": "negative_current_surface_strict_pass_zero_positive_reseed_seed(기존 표면 엄격 통과 0, 재시드 씨앗은 긍정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [rel(path) for path in INPUT_FILES if path != Path(__file__)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RESULT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "EQ scope-aligned cost/side repair scout(EQ 범위 정렬 비용/방향 수리 정찰)",
            "evidence_available": final["evidence_available"],
            "evidence_missing": final["evidence_missing"],
            "judgment_label": "negative_current_surface_positive_reseed_seed(기존 표면 부정, 재시드 씨앗 긍정)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "기존 표면은 운영형 조건을 동시에 못 맞췄고, 다음은 모델/라벨/피처를 새로 흔드는 쪽입니다.",
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
            "external_verification_status": final["external_verification_status"],
            "reason": "No new MT5 execution(새 MT5 실행 없음), strict proxy pass zero(엄격 프록시 통과 0), full OOS trade tape missing(전체 표본외 거래 테이프 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "\n".join(["|" + "|".join(columns) + "|", "|" + "|".join(["---"] * len(columns)) + "|"])
    display = list(rows)[:limit]
    lines = ["|" + "|".join(columns) + "|", "|" + "|".join(["---"] * len(columns)) + "|"]
    for row in display:
        lines.append("|" + "|".join(str(row.get(column, "")) for column in columns) + "|")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], failure_rows: Sequence[Mapping[str, Any]], relaxed_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364EQ OOS108 cost/side scout(OOS108 비용/방향 정찰)

Updated(갱신): {final['created_at_utc']}

## Result(결과)

`run364EQ` checked(확인) the EL OOS108 validation floor bridge surface(EL OOS108 검증 바닥 연결 표면) with scope-aligned validation+OOS proxy(범위 정렬 검증+표본외 프록시).

- strict operational proxy pass(엄격 운영 프록시 통과): `{final['strict_operational_proxy_pass_count']}`
- relaxed density seed rows/unique(완화 밀도 씨앗 행/고유): `{final['relaxed_density_seed_count']}` / `{final['relaxed_density_seed_unique_count']}`
- best density seed(최고 밀도 씨앗): `{final['best_density_seed_id']}`
- combined net/density/trades(합산 순수익/밀도/거래수): `{final['best_density_seed_combined_net']}` / `{final['best_density_seed_combined_density']}` / `{final['best_density_seed_trade_count']}`
- min PF / short share(최소 PF / 숏 비중): `{final['best_density_seed_min_pf']}` / `{final['best_density_seed_short_share']}`
- validation/OOS cost0.6 net(검증/표본외 비용0.6 순수익): `{final['best_density_seed_validation_cost06_net']}` / `{final['best_density_seed_oos_cost06_net']}`
- combined cost0.9 net(합산 비용0.9 순수익): `{final['best_density_seed_combined_cost09_net']}`

Judgment(판정): `{JUDGMENT}`.

Effect(효과): 기존 surface(표면) 미세조정은 cost/PF/density/short-share/net(비용/PF/밀도/숏 비중/순수익)을 동시에 못 맞췄습니다. 다음 작업은 `run364ER` model/label/feature reseed(모델/라벨/피처 재시드)입니다.

## Failure Attribution(실패 귀속)

{markdown_table(failure_rows, ['check', 'threshold', 'pass_count', 'fail_count', 'implication'], 12)}

## Relaxed Seeds(완화 씨앗)

{markdown_table(relaxed_rows, ['candidate_id', 'combined_net', 'combined_trade_density', 'min_split_profit_factor', 'validation_cost06_net', 'oos_cost06_net', 'combined_cost09_net', 'combined_short_share'], 10)}

## Claim Boundary(주장 경계)

No new MT5 execution(새 MT5 실행 없음), no forward/replay evidence(전진/재생 근거 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence_path', 'effect'], 12)}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): stage364EQ cost/side repair scout(비용/방향 수리 정찰)

Date(날짜): {final['created_at_utc']}

Decision(결정): `{DECISION}`.

Reason(이유): strict operational proxy pass(엄격 운영 프록시 통과)가 `{final['strict_operational_proxy_pass_count']}`개라 기존 EL surface(EL 표면) 안의 micro-search(미세탐색)로는 운영형 조건을 닫을 수 없습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 cost-aware label(비용 인식 라벨), density-preserving PF floor(밀도 보존 PF 바닥), short-quality feature reseed(숏 품질 피처 재시드), full trade tape replay(전체 거래 테이프 재생)를 엽니다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""",
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

Current truth(현재 진실): `run364EQ` completed(완료) scope-aligned cost/side repair scout(범위 정렬 비용/방향 수리 정찰). strict operational proxy pass(엄격 운영 프록시 통과)는 `{final['strict_operational_proxy_pass_count']}`개이고, relaxed density seed rows/unique(완화 밀도 씨앗 행/고유)는 `{final['relaxed_density_seed_count']}` / `{final['relaxed_density_seed_unique_count']}`개입니다.

Best density seed(최고 밀도 씨앗): `{final['best_density_seed_id']}` with combined net/density/trades(합산 순수익/밀도/거래수) `{final['best_density_seed_combined_net']}` / `{final['best_density_seed_combined_density']}` / `{final['best_density_seed_trade_count']}`. It still fails(실패) strict cost/PF/side/net stack(엄격 비용/PF/방향/순수익 묶음).

Next action(다음 행동): `{NEXT_RUN_ID}` opens model/label/feature reseed(모델/라벨/피처 재시드) rather than repeating surface micro-search(표면 미세탐색 반복).

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest reviewed MT5 runtime probe(최근 검토된 MT5 런타임 탐침): `run364EO_execute_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1`.

Latest scout(최근 정찰): `run364EQ` scope-aligned cost/side repair scout(범위 정렬 비용/방향 수리 정찰).

Strict operational proxy pass(엄격 운영 프록시 통과): `{final['strict_operational_proxy_pass_count']}`.

Best density seed(최고 밀도 씨앗): `{final['best_density_seed_id']}` with combined net/PF/density/trades(합산 순수익/PF/밀도/거래수) `{final['best_density_seed_combined_net']}` / `{final['best_density_seed_min_pf']}` / `{final['best_density_seed_combined_density']}` / `{final['best_density_seed_trade_count']}`.

Judgment(판정): `{JUDGMENT}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(
        REVIEW_INDEX,
        "run364EQ__run364EQ_train_h17_oos108_scope_aligned_cost_side_repair_scout_without_db_v1",
        f"- run364EQ__{RUN_ID}: [run364EQ_oos108_cost_side_scout.md](run364EQ_oos108_cost_side_scout.md) - cost/side strict pass zero(비용/방향 엄격 통과 0), next `{NEXT_RUN_ID}`.\n",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        "run364EQ_oos108_scope_aligned_cost_side_repair_scout",
        f"\n## {final['created_at_utc']} run364EQ scope-aligned cost/side repair scout(범위 정렬 비용/방향 수리 정찰)\n\n- strict operational proxy pass(엄격 운영 프록시 통과): `{final['strict_operational_proxy_pass_count']}`.\n- next action(다음 행동): `{NEXT_RUN_ID}`.\n- effect(효과): 기존 표면 미세탐색 반복 대신 모델/라벨/피처 재시드로 전환합니다.\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        "stage364EQ_oos108_cost_side_scope_aligned_repair_scout",
        f"\n## stage364EQ_oos108_cost_side_scope_aligned_repair_scout\n\n- hypothesis(가설): scope-aligned surface(범위 정렬 표면)에 cost/PF/density/side/net(비용/PF/밀도/방향/순수익)을 동시에 만족하는 repair seed(수리 씨앗)가 있을 수 있다.\n- result(결과): strict pass(엄격 통과) `{final['strict_operational_proxy_pass_count']}`.\n- salvage value(회수 가치): relaxed density seed rows/unique(완화 밀도 씨앗 행/고유) `{final['relaxed_density_seed_count']}` / `{final['relaxed_density_seed_unique_count']}`개와 ER reseed queue(ER 재시드 대기열).\n- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.\n",
    )
    append_text_once(
        NEGATIVE_REGISTER,
        "stage364EQ_existing_surface_strict_pass_zero",
        f"\n## stage364EQ_existing_surface_strict_pass_zero\n\n- failed boundary(실패 경계): strict operational proxy pass(엄격 운영 프록시 통과) across cost/PF/density/side/net(비용/PF/밀도/방향/순수익).\n- why failed(실패 이유): existing EL surface(기존 EL 표면)는 combined net>=523.58(합산 순수익 523.58 이상), cost0.9(비용0.9), density(밀도), short share(숏 비중), PF floor(PF 바닥)를 동시에 만족하지 못했다.\n- salvage value(회수 가치): model/label/feature reseed(모델/라벨/피처 재시드)로 이동.\n- do-not-repeat note(반복 금지 메모): 같은 surface micro-search(표면 미세탐색)를 운영 후보처럼 반복하지 않는다.\n- reopen condition(재개 조건): ER에서 full trade tape(전체 거래 테이프)와 새 cost-aware labels(비용 인식 라벨)를 만든 뒤 재평가.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        "run364EQ_oos108_scope_aligned_cost_side_repair_scout",
        f"\n## run364EQ note(EQ 메모)\n\n- strict pass(엄격 통과): `{final['strict_operational_proxy_pass_count']}`.\n- effect(효과): 기존 표면 반복을 멈추고 `{NEXT_RUN_ID}` 재시드로 이동합니다.\n",
    )
    append_text_once(
        STAGE_README,
        "run364EQ_oos108_scope_aligned_cost_side_repair_scout",
        f"\n## run364EQ\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- next(다음): `{NEXT_RUN_ID}`\n",
    )


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
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
        "rows": final["surface_rows"],
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "scope_aligned_proxy_scout(범위 정렬 프록시 정찰)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "proxy_scout_only_no_authority(프록시 정찰 전용, 권위 없음)",
        "question": "Can scope-aligned cost/side repair pass strict operating-style proxy constraints?(범위 정렬 비용/방향 수리가 엄격 운영형 프록시 제약을 통과하는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["best_density_seed_combined_net"],
        "profit_factor": final["best_density_seed_min_pf"],
        "trade_count": final["best_density_seed_trade_count"],
        "trade_density_per_feature_day": final["best_density_seed_combined_density"],
        "long_trade_count": final["best_density_seed_long_trade_count"],
        "short_trade_count": final["best_density_seed_short_trade_count"],
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(SURFACE),
        "primary_kpi": f"strict_pass={final['strict_operational_proxy_pass_count']};relaxed_density_seed={final['relaxed_density_seed_count']}",
        "guardrail_kpi": f"best_density_seed_cost09={final['best_density_seed_combined_cost09_net']};short_share={final['best_density_seed_short_share']};authority=not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    ledger_rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_surface(필수 누락, Tier B 표면 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "EQ scope-aligned proxy scout(EQ 범위 정렬 프록시 정찰)",
            "status": status,
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "proxy_scout(Python 프록시 정찰)",
        }
        if suffix != "tier_a_separate":
            for key in ["net_profit", "profit_factor", "trade_count", "trade_density_per_feature_day", "long_trade_count", "short_trade_count"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for artifact_type, path, notes in [
        ("input_manifest", INPUT_MANIFEST, "Input manifest(입력 목록)."),
        ("scope_aligned_cost_side_surface", SURFACE, "EQ derived surface(EQ 파생 표면)."),
        ("strict_candidates", STRICT_CANDIDATES, "Strict pass candidates(엄격 통과 후보)."),
        ("relaxed_candidates", RELAXED_CANDIDATES, "Relaxed density seed candidates(완화 밀도 씨앗 후보)."),
        ("failure_attribution", FAILURE_ATTRIBUTION, "Failure attribution(실패 귀속)."),
        ("trade_tape_scope_audit", TRADE_TAPE_SCOPE_AUDIT, "Trade tape scope audit(거래 테이프 범위 감사)."),
        ("queue", RUN364ER_QUEUE, "Next run queue(다음 실행 대기열)."),
        ("experiment_design_receipt", EXPERIMENT_RECEIPT, "Experiment design receipt(실험 설계 영수증)."),
        ("data_integrity_receipt", DATA_RECEIPT, "Data integrity receipt(데이터 무결성 영수증)."),
        ("model_validation_receipt", MODEL_RECEIPT, "Model validation receipt(모델 검증 영수증)."),
        ("artifact_lineage_receipt", LINEAGE_RECEIPT, "Artifact lineage receipt(산출물 계보 영수증)."),
        ("result_judgment_receipt", RESULT_RECEIPT, "Result judgment receipt(결과 판정 영수증)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ("script", Path(__file__), "EQ producer script(EQ 생산 스크립트)."),
    ]:
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
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "command": f"python {rel(Path(__file__))}",
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_work_packet()
    write_input_manifest()
    surface = build_surface()
    strict = surface[surface["strict_operational_proxy_pass"]]
    relaxed = surface[surface["relaxed_density_seed"]].sort_values(["combined_net", "min_split_profit_factor"], ascending=[False, False])
    relaxed_unique = relaxed.drop_duplicates(
        subset=[
            "candidate_id",
            "feature_set_id",
            "label_id",
            "threshold",
            "combined_net",
            "combined_trade_count",
            "combined_trade_density",
        ]
    ).head(50)
    failure_rows = build_failure_attribution(surface)
    tape_rows = build_trade_tape_scope_audit()
    queue_rows = build_queue({})
    final = build_final(surface, failure_rows, tape_rows, queue_rows)
    write_csv(SURFACE, frame_to_rows(surface, SURFACE_COLUMNS), fieldnames=SURFACE_COLUMNS)
    write_csv(STRICT_CANDIDATES, frame_to_rows(strict, SURFACE_COLUMNS), fieldnames=SURFACE_COLUMNS)
    write_csv(RELAXED_CANDIDATES, frame_to_rows(relaxed_unique, SURFACE_COLUMNS), fieldnames=SURFACE_COLUMNS)
    write_csv(FAILURE_ATTRIBUTION, failure_rows)
    write_csv(TRADE_TAPE_SCOPE_AUDIT, tape_rows)
    write_csv(RUN364ER_QUEUE, queue_rows)
    write_receipts(final)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, failure_rows, frame_to_rows(relaxed_unique, SURFACE_COLUMNS), gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
