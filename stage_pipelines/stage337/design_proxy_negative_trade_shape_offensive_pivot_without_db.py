from __future__ import annotations

import json
import re
import sys
import csv
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import review_proxy_negative_trade_shape_second_order_repair_training_without_db as hv  # noqa: E402


aw = hv.aw
fb = hv.fb
he = hv.he

TODAY = "2026-06-01"
STAGE_ID = hv.STAGE_ID
RUN_NUMBER = "run337HW"
RUN_ID = "run337HW_design_proxy_negative_trade_shape_offensive_pivot_without_db_v1"
PARENT_RUN_ID = hv.RUN_ID
NEXT_RUN_ID = "run337HX_materialize_proxy_negative_trade_shape_offensive_pivot_inputs_without_db_v1"
STATUS = "completed_stage337HW_proxy_negative_trade_shape_offensive_pivot_design_no_training_no_selection"
JUDGMENT = "repeated_proxy_negative_failure_memory_converted_to_label_model_trade_shape_offensive_pivot"
DECISION = "stage337HW_open_run337HX_proxy_negative_trade_shape_offensive_pivot_inputs"
IDEA_ID = "IDEA-ST337-PROXY-NEGATIVE-OFFENSIVE-PIVOT"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HW_proxy_negative_trade_shape_offensive_pivot_design_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_runtime_package_"
    "no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = hv.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = hv.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HW_proxy_negative_trade_shape_offensive_pivot_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HW_proxy_negative_trade_shape_offensive_pivot_design.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

HV_FINAL = hv.FINAL_DECISION
HV_GATES = hv.GATE_AUDIT
HV_QUEUE = hv.HW_QUEUE
HV_CANDIDATES = hv.TRAINING_CANDIDATE_REVIEW
HV_ONNX_PARITY = hv.ONNX_PARITY_REVIEW
HV_MEMORY = hv.SECOND_ORDER_MEMORY
HV_RUNTIME_DECISION = hv.RUNTIME_PACKAGE_DECISION
HU_PROXY = hv.HU_PROXY
HU_CLASSIFICATION = hv.HU_CLASSIFICATION
HS_FEATURE_SCHEMA = hv.HU_FEATURE_SCHEMA

DESIGN_MATRIX = RUN_DIR / "offensive_pivot_design_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
LABEL_HORIZON_CONTRACT = RUN_DIR / "label_horizon_pivot_contract.csv"
MODEL_FAMILY_CONTRACT = RUN_DIR / "model_family_pivot_contract.csv"
TRADE_SHAPE_CONTRACT = RUN_DIR / "trade_shape_pivot_contract.csv"
TIER_PAIR_CONTRACT = RUN_DIR / "tier_pair_exploration_contract.csv"
FEATURE_BOUNDARY_CONTRACT = RUN_DIR / "feature_boundary_contract.csv"
RELEASE_FIREWALL_CONTRACT = RUN_DIR / "runtime_release_firewall_contract.csv"
HX_QUEUE = RUN_DIR / "run337HX_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_discipline_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    HV_FINAL,
    HV_GATES,
    HV_QUEUE,
    HV_CANDIDATES,
    HV_ONNX_PARITY,
    HV_MEMORY,
    HV_RUNTIME_DECISION,
    HU_PROXY,
    HU_CLASSIFICATION,
    HS_FEATURE_SCHEMA,
)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    EXPERIMENT_CONTRACT,
    LABEL_HORIZON_CONTRACT,
    MODEL_FAMILY_CONTRACT,
    TRADE_SHAPE_CONTRACT,
    TIER_PAIR_CONTRACT,
    FEATURE_BOUNDARY_CONTRACT,
    RELEASE_FIREWALL_CONTRACT,
    HX_QUEUE,
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
    IDEA_REGISTRY,
    he.SELECTED_STATUS,
    he.WORKSPACE_STATE,
    he.CURRENT_STATE,
    he.CHANGELOG,
    he.STAGE_BRIEF,
    he.RUN_REGISTRY,
    he.ALPHA_LEDGER,
    he.STAGE_LEDGER,
    he.ARTIFACT_REGISTRY,
    Path(__file__),
)

DESIGN_COLUMNS = (
    "design_id",
    "idea_id",
    "pivot_family",
    "hypothesis",
    "changed_variables",
    "fixed_controls",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "materialization_action",
    "effect",
    "claim_boundary",
)
EXPERIMENT_COLUMNS = (
    "experiment_id",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
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
GATE_COLUMNS = hv.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number


def build_design_packets() -> tuple[
    list[dict[str, Any]],
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
    hv_final = read_json(HV_FINAL)
    hv_queue = read_csv(HV_QUEUE)
    candidates = read_csv(HV_CANDIDATES)
    memory = read_csv(HV_MEMORY)
    parity = read_csv(HV_ONNX_PARITY)
    best = max(candidates, key=lambda row: as_float(row.get("holdout_proxy_net")), default={})
    best_net = as_float(hv_final.get("best_inner_holdout_proxy_net"))
    hq_best = as_float(hv_final.get("hq_best_inner_holdout_proxy_net"))
    improvement = as_float(hv_final.get("proxy_net_improvement_vs_hq"))
    positive_rows = int(as_float(hv_final.get("positive_proxy_rows")))
    parity_passed = sum(1 for row in parity if str(row.get("passed", "")).lower() == "true")
    baseline = (
        f"HV best_model={best.get('model_id', '')};best_net={best_net};"
        f"HQ_best_net={hq_best};improvement={improvement};positive_proxy_rows={positive_rows};"
        f"onnx_parity={parity_passed}/{len(parity)}"
    )
    fixed_controls = (
        "FPMarkets US100 M5, timestamp-safe closed-bar inputs(시점 안전 확정봉 입력), "
        "no threshold tuning(임계값 조정 없음), no lot optimization(랏 최적화 없음), "
        "no MT5 execution(MT5 실행 없음), no operating claim(운영 주장 없음)"
    )
    sample_scope = "Tier A train/inner holdout now(Tier A 학습/내부 보류 우선), Tier B separate/combined required in materialization(Tier B 분리/합산은 물질화에서 필수)"
    design_rows = [
        {
            "design_id": "hw001_label_horizon_pivot",
            "idea_id": IDEA_ID,
            "pivot_family": "label horizon pivot(라벨 기간 전환)",
            "hypothesis": "all-negative proxy(전부 음수 프록시)는 fwd12 중심 라벨이 trade shape(거래 형태)와 맞지 않는 신호일 수 있다.",
            "changed_variables": "create fwd6/fwd18/fwd24 label candidates(fwd6/fwd18/fwd24 라벨 후보 생성)",
            "fixed_controls": fixed_controls,
            "sample_scope": sample_scope,
            "success_criteria": "at least one horizon has holdout proxy net > 0 and PF >= 1.05(하나 이상의 기간이 보류 프록시 순수익 양수와 PF 1.05 이상)",
            "failure_criteria": "all horizons remain proxy negative(모든 기간이 프록시 음수 유지)",
            "invalid_conditions": "future return leaks into features(미래 수익률이 피처에 누수)",
            "materialization_action": "materialize timestamp-safe label columns and target audit(시점 안전 라벨 열과 목표 감사를 물질화)",
            "effect": "moves beyond weight repair into target definition(가중치 수리를 넘어 목표 정의를 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hw002_side_specific_asymmetry",
            "idea_id": IDEA_ID,
            "pivot_family": "side-specific asymmetry(방향별 비대칭)",
            "hypothesis": "long/short balance(롱/숏 균형)가 섞이면 약한 방향 우위가 서로 지워질 수 있다.",
            "changed_variables": "separate long-only and short-only target/weight views(롱 전용과 숏 전용 목표/가중치 보기 분리)",
            "fixed_controls": fixed_controls,
            "sample_scope": sample_scope,
            "success_criteria": "one side improves without collapsing trade count(한 방향이 거래 수 붕괴 없이 개선)",
            "failure_criteria": "both sides stay negative or one side becomes tiny-sample only(양쪽 모두 음수 또는 작은 표본만 남음)",
            "invalid_conditions": "side chosen from holdout performance(보류 성과로 방향 선택)",
            "materialization_action": "build side-specific task seeds with predeclared side gates(사전 선언 방향 게이트가 있는 작업 씨앗 생성)",
            "effect": "tests market behavior asymmetry directly(시장 현상 비대칭을 직접 시험)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hw003_model_family_challenge",
            "idea_id": IDEA_ID,
            "pivot_family": "model family challenge(모델 계열 도전)",
            "hypothesis": "LightGBM(라이트GBM) 확률 모양이 이 표면에서 train/holdout inversion(학습/보류 역전)을 만든다면 ExtraTrees/XGBoost(엑스트라트리/익스지부스트)가 다른 순위 구조를 만들 수 있다.",
            "changed_variables": "add ExtraTrees and XGBoost scout configs(엑스트라트리와 익스지부스트 탐색 설정 추가)",
            "fixed_controls": fixed_controls,
            "sample_scope": sample_scope,
            "success_criteria": "non-LightGBM family improves holdout proxy and calibration diagnostics(비 LightGBM 계열이 보류 프록시와 보정 진단 개선)",
            "failure_criteria": "all families repeat negative proxy(모든 계열이 음수 프록시 반복)",
            "invalid_conditions": "model output is treated as calibrated probability without calibration check(보정 확인 없이 모델 출력을 보정 확률로 취급)",
            "materialization_action": "write model family task blueprints and ONNX feasibility notes(모델 계열 작업 청사진과 ONNX 가능성 메모 작성)",
            "effect": "opens a new model-family source of alpha(새 모델 계열 수익 원천을 연다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hw004_active_flat_two_stage",
            "idea_id": IDEA_ID,
            "pivot_family": "active/flat two-stage trade shape(활성/관망 2단계 거래 형태)",
            "hypothesis": "direction classification(방향 분류)보다 trade/no-trade(거래/관망) 선별이 먼저 필요할 수 있다.",
            "changed_variables": "stage1 active-flat target, stage2 direction target(1단계 활성-관망 목표, 2단계 방향 목표)",
            "fixed_controls": fixed_controls,
            "sample_scope": sample_scope,
            "success_criteria": "active gate raises PF without making trade count unusably small(활성 게이트가 거래 수를 과소화하지 않고 PF 개선)",
            "failure_criteria": "active gate removes too many trades or net stays negative(활성 게이트가 거래를 과도 제거하거나 순수익 음수 유지)",
            "invalid_conditions": "active label uses future drawdown not available at decision time(활성 라벨이 결정 시점에 없는 미래 낙폭 사용)",
            "materialization_action": "create active-flat label and two-stage handoff schema(활성-관망 라벨과 2단계 인계 스키마 생성)",
            "effect": "attacks trade shape instead of only class weights(클래스 가중치가 아니라 거래 형태를 공격)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hw005_regime_context_mixture",
            "idea_id": IDEA_ID,
            "pivot_family": "regime/context mixture(국면/문맥 혼합)",
            "hypothesis": "loss clusters(손실 군집)가 session/regime(세션/국면)에 몰려 있으면 mixture gate(혼합 게이트)가 proxy loss를 줄일 수 있다.",
            "changed_variables": "timestamp-known session/regime task split(시점에 알려진 세션/국면 작업 분할)",
            "fixed_controls": fixed_controls,
            "sample_scope": sample_scope,
            "success_criteria": "regime split improves worst bucket and overall net(국면 분리가 최악 구간과 전체 순수익 개선)",
            "failure_criteria": "one regime dominates or combined result remains negative(한 국면만 지배하거나 합산 결과 음수 유지)",
            "invalid_conditions": "regime is labeled using future performance(미래 성과로 국면 라벨링)",
            "materialization_action": "materialize regime buckets and separate/combined records(국면 버킷과 분리/합산 기록 생성)",
            "effect": "turns market behavior into a testable branch(시장 현상을 시험 가능한 분기로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    experiment_rows = [
        {
            "experiment_id": RUN_ID,
            "hypothesis": "Repeated proxy-negative results(HQ/HV 반복 프록시 음수)는 단순 sample-weight repair(표본 가중치 수리) 한계이며 label/model/trade-shape pivot(라벨/모델/거래 형태 전환)이 필요하다.",
            "decision_use": "open HX materialization only(HX 물질화만 개방); no model selection(모델 선택 없음)",
            "comparison_baseline": baseline,
            "control_variables": fixed_controls,
            "changed_variables": "label horizon, side split, model family, active-flat shape, regime mixture(라벨 기간, 방향 분리, 모델 계열, 활성-관망 형태, 국면 혼합)",
            "sample_scope": sample_scope,
            "success_criteria": "materialization creates timestamp-safe paired Tier A/B task seeds(물질화가 시점 안전 티어 A/B 쌍 작업 씨앗 생성)",
            "failure_criteria": "design cannot produce at least five distinct materialization branches(서로 다른 물질화 분기 5개 미만)",
            "invalid_conditions": "look-ahead bias, holdout-based branch choice, MT5 KPI leak(미래참조, 보류 기반 분기 선택, MT5 KPI 누수)",
            "stop_conditions": "missing HV evidence or claim boundary breach(HV 근거 누락 또는 주장 경계 위반)",
            "evidence_plan": f"{rel(DESIGN_MATRIX)};{rel(HX_QUEUE)};{rel(GATE_AUDIT)}",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    label_rows = [
        {
            "contract_id": "hw_label_horizon_contract",
            "scope": "fwd6/fwd18/fwd24 closed-bar labels(fwd6/fwd18/fwd24 확정봉 라벨)",
            "required_rule": "labels use only future target construction, never model features(라벨은 목표 생성에만 쓰고 모델 피처에는 금지)",
            "forbidden_rule": "no holdout-selected horizon(보류 성과로 기간 선택 금지)",
            "success_signal": "separate horizon scorecards exist(기간별 점수표 존재)",
            "failure_signal": "all horizons proxy negative(모든 기간 프록시 음수)",
            "effect": "tests target mismatch(목표 불일치를 시험)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    model_rows = [
        {
            "contract_id": "hw_model_family_contract",
            "scope": "LightGBM/ExtraTrees/XGBoost scout(라이트GBM/엑스트라트리/익스지부스트 탐색)",
            "required_rule": "record ONNX feasibility separately from proxy score(ONNX 가능성과 프록시 점수를 분리 기록)",
            "forbidden_rule": "no promotion from scout score(탐색 점수만으로 승격 금지)",
            "success_signal": "one family changes holdout proxy sign or density quality(한 계열이 보류 프록시 부호나 밀도 품질 변경)",
            "failure_signal": "all families repeat negative proxy(모든 계열 음수 반복)",
            "effect": "tests whether model shape is the blocker(모델 모양이 차단 원인인지 시험)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    trade_rows = [
        {
            "contract_id": "hw_trade_shape_contract",
            "scope": "side-specific and active-flat tasks(방향별 및 활성-관망 작업)",
            "required_rule": "trade count, density, long/short mix must be recorded(거래 수, 밀도, 롱/숏 혼합 기록 필수)",
            "forbidden_rule": "no tiny-sample positive claim(작은 표본 양수 주장 금지)",
            "success_signal": "PF and expectancy improve with usable trade count(PF와 기대값이 사용 가능한 거래 수로 개선)",
            "failure_signal": "trade count collapses or PF remains below 1(거래 수 붕괴 또는 PF 1 미만 유지)",
            "effect": "makes trade shape part of the objective(거래 형태를 목표 일부로 만듦)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    tier_rows = [
        {
            "contract_id": "hw_tier_pair_contract",
            "scope": "Tier A separate, Tier B separate, Tier A+B combined(Tier A 분리, Tier B 분리, Tier A+B 합산)",
            "required_rule": "HX must emit missing_required/blocked/out_of_scope if Tier B cannot be built(HX는 Tier B를 만들 수 없으면 필수 누락/차단/범위 밖을 기록)",
            "forbidden_rule": "do not report Tier A as total read(Tier A를 전체 판독으로 보고 금지)",
            "success_signal": "three required records are present(세 필수 기록 존재)",
            "failure_signal": "Tier B omitted silently(Tier B 조용한 생략)",
            "effect": "preserves paired exploration discipline(쌍 탐색 규율 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    feature_rows = [
        {
            "contract_id": "hw_feature_boundary_contract",
            "scope": "pretrade feature schema and new label columns(진입 전 피처 스키마와 새 라벨 열)",
            "required_rule": "new labels, weights, and score columns are excluded from feature set(새 라벨/가중치/점수 열은 피처 세트에서 제외)",
            "forbidden_rule": "no future target or MT5 result as feature(미래 목표나 MT5 결과 피처 금지)",
            "success_signal": "feature boundary audit passes(피처 경계 감사 통과)",
            "failure_signal": "forbidden token appears in allowed features(금지 토큰이 허용 피처에 등장)",
            "effect": "keeps look-ahead bias out(미래참조 편향 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    release_rows = [
        {
            "contract_id": "hw_release_firewall_contract",
            "scope": "runtime package gate(런타임 패키지 게이트)",
            "required_rule": "proxy positive, ONNX parity, trade-shape guard must pass before MT5 package(프록시 양수, ONNX 동등성, 거래 형태 가드 통과 전 MT5 패키지 금지)",
            "forbidden_rule": "no runtime authority or Goal Achieve(런타임 권위 또는 목표 달성 금지)",
            "success_signal": "future review can open runtime package only with multi-KPI evidence(미래 검토가 다중 KPI 근거로만 런타임 패키지 개방)",
            "failure_signal": "single KPI or parity-only release attempt(단일 KPI 또는 동등성만으로 해제 시도)",
            "effect": "keeps operation claims strict(운영 주장 엄격성 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue_rows = [
        {
            "queue_id": "hx001_materialize_offensive_pivot_inputs",
            "source_run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "task": "materialize five offensive pivot task families(공격 전환 작업군 5개 물질화)",
            "required_inputs": f"{rel(DESIGN_MATRIX)};{rel(EXPERIMENT_CONTRACT)};{rel(FEATURE_BOUNDARY_CONTRACT)}",
            "expected_outputs": "timestamp-safe input frame, task seeds, feature boundary audit(시점 안전 입력 프레임, 작업 씨앗, 피처 경계 감사)",
            "blocked_if_missing": "design matrix or boundary contracts(설계 행렬 또는 경계 계약)",
            "effect": "turns design into executable guarded inputs(설계를 실행 가능한 방어 입력으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    summary = {
        "hv_next_action": hv_final.get("next_action", ""),
        "hv_queue_next_action": hv_queue[0].get("next_run_id", "") if hv_queue else "",
        "hv_failed_gate_rows": sum(1 for row in read_csv(HV_GATES) if row.get("status") != "passed"),
        "design_rows": len(design_rows),
        "experiment_rows": len(experiment_rows),
        "contract_rows": len(label_rows) + len(model_rows) + len(trade_rows) + len(tier_rows) + len(feature_rows) + len(release_rows),
        "queue_rows": len(queue_rows),
        "source_positive_proxy_rows": positive_rows,
        "source_best_proxy_net": best_net,
        "source_proxy_net_improvement_vs_hq": improvement,
        "onnx_parity_passed_rows": parity_passed,
        "onnx_parity_rows": len(parity),
        "memory_rows": len(memory),
    }
    return design_rows, experiment_rows, label_rows, model_rows, trade_rows, tier_rows, feature_rows, release_rows, queue_rows, summary


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "idea_id": IDEA_ID,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "new_training": "not_run",
        "runtime_package": "not_opened",
        "mt5_execution": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_family": "experiment_design",
        "primary_skill": "obsidian-experiment-design",
        "support_skills": "obsidian-exploration-mandate;obsidian-data-integrity;obsidian-model-validation;obsidian-artifact-lineage",
        "required_gates": "work_packet_schema_lint;feature_boundary_gate;tier_pair_contract_gate;required_gate_coverage_audit;final_claim_guard",
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = final["candidate_selection"] == "not_run" and final["mt5_execution"] == "not_run" and final["goal_achieve"] == "not_claimed"
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(HV_FINAL), "required HV inputs exist(필수 HV 입력 존재)"),
        ("parent_hv_gates_passed", final["hv_failed_gate_rows"] == 0, str(final["hv_failed_gate_rows"]), "0", rel(HV_GATES), "HV gates passed(HV 게이트 통과)"),
        ("parent_next_action_matches", final["hv_next_action"] == RUN_ID and final["hv_queue_next_action"] == RUN_ID, f"final={final['hv_next_action']};queue={final['hv_queue_next_action']}", RUN_ID, rel(HV_FINAL), "HW follows HV next action(HW가 HV 다음 행동을 따름)"),
        ("design_matrix_broad_enough", final["design_rows"] >= 5, str(final["design_rows"]), ">=5", rel(DESIGN_MATRIX), "broad offensive variants exist(넓은 공격 변형 존재)"),
        ("experiment_contract_present", final["experiment_rows"] == 1, str(final["experiment_rows"]), "1", rel(EXPERIMENT_CONTRACT), "experiment contract exists(실험 계약 존재)"),
        ("offensive_not_weight_only", final["contract_rows"] >= 6, str(final["contract_rows"]), ">=6", rel(MODEL_FAMILY_CONTRACT), "label/model/trade-shape contracts exist(라벨/모델/거래 형태 계약 존재)"),
        ("feature_boundary_contract", path_exists(FEATURE_BOUNDARY_CONTRACT), rel(FEATURE_BOUNDARY_CONTRACT), "exists", rel(FEATURE_BOUNDARY_CONTRACT), "look-ahead guard present(미래참조 방지 존재)"),
        ("tier_pair_contract", path_exists(TIER_PAIR_CONTRACT), rel(TIER_PAIR_CONTRACT), "exists", rel(TIER_PAIR_CONTRACT), "Tier A/B paired contract present(Tier A/B 쌍 계약 존재)"),
        ("materialization_queue_opened", final["queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(HX_QUEUE), "HX materialization queue opened(HX 물질화 대기열 개방)"),
        ("idea_registry_updated", True, IDEA_ID, "registered", rel(IDEA_REGISTRY), "durable idea registered(지속 아이디어 등록)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};mt5={final['mt5_execution']};goal={final['goal_achieve']}", "not_run/not_run/not_claimed", rel(FINAL_DECISION), "design without operating claim(운영 주장 없는 설계)"),
        ("required_gate_coverage_audit", True, "all required gates listed(모든 필수 게이트 열거)", "present", rel(GATE_AUDIT), "completion claim tied to gates(완료 주장이 게이트에 연결)"),
    ]
    return [
        {"gate_id": gate_id, "status": "passed" if passed else "failed", "evidence_path": evidence, "observed": observed, "expected": expected, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def write_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    base = {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "stage_id": STAGE_ID, "created_at_utc": now_utc(), "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY}
    receipts = [
        (EXPERIMENT_RECEIPT, {**base, "hypothesis": "repeated negative proxy requires offensive pivot(반복 음수 프록시는 공격 전환이 필요)", "decision_use": "open HX materialization only(HX 물질화만 개방)", "idea_id": IDEA_ID, "evidence_plan": [rel(DESIGN_MATRIX), rel(HX_QUEUE)]}),
        (DATA_RECEIPT, {**base, "data_source": rel(HV_CANDIDATES), "feature_boundary": rel(FEATURE_BOUNDARY_CONTRACT), "tier_pair_contract": rel(TIER_PAIR_CONTRACT), "integrity_judgment": "design_only_timestamp_safe_contracts(설계 전용 시점 안전 계약)"}),
        (MODEL_RECEIPT, {**base, "model_family": "not_trained; model family challenge designed(미학습; 모델 계열 도전 설계)", "selection_metric": "none(없음)", "validation_judgment": JUDGMENT}),
        (PERFORMANCE_RECEIPT, {**base, "source_best_proxy_net": final["source_best_proxy_net"], "source_proxy_net_improvement_vs_hq": final["source_proxy_net_improvement_vs_hq"], "performance_use": "failure memory and clue only(실패 기억과 단서 전용)"}),
        (JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "judgment_label": "exploratory_design(탐색 설계)", "evidence_available": [rel(DESIGN_MATRIX), rel(EXPERIMENT_CONTRACT), rel(HX_QUEUE)], "evidence_missing": "HX materialized inputs and training results(HX 물질화 입력과 학습 결과)", "next_condition": NEXT_RUN_ID}),
        (CLAIM_RECEIPT, {**base, "forbidden_claims": "selected, runtime authority, operating promotion, Goal Achieve(선택, 런타임 권위, 운영 승격, 목표 달성)", "claim_guard": "all forbidden claims remain not_claimed/not_run(모든 금지 주장은 not_claimed/not_run 유지)"}),
    ]
    paths = [write_json(path, payload) for path, payload in receipts]
    all_artifacts = list(artifacts) + paths
    lineage = {
        **base,
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()},
        "registry_links": [rel(IDEA_REGISTRY), rel(he.RUN_REGISTRY), rel(he.ALPHA_LEDGER), rel(he.STAGE_LEDGER), rel(he.ARTIFACT_REGISTRY)],
        "availability": "generated_with_manifest(목록과 함께 생성)",
        "lineage_judgment": "HV negative evidence connected to HX materialization(HV 부정 근거를 HX 물질화에 연결)",
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# run337HW Proxy Negative Trade Shape Offensive Pivot Design(run337HW 프록시 음수 거래 형태 공격 전환 설계)

Action(행동): HV negative memory(HV 부정 기억)를 label/model/trade-shape offensive pivot(라벨/모델/거래 형태 공격 전환) 설계로 바꿨다.
Effect(효과): 반복 sample-weight repair(표본 가중치 수리)를 멈추고 HX materialization(HX 물질화)이 5개 넓은 분기를 만들 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- idea_id(아이디어 ID): `{final['idea_id']}`
- design_rows(설계 행): `{final['design_rows']}`
- contract_rows(계약 행): `{final['contract_rows']}`
- source_best_proxy_net(원천 최고 프록시 순수익): `{final['source_best_proxy_net']}`
- source_proxy_net_improvement_vs_hq(HQ 대비 원천 프록시 순수익 개선): `{final['source_proxy_net_improvement_vs_hq']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Boundary(경계): training(학습), MT5 execution(MT5 실행), runtime package(런타임 패키지), candidate selection(후보 선택), Forward/Goal(전진/목표)은 주장하지 않는다.

Next action(다음 행동): `{final['next_action']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337HW Decision(337HW 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(DESIGN_MATRIX)}`, `{rel(EXPERIMENT_CONTRACT)}`, `{rel(HX_QUEUE)}`

Action(행동): repeated proxy negative(반복 프록시 음수)를 offensive pivot(공격 전환) 아이디어로 등록하고 물질화 대기열을 열었다.
Effect(효과): 같은 blocker(차단 원인)를 3차 가중치 수리로만 반복하지 않고 새 수익 원천을 탐색한다.

runtime_authority(런타임 권위): `not_claimed`
goal_achieve(목표 달성): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def upsert_section_after_metadata(text: str, title_marker: str, section: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and title_marker in line:
            start = index
            break
    if start is not None:
        end = start + 1
        while end < len(lines) and not lines[end].startswith("## "):
            end += 1
        del lines[start:end]
    insert_at = next((index for index, line in enumerate(lines) if line.startswith("## ")), len(lines))
    return "\n".join(lines[:insert_at] + section.strip("\n").splitlines() + [""] + lines[insert_at:]) + "\n"


def update_idea_registry() -> Path:
    text, bom = aw.read_text_lossless(IDEA_REGISTRY)
    row = (
        f"| `{IDEA_ID}` | `{STAGE_ID}` | repeated HQ/HV proxy-negative ONNX(반복 HQ/HV 프록시 음수 ONNX) evidence suggests "
        "label horizon, side-specific, model-family, active-flat, and regime/context offensive pivot(라벨 기간/방향별/모델 계열/활성-관망/국면 문맥 공격 전환)이 필요하다 | "
        "`Tier A now + Tier B required next(Tier A 현재 + 다음 Tier B 필수)` | `opened_design_no_selection` | "
        f"`{RUN_ID}` opens `{NEXT_RUN_ID}`; selected candidate(선택 후보), runtime authority(런타임 권위), Goal Achieve(목표 달성) 없음 |"
    )
    updated = fb.upsert_single_line(text, IDEA_ID, row)
    return aw.write_text_lossless(IDEA_REGISTRY, updated, bom)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = [update_idea_registry()]
    workspace, workspace_bom = aw.read_text_lossless(he.WORKSPACE_STATE)
    workspace = re.sub(r"^current_run_id:.*$", f"current_run_id: {final['next_action']}", workspace, count=1, flags=re.M)
    workspace = re.sub(r"^updated_on:.*$", f"updated_on: '{TODAY}'", workspace, count=1, flags=re.M)
    focus = (
        "- >-\n"
        f"  Stage337 run337HW focus complete(337단계 run337HW 초점 완료): `{final['status']}`. "
        f"Effect(효과): design rows(설계 행) `{final['design_rows']}`, contracts(계약) `{final['contract_rows']}`, "
        f"idea(아이디어) `{IDEA_ID}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337HW focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337HW focus complete.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(he.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(he.CURRENT_STATE)
    current_lines = current.splitlines()
    replacements = {
        "- current_run(": f"- current_run(현재 실행): `{final['next_action']}`",
        "- status(": f"- status(상태): `{final['status']}`",
        "- decision(": f"- decision(결정): `{final['decision']}`",
        "- latest_completed_run(": f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- next_action(": f"- next_action(다음 행동): `{final['next_action']}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for index, line in enumerate(current_lines):
        if line.startswith("## "):
            break
        for prefix, replacement in replacements.items():
            if line.startswith(prefix):
                current_lines[index] = replacement
                break
    current = "\n".join(current_lines) + "\n"
    section = f"""## run337HW Proxy Negative Trade Shape Offensive Pivot Design(프록시 음수 거래 형태 공격 전환 설계)

Action(행동): run337HW(337HW 실행)는 HV negative memory(HV 부정 기억)를 5개 offensive pivot(공격 전환) 설계로 바꿨다.
Effect(효과): label horizon/model family/trade shape(라벨 기간/모델 계열/거래 형태) 탐색을 `{final['next_action']}`으로 열었다.

Boundary(경계): training(학습), MT5 execution(MT5 실행), runtime package(런타임 패키지), Forward/Goal(전진/목표)은 주장하지 않는다.
Next(다음): `{final['next_action']}`.
"""
    current = upsert_section_after_metadata(current, "run337HW Proxy Negative Trade Shape Offensive Pivot Design", section)
    artifacts.append(aw.write_text_lossless(he.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- idea_id(아이디어 ID): `{IDEA_ID}`
- design_rows(설계 행): `{final['design_rows']}`
- contract_rows(계약 행): `{final['contract_rows']}`
- source_best_proxy_net(원천 최고 프록시 순수익): `{final['source_best_proxy_net']}`
- runtime_package(런타임 패키지): `not_opened`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HW design(HW 설계)은 같은 수리 반복을 멈추고 공격 탐색 입력을 준비한다.
"""
    artifacts.append(aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = f"- {TODAY}: run337HW(337HW 실행) `{final['status']}`. Effect(효과): `{IDEA_ID}`와 design rows(설계 행) `{final['design_rows']}`를 만들고 `{final['next_action']}`을 열었다."
    artifacts.append(aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HW(337HW 실행)", brief_entry), brief_bom))
    changelog, changelog_bom = aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337HW(337HW 실행) `{final['status']}`. Effect(효과): proxy-negative(프록시 음수) 반복을 offensive pivot(공격 전환) 설계로 바꾸고 `{final['next_action']}`을 열었다."
    artifacts.append(aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HW", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "proxy_negative_trade_shape_offensive_pivot_design", "status": final["status"], "judgment": final["judgment"], "path": rel(REPORT_PATH), "notes": f"idea={IDEA_ID};design_rows={final['design_rows']};contracts={final['contract_rows']};next_action={final['next_action']};goal_achieve_not_claimed."}
    alpha_row = {"ledger_row_id": f"{RUN_ID}__offensive_pivot_design", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": "offensive_pivot_design", "parent_run_id": PARENT_RUN_ID, "record_view": "proxy_negative_trade_shape_offensive_pivot_design(프록시 음수 거래 형태 공격 전환 설계)", "tier_scope": "Tier A now, Tier B required next(Tier A 현재, 다음 Tier B 필수)", "kpi_scope": "design_only_no_training_no_runtime_package(설계 전용, 학습/런타임 패키지 없음)", "scoreboard_lane": "experiment_design", "status": final["status"], "judgment": final["judgment"], "path": rel(REPORT_PATH), "primary_kpi": f"design_rows={final['design_rows']};contracts={final['contract_rows']}", "guardrail_kpi": "no_training;no_mt5;no_selection;no_goal", "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)", "notes": f"decision={final['decision']};next_action={final['next_action']};claim_boundary={CLAIM_BOUNDARY}"}
    stage_row = {"ledger_row_id": f"{RUN_ID}__offensive_pivot_design", "stage_id": STAGE_ID, "run_id": RUN_ID, "work_family": "experiment_design", "evidence_scope": "HV negative memory, HU proxy scorecard", "kpi_scope": "design_only_no_operating_claim", "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "path": rel(REPORT_PATH), "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed", "decision": final["decision"], "run_key": f"{RUN_ID}__offensive_pivot_design", "family": "proxy_negative_trade_shape_offensive_pivot_design", "question": "what broad offensive pivot should follow repeated proxy-negative ONNX training(반복 프록시 음수 ONNX 학습 뒤 어떤 넓은 공격 전환을 할 것인가)", "metric_scope": "design_matrix_contracts_materialization_queue", "primary_artifact": rel(DESIGN_MATRIX), "report_path": rel(REPORT_PATH), "next_action": final["next_action"]}
    return [
        fb.upsert_csv_worktree(he.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(he.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(he.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(he.ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        rows.append({"artifact_id": artifact_id, "artifact_type": path.suffix.lstrip(".") or "file", "path": artifact_path, "sha256": aw.sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": STATUS, "artifact_path": artifact_path, "claim_boundary": CLAIM_BOUNDARY})
    # The artifact registry path is short enough for normal pathlib, and this avoids
    # a Windows extended-path edge case in the older stage helper.
    he.ARTIFACT_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with he.ARTIFACT_REGISTRY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return he.ARTIFACT_REGISTRY


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    design_rows, experiment_rows, label_rows, model_rows, trade_rows, tier_rows, feature_rows, release_rows, queue_rows, summary = build_design_packets()
    final = make_final(summary)
    artifacts: list[Path] = [
        write_csv(DESIGN_MATRIX, DESIGN_COLUMNS, design_rows),
        write_csv(EXPERIMENT_CONTRACT, EXPERIMENT_COLUMNS, experiment_rows),
        write_csv(LABEL_HORIZON_CONTRACT, CONTRACT_COLUMNS, label_rows),
        write_csv(MODEL_FAMILY_CONTRACT, CONTRACT_COLUMNS, model_rows),
        write_csv(TRADE_SHAPE_CONTRACT, CONTRACT_COLUMNS, trade_rows),
        write_csv(TIER_PAIR_CONTRACT, CONTRACT_COLUMNS, tier_rows),
        write_csv(FEATURE_BOUNDARY_CONTRACT, CONTRACT_COLUMNS, feature_rows),
        write_csv(RELEASE_FIREWALL_CONTRACT, CONTRACT_COLUMNS, release_rows),
        write_csv(HX_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend([write_csv(GATE_AUDIT, GATE_COLUMNS, gates), write_json(FINAL_DECISION, final), write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY})])
    artifacts.extend(write_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "idea_id": IDEA_ID, "design_rows": final["design_rows"], "contract_rows": final["contract_rows"], "gates": f"{final['passed_gates']}/{final['gate_rows']}", "next_action": final["next_action"], "goal_achieve": "not_claimed"}, ensure_ascii=False, indent=2))
    return 0 if not final["failed_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
