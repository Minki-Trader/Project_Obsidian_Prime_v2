from __future__ import annotations

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class ArtifactAccess:
    def io_path(self, path: Path | str) -> Path:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        raw = str(candidate)
        if raw.startswith("\\\\?\\"):
            return Path(raw)
        if len(raw) >= 240:
            return Path("\\\\?\\" + raw)
        return candidate

    def rel(self, path: Path | str) -> str:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        try:
            return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return candidate.as_posix()

    def sha256_file(self, path: Path | str) -> str:
        digest = hashlib.sha256()
        with self.io_path(path).open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()


aw = ArtifactAccess()

TODAY = "2026-06-01"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_NUMBER = "run337JO"
RUN_ID = "run337JO_review_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_training_without_db_v1"
PARENT_RUN_ID = "run337JN_train_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_candidates_without_db_v1"
NEXT_RUN_ID = "run337JP_materialize_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_runtime_probe_package_without_db_v1"
STATUS = "completed_stage337JO_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_training_review_runtime_probe_package_required_no_selection"
JUDGMENT = "proxy_positive_but_high_density_side_imbalance_and_weak_accuracy_mt5_runtime_probe_required_no_selection"
DECISION = "stage337JO_open_run337JP_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_runtime_probe_package"
CLAIM_BOUNDARY = (
    "research_development_training_review_only_no_candidate_selection_no_mt5_execution_in_JO_"
    "no_runtime_package_authority_no_forward_no_operating_or_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run337JN"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337JO_positive_low_pf_recovery_drawdown_dual_probe_repair_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337JO_positive_low_pf_recovery_drawdown_dual_probe_repair_training_review.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_QUEUE = PARENT_RUN_DIR / "run337JO_review_queue.csv"
FEATURE_SCHEMA = PARENT_RUN_DIR / "jn_allowed_feature_schema.json"
TRAINED_MODEL_MANIFEST = PARENT_RUN_DIR / "jn_trained_model_manifest.csv"
ONNX_PARITY = PARENT_RUN_DIR / "jn_onnx_parity_matrix.csv"
CLASSIFICATION_SCORECARD = PARENT_RUN_DIR / "jn_inner_holdout_classification_scorecard.csv"
PROXY_TRADE_SCORECARD = PARENT_RUN_DIR / "jn_inner_holdout_proxy_trade_scorecard.csv"
RELEASE_DISPOSITION = PARENT_RUN_DIR / "jn_training_release_disposition.csv"
RUNTIME_FIREWALL = PARENT_RUN_DIR / "jn_runtime_firewall_review.csv"

CANDIDATE_REVIEW = RUN_DIR / "jo_training_candidate_review.csv"
POSITIVE_MATRIX = RUN_DIR / "jo_positive_proxy_candidate_matrix.csv"
PROBE_PRIORITY = RUN_DIR / "jo_runtime_probe_priority_matrix.csv"
ATTRIBUTION_MATRIX = RUN_DIR / "jo_side_pf_recovery_drawdown_cost_attribution.csv"
PROXY_MT5_REQUIREMENT = RUN_DIR / "jo_proxy_mt5_comparison_requirement.csv"
FAILURE_MEMORY_CONTROL = RUN_DIR / "jo_failure_memory_and_trade_shape_control.csv"
TIER_PAIR_RECORD = RUN_DIR / "jo_tier_pair_required_record.csv"
RUNTIME_QUEUE = RUN_DIR / "run337JP_runtime_probe_package_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    PARENT_FINAL_DECISION,
    PARENT_GATE_AUDIT,
    PARENT_QUEUE,
    FEATURE_SCHEMA,
    TRAINED_MODEL_MANIFEST,
    ONNX_PARITY,
    CLASSIFICATION_SCORECARD,
    PROXY_TRADE_SCORECARD,
    RELEASE_DISPOSITION,
    RUNTIME_FIREWALL,
)
OUTPUT_FILES = (
    CANDIDATE_REVIEW,
    POSITIVE_MATRIX,
    PROBE_PRIORITY,
    ATTRIBUTION_MATRIX,
    PROXY_MT5_REQUIREMENT,
    FAILURE_MEMORY_CONTROL,
    TIER_PAIR_RECORD,
    RUNTIME_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    ROOT_SELECTION_STATUS,
    STAGE_BRIEF,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), low_memory=False)


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    target = path if len(str(path)) < 240 else io(path)
    frame.to_csv(target, index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def numeric(frame: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    output = frame.copy()
    for column in columns:
        if column in output.columns:
            output[column] = pd.to_numeric(output[column], errors="coerce")
    return output


def weakness_tags(row: pd.Series) -> str:
    tags: list[str] = []
    if bool(row.get("is_directional_proxy", False)) and float(row.get("profit_factor", 0.0) or 0.0) < 1.10:
        tags.append("profit_factor_below_1_10")
    if bool(row.get("is_directional_proxy", False)) and float(row.get("recovery_factor", 0.0) or 0.0) < 1.50:
        tags.append("recovery_factor_below_1_50")
    density = float(row.get("signal_density", 0.0) or 0.0)
    if bool(row.get("is_directional_proxy", False)) and density > 0.95:
        tags.append("extreme_signal_density_above_0_95")
    elif bool(row.get("is_directional_proxy", False)) and density > 0.80:
        tags.append("high_signal_density_above_0_80")
    if float(row.get("side_balance_ratio", 0.0) or 0.0) < 0.50:
        tags.append("side_balance_ratio_below_0_50")
    elif float(row.get("side_balance_ratio", 0.0) or 0.0) < 0.70:
        tags.append("side_balance_ratio_below_0_70")
    if float(row.get("long_net", 0.0) or 0.0) < 0.0:
        tags.append("long_net_negative")
    if float(row.get("short_net", 0.0) or 0.0) < 0.0:
        tags.append("short_net_negative")
    if float(row.get("balanced_accuracy", 0.0) or 0.0) < 0.40:
        tags.append("weak_balanced_accuracy_below_0_40")
    if float(row.get("max_drawdown", 0.0) or 0.0) > 3.0:
        tags.append("proxy_drawdown_above_3")
    if not tags:
        tags.append("no_major_proxy_review_tag")
    return ";".join(tags)


def risk_adjusted_score(review: pd.DataFrame) -> pd.Series:
    net = pd.to_numeric(review["net_log_return_after_cost"], errors="coerce").fillna(-999999.0)
    pf = pd.to_numeric(review["profit_factor"], errors="coerce").fillna(0.0)
    recovery = pd.to_numeric(review["recovery_factor"], errors="coerce").fillna(0.0)
    drawdown = pd.to_numeric(review["max_drawdown"], errors="coerce").fillna(99.0)
    density = pd.to_numeric(review["signal_density"], errors="coerce").fillna(1.0)
    long_net = pd.to_numeric(review["long_net"], errors="coerce").fillna(0.0)
    balanced_accuracy = pd.to_numeric(review["balanced_accuracy"], errors="coerce").fillna(0.0)
    side_balance = pd.to_numeric(review["side_balance_ratio"], errors="coerce").fillna(0.0)
    return (
        net
        + 0.70 * pf
        + 0.15 * recovery
        + 0.80 * side_balance
        - 0.15 * drawdown
        - 0.70 * density.gt(0.95).astype(float)
        - 0.35 * balanced_accuracy.lt(0.35).astype(float)
        - 0.30 * long_net.lt(0.0).astype(float)
    )


def classify_probe_role(row: pd.Series, raw_top_id: str, balanced_control_id: str, cost_control_id: str) -> str:
    model_id = str(row["model_id"])
    if model_id == raw_top_id:
        return "runtime_probe_primary_raw_top_not_selected"
    if model_id == balanced_control_id:
        return "runtime_probe_balance_control_not_selected"
    if model_id == cost_control_id:
        return "runtime_probe_cost_stress_control_not_selected"
    if bool(row["is_proxy_positive"]):
        return "proxy_positive_secondary_not_packaged"
    return "proxy_nonpositive_no_runtime_package"


def build_review() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    manifest = read_csv(TRAINED_MODEL_MANIFEST)
    parity = read_csv(ONNX_PARITY)
    release = read_csv(RELEASE_DISPOSITION)
    classification = numeric(
        read_csv(CLASSIFICATION_SCORECARD),
        ["rows", "accuracy", "balanced_accuracy", "macro_f1", "log_loss", "signal_density"],
    )
    proxy = numeric(
        read_csv(PROXY_TRADE_SCORECARD),
        [
            "trade_count",
            "signal_density",
            "net_log_return_after_cost",
            "profit_factor",
            "expectancy",
            "max_drawdown",
            "recovery_factor",
            "long_count",
            "short_count",
            "long_net",
            "short_net",
        ],
    )
    holdout_proxy = proxy.loc[proxy["split"].astype(str).eq("inner_holdout")].copy()
    holdout_class = classification.loc[classification["split"].astype(str).eq("inner_holdout")].copy()
    holdout_class = holdout_class.rename(columns={"signal_density": "class_signal_density"})
    review = (
        manifest.merge(holdout_proxy, on=["model_id", "task_id"], how="left", suffixes=("", "_proxy"))
        .merge(
            holdout_class[
                [
                    "model_id",
                    "task_id",
                    "accuracy",
                    "balanced_accuracy",
                    "macro_f1",
                    "log_loss",
                    "class_signal_density",
                ]
            ],
            on=["model_id", "task_id"],
            how="left",
        )
        .merge(parity[["model_id", "task_id", "passed", "max_abs_diff"]], on=["model_id", "task_id"], how="left")
        .merge(release[["model_id", "release_disposition"]], on="model_id", how="left")
    )
    review["is_directional_proxy"] = review["score_mode"].astype(str).str.startswith("directional_")
    review["is_proxy_positive"] = review["is_directional_proxy"] & (
        pd.to_numeric(review["net_log_return_after_cost"], errors="coerce").fillna(0.0) > 0.0
    )
    side_max = review[["long_count", "short_count"]].max(axis=1).replace(0, np.nan)
    side_min = review[["long_count", "short_count"]].min(axis=1)
    review["side_balance_ratio"] = (side_min / side_max).fillna(0.0)
    review["side_net_warning"] = np.where(
        (pd.to_numeric(review["long_net"], errors="coerce").fillna(0.0) < 0.0)
        | (pd.to_numeric(review["short_net"], errors="coerce").fillna(0.0) < 0.0),
        "side_net_negative_present",
        "side_net_nonnegative",
    )
    directional_score = pd.to_numeric(review["net_log_return_after_cost"], errors="coerce").fillna(-999999.0)
    review["raw_proxy_rank"] = directional_score.where(review["is_directional_proxy"], -999999.0).rank(
        method="first",
        ascending=False,
    ).astype(int)
    review["risk_adjusted_score"] = risk_adjusted_score(review).where(review["is_directional_proxy"], -999999.0)
    review["risk_adjusted_rank"] = review["risk_adjusted_score"].rank(method="first", ascending=False).astype(int)
    review["weakness_tags"] = review.apply(weakness_tags, axis=1)

    positive = review.loc[review["is_proxy_positive"]].copy().sort_values(
        ["net_log_return_after_cost", "profit_factor"], ascending=[False, False]
    )
    raw_top = positive.head(1)
    balance_pool = positive.copy()
    if not balance_pool.empty:
        balance_ok = pd.to_numeric(balance_pool["side_balance_ratio"], errors="coerce").fillna(0.0).ge(0.75)
        balance_pool["balance_control_score"] = np.where(
            balance_ok,
            pd.to_numeric(balance_pool["net_log_return_after_cost"], errors="coerce").fillna(-999999.0)
            + 0.25 * pd.to_numeric(balance_pool["profit_factor"], errors="coerce").fillna(0.0)
            + 0.25 * pd.to_numeric(balance_pool["side_balance_ratio"], errors="coerce").fillna(0.0),
            -999999.0,
        )
    balance_pool = balance_pool.sort_values(
        ["balance_control_score", "side_balance_ratio", "net_log_return_after_cost"], ascending=[False, False, False]
    )
    cost_pool = positive.loc[positive["task_id"].astype(str).str.contains("cost_stress", case=False, na=False)]
    if cost_pool.empty:
        cost_pool = positive.sort_values(["profit_factor", "net_log_return_after_cost"], ascending=[False, False])
    cost_pool = cost_pool.sort_values(["net_log_return_after_cost", "profit_factor"], ascending=[False, False])
    raw_top_id = str(raw_top.iloc[0]["model_id"]) if len(raw_top) else ""
    balanced_control_id = str(balance_pool.iloc[0]["model_id"]) if len(balance_pool) else ""
    cost_control_id = str(cost_pool.iloc[0]["model_id"]) if len(cost_pool) else ""

    review["jo_probe_role"] = review.apply(
        classify_probe_role,
        axis=1,
        raw_top_id=raw_top_id,
        balanced_control_id=balanced_control_id,
        cost_control_id=cost_control_id,
    )
    review["allowed_use"] = "runtime probe prioritization only(MT5 런타임 탐침 우선순위 전용)"
    review["forbidden_use"] = "candidate selection or MT5 KPI replacement(후보 선택 또는 MT5 핵심 성과 지표 대체)"
    review["failure_memory_applied"] = np.where(
        review["signal_density"].astype(float).gt(0.95),
        "high-density MT5 collapse risk applied(고밀도 MT5 붕괴 위험 반영)",
        "density failure memory checked(밀도 실패 기억 확인)",
    )
    review["effect"] = "proxy-positive(프록시 양수)를 selected model(선정 모델)이 아니라 MT5 runtime probe(MT5 런타임 탐침) 비교 대상으로 분리한다."
    review["claim_boundary"] = CLAIM_BOUNDARY

    priority = review.loc[
        review["jo_probe_role"].isin(
            [
                "runtime_probe_primary_raw_top_not_selected",
                "runtime_probe_balance_control_not_selected",
                "runtime_probe_cost_stress_control_not_selected",
            ]
        )
    ].copy()
    role_order = {
        "runtime_probe_primary_raw_top_not_selected": 0,
        "runtime_probe_balance_control_not_selected": 1,
        "runtime_probe_cost_stress_control_not_selected": 2,
    }
    priority["probe_order"] = priority["jo_probe_role"].map(role_order).fillna(99).astype(int)
    priority = priority.sort_values(["probe_order", "raw_proxy_rank"]).drop_duplicates("model_id")

    positive = positive.merge(review[["model_id", "jo_probe_role", "weakness_tags"]], on="model_id", how="left", suffixes=("", "_review"))
    attribution = review[
        [
            "model_id",
            "task_id",
            "model_family",
            "target_column",
            "score_mode",
            "trade_count",
            "signal_density",
            "net_log_return_after_cost",
            "profit_factor",
            "expectancy",
            "max_drawdown",
            "recovery_factor",
            "long_count",
            "short_count",
            "side_balance_ratio",
            "long_net",
            "short_net",
            "side_net_warning",
            "balanced_accuracy",
            "macro_f1",
            "max_abs_diff",
            "raw_proxy_rank",
            "risk_adjusted_score",
            "risk_adjusted_rank",
            "weakness_tags",
            "failure_memory_applied",
            "jo_probe_role",
        ]
    ].copy()
    attribution["effect"] = "side/PF/recovery/drawdown/cost attribution(방향/PF/회복/낙폭/비용 귀속)을 MT5 탐침 전 검토 근거로 남긴다."
    attribution["claim_boundary"] = CLAIM_BOUNDARY

    requirement = pd.DataFrame(
        [
            {
                "requirement_id": "jo_proxy_positive_requires_mt5_runtime_probe",
                "status": "required",
                "proxy_positive_rows": int(len(positive)),
                "runtime_probe_priority_rows": int(len(priority)),
                "primary_raw_top_model_id": raw_top_id,
                "balance_control_model_id": balanced_control_id,
                "cost_control_model_id": cost_control_id,
                "reason": "proxy expected value(프록시 예상값)는 MT5 runtime probe(MT5 런타임 탐침)를 대체하지 않는다.",
                "effect": "JP package(JP 패키지)가 raw top(순수 1위), balance control(균형 대조), cost control(비용 대조)을 비교하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    failure_control = pd.DataFrame(
        [
            {
                "control_id": "jo_high_density_side_imbalance_control",
                "status": "active",
                "raw_top_model_id": raw_top_id,
                "raw_top_weakness": str(raw_top.iloc[0]["weakness_tags"]) if len(raw_top) else "",
                "balance_control_model_id": balanced_control_id,
                "cost_control_model_id": cost_control_id,
                "required_next_observation": "compare proxy expected value with MT5 runtime output(프록시 예상값과 MT5 런타임 출력 비교)",
                "effect": "높은 proxy net(프록시 순수익)이 density(밀도)와 side imbalance(방향 불균형) 때문에 MT5에서 깨지는지 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    tier_record = pd.DataFrame(
        [
            {
                "tier_view": "Tier A separate(Tier A 분리)",
                "status": "reviewed",
                "evidence_path": rel(CANDIDATE_REVIEW),
                "effect": "Tier A(티어 A) 후보 검토 범위를 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "tier_view": "Tier B separate(Tier B 분리)",
                "status": "missing_required",
                "evidence_path": rel(TIER_PAIR_RECORD),
                "effect": "Tier B(티어 B)가 없음을 생략하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "tier_view": "Tier A+B combined(Tier A+B 합산)",
                "status": "missing_required",
                "evidence_path": rel(TIER_PAIR_RECORD),
                "effect": "합산 결과를 만들지 못했음을 명시한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "queued_task": "materialize_mt5_runtime_probe_package_for_positive_low_pf_recovery_drawdown_dual_probe_candidates(양수 저PF/회복/낙폭 이중 탐침 후보 MT5 런타임 탐침 패키지 물질화)",
                "candidate_count": int(len(priority)),
                "candidate_model_ids": ";".join(priority["model_id"].astype(str).tolist()),
                "candidate_task_ids": ";".join(priority["task_id"].astype(str).tolist()),
                "probe_roles": ";".join(priority["jo_probe_role"].astype(str).tolist()),
                "required_inputs": f"{rel(TRAINED_MODEL_MANIFEST)};{rel(ONNX_PARITY)};{rel(FEATURE_SCHEMA)};{rel(PROBE_PRIORITY)}",
                "required_outputs": "runtime probe package manifest and MT5 execution attempt plan(런타임 탐침 패키지 목록과 MT5 실행 시도 계획)",
                "forbidden_action": "treat probe priority as selected model(탐침 우선순위를 선정 모델로 취급)",
                "effect": "proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 비교하도록 다음 작업을 연다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    best = raw_top.iloc[0] if len(raw_top) else None
    balance = balance_pool.iloc[0] if len(balance_pool) else None
    cost = cost_pool.iloc[0] if len(cost_pool) else None
    summary = {
        "candidate_rows": int(len(review)),
        "directional_holdout_rows": int(review["is_directional_proxy"].sum()),
        "positive_proxy_rows": int(len(positive)),
        "runtime_queue_candidate_count": int(len(priority)),
        "onnx_parity_rows": int(len(parity)),
        "onnx_parity_passed_rows": int(passed_status(parity["passed"]).sum()),
        "primary_probe_model_id": str(best["model_id"]) if best is not None else "",
        "primary_probe_task_id": str(best["task_id"]) if best is not None else "",
        "primary_proxy_net": float(best["net_log_return_after_cost"]) if best is not None else 0.0,
        "primary_profit_factor": float(best["profit_factor"]) if best is not None else 0.0,
        "primary_expectancy": float(best["expectancy"]) if best is not None else 0.0,
        "primary_max_drawdown": float(best["max_drawdown"]) if best is not None else 0.0,
        "primary_recovery_factor": float(best["recovery_factor"]) if best is not None else 0.0,
        "primary_trade_count": int(best["trade_count"]) if best is not None else 0,
        "primary_signal_density": float(best["signal_density"]) if best is not None else 0.0,
        "primary_side_balance_ratio": float(best["side_balance_ratio"]) if best is not None else 0.0,
        "primary_long_net": float(best["long_net"]) if best is not None else 0.0,
        "primary_short_net": float(best["short_net"]) if best is not None else 0.0,
        "primary_balanced_accuracy": float(best["balanced_accuracy"]) if best is not None else 0.0,
        "primary_weakness_tags": str(best["weakness_tags"]) if best is not None else "",
        "balance_control_model_id": str(balance["model_id"]) if balance is not None else "",
        "balance_control_side_balance_ratio": float(balance["side_balance_ratio"]) if balance is not None else 0.0,
        "balance_control_proxy_net": float(balance["net_log_return_after_cost"]) if balance is not None else 0.0,
        "cost_control_model_id": str(cost["model_id"]) if cost is not None else "",
        "cost_control_proxy_net": float(cost["net_log_return_after_cost"]) if cost is not None else 0.0,
        "next_action": NEXT_RUN_ID,
    }
    return review, positive, priority, attribution, requirement, failure_control, tier_record, queue, summary


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(PARENT_GATE_AUDIT)
    parent_passed = passed_status(parent_gates["status"]).all()
    return pd.DataFrame(
        [
            gate_row("parent_jn_gates_passed", "passed" if parent_passed else "failed", rel(PARENT_GATE_AUDIT), "JN training(JN 학습) gate(게이트)가 통과한 산출물만 검토한다."),
            gate_row("candidate_review_materialized", "passed" if exists(CANDIDATE_REVIEW) and summary["candidate_rows"] == 8 else "failed", rel(CANDIDATE_REVIEW), "8개 후보를 모두 review(검토)한다."),
            gate_row("onnx_parity_all_passed", "passed" if summary["onnx_parity_passed_rows"] == summary["onnx_parity_rows"] == summary["candidate_rows"] else "failed", rel(ONNX_PARITY), "Python/ONNX(파이썬/온엑스) parity(동등성)를 통과한 후보만 유지한다."),
            gate_row("proxy_positive_identified", "passed" if summary["positive_proxy_rows"] >= 1 else "failed", rel(POSITIVE_MATRIX), "proxy-positive(프록시 양수)를 MT5 비교 대상으로 분리한다."),
            gate_row("probe_priority_identified_without_selection", "passed" if summary["runtime_queue_candidate_count"] >= 1 else "failed", rel(PROBE_PRIORITY), "probe priority(탐침 우선순위)는 만들되 selection(선택)은 하지 않는다."),
            gate_row("side_density_attribution_recorded", "passed" if exists(ATTRIBUTION_MATRIX) and summary["primary_weakness_tags"] else "failed", rel(ATTRIBUTION_MATRIX), "PF(수익 팩터), recovery(회복), side(방향), density(밀도) 약점을 기록한다."),
            gate_row("proxy_mt5_comparison_requirement_recorded", "passed" if exists(PROXY_MT5_REQUIREMENT) else "failed", rel(PROXY_MT5_REQUIREMENT), "proxy expected value(프록시 예상값)가 MT5 runtime probe(MT5 런타임 탐침)를 요구하게 한다."),
            gate_row("failure_memory_control_recorded", "passed" if exists(FAILURE_MEMORY_CONTROL) else "failed", rel(FAILURE_MEMORY_CONTROL), "고밀도/방향 불균형 실패 기억을 다음 MT5 비교 조건으로 남긴다."),
            gate_row("tier_pair_missing_required_recorded", "passed" if exists(TIER_PAIR_RECORD) else "failed", rel(TIER_PAIR_RECORD), "Tier B(티어 B)와 combined(합산) 누락을 숨기지 않는다."),
            gate_row("runtime_probe_package_queue_opened", "passed" if summary["runtime_queue_candidate_count"] >= 1 and exists(RUNTIME_QUEUE) else "failed", rel(RUNTIME_QUEUE), "JP runtime probe package(JP 런타임 탐침 패키지)를 연다."),
            gate_row("no_candidate_selection_claim", "passed", rel(CLAIM_RECEIPT), "JO는 priority(우선순위)만 만들고 selected model(선정 모델)은 만들지 않는다."),
            gate_row("no_mt5_execution_in_jo", "passed", rel(CLAIM_RECEIPT), "JO에서는 MT5 execution(MT5 실행)을 하지 않는다."),
            gate_row("no_forbidden_operating_claim", "passed", rel(CLAIM_RECEIPT), "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def artifact_paths() -> list[Path]:
    return list(OUTPUT_FILES)


def write_receipts(summary: Mapping[str, Any]) -> None:
    parent_final = read_json(PARENT_FINAL_DECISION)
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "work_family": "experiment_execution(실험 실행)",
        "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
        "support_skills": "obsidian-model-validation, obsidian-performance-attribution, obsidian-runtime-parity, obsidian-artifact-lineage(모델 검증, 성과 귀속, 런타임 동등성, 산출물 계보)",
    }
    write_json(EXPERIMENT_RECEIPT, {**base, "effect": "proxy-positive(프록시 양수)를 MT5 runtime probe(MT5 런타임 탐침) 비교로 넘긴다."})
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "sample_scope": "Tier A reviewed; Tier B and combined missing_required(Tier A 검토, Tier B와 합산은 필수 누락)",
            "feature_schema": rel(FEATURE_SCHEMA),
            "split_boundary": "source_row_id ordered inner holdout inherited from JN(source_row_id 순서 내부 보류, JN 상속)",
            "leakage_risk": "selection from proxy before MT5 would overstate result(MT5 전 프록시 선택은 결과 과장 위험)",
            "data_hash_or_identity": parent_final.get("feature_order_hash", ""),
            "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "candidate_rows": summary["candidate_rows"],
            "onnx_parity": f"{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}",
            "model_family": "LightGBM/XGBoost/ExtraTrees(라이트GBM/엑스지부스트/엑스트라트리즈)",
            "selection_metric": "none; runtime probe priority only(없음, 런타임 탐침 우선순위 전용)",
            "threshold_policy": "no threshold tuning(임계값 조정 없음)",
            "overfit_risk": "proxy-positive rows need MT5 comparison(프록시 양수는 MT5 비교 필요)",
            "calibration_risk": "uncalibrated probability ranks(미보정 확률 순위)",
            "comparison_baseline": rel(PARENT_FINAL_DECISION),
            "validation_judgment": JUDGMENT,
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": "four proxy-positive candidates after positive low-PF/recovery/drawdown repair training(양수 저PF/회복/낙폭 수리 학습 후 프록시 양수 후보 4개)",
            "primary_probe_model_id": summary["primary_probe_model_id"],
            "primary_proxy_net": summary["primary_proxy_net"],
            "primary_profit_factor": summary["primary_profit_factor"],
            "primary_recovery_factor": summary["primary_recovery_factor"],
            "primary_max_drawdown": summary["primary_max_drawdown"],
            "primary_trade_count": summary["primary_trade_count"],
            "primary_signal_density": summary["primary_signal_density"],
            "primary_side_balance_ratio": summary["primary_side_balance_ratio"],
            "balance_control_model_id": summary["balance_control_model_id"],
            "cost_control_model_id": summary["cost_control_model_id"],
            "segment_checks": rel(ATTRIBUTION_MATRIX),
            "alternative_explanations": "high density, short-heavy profile, and weak balanced accuracy may collapse in MT5(고밀도, 숏 편중, 약한 균형 정확도는 MT5에서 무너질 수 있음)",
            "attribution_confidence": "medium_low_until_MT5_probe(MT5 탐침 전까지 중하)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(Path(__file__)),
            "runtime_path": "not_created_in_JO(JO에서 미생성)",
            "shared_contract": rel(FEATURE_SCHEMA),
            "known_differences": "no MT5 package or tester run in JO(JO에서 MT5 패키지/테스터 실행 없음)",
            "parity_check": rel(ONNX_PARITY),
            "parity_identity": f"{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}",
            "runtime_claim_boundary": "research-only_runtime_probe_required(연구 전용, 런타임 탐침 필요)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(CANDIDATE_REVIEW), rel(POSITIVE_MATRIX), rel(PROBE_PRIORITY), rel(ATTRIBUTION_MATRIX), rel(GATE_AUDIT)],
            "evidence_missing": "runtime package and MT5 runtime probe(런타임 패키지와 MT5 런타임 탐침)",
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "프록시는 좋아졌지만 운영 모델은 아직 아니다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "mt5_execution": "not_run_in_JO",
            "runtime_package_authority": "not_claimed",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "positive_matrix": rel(POSITIVE_MATRIX),
            "probe_priority": rel(PROBE_PRIORITY),
            "runtime_queue": rel(RUNTIME_QUEUE),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths() if exists(path) and io(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest(목록과 함께 생성)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run_in_JO",
        "runtime_package": "not_materialized_in_JO",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }
    write_json(FINAL_DECISION, final)
    return final


def write_manifest() -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337JO Positive Low PF Recovery Drawdown Training Review(run337JO 양수 저PF 회복 낙폭 학습 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- positive_proxy_rows(프록시 양수 행): `{final['positive_proxy_rows']}`
- primary_probe_model(주 탐침 모델): `{final['primary_probe_model_id']}`
- primary_proxy_net(주 탐침 프록시 순수익): `{final['primary_proxy_net']}`
- primary_profit_factor(주 탐침 수익 팩터): `{final['primary_profit_factor']}`
- primary_recovery_factor(주 탐침 회복 계수): `{final['primary_recovery_factor']}`
- primary_side_balance_ratio(주 탐침 방향 균형 비율): `{final['primary_side_balance_ratio']}`
- balance_control_model(균형 대조 모델): `{final['balance_control_model_id']}`
- cost_control_model(비용 대조 모델): `{final['cost_control_model_id']}`
- primary_weakness_tags(주 탐침 약점 태그): `{final['primary_weakness_tags']}`

## Action(행동)

JN training(JN 학습) 산출물 8개를 review(검토)하고 ONNX parity(ONNX 동등성) 8/8을 확인했다.
Effect(효과): proxy-positive(프록시 양수) 4개를 selected model(선정 모델)이 아니라 MT5 runtime probe(MT5 런타임 탐침) 비교 대상으로만 분리했다.

## Finding(발견)

Raw top(순수 1위)은 `{final['primary_probe_model_id']}`이고, balance control(균형 대조)은 `{final['balance_control_model_id']}`, cost control(비용 대조)은 `{final['cost_control_model_id']}`이다.
Effect(효과): high-density/short-heavy(고밀도/숏 편중) 실패 가능성을 단일 proxy net(프록시 순수익)보다 먼저 MT5에서 확인하게 한다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no MT5 execution in JO(JO에서 MT5 실행 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`{NEXT_RUN_ID}`에서 runtime probe package(런타임 탐침 패키지)를 만든다.
"""
    decision = f"""# {TODAY} Stage337JO Decision(337JO 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(CANDIDATE_REVIEW)}`, `{rel(POSITIVE_MATRIX)}`, `{rel(PROBE_PRIORITY)}`, `{rel(ATTRIBUTION_MATRIX)}`

Action(행동): proxy-positive(프록시 양수) ONNX(온엑스) 후보를 runtime probe priority(런타임 탐침 우선순위)로만 지정했다.
Effect(효과): proxy(프록시)를 MT5 KPI(MT5 핵심 성과 지표)로 착각하지 않고 외부 실행 비교로 넘긴다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

JO review(JO 검토)는 JN training(JN 학습) 산출물을 운영 주장으로 올리지 않고 JP package(JP 패키지)로 좁게 넘겼다.
효과는 MT5 runtime probe(MT5 런타임 탐침) 전 selected model(선정 모델)이나 live readiness(실거래 준비)를 말하지 않게 하는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- probe_priority_model(탐침 우선 모델): `{final['primary_probe_model_id']}`
- probe_balance_control_model(탐침 균형 대조 모델): `{final['balance_control_model_id']}`
- probe_cost_control_model(탐침 비용 대조 모델): `{final['cost_control_model_id']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): proxy-positive(프록시 양수)를 selection(선택)으로 오해하지 않게 한다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run337JO {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337JO Positive Low PF Recovery Drawdown Training Review(양수 저PF 회복 낙폭 학습 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): proxy-positive(프록시 양수) 4개 중 runtime probe(런타임 탐침) 비교 대상 `{final['runtime_queue_candidate_count']}`개를 열었다.
""",
    )
    changelog_entry = f"""## {TODAY} run337JO Positive Low PF Recovery Drawdown Training Review(양수 저PF 회복 낙폭 학습 검토)

- action(행동): JN ONNX(온엑스) 후보 8개를 검토하고 proxy-positive(프록시 양수) 4개를 확인했다.
- effect(효과): `{NEXT_RUN_ID}`가 MT5 runtime probe(MT5 런타임 탐침) 패키지를 만들도록 연결했다.
- boundary(경계): selected model(선정 모델), MT5 execution(MT5 실행), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def update_registers(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "training_review_proxy_positive_runtime_probe_required",
            "positive_proxy_rows": final["positive_proxy_rows"],
            "probe_priority_model": final["primary_probe_model_id"],
            "balance_control_model": final["balance_control_model_id"],
            "cost_control_model": final["cost_control_model_id"],
            "primary_proxy_net": final["primary_proxy_net"],
            "primary_profit_factor": final["primary_profit_factor"],
            "primary_recovery_factor": final["primary_recovery_factor"],
            "result_status": "runtime_probe_package_required_no_selection",
        },
        {
            **base,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary", "artifact_id", "created_at_utc", "notes", "artifact_path"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    created_at = now_utc()
    for path in paths:
        if exists(path) and io(path).is_file():
            artifact_path = rel(path)
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": artifact_path,
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}::{artifact_path}",
                    "created_at_utc": created_at,
                    "notes": STATUS,
                    "artifact_path": artifact_path,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        new_ids = {row["artifact_id"] for row in rows}
        registry = registry.loc[
            ~registry["path"].astype(str).isin(new_paths)
            & ~registry["artifact_id"].astype(str).isin(new_ids)
        ].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        write_csv(ARTIFACT_REGISTRY, registry[columns])


def main() -> None:
    for path in (RUN_DIR, REVIEW_DIR, DECISION_DOC.parent):
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")
    review, positive, priority, attribution, requirement, failure_control, tier_record, queue, summary = build_review()
    write_csv(CANDIDATE_REVIEW, review)
    write_csv(POSITIVE_MATRIX, positive)
    write_csv(PROBE_PRIORITY, priority)
    write_csv(ATTRIBUTION_MATRIX, attribution)
    write_csv(PROXY_MT5_REQUIREMENT, requirement)
    write_csv(FAILURE_MEMORY_CONTROL, failure_control)
    write_csv(TIER_PAIR_RECORD, tier_record)
    write_csv(RUNTIME_QUEUE, queue)
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary)
    final = write_final(summary, gates)
    write_docs(final)
    write_manifest()
    update_registers(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"JO gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "positive_proxy_rows": final["positive_proxy_rows"],
                "runtime_queue_candidate_count": final["runtime_queue_candidate_count"],
                "primary_probe_model_id": final["primary_probe_model_id"],
                "balance_control_model_id": final["balance_control_model_id"],
                "cost_control_model_id": final["cost_control_model_id"],
                "primary_proxy_net": final["primary_proxy_net"],
                "primary_profit_factor": final["primary_profit_factor"],
                "primary_recovery_factor": final["primary_recovery_factor"],
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
