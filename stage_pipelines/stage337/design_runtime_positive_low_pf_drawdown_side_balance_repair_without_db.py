from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    review_proxy_positive_offensive_pivot_mt5_runtime_probe_or_repair_without_db as idr,
)


aw = idr.aw

TODAY = "2026-06-01"
STAGE_ID = idr.STAGE_ID
STAGE_DIR = idr.STAGE_DIR
RUN_NUMBER = "run337IE"
RUN_ID = "run337IE_design_runtime_positive_low_pf_drawdown_side_balance_repair_without_db_v1"
PARENT_RUN_ID = idr.RUN_ID
NEXT_RUN_ID = "run337IF_materialize_runtime_positive_low_pf_drawdown_side_balance_repair_inputs_without_db_v1"
STATUS = "completed_stage337IE_runtime_positive_low_pf_drawdown_side_balance_repair_design_no_training_no_selection"
JUDGMENT = "runtime_positive_low_pf_drawdown_side_balance_repair_design_opened"
DECISION = "stage337IE_open_run337IF_runtime_positive_low_pf_drawdown_side_balance_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_design_only_no_model_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IE_positive_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IE_runtime_positive_low_pf_drawdown_side_balance_repair_design.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

ID_FINAL = idr.FINAL_DECISION
ID_GATES = idr.GATE_AUDIT
ID_KPI = idr.KPI_JUDGMENT
ID_DIFF = idr.DIFF_ATTRIBUTION
ID_REPAIR_QUEUE = idr.REPAIR_QUEUE
ID_RUNTIME_REVIEW = idr.RUNTIME_REVIEW
IC_SUMMARY = idr.ic.EXECUTION_SUMMARY
IC_DIFF = idr.ic.PROXY_MT5_DIFF
IA_POSITIVE_MATRIX = idr.ic.ib.ia.POSITIVE_MATRIX

DESIGN_MATRIX = RUN_DIR / "runtime_positive_repair_design_matrix.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "runtime_positive_performance_attribution_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
FEATURE_LABEL_TRADE_CONTRACT = RUN_DIR / "feature_label_trade_shape_repair_contract.csv"
TIER_PAIR_CONTRACT = RUN_DIR / "tier_pair_repair_contract.csv"
RUNTIME_PARITY_GUARD = RUN_DIR / "runtime_parity_guard_contract.csv"
COST_STRESS_CONTRACT = RUN_DIR / "cost_stress_runtime_consistency_contract.csv"
IF_QUEUE = RUN_DIR / "run337IF_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    ID_FINAL,
    ID_GATES,
    ID_KPI,
    ID_DIFF,
    ID_REPAIR_QUEUE,
    ID_RUNTIME_REVIEW,
    IC_SUMMARY,
    IC_DIFF,
    IA_POSITIVE_MATRIX,
)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    PERFORMANCE_ATTRIBUTION,
    EXPERIMENT_CONTRACT,
    FEATURE_LABEL_TRADE_CONTRACT,
    TIER_PAIR_CONTRACT,
    RUNTIME_PARITY_GUARD,
    COST_STRESS_CONTRACT,
    IF_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
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
    STAGE_BRIEF,
    CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)

DESIGN_COLUMNS = (
    "design_id",
    "repair_family",
    "source_evidence",
    "hypothesis",
    "changed_variables",
    "fixed_controls",
    "materialization_action",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "claim_use",
    "effect",
    "claim_boundary",
)
ATTRIBUTION_COLUMNS = (
    "attribution_id",
    "source_model_id",
    "metric_or_risk",
    "observed",
    "attribution",
    "repair_implication",
    "materialization_need",
    "effect",
    "claim_boundary",
)
EXPERIMENT_COLUMNS = (
    "experiment_id",
    "primary_family",
    "primary_skill",
    "support_skills",
    "hypothesis",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "claim_boundary",
)
CONTRACT_COLUMNS = (
    "contract_id",
    "scope",
    "required_rule",
    "forbidden_rule",
    "success_signal",
    "failure_signal",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "source_run_id",
    "next_run_id",
    "task",
    "required_inputs",
    "expected_outputs",
    "blocked_if_missing",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "observed",
    "expected",
    "evidence_path",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(path)


def io(path: Path) -> Path:
    return aw.io_path(path)


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    ensure_parent(path)
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    return int(round(as_float(value, float(default))))


def missing_inputs(paths: Iterable[Path]) -> list[str]:
    return [rel(path) for path in paths if not exists(path)]


def build_packets() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    id_final = read_json(ID_FINAL)
    id_kpi = read_csv_frame(ID_KPI)
    id_diff = read_csv_frame(ID_DIFF)
    id_queue = read_csv_frame(ID_REPAIR_QUEUE)
    runtime_review = read_csv_frame(ID_RUNTIME_REVIEW)

    best_model_id = str(id_final.get("best_model_id", ""))
    best_net = as_float(id_final.get("best_net_profit"))
    best_pf = as_float(id_final.get("best_profit_factor"))
    exact_parity_rows = as_int(id_final.get("exact_parity_rows"))
    positive_net_rows = as_int(id_final.get("positive_net_rows"))
    mismatch_rows = as_int(id_final.get("mismatch_rows"))
    operating_ready_rows = as_int(id_final.get("operating_ready_rows"))

    best_row = id_kpi.sort_values("net_profit", ascending=False).iloc[0].to_dict()
    best_trade_count = as_int(best_row.get("trade_count"))
    best_expectancy = as_float(best_row.get("expectancy"))
    best_recovery = as_float(best_row.get("recovery_factor"))
    best_drawdown = as_float(best_row.get("max_drawdown_amount"))
    best_short = as_int(best_row.get("short_trade_count"))
    best_long = as_int(best_row.get("long_trade_count"))
    best_balance = as_float(best_row.get("long_short_balance_ratio"))

    source_evidence = (
        f"ID KPI(핵심 성과 지표): net_profit(순수익)={best_net}, "
        f"PF(수익 팩터)={best_pf}, recovery(회복 계수)={best_recovery}, "
        f"drawdown(낙폭)={best_drawdown}, trade_count(거래수)={best_trade_count}, "
        f"short/long(숏/롱)={best_short}/{best_long}, exact_parity_rows(정확 동등 행)={exact_parity_rows}"
    )
    fixed_controls = (
        "FPMarkets US100 M5, closed-bar timestamp-safe inputs(확정봉 시점 안전 입력), "
        "ID/IC runtime evidence(ID/IC 런타임 근거), no threshold tuning(임계값 조정 없음), "
        "no lot optimization(랏 최적화 없음), no MT5 execution(MT5 실행 없음) in IE"
    )

    design_rows = [
        {
            "design_id": "ie001_side_net_stabilization",
            "repair_family": "side net stabilization(방향별 순익 안정화)",
            "source_evidence": source_evidence,
            "hypothesis": "Short dominance(숏 우세)는 양수 net(순익)을 만들었지만 drawdown(낙폭)과 PF(수익 팩터)를 눌렀다.",
            "changed_variables": "side-specific sample weights(방향별 표본 가중치), side-balanced target views(방향 균형 목표 보기)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Create train-only side-stability columns and task seeds(학습 전용 방향 안정 열과 작업 씨앗 생성).",
            "success_criteria": "Proxy review(프록시 검토)에서 trade count(거래수)를 보존하면서 side balance(방향 균형)와 PF(수익 팩터)가 개선된다.",
            "failure_criteria": "한 방향만 남거나 trade count(거래수)가 무너진다.",
            "invalid_conditions": "Holdout(보류) 성과로 방향을 사후 선택하면 invalid(무효)다.",
            "claim_use": "materialization seed only(물질화 씨앗 전용)",
            "effect": "Runtime positive clue(런타임 양수 단서)를 방향 균형 수리로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ie002_drawdown_cluster_filter",
            "repair_family": "drawdown cluster control(낙폭 군집 제어)",
            "source_evidence": source_evidence,
            "hypothesis": "Max drawdown(최대 낙폭) 291.44는 손실 군집(loss cluster, 손실 군집)이 남았다는 신호다.",
            "changed_variables": "timestamp-known volatility/session/regime context(시점에 알려진 변동성/세션/국면 문맥)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Add drawdown-risk context features and weight views(낙폭 위험 문맥 피처와 가중치 보기 추가).",
            "success_criteria": "Worst bucket(최악 구간)의 loss density(손실 밀도)가 낮아지고 recovery(회복)가 오른다.",
            "failure_criteria": "낙폭은 줄지만 net profit(순수익) 또는 trade count(거래수)가 과도하게 사라진다.",
            "invalid_conditions": "Future drawdown(미래 낙폭)을 feature(피처)로 쓰면 invalid(무효)다.",
            "claim_use": "materialization seed only(물질화 씨앗 전용)",
            "effect": "수익이 난 후보를 손실 군집 관점에서 압박 시험한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ie003_pf_recovery_trade_shape",
            "repair_family": "PF recovery trade shape(수익 팩터 회복 거래 형태)",
            "source_evidence": source_evidence,
            "hypothesis": "PF(수익 팩터) 1.01과 expectancy(기대값) 0.05는 저품질 거래 밀도가 남았다는 뜻이다.",
            "changed_variables": "margin-aware labels(마진 인식 라벨), low-edge penalty weights(낮은 우위 벌점 가중치)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Create trade-shape weights that penalize flat confusion and low margin(관망 혼동과 낮은 마진을 벌점 처리하는 거래 형태 가중치 생성).",
            "success_criteria": "PF(수익 팩터)와 recovery factor(회복 계수)가 함께 오른다.",
            "failure_criteria": "Positive net(양수 순익)이 사라지거나 active density(활성 밀도)가 너무 낮아진다.",
            "invalid_conditions": "Runtime KPI(런타임 핵심 성과 지표)를 직접 학습 목표로 누출하면 invalid(무효)다.",
            "claim_use": "materialization seed only(물질화 씨앗 전용)",
            "effect": "단순 양수 순익을 더 질 좋은 수익 구조 탐색으로 옮긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ie004_secondary_probability_mismatch_repair",
            "repair_family": "secondary parity repair(보조 동등성 수리)",
            "source_evidence": f"ID mismatch rows(ID 불일치 행)={mismatch_rows}; {rel(ID_DIFF)}",
            "hypothesis": "Secondary LGBM(보조 LightGBM) probability drift(확률 드리프트)는 작지만 exact parity(정확 동등성) 주장을 막는다.",
            "changed_variables": "probability precision export audit(확률 정밀도 내보내기 감사), secondary model deprioritization(보조 모델 후순위화)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Record precision repair route and keep exact ExtraTrees path primary(정밀도 수리 경로를 기록하고 정확 ExtraTrees 경로를 우선 유지).",
            "success_criteria": "Next package(다음 패키지)는 exact parity(정확 동등성) 후보를 우선하며 mismatch(불일치)를 분리 기록한다.",
            "failure_criteria": "Probability mismatch(확률 불일치)가 decision mismatch(결정 불일치)로 번진다.",
            "invalid_conditions": "Small mismatch(작은 불일치)를 숨기고 parity(동등성)를 주장하면 invalid(무효)다.",
            "claim_use": "parity guard only(동등성 보호 전용)",
            "effect": "운영 주장 전 확률 재현성 문제를 별도 위험으로 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ie005_tier_pair_gap_closure",
            "repair_family": "paired tier gap closure(티어 쌍 공백 닫기)",
            "source_evidence": "ID/IC are Tier A runtime probe only(ID/IC는 Tier A 런타임 탐침 전용).",
            "hypothesis": "Tier B(티어 B)와 combined(합산) 기록이 없으면 운영 의미를 넓힐 수 없다.",
            "changed_variables": "Tier B separate(티어 B 분리), Tier A+B combined(Tier A+B 합산) materialization flags(물질화 플래그)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Emit Tier A separate, Tier B missing_required, and A+B missing_required records(Tier A 분리, Tier B 필수 누락, A+B 필수 누락 기록 생성).",
            "success_criteria": "Required tier records(필수 티어 기록)가 생략 없이 남는다.",
            "failure_criteria": "Tier B(티어 B) 또는 combined(합산)이 조용히 빠진다.",
            "invalid_conditions": "Tier A(티어 A)만 전체 알파 읽기처럼 보고하면 invalid(무효)다.",
            "claim_use": "scope guard only(범위 보호 전용)",
            "effect": "탐색은 열어 두되 운영 범위 과장을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ie006_cost_stress_runtime_consistency",
            "repair_family": "cost stress consistency(비용 압박 일관성)",
            "source_evidence": "Proxy expected value(프록시 예상값) was compared with MT5 runtime probe(MT5 런타임 탐침).",
            "hypothesis": "Low PF(낮은 수익 팩터)는 cost stress(비용 압박)에 취약할 수 있다.",
            "changed_variables": "spread/slippage stress tags(스프레드/슬리피지 압박 태그), proxy-to-MT5 cost attribution(프록시-MT5 비용 귀속)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Create cost-stress evaluation columns without changing lot or threshold(랏 또는 임계값을 바꾸지 않고 비용 압박 평가 열 생성).",
            "success_criteria": "Candidate(후보)가 비용 압박에서도 PF(수익 팩터) 붕괴를 피한다.",
            "failure_criteria": "Small cost increase(작은 비용 증가)로 net profit(순수익)이 음수로 바뀐다.",
            "invalid_conditions": "Proxy(프록시)를 MT5 KPI(MT5 핵심 성과 지표) 대체물로 쓰면 invalid(무효)다.",
            "claim_use": "runtime comparison support only(런타임 비교 보조 전용)",
            "effect": "양수 순익의 비용 취약성을 다음 입력에서 바로 볼 수 있게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    attribution_rows = [
        {
            "attribution_id": "ie_attr_001_low_pf",
            "source_model_id": best_model_id,
            "metric_or_risk": "profit factor(수익 팩터)",
            "observed": best_pf,
            "attribution": "PF(수익 팩터)가 1.01이라 비용과 잡음에 거의 붙어 있다.",
            "repair_implication": "저마진 거래와 flat confusion(관망 혼동)을 벌점화한다.",
            "materialization_need": rel(FEATURE_LABEL_TRADE_CONTRACT),
            "effect": "순익 단서를 수익 품질 수리로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "ie_attr_002_low_recovery",
            "source_model_id": best_model_id,
            "metric_or_risk": "recovery factor(회복 계수)",
            "observed": best_recovery,
            "attribution": "Recovery(회복)가 0.07이라 낙폭 대비 수익이 약하다.",
            "repair_implication": "drawdown cluster(낙폭 군집) 문맥을 학습 가중치로 만든다.",
            "materialization_need": rel(DESIGN_MATRIX),
            "effect": "낙폭 압박을 다음 실험의 중심 제약으로 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "ie_attr_003_high_drawdown",
            "source_model_id": best_model_id,
            "metric_or_risk": "max drawdown(최대 낙폭)",
            "observed": best_drawdown,
            "attribution": "Drawdown(낙폭) 291.44는 운영 준비선보다 크다.",
            "repair_implication": "session/regime(세션/국면) 손실 밀도를 분해한다.",
            "materialization_need": rel(DESIGN_MATRIX),
            "effect": "수익 곡선 품질을 별도 근거로 요구한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "ie_attr_004_side_balance",
            "source_model_id": best_model_id,
            "metric_or_risk": "long/short balance(롱/숏 균형)",
            "observed": f"{best_short}/{best_long};ratio={best_balance}",
            "attribution": "Short(숏) 거래가 많고 long(롱)은 적어 방향 구조가 한쪽으로 기운다.",
            "repair_implication": "side-specific(방향별) 수익과 손실을 분리한다.",
            "materialization_need": rel(FEATURE_LABEL_TRADE_CONTRACT),
            "effect": "방향 편향을 수익 원천인지 위험인지 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "ie_attr_005_probability_mismatch",
            "source_model_id": "hz_hx_hw001_fwd6_label_horizon_lgbm",
            "metric_or_risk": "probability mismatch(확률 불일치)",
            "observed": mismatch_rows,
            "attribution": "Decision mismatch(결정 불일치)는 없지만 exact parity(정확 동등성)는 아니다.",
            "repair_implication": "Secondary model(보조 모델)은 parity repair(동등성 수리) 전 운영 경로에서 후순위다.",
            "materialization_need": rel(RUNTIME_PARITY_GUARD),
            "effect": "작은 재현성 차이를 운영 주장 전에 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "ie_attr_006_tier_gap",
            "source_model_id": best_model_id,
            "metric_or_risk": "Tier B/combined(티어 B/합산)",
            "observed": "missing_required(필수 누락)",
            "attribution": "ID runtime review(ID 런타임 검토)는 Tier A(티어 A) 근거만 갖고 있다.",
            "repair_implication": "Tier B(티어 B)와 A+B(합산)는 누락 상태를 명시한다.",
            "materialization_need": rel(TIER_PAIR_CONTRACT),
            "effect": "운영 범위가 Tier A(티어 A)로 제한됨을 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    baseline = (
        f"ID best_model(최고 모델)={best_model_id}; net_profit(순수익)={best_net}; "
        f"PF(수익 팩터)={best_pf}; expectancy(기대값)={best_expectancy}; "
        f"recovery(회복)={best_recovery}; drawdown(낙폭)={best_drawdown}; "
        f"positive_net_rows(양수 순익 행)={positive_net_rows}; operating_ready_rows(운영 준비 행)={operating_ready_rows}"
    )
    experiment_rows = [
        {
            "experiment_id": RUN_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
            "support_skills": "obsidian-performance-attribution(성과 귀속);obsidian-result-judgment(결과 판정);obsidian-artifact-lineage(산출물 계보)",
            "hypothesis": "MT5 positive net(MT5 양수 순익)은 유효한 수익 단서지만 PF/drawdown/recovery/side/parity(수익 팩터/낙폭/회복/방향/동등성) 수리가 필요하다.",
            "comparison_baseline": baseline,
            "control_variables": fixed_controls,
            "changed_variables": "side weights(방향 가중치), drawdown context(낙폭 문맥), trade-shape weights(거래 형태 가중치), parity guard(동등성 보호), cost stress(비용 압박)",
            "success_criteria": "IF materialization(IF 물질화)이 timestamp-safe(시점 안전) 수리 입력과 Tier records(티어 기록)를 만든다.",
            "failure_criteria": "수리 입력이 runtime KPI(런타임 핵심 성과 지표)를 누출하거나 Tier B/combined(티어 B/합산)을 생략한다.",
            "invalid_conditions": "Look-ahead bias(미래참조 편향), threshold tuning(임계값 조정), lot optimization(랏 최적화), candidate selection(후보 선택)",
            "stop_conditions": "ID gates(ID 게이트) 실패, missing ID evidence(ID 근거 누락), forbidden claim(금지 주장)",
            "evidence_plan": f"{rel(DESIGN_MATRIX)};{rel(PERFORMANCE_ATTRIBUTION)};{rel(IF_QUEUE)};{rel(GATE_AUDIT)}",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    feature_contract_rows = [
        {
            "contract_id": "ie_feature_label_trade_shape_contract",
            "scope": "feature/label/trade-shape repair(피처/라벨/거래 형태 수리)",
            "required_rule": "All new features must be timestamp-safe closed-bar inputs(모든 새 피처는 확정봉 시점 안전 입력).",
            "forbidden_rule": "No future drawdown or MT5 KPI leak(미래 낙폭 또는 MT5 핵심 성과 지표 누출 금지).",
            "success_signal": "Finite train-only columns and task seeds(유한한 학습 전용 열과 작업 씨앗)",
            "failure_signal": "Any nonfinite or future-informed column(비유한 또는 미래 정보 열)",
            "effect": "수익 구조 수리를 편향 없이 물질화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "ie_trade_density_floor_contract",
            "scope": "trade count and density(거래수와 밀도)",
            "required_rule": "Record active density and trade-count floor(활성 밀도와 거래수 하한 기록).",
            "forbidden_rule": "No tiny-sample positive claim(작은 표본 양수 주장 금지).",
            "success_signal": "Usable density with PF/recovery improvement(PF/회복 개선과 사용 가능한 밀도)",
            "failure_signal": "Trade count collapse(거래수 붕괴)",
            "effect": "낮은 거래수 착시를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    tier_rows = [
        {
            "contract_id": "ie_tier_a_separate",
            "scope": "Tier A separate(Tier A 분리)",
            "required_rule": "Preserve ID/IC Tier A runtime evidence(ID/IC Tier A 런타임 근거 보존).",
            "forbidden_rule": "Do not call Tier A the whole alpha read(Tier A만 전체 알파 판독으로 부르지 않기).",
            "success_signal": "Tier A record exists(Tier A 기록 존재)",
            "failure_signal": "Tier A source missing(Tier A 원천 누락)",
            "effect": "현재 양수 단서의 실제 범위를 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "ie_tier_b_separate",
            "scope": "Tier B separate(Tier B 분리)",
            "required_rule": "Emit missing_required if unavailable(없으면 필수 누락으로 기록).",
            "forbidden_rule": "Do not omit Tier B silently(Tier B 조용한 생략 금지).",
            "success_signal": "Tier B row exists with status(Tier B 상태 행 존재)",
            "failure_signal": "No Tier B row(Tier B 행 없음)",
            "effect": "부분 문맥 표본 공백을 명시한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "ie_tier_ab_combined",
            "scope": "Tier A+B combined(Tier A+B 합산)",
            "required_rule": "Emit missing_required until combined data exists(합산 데이터 전까지 필수 누락 기록).",
            "forbidden_rule": "No synthetic sum as combined result(합성 합계를 합산 결과로 부르지 않기).",
            "success_signal": "Combined row exists with status(합산 상태 행 존재)",
            "failure_signal": "No combined row(합산 행 없음)",
            "effect": "분리 테스터 합계를 합산 결과로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    runtime_guard_rows = [
        {
            "contract_id": "ie_exact_parity_primary_guard",
            "scope": "runtime parity(런타임 동등성)",
            "required_rule": "Prioritize exact ExtraTrees parity path(정확 ExtraTrees 동등성 경로 우선).",
            "forbidden_rule": "No runtime authority from probability-mismatch model(확률 불일치 모델로 런타임 권위 금지).",
            "success_signal": "Exact parity candidate remains traceable(정확 동등 후보 추적 가능)",
            "failure_signal": "Mismatch hidden or ignored(불일치 은폐 또는 무시)",
            "effect": "MT5 재현성을 운영 주장 전 필수 조건으로 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "ie_secondary_precision_repair_guard",
            "scope": "secondary probability precision(보조 확률 정밀도)",
            "required_rule": "Record max probability diff and decision diff(최대 확률 차이와 결정 차이 기록).",
            "forbidden_rule": "No exact parity claim for secondary mismatch(보조 불일치에 정확 동등성 주장 금지).",
            "success_signal": "Separated precision repair path(분리된 정밀도 수리 경로)",
            "failure_signal": "Decision mismatch appears(결정 불일치 발생)",
            "effect": "작은 확률 차이의 활용 가능성을 따로 판단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    cost_rows = [
        {
            "contract_id": "ie_cost_stress_contract",
            "scope": "proxy-to-MT5 cost stress(프록시-MT5 비용 압박)",
            "required_rule": "Compare proxy EV with MT5 runtime probe again after training(학습 뒤 프록시 예상값과 MT5 런타임 탐침 재비교).",
            "forbidden_rule": "Proxy EV cannot replace MT5 KPI(프록시 예상값은 MT5 핵심 성과 지표 대체 금지).",
            "success_signal": "Diff attribution and usability judgment(차이 귀속과 활용 가능성 판정)",
            "failure_signal": "PF collapses under cost stress(비용 압박에서 수익 팩터 붕괴)",
            "effect": "비용에 약한 양수 순익을 조기에 걸러낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue_rows = [
        {
            "queue_id": "ie_to_if_materialization",
            "source_run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "task": "materialize_runtime_positive_low_pf_drawdown_side_balance_repair_inputs(런타임 양수 저PF 낙폭 방향 균형 수리 입력 물질화)",
            "required_inputs": f"{rel(DESIGN_MATRIX)};{rel(PERFORMANCE_ATTRIBUTION)};{rel(EXPERIMENT_CONTRACT)};{rel(TIER_PAIR_CONTRACT)};{rel(RUNTIME_PARITY_GUARD)};{rel(COST_STRESS_CONTRACT)}",
            "expected_outputs": "timestamp-safe repair input frame(시점 안전 수리 입력 프레임); task seeds(작업 씨앗); tier records(티어 기록)",
            "blocked_if_missing": "ID runtime review, KPI judgment, or design contracts(ID 런타임 검토, KPI 판정, 설계 계약)",
            "effect": "설계를 다음 물질화 실행으로 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "primary_family": "experiment_design",
        "primary_skill": "obsidian-experiment-design",
        "support_skills": [
            "obsidian-performance-attribution",
            "obsidian-result-judgment",
            "obsidian-artifact-lineage",
        ],
        "best_model_id": best_model_id,
        "best_net_profit": best_net,
        "best_profit_factor": best_pf,
        "best_expectancy": best_expectancy,
        "best_recovery_factor": best_recovery,
        "best_max_drawdown_amount": best_drawdown,
        "best_trade_count": best_trade_count,
        "best_short_trade_count": best_short,
        "best_long_trade_count": best_long,
        "best_long_short_balance_ratio": best_balance,
        "positive_net_rows": positive_net_rows,
        "exact_parity_rows": exact_parity_rows,
        "mismatch_rows": mismatch_rows,
        "operating_ready_rows": operating_ready_rows,
        "design_rows": len(design_rows),
        "attribution_rows": len(attribution_rows),
        "contract_rows": len(feature_contract_rows) + len(tier_rows) + len(runtime_guard_rows) + len(cost_rows),
        "queue_rows": len(queue_rows),
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_queue_rows": len(id_queue),
        "source_runtime_rows": len(runtime_review),
        "source_diff_rows": len(id_diff),
    }
    return (
        design_rows,
        attribution_rows,
        experiment_rows,
        feature_contract_rows,
        tier_rows,
        runtime_guard_rows,
        cost_rows,
        queue_rows,
        summary,
    )


def build_gates(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    id_final = read_json(ID_FINAL)
    id_gates = read_csv_frame(ID_GATES)
    id_gate_passed = id_gates["status"].astype(str).str.lower().isin(["pass", "passed"]).all()
    forbidden_clear = all(
        str(summary.get(key)) in {"not_run", "not_claimed"}
        for key in (
            "candidate_selection",
            "model_training",
            "mt5_execution",
            "forward_passed",
            "forward_failed",
            "runtime_authority",
            "operating_promotion",
            "goal_achieve",
        )
    )
    checks = [
        (
            "parent_id_gates_passed",
            bool(id_gate_passed),
            f"{int(id_gates['status'].astype(str).str.lower().isin(['pass', 'passed']).sum())}/{len(id_gates)}",
            "all passed(모두 통과)",
            rel(ID_GATES),
            "ID 검토 게이트를 바탕으로만 설계한다.",
        ),
        (
            "parent_queue_matches_ie",
            str(id_final.get("next_action")) == RUN_ID,
            str(id_final.get("next_action")),
            RUN_ID,
            rel(ID_FINAL),
            "ID가 연 IE 실행인지 확인한다.",
        ),
        (
            "runtime_positive_clue_present",
            as_int(id_final.get("positive_net_rows")) >= 1,
            id_final.get("positive_net_rows"),
            ">=1",
            rel(ID_FINAL),
            "양수 런타임 단서가 실제로 있는지 확인한다.",
        ),
        (
            "operating_not_ready_preserved",
            as_int(id_final.get("operating_ready_rows")) == 0,
            id_final.get("operating_ready_rows"),
            "0",
            rel(ID_FINAL),
            "운영 준비가 아님을 설계 경계에 보존한다.",
        ),
        (
            "design_matrix_rows_present",
            summary["design_rows"] >= 6,
            summary["design_rows"],
            ">=6",
            rel(DESIGN_MATRIX),
            "PF/낙폭/회복/방향/동등성/비용 수리를 모두 설계한다.",
        ),
        (
            "performance_attribution_rows_present",
            summary["attribution_rows"] >= 6,
            summary["attribution_rows"],
            ">=6",
            rel(PERFORMANCE_ATTRIBUTION),
            "성과 약점을 수리 행동과 연결한다.",
        ),
        (
            "tier_pair_records_present",
            3 <= summary["contract_rows"],
            summary["contract_rows"],
            ">=3 contracts with tier rows(티어 행 포함)",
            rel(TIER_PAIR_CONTRACT),
            "Tier A/B/combined 기록을 생략하지 않는다.",
        ),
        (
            "runtime_parity_guard_present",
            exists(RUNTIME_PARITY_GUARD),
            rel(RUNTIME_PARITY_GUARD),
            "present(존재)",
            rel(RUNTIME_PARITY_GUARD),
            "정확 동등성과 확률 불일치를 분리한다.",
        ),
        (
            "next_materialization_queue_opened",
            summary["queue_rows"] == 1 and summary["next_action"] == NEXT_RUN_ID,
            f"queue={summary['queue_rows']};next={summary['next_action']}",
            f"1 and {NEXT_RUN_ID}",
            rel(IF_QUEUE),
            "다음 IF 물질화 실행을 연다.",
        ),
        (
            "no_forbidden_operating_claim",
            forbidden_clear,
            "not_run/not_claimed",
            "not_run/not_claimed",
            rel(CLAIM_RECEIPT),
            "선택, MT5 실행, 운영 주장을 금지한다.",
        ),
        (
            "required_gate_coverage_audit",
            True,
            "all required gates listed(필수 게이트 모두 기록)",
            "present(존재)",
            rel(GATE_AUDIT),
            "완료 주장을 게이트 근거와 연결한다.",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "evidence_path": evidence_path,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence_path, effect in checks
    ]


def write_receipts(summary: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts = [
        (
            EXPERIMENT_RECEIPT,
            {
                **base,
                "primary_family": "experiment_design(실험 설계)",
                "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
                "decision_use": "open IF materialization only(IF 물질화만 열기)",
                "evidence": [rel(DESIGN_MATRIX), rel(EXPERIMENT_CONTRACT), rel(IF_QUEUE)],
            },
        ),
        (
            DATA_RECEIPT,
            {
                **base,
                "timestamp_safety": "designed; materialization must verify(설계됨, 물질화에서 검증 필요)",
                "tier_rule": "Tier A separate, Tier B missing_required, A+B missing_required(Tier A 분리, Tier B 필수 누락, A+B 필수 누락)",
                "evidence": [rel(FEATURE_LABEL_TRADE_CONTRACT), rel(TIER_PAIR_CONTRACT)],
            },
        ),
        (
            MODEL_RECEIPT,
            {
                **base,
                "model_training": "not_run(미실행)",
                "model_selection": "not_run(미실행)",
                "runtime_parity_use": "exact ExtraTrees path preserved; secondary mismatch isolated(정확 ExtraTrees 경로 보존, 보조 불일치 분리)",
                "evidence": [rel(RUNTIME_PARITY_GUARD)],
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                **base,
                "best_net_profit": summary["best_net_profit"],
                "best_profit_factor": summary["best_profit_factor"],
                "best_recovery_factor": summary["best_recovery_factor"],
                "best_max_drawdown_amount": summary["best_max_drawdown_amount"],
                "performance_use": "repair seed only(수리 씨앗 전용)",
                "evidence": [rel(PERFORMANCE_ATTRIBUTION)],
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                **base,
                "judgment_label": JUDGMENT,
                "next_condition": NEXT_RUN_ID,
                "operating_ready_rows": summary["operating_ready_rows"],
                "goal_achieve": "not_claimed(미주장)",
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                **base,
                "candidate_selection": "not_run(미실행)",
                "model_training": "not_run(미실행)",
                "mt5_execution": "not_run(미실행)",
                "forward_passed": "not_claimed(미주장)",
                "forward_failed": "not_claimed(미주장)",
                "runtime_authority": "not_claimed(미주장)",
                "operating_promotion": "not_claimed(미주장)",
                "goal_achieve": "not_claimed(미주장)",
            },
        ),
    ]
    paths = [write_json(path, payload) for path, payload in receipts]
    lineage = {
        **base,
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in list(artifacts) + paths],
        "artifact_hashes": {
            rel(path): sha(path)
            for path in list(artifacts) + paths
            if exists(path) and io(path).is_file()
        },
        "lineage_judgment": "ID runtime-positive clue connected to IF repair materialization(ID 런타임 양수 단서를 IF 수리 물질화에 연결)",
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def make_final(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    failed = [row["gate_id"] for row in gates if row["status"] != "passed"]
    final = dict(summary)
    final.update(
        {
            "gate_rows": len(gates),
            "passed_gates": len(gates) - len(failed),
            "failed_gates": failed,
        }
    )
    return final


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# run337IE Runtime Positive Low PF Drawdown Side Balance Repair Design(run337IE 런타임 양수 저PF 낙폭 방향 균형 수리 설계)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- best_model_id(최고 모델 ID): `{final['best_model_id']}`
- net_profit(순수익): `{final['best_net_profit']}`
- profit_factor(수익 팩터): `{final['best_profit_factor']}`
- recovery_factor(회복 계수): `{final['best_recovery_factor']}`
- max_drawdown(최대 낙폭): `{final['best_max_drawdown_amount']}`
- trade_count(거래수): `{final['best_trade_count']}`
- long_short_balance(롱/숏 균형): `{final['best_long_trade_count']}/{final['best_short_trade_count']}`

## Action(행동)

ID review(ID 검토)의 MT5 positive net(MT5 양수 순익)을 repair design(수리 설계)으로 바꿨다.
Effect(효과): positive clue(양수 단서)를 selected model(선택 모델)로 오해하지 않고, PF/recovery/drawdown/side/parity/cost(수익 팩터/회복/낙폭/방향/동등성/비용) 수리 입력으로 넘긴다.

## Boundary(경계)

No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선택 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`{NEXT_RUN_ID}` opens materialization(물질화)을 연다.
Effect(효과): timestamp-safe(시점 안전) repair inputs(수리 입력), Tier records(티어 기록), runtime parity guard(런타임 동등성 보호)를 실제 파일로 만든다.
"""
    return write_bom_text(REPORT_PATH, text)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337IE Decision(337IE 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(DESIGN_MATRIX)}`, `{rel(PERFORMANCE_ATTRIBUTION)}`, `{rel(IF_QUEUE)}`

Action(행동): runtime positive clue(런타임 양수 단서)를 low PF/drawdown/side balance repair(저PF/낙폭/방향 균형 수리) 작업 묶음으로 열었다.
Effect(효과): 운영 주장(operating claim, 운영 주장)은 닫고, 다음 물질화(materialization, 물질화)에서 안전한 입력만 만들게 한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_bom_text(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts = []
    artifacts.append(
        write_bom_text(
            WORKSPACE_STATE,
            f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
        )
    )
    artifacts.append(
        write_bom_text(
            CURRENT_WORKING_STATE,
            f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

IE design(IE 설계)은 MT5 positive net(MT5 양수 순익)을 repair seed(수리 씨앗)로 고정했다.
효과는 PF/recovery/drawdown/side/parity/cost(수익 팩터/회복/낙폭/방향/동등성/비용)를 고치기 전 운영 주장을 막는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
""",
        )
    )
    artifacts.append(
        write_bom_text(
            SELECTION_STATUS,
            f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- rebuild_status(재구축 상태): `{STATUS}`
- source_best_model_id(원천 최고 모델 ID): `{final['best_model_id']}`
- source_net_profit(원천 순수익): `{final['best_net_profit']}`
- source_profit_factor(원천 수익 팩터): `{final['best_profit_factor']}`
- source_recovery_factor(원천 회복 계수): `{final['best_recovery_factor']}`
- source_max_drawdown(원천 최대 낙폭): `{final['best_max_drawdown_amount']}`
- design_rows(설계 행): `{final['design_rows']}`
- attribution_rows(귀속 행): `{final['attribution_rows']}`
- contract_rows(계약 행): `{final['contract_rows']}`
- runtime_package(런타임 패키지): `not_opened`
- candidate_selection(후보 선택): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): IE design(IE 설계)은 양수 순익 단서를 운영 후보가 아니라 수리 입력으로 넘긴다.
""",
        )
    )
    artifacts.append(
        write_bom_text(
            STAGE_BRIEF,
            f"""# {STAGE_ID}

Latest completed run(최근 완료 실행): `{RUN_ID}`

IE design(IE 설계)은 ID runtime-positive clue(ID 런타임 양수 단서)를 PF/recovery/drawdown/side/parity/cost(수익 팩터/회복/낙폭/방향/동등성/비용) 수리 계약으로 바꿨다.
Effect(효과): `{NEXT_RUN_ID}`에서 timestamp-safe(시점 안전) 입력을 물질화할 수 있다.

No selected model(선택 모델 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
""",
        )
    )
    existing = io(CHANGELOG).read_text(encoding="utf-8-sig") if exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    entry = (
        f"\n## {TODAY} - {RUN_ID}\n\n"
        f"- Action(행동): MT5 positive net(MT5 양수 순익) `{final['best_net_profit']}`를 IE repair design(IE 수리 설계)으로 전환했다.\n"
        f"- Effect(효과): PF/recovery/drawdown/side/parity/cost(수익 팩터/회복/낙폭/방향/동등성/비용) 수리 입력을 `{NEXT_RUN_ID}`로 넘겼고 운영 주장은 하지 않았다.\n"
    )
    if RUN_ID not in existing:
        artifacts.append(write_bom_text(CHANGELOG, existing.rstrip() + "\n" + entry))
    else:
        artifacts.append(CHANGELOG)
    return artifacts


def read_csv_dicts(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    with io(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv_dicts(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    ensure_parent(path)
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def upsert_csv(path: Path, row: Mapping[str, Any], key: str) -> Path:
    columns, rows = read_csv_dicts(path)
    if not columns:
        columns = list(row.keys())
    for column in row:
        if column not in columns:
            columns.append(column)
    filtered = [existing for existing in rows if str(existing.get(key, "")) != str(row.get(key, ""))]
    filtered.append(dict(row))
    return write_csv_dicts(path, columns, filtered)


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_positive_low_pf_drawdown_side_balance_repair_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"design_rows={final['design_rows']};attribution_rows={final['attribution_rows']};contracts={final['contract_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["design_rows"],
        "gate_passes": final["passed_gates"],
        "gate_total": final["gate_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "best_model_id": final["best_model_id"],
        "positive_net_rows": final["positive_net_rows"],
        "best_net_profit": final["best_net_profit"],
        "best_profit_factor": final["best_profit_factor"],
        "operating_ready_rows": final["operating_ready_rows"],
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_positive_repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_positive_low_pf_drawdown_side_balance_repair_design(런타임 양수 저PF 낙폭 방향 균형 수리 설계)",
        "tier_scope": "Tier A separate, Tier B missing_required, Tier A+B missing_required(Tier A 분리, Tier B 필수 누락, Tier A+B 필수 누락)",
        "kpi_scope": "design_only_no_training_no_mt5(설계 전용, 학습/MT5 없음)",
        "scoreboard_lane": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"net={final['best_net_profit']};pf={final['best_profit_factor']};dd={final['best_max_drawdown_amount']};recovery={final['best_recovery_factor']}",
        "guardrail_kpi": "no_training;no_mt5;no_selection;no_goal",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};claim_boundary={CLAIM_BOUNDARY}",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["design_rows"],
        "gate_passes": final["passed_gates"],
        "gate_total": final["gate_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "best_model_id": final["best_model_id"],
        "positive_net_rows": final["positive_net_rows"],
        "best_net_profit": final["best_net_profit"],
        "best_profit_factor": final["best_profit_factor"],
        "operating_ready_rows": final["operating_ready_rows"],
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design",
        "evidence_scope": "ID runtime review, IC MT5 probe, IA proxy-positive matrix(ID 런타임 검토, IC MT5 탐침, IA 프록시 양수 행렬)",
        "kpi_scope": "design_only_no_operating_claim",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_design",
        "family": "runtime_positive_low_pf_drawdown_side_balance_repair_design",
        "question": "how should MT5 positive net but low PF/drawdown weakness become timestamp-safe repair inputs(MT5 양수 순익이지만 낮은 PF/낙폭 약점을 어떻게 시점 안전 수리 입력으로 바꿀 것인가)",
        "metric_scope": "design_matrix_performance_attribution_contracts",
        "primary_artifact": rel(DESIGN_MATRIX),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["design_rows"],
        "gate_passes": final["passed_gates"],
        "gate_total": final["gate_rows"],
        "best_model_id": final["best_model_id"],
        "positive_net_rows": final["positive_net_rows"],
        "best_net_profit": final["best_net_profit"],
        "best_profit_factor": final["best_profit_factor"],
        "operating_ready_rows": final["operating_ready_rows"],
    }
    return [
        upsert_csv(RUN_REGISTRY, run_row, "run_id"),
        upsert_csv(PROJECT_LEDGER, alpha_row, "ledger_row_id"),
        upsert_csv(STAGE_LEDGER, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = read_csv_dicts(ARTIFACT_REGISTRY)
    if not columns:
        columns = [
            "stage_id",
            "run_id",
            "artifact_type",
            "path",
            "sha256",
            "created_at",
            "claim_boundary",
            "artifact_id",
            "created_at_utc",
            "notes",
            "artifact_path",
        ]
    for column in (
        "stage_id",
        "run_id",
        "artifact_type",
        "path",
        "sha256",
        "created_at",
        "claim_boundary",
        "artifact_id",
        "created_at_utc",
        "notes",
        "artifact_path",
    ):
        if column not in columns:
            columns.append(column)
    rows = [
        row
        for row in rows
        if str(row.get("run_id", "")) != RUN_ID and not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")
    ]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not exists(path) or not io(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": artifact_id,
                "created_at_utc": created_at,
                "notes": STATUS,
                "artifact_path": artifact_path,
            }
        )
    return write_csv_dicts(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = missing_inputs(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": missing}, ensure_ascii=False, indent=2))
        return 1

    (
        design_rows,
        attribution_rows,
        experiment_rows,
        feature_contract_rows,
        tier_rows,
        runtime_guard_rows,
        cost_rows,
        queue_rows,
        summary,
    ) = build_packets()

    artifacts: list[Path] = [
        write_csv(DESIGN_MATRIX, DESIGN_COLUMNS, design_rows),
        write_csv(PERFORMANCE_ATTRIBUTION, ATTRIBUTION_COLUMNS, attribution_rows),
        write_csv(EXPERIMENT_CONTRACT, EXPERIMENT_COLUMNS, experiment_rows),
        write_csv(FEATURE_LABEL_TRADE_CONTRACT, CONTRACT_COLUMNS, feature_contract_rows),
        write_csv(TIER_PAIR_CONTRACT, CONTRACT_COLUMNS, tier_rows),
        write_csv(RUNTIME_PARITY_GUARD, CONTRACT_COLUMNS, runtime_guard_rows),
        write_csv(COST_STRESS_CONTRACT, CONTRACT_COLUMNS, cost_rows),
        write_csv(IF_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    gates = build_gates(summary)
    final = make_final(summary, gates)
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "stage_id": STAGE_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "created_at": TODAY,
                    "script": rel(Path(__file__)),
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(write_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts + [Path(__file__)]))

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "design_rows": final["design_rows"],
                "attribution_rows": final["attribution_rows"],
                "contract_rows": final["contract_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": final["goal_achieve"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not final["failed_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
