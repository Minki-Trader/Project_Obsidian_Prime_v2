from __future__ import annotations

import csv
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
from stage_pipelines.stage364 import train_h17_density_failure_regime_behavior_reseed_without_db as dt  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dt.STAGE_ID
RUN_NUMBER = "run364DU"
RUN_ID = "run364DU_review_h17_density_failure_regime_behavior_reseed_without_db_v1"
PARENT_RUN_ID = dt.RUN_ID
NEXT_RUN_ID = "run364DV_train_h17_validation_stability_regime_source_reseed_without_db_v1"

STATUS = "completed_stage364DU_regime_behavior_review_package_rejected_open_dv_no_authority"
JUDGMENT = "negative_regime_behavior_review_oos_clue_validation_failure_no_package_no_authority"
DECISION = "stage364DU_reject_package_open_run364DV_validation_stability_reseed"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_regime_behavior_reseed_rejected_no_runtime_package_"
    "no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_DIR = dt.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "du_regime_behavior_review_summary.csv"
GAP_ATTRIBUTION = RUN_DIR / "du_validation_oos_gap_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "regime_behavior_failure_memory.csv"
RUN364DV_QUEUE = RUN_DIR / "run364DV_validation_stability_reseed_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DU_h17_density_failure_regime_behavior_reseed_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DU_h17_density_failure_regime_behavior_reseed_review.md"
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
    dt.FINAL_DECISION,
    dt.GATE_AUDIT,
    dt.TRADE_SURFACE,
    dt.SELECTED_CANDIDATE,
    dt.SELECTED_TRADE_TAPE,
    dt.MONTH_STABILITY,
    dt.COST_STRESS,
    dt.MODEL_SCORECARD,
    dt.ONNX_SMOKE_REPORT,
    dt.DATA_INTEGRITY_AUDIT,
    dt.RUN364DU_QUEUE,
    dt.RUN_EVIDENCE_RECEIPT,
    dt.EXPERIMENT_RECEIPT,
    dt.DATA_RECEIPT,
    dt.MODEL_RECEIPT,
    dt.ATTRIBUTION_RECEIPT,
    dt.JUDGMENT_RECEIPT,
    dt.LINEAGE_RECEIPT,
    dt.CLAIM_RECEIPT,
    dt.RUN_MANIFEST,
    dt.REPORT_PATH,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    GAP_ATTRIBUTION,
    PACKAGE_DECISION,
    FAILURE_MEMORY,
    RUN364DV_QUEUE,
    RESULT_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    LINEAGE_RECEIPT,
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


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return dt.rel(path)


def exists(path: Path | str) -> bool:
    return dt.exists(path)


def sha(path: Path | str) -> str:
    return dt.sha(path)


def read_json(path: Path) -> Any:
    return dt.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    dt.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dt.write_text(path, text, bom=bom)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(inner) for key, inner in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(inner) for inner in value]
    if hasattr(value, "item"):
        try:
            return value.item()
        except (TypeError, ValueError):
            return str(value)
    if isinstance(value, float) and not math.isfinite(value):
        return ""
    return value


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fields: list[str] = []
        for row in materialized:
            for key in row:
                if key not in fields:
                    fields.append(key)
        fieldnames = fields or ["empty"]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dt.append_or_replace_csv(path, key_fields, [{str(key): json_ready(value) for key, value in row.items()} for row in rows], extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dt.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dt.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return dt.as_float(value, default)


def ratio_text(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return "0/0"
    return f"{numerator}/{denominator}"


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "\n".join(["|" + "|".join(columns) + "|", "|" + "|".join("---" for _ in columns) + "|"])
    materialized = list(rows)[:limit]
    lines = ["|" + "|".join(columns) + "|", "|" + "|".join("---" for _ in columns) + "|"]
    for row in materialized:
        lines.append("|" + "|".join(str(row.get(column, "")) for column in columns) + "|")
    return "\n".join(lines)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing DU inputs(DU 입력 누락): " + ", ".join(missing))
    final = read_json(dt.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DT next_run_id mismatch(DT 다음 실행 ID 불일치): {final.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if final.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"DT forbidden claim(DT 금지 주장): {key}={final.get(key)}")
    gates = read_csv(dt.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DT gate audit(DT 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DU review input(DU 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def positive_months(months: pd.DataFrame, split: str) -> tuple[int, int, float]:
    subset = months[months["split"].astype(str) == split]
    total = int(len(subset))
    positive = int((subset["net_profit"].map(as_float) > 0).sum()) if total else 0
    ratio = round(positive / total, 6) if total else 0.0
    return positive, total, ratio


def cost_line(costs: pd.DataFrame, split: str, cost: float) -> dict[str, Any]:
    subset = costs[(costs["split"].astype(str) == split) & (costs["cost_per_trade"].map(as_float) == cost)]
    if subset.empty:
        return {"net_profit": "", "profit_factor": "", "expectancy": ""}
    row = subset.iloc[0].to_dict()
    return {
        "net_profit": row.get("net_profit", ""),
        "profit_factor": row.get("profit_factor", ""),
        "expectancy": row.get("expectancy", ""),
    }


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-model-validation(모델 검증)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "review_subject": PARENT_RUN_ID,
            "review_question": "Does DT regime/behavior reseed deserve package work or only failure-memory carryover?(DT 국면/현상 재시드가 패키지 작업 가치가 있는가, 아니면 실패 기억인가?)",
            "decision_use": "Open package only if validation and OOS both satisfy net/PF/density(검증과 표본외가 순수익/PF/밀도를 모두 만족할 때만 패키지를 엽니다).",
            "claim_boundary": CLAIM_BOUNDARY,
            "required_gates": [
                "input_lineage_gate",
                "dt_gate_inheritance_gate",
                "review_summary_gate",
                "validation_failure_gate",
                "package_rejection_gate",
                "next_queue_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
        },
    )


def build_reviews(dt_final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    surface = read_csv(dt.TRADE_SURFACE)
    months = read_csv(dt.MONTH_STABILITY)
    costs = read_csv(dt.COST_STRESS)
    smoke = read_csv(dt.ONNX_SMOKE_REPORT)

    smoke_pass = int(smoke["status"].astype(str).str.startswith("passed").sum()) if not smoke.empty else 0
    density_pass = surface[
        (surface["validation_trade_density"].map(as_float) >= 3.0)
        & (surface["oos_trade_density"].map(as_float) >= 3.0)
    ]
    density_net_pass = density_pass[
        (density_pass["validation_net"].map(as_float) > 0.0)
        & (density_pass["oos_net"].map(as_float) > 0.0)
    ]
    best_oos_net = surface.sort_values("oos_net", key=lambda col: col.map(as_float), ascending=False).head(1).to_dict("records")
    best_validation_net = surface.sort_values("validation_net", key=lambda col: col.map(as_float), ascending=False).head(1).to_dict("records")
    best_density = surface.sort_values(
        "validation_trade_density",
        key=lambda col: col.map(as_float),
        ascending=False,
    ).head(1).to_dict("records")

    val_pos, val_total, val_ratio = positive_months(months, "validation")
    oos_pos, oos_total, oos_ratio = positive_months(months, "oos")
    val_cost_03 = cost_line(costs, "validation", 0.3)
    oos_cost_03 = cost_line(costs, "oos", 0.3)
    val_cost_09 = cost_line(costs, "validation", 0.9)
    oos_cost_09 = cost_line(costs, "oos", 0.9)

    validation_net = as_float(dt_final["selected_validation_net"])
    oos_net = as_float(dt_final["selected_oos_net"])
    validation_pf = as_float(dt_final["selected_validation_profit_factor"])
    oos_pf = as_float(dt_final["selected_oos_profit_factor"])
    validation_density = as_float(dt_final["selected_validation_trade_density"])
    oos_density = as_float(dt_final["selected_oos_trade_density"])
    strict_count = int(dt_final["strict_candidate_count"])
    package_eligible = strict_count > 0 and validation_net > 0 and oos_net > 0 and validation_pf >= 1.2 and oos_pf >= 1.2 and validation_density >= 3 and oos_density >= 3

    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "selected_model_id": dt_final["selected_model_id"],
            "selected_label_id": dt_final["selected_label_id"],
            "selected_feature_set_id": dt_final["selected_feature_set_id"],
            "selected_hours_id": dt_final["selected_hours_id"],
            "selected_extra_filter": dt_final["selected_extra_filter"],
            "selected_validation_net": dt_final["selected_validation_net"],
            "selected_validation_profit_factor": dt_final["selected_validation_profit_factor"],
            "selected_validation_trade_density": dt_final["selected_validation_trade_density"],
            "selected_oos_net": dt_final["selected_oos_net"],
            "selected_oos_profit_factor": dt_final["selected_oos_profit_factor"],
            "selected_oos_trade_density": dt_final["selected_oos_trade_density"],
            "selected_oos_long_short": f"{dt_final['selected_oos_long_trade_count']}/{dt_final['selected_oos_short_trade_count']}",
            "strict_candidate_count": strict_count,
            "density_both_count": int(len(density_pass)),
            "density_and_net_count": int(len(density_net_pass)),
            "onnx_smoke_pass_rows": smoke_pass,
            "validation_positive_months": ratio_text(val_pos, val_total),
            "oos_positive_months": ratio_text(oos_pos, oos_total),
            "validation_positive_month_ratio": val_ratio,
            "oos_positive_month_ratio": oos_ratio,
            "validation_cost_0p9_net": val_cost_09["net_profit"],
            "oos_cost_0p9_net": oos_cost_09["net_profit"],
            "validation_oos_net_gap": round(oos_net - validation_net, 6),
            "package_eligible": str(package_eligible).lower(),
            "review_status": "package_rejected_open_dv(패키지 거절, DV 열기)",
            "effect": "OOS clue(표본외 단서)는 보존하지만 validation failure(검증 실패) 때문에 패키지로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "du01_validation_net_break",
            "observed_change": f"validation net/PF {validation_net}/{validation_pf} versus OOS net/PF {oos_net}/{oos_pf}",
            "likely_driver": "validation regime mismatch or source instability(검증 국면 불일치 또는 원천 불안정)",
            "evidence": rel(dt.MONTH_STABILITY),
            "confidence": "medium(중간)",
            "effect": "OOS 수익을 운영 후보로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "du02_density_below_trade_objective",
            "observed_change": f"validation/OOS density {validation_density}/{oos_density}",
            "likely_driver": "threshold and filter shape still too sparse(임계값과 필터 형태가 아직 희박함)",
            "evidence": rel(dt.TRADE_SURFACE),
            "confidence": "high(높음)",
            "effect": "Trade per day(일별 거래수) 3 이상 목표와의 차이를 명시합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "du03_oos_month_clue",
            "observed_change": f"validation positive months {val_pos}/{val_total}, OOS positive months {oos_pos}/{oos_total}",
            "likely_driver": "recent OOS behavior is favorable but not cross-split stable(최근 표본외 현상은 우호적이나 교차 분할 안정은 아님)",
            "evidence": rel(dt.MONTH_STABILITY),
            "confidence": "medium(중간)",
            "effect": "긍정 단서는 다음 source stability(원천 안정성) 탐색 씨앗으로만 씁니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "du04_cost_stress_split_asymmetry",
            "observed_change": f"cost0.3 validation/OOS net {val_cost_03['net_profit']}/{oos_cost_03['net_profit']}; cost0.9 validation/OOS net {val_cost_09['net_profit']}/{oos_cost_09['net_profit']}",
            "likely_driver": "signal split asymmetry dominates cost stress(신호 분할 비대칭이 비용 압박보다 큼)",
            "evidence": rel(dt.COST_STRESS),
            "confidence": "medium(중간)",
            "effect": "수수료/스프레드 조정보다 검증 안정성 재시드가 우선임을 정합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    if best_oos_net:
        attribution.append(
            {
                "run_id": RUN_ID,
                "attribution_id": "du05_best_oos_surface_is_not_decision",
                "observed_change": f"best OOS row model {best_oos_net[0].get('model_id')} OOS net {best_oos_net[0].get('oos_net')}",
                "likely_driver": "multiple surface search can over-select OOS(다중 표면 탐색이 표본외를 과선택할 수 있음)",
                "evidence": rel(dt.TRADE_SURFACE),
                "confidence": "high(높음)",
                "effect": "OOS 최고 행을 패키지 근거로 쓰지 않습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    package = [
        {
            "run_id": RUN_ID,
            "decision": "do_not_open_runtime_package(런타임 패키지 열지 않음)",
            "reason": "strict_candidate_count=0 and selected validation net/PF are negative/below 1(엄격 후보 0개, 선택 검증 순수익/PF가 음수 또는 1 미만)",
            "selected_model_id": dt_final["selected_model_id"],
            "selected_validation_net": validation_net,
            "selected_validation_profit_factor": validation_pf,
            "selected_validation_trade_density": validation_density,
            "selected_oos_net": oos_net,
            "selected_oos_profit_factor": oos_pf,
            "selected_oos_trade_density": oos_density,
            "next_run_id": NEXT_RUN_ID,
            "effect": "좋아 보이는 OOS 결과를 MT5 package(MT5 패키지)로 착각하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "du01_regime_behavior_oos_clue_validation_fail",
            "observation": f"validation {validation_net}/{validation_pf}/{validation_density}; OOS {oos_net}/{oos_pf}/{oos_density}; strict={strict_count}",
            "why_failed": "validation net and PF failed while OOS looked strong(검증 순수익과 PF가 실패했지만 표본외는 강하게 보임)",
            "salvage_value": "3-class regime/behavior features produced a real OOS clue(3분류 국면/현상 피처가 표본외 단서를 만들었음)",
            "reopen_condition": "validation stability reseed must make validation net positive and density >=3 before package(검증 안정성 재시드가 검증 순수익 양수와 밀도 3 이상을 먼저 만들어야 함)",
            "do_not_repeat": "do not package or tune only on OOS-positive rows(OOS 양수 행만 보고 패키지하거나 미세조정하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "dv01_validation_stability_reseed",
            "seed": "DT has strong OOS net/PF but validation net/PF fails(DT는 OOS 순수익/PF가 강하지만 검증 순수익/PF가 실패함)",
            "target_question": "Can validation-stability source filters or labels keep the OOS clue while repairing validation quality?(검증 안정성 원천 필터나 라벨이 OOS 단서를 보존하면서 검증 품질을 고칠 수 있는가?)",
            "must_keep": "train/validation/OOS split(학습/검증/표본외 분할), no trade splitting(거래 쪼개기 금지), no package before review(검토 전 패키지 금지), ONNX smoke boundary(ONNX 스모크 경계)",
            "avoid": "OOS-only selection(OOS 전용 선택), risk multiplier only(위험 배수만), cost tweak only(비용 조정만), package despite validation loss(검증 손실에도 패키지)",
            "candidate_ideas": "validation-negative month/session guard(검증 음수 월/세션 가드), score monotonicity filter(점수 단조성 필터), long/short source balance(롱/숏 원천 균형), regime-stability label(국면 안정성 라벨), bad-month exclusion stress(나쁜 달 제외 압박 시험)",
            "effect": "DT의 긍정 단서를 살리되 validation failure(검증 실패)를 다음 탐색의 중심 제약으로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    write_csv(REVIEW_SUMMARY, summary)
    write_csv(GAP_ATTRIBUTION, attribution)
    write_csv(PACKAGE_DECISION, package)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(RUN364DV_QUEUE, queue)
    _ = best_validation_net, best_density
    return summary, attribution, package, failure, queue


def build_final(dt_final: Mapping[str, Any], summary: Mapping[str, Any], created_at: str, gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "selected_model_id": dt_final["selected_model_id"],
        "selected_label_id": dt_final["selected_label_id"],
        "selected_feature_set_id": dt_final["selected_feature_set_id"],
        "selected_validation_net": dt_final["selected_validation_net"],
        "selected_validation_profit_factor": dt_final["selected_validation_profit_factor"],
        "selected_validation_trade_density": dt_final["selected_validation_trade_density"],
        "selected_oos_net": dt_final["selected_oos_net"],
        "selected_oos_profit_factor": dt_final["selected_oos_profit_factor"],
        "selected_oos_trade_density": dt_final["selected_oos_trade_density"],
        "strict_candidate_count": dt_final["strict_candidate_count"],
        "density_both_count": summary["density_both_count"],
        "density_and_net_count": summary["density_and_net_count"],
        "onnx_smoke_pass_rows": summary["onnx_smoke_pass_rows"],
        "validation_positive_months": summary["validation_positive_months"],
        "oos_positive_months": summary["oos_positive_months"],
        "runtime_package": "not_opened",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    dt_gates = read_csv(dt.GATE_AUDIT)
    receipts = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    final_exists = exists(FINAL_DECISION)
    final = read_json(FINAL_DECISION) if final_exists else {}
    gates = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES if path != Path(__file__)), INPUT_MANIFEST, "DT 입력 산출물을 모두 연결했습니다."),
        ("dt_gate_inheritance_gate", not dt_gates.empty and all(dt_gates["status"].astype(str) == "passed"), dt.GATE_AUDIT, "DT 게이트 통과 상태를 상속했습니다."),
        ("review_summary_gate", exists(REVIEW_SUMMARY) and exists(GAP_ATTRIBUTION), REVIEW_SUMMARY, "검증/OOS 차이를 요약했습니다."),
        ("validation_failure_gate", exists(FAILURE_MEMORY) and as_float(final.get("selected_validation_net", 0)) < 0, FAILURE_MEMORY, "검증 실패를 실패 기억으로 기록했습니다."),
        ("package_rejection_gate", exists(PACKAGE_DECISION) and int(final.get("strict_candidate_count", 0)) == 0, PACKAGE_DECISION, "패키지를 열지 않는 결정을 기록했습니다."),
        ("next_queue_gate", exists(RUN364DV_QUEUE), RUN364DV_QUEUE, "DV 검증 안정성 재시드 대기열을 기록했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RESULT_RECEIPT, "필수 영수증이 있습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    return [
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


def write_receipts(final: Mapping[str, Any], attribution: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RESULT_RECEIPT,
        {
            **base,
            "result_subject": PARENT_RUN_ID,
            "evidence_available": [rel(REVIEW_SUMMARY), rel(GAP_ATTRIBUTION), rel(PACKAGE_DECISION), rel(FAILURE_MEMORY), rel(dt.ONNX_SMOKE_REPORT)],
            "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "OOS 단서는 있지만 검증 손실이 커서 패키지로 올리지 않습니다.",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "ExtraTrees/RandomForest(엑스트라트리/랜덤포레스트)",
            "selected_model_id": final["selected_model_id"],
            "target_and_label": final["selected_label_id"],
            "split_method": "chronological train/validation/OOS(시간순 학습/검증/표본외)",
            "selection_metric": "cross-split net/PF/density contract(교차 분할 순수익/PF/밀도 계약)",
            "secondary_metrics": ["month stability(월 안정성)", "cost stress(비용 압박)", "long/short count(롱/숏 거래수)", "ONNX smoke(온엑스 스모크)"],
            "threshold_policy": "searched proxy threshold(프록시 탐색 임계값)",
            "overfit_risk": "OOS-positive row over-selection(OOS 양수 행 과선택)",
            "calibration_risk": "tree scores are ranking signals, not operating probabilities(트리 점수는 운영 확률이 아니라 순위 신호)",
            "comparison_baseline": "DT selected model and DS bridge failure(DT 선택 모델과 DS 브리지 실패)",
            "validation_judgment": JUDGMENT,
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": f"validation net/PF/density {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']}; OOS {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}",
            "comparison_baseline": "DT training closeout(DT 학습 종료 기록)",
            "likely_drivers": [row["likely_driver"] for row in attribution],
            "segment_checks": [rel(dt.MONTH_STABILITY), rel(dt.COST_STRESS), rel(dt.TRADE_SURFACE)],
            "attribution_confidence": "medium(중간)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_review_no_package(검토 연결, 패키지 없음)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_package": "not_opened",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "프록시 OOS 단서를 운영 주장으로 바꾸지 않습니다.",
        },
    )


def write_docs(final: Mapping[str, Any], summary: Sequence[Mapping[str, Any]], attribution: Sequence[Mapping[str, Any]], package: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DU H17 Density-Failure Regime/Behavior Review(밀도 실패 국면/현상 검토)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_package(런타임 패키지): `not_opened(열지 않음)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Review Summary(검토 요약)

{markdown_table(summary, ['selected_model_id', 'selected_validation_net', 'selected_validation_profit_factor', 'selected_validation_trade_density', 'selected_oos_net', 'selected_oos_profit_factor', 'selected_oos_trade_density', 'strict_candidate_count', 'validation_positive_months', 'oos_positive_months', 'review_status'])}

## Attribution(귀속)

{markdown_table(attribution, ['attribution_id', 'observed_change', 'likely_driver', 'confidence', 'effect'])}

## Package Decision(패키지 결정)

{markdown_table(package, ['decision', 'reason', 'selected_validation_net', 'selected_oos_net', 'next_run_id'])}

## Failure Memory(실패 기억)

{markdown_table(failure, ['memory_id', 'why_failed', 'salvage_value', 'reopen_condition', 'do_not_repeat'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This is review-only(검토 전용)입니다. ONNX smoke(온엑스 스모크)는 model artifact sanity(모델 산출물 점검)일 뿐이고, MT5 execution(MT5 실행), runtime package(런타임 패키지), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DU decision(결정): regime/behavior reseed review(국면/현상 재시드 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- runtime package(런타임 패키지): `not_opened(열지 않음)`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): OOS clue(표본외 단서)를 살리되 validation failure(검증 실패)를 다음 source stability(원천 안정성) 탐색의 제약으로 바꿉니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DU__{RUN_ID}", f"\n- run364DU__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - regime/behavior reseed review(국면/현상 재시드 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DU__{RUN_ID}", f"\n<!-- run364DU__{RUN_ID} -->\n\n## run364DU Regime/Behavior Review(국면/현상 검토)\n\nAction(행동): DT OOS clue(DT 표본외 단서)와 validation failure(검증 실패)를 분리 판정했습니다.\n\nEffect(효과): package(패키지)는 거절하고 `{NEXT_RUN_ID}`에서 validation-stability source(검증 안정성 원천)를 탐색합니다.\n")
    append_text_once(STAGE_README, f"run364DU__{RUN_ID}", f"\n<!-- run364DU__{RUN_ID} -->\n## run364DU review(검토)\n\nDT regime/behavior reseed(DT 국면/현상 재시드)는 OOS clue(표본외 단서)가 있으나 validation failure(검증 실패) 때문에 package rejected(패키지 거절)입니다. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364DU` reviewed(검토 완료) DT regime/behavior reseed(DT 국면/현상 재시드). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다. strict_candidate_count(엄격 후보 수)는 `{final['strict_candidate_count']}`라서 runtime package(런타임 패키지)는 열지 않았습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 validation-stability source reseed(검증 안정성 원천 재시드)를 실행합니다.

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

Latest review(최근 검토): DT regime/behavior reseed(DT 국면/현상 재시드)는 OOS clue(표본외 단서)가 있지만 validation failure(검증 실패) 때문에 package rejected(패키지 거절)입니다.

Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Next seed(다음 씨앗): validation-stability source reseed(검증 안정성 원천 재시드).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364DU__{RUN_ID}", f"\n<!-- run364DU__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed DT regime/behavior reseed(국면/현상 재시드); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DU__{RUN_ID}", f"\n<!-- run364DU__{RUN_ID} -->\n- `{RUN_ID}`: DT 3-class regime/behavior model(3분류 국면/현상 모델)은 OOS clue(표본외 단서)를 만들었지만 validation failure(검증 실패)로 패키지 불가입니다. Effect(효과): 다음 탐색은 validation-stability source(검증 안정성 원천)에 집중합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364DU__validation_failure__{RUN_ID}", f"\n<!-- run364DU__validation_failure__{RUN_ID} -->\n- `{RUN_ID}`: regime/behavior reseed(국면/현상 재시드)는 validation net/PF(검증 순수익/PF) 실패로 package rejected(패키지 거절)입니다. Effect(효과): OOS-only success(OOS 전용 성공)를 운영 근거로 쓰지 않습니다.\n")


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
        "rows": 1,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "work_family": "kpi_evidence(KPI 근거)",
        "scoreboard_lane": "regime_behavior_reseed_review(국면/현상 재시드 검토)",
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 검토 전용)",
        "evidence_boundary": "proxy_review_no_mt5_no_package(프록시 검토, MT5/패키지 없음)",
        "question": "Does DT regime/behavior reseed deserve package work or only failure-memory carryover?(DT 국면/현상 재시드가 패키지 작업 가치가 있는가, 아니면 실패 기억인가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_oos_net"],
        "profit_factor": final["selected_oos_profit_factor"],
        "trade_density_per_feature_day": final["selected_oos_trade_density"],
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(REVIEW_SUMMARY),
        "primary_kpi": f"validation_net={final['selected_validation_net']};oos_net={final['selected_oos_net']};strict={final['strict_candidate_count']}",
        "guardrail_kpi": "package=not_opened;runtime_authority=not_claimed;operating_promotion=not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "view": record_view,
            "tier": tier_scope,
            "kpi_scope": "DU regime/behavior review(DU 국면/현상 검토)",
            "metric_scope": "proxy_review(Python 프록시 검토)",
            "status": status,
            "source_authority": "proxy_review_no_mt5_no_package(프록시 검토, MT5/패키지 없음)",
        }
        if suffix != "tier_a_separate":
            for key in ["net_profit", "profit_factor", "trade_density_per_feature_day"]:
                row[key] = ""
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for artifact_type, path, notes in [
        ("review_summary", REVIEW_SUMMARY, "DU review summary(DU 검토 요약)."),
        ("gap_attribution", GAP_ATTRIBUTION, "Validation/OOS gap attribution(검증/표본외 차이 귀속)."),
        ("package_decision", PACKAGE_DECISION, "Package decision(패키지 결정)."),
        ("failure_memory", FAILURE_MEMORY, "Failure memory(실패 기억)."),
        ("queue", RUN364DV_QUEUE, "Next run queue(다음 실행 대기열)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ("script", Path(__file__), "DU producer script(DU 생산 스크립트)."),
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
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    dt_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    summary, attribution, package, failure, _queue = build_reviews(dt_final)
    created_at = now_utc()
    gates = gate_rows(final_written=False)
    final = build_final(dt_final, summary[0], created_at, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final, attribution)
    gates = gate_rows(final_written=True)
    write_csv(GATE_AUDIT, gates)
    final = build_final(dt_final, summary[0], created_at, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, summary, attribution, package, failure, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
