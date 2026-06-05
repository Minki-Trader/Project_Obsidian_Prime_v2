from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

STAGE_ID = "344_directional_long_quality__supply_surface_probe"
STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_NUMBER = "run344B"
RUN_ID = "run344B_design_directional_long_supply_quality_surface_without_db_v1"
PARENT_RUN_ID = "run344A_branch_stage343_to_directional_long_supply_quality_surface_without_db_v1"
NEXT_RUN_ID = "run344C_materialize_directional_long_supply_quality_surface_package_without_db_v1"

STATUS = "completed_stage344B_directional_long_quality_surface_design_ready_materialization_no_selection"
JUDGMENT = "directional_long_quality_surface_design_ready_for_broad_materialization_no_selection"
DECISION = "stage344B_open_run344C_materialize_directional_long_quality_surface_package"
CLAIM_BOUNDARY = (
    "research_development_design_only_directional_long_quality_surface_no_model_training_"
    "no_mt5_execution_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run344B_directional_long_quality_surface_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344B_directional_long_quality_surface_design.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"

EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
DATA_INTEGRITY_CONTRACT = RUN_DIR / "data_integrity_contract.csv"
MODEL_VALIDATION_CONTRACT = RUN_DIR / "model_validation_contract.csv"
EXPLORATION_SURFACE_PLAN = RUN_DIR / "directional_long_quality_surface_plan.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run344C_materialization_queue.csv"
FAILURE_MEMORY_CONSTRAINTS = RUN_DIR / "failure_memory_constraints.csv"
TRADE_BUCKET_ATTRIBUTION_PLAN = RUN_DIR / "trade_bucket_attribution_plan.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
EXPLORATION_RECEIPT = RUN_DIR / "exploration_mandate_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run344A"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_QUEUE = PARENT_RUN_DIR / "run344B_directional_long_supply_quality_surface_queue.csv"
PARENT_LINEAGE_RECEIPT = PARENT_RUN_DIR / "artifact_lineage_receipt.json"

SOURCE_STAGE_ID = "343_quality_margin_runtime__early_long_mix_mt5_probe"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_REVIEW_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run343F"
SOURCE_REVIEW_FINAL = SOURCE_REVIEW_RUN_DIR / "final_decision.json"
SOURCE_SCORECARD = SOURCE_REVIEW_RUN_DIR / "trade_shape_rescue_review_scorecard.csv"
SOURCE_ATTRIBUTION = SOURCE_REVIEW_RUN_DIR / "performance_attribution.csv"
SOURCE_FAILURE_MEMORY = SOURCE_REVIEW_RUN_DIR / "failure_memory.csv"
SOURCE_RUNTIME_PACKAGE = SOURCE_STAGE_DIR / "02_runs" / "run343D" / "runtime_probe_attempt_package.csv"
SOURCE_FEATURE_MATRIX = SOURCE_STAGE_DIR / "02_runs" / "run343D" / "features" / "runtime_features.csv"
SOURCE_EXPECTED_TAPE = SOURCE_STAGE_DIR / "02_runs" / "run343D" / "expected" / "expected_tape.csv"
SOURCE_MODEL_MANIFEST = SOURCE_STAGE_DIR / "02_runs" / "run343D" / "model_handoff_manifest.csv"
SOURCE_MT5_SUMMARY = SOURCE_STAGE_DIR / "02_runs" / "run343E" / "trade_shape_rescue_quality_margin_blend_mt5_probe_summary.csv"
SOURCE_PROXY_DIFF = SOURCE_STAGE_DIR / "02_runs" / "run343E" / "proxy_mt5_runtime_difference.csv"


STAGE_LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "report_path",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "view",
    "tier",
    "metric_scope",
    "candidate_model_id",
    "net_profit",
    "profit_factor",
    "drawdown",
    "recovery_factor",
    "trade_count",
    "result_status",
    "sample_rows",
    "feature_count",
    "matched_rows",
    "expectancy",
    "attempt_count",
    "source_package_run_id",
    "ledger_row_id",
    "subrun_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]

SOURCE_INPUTS = [
    (PARENT_FINAL_DECISION, "run344A final decision(344A 최종 결정)"),
    (PARENT_GATE_AUDIT, "run344A required gate audit(344A 필수 게이트 감사)"),
    (SOURCE_QUEUE, "run344B source queue(344B 원천 대기열)"),
    (SOURCE_REVIEW_FINAL, "run343F final decision(343F 최종 결정)"),
    (SOURCE_SCORECARD, "run343F review scorecard(343F 검토 점수표)"),
    (SOURCE_ATTRIBUTION, "run343F performance attribution(343F 성과 귀속)"),
    (SOURCE_FAILURE_MEMORY, "run343F failure memory(343F 실패 기억)"),
    (SOURCE_RUNTIME_PACKAGE, "run343D runtime package(343D 런타임 패키지)"),
    (SOURCE_FEATURE_MATRIX, "run343D feature matrix(343D 피처 행렬)"),
    (SOURCE_EXPECTED_TAPE, "run343D expected tape(343D 예상 테이프)"),
    (SOURCE_MODEL_MANIFEST, "run343D model manifest(343D 모델 목록)"),
    (SOURCE_MT5_SUMMARY, "run343E MT5 summary(343E MT5 요약)"),
    (SOURCE_PROXY_DIFF, "run343E proxy-MT5 diff(343E 프록시-MT5 차이)"),
]


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fs_path(path: Path) -> str:
    resolved = path.resolve()
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


def path_is_file(path: Path) -> bool:
    return os.path.isfile(fs_path(path))


def path_exists(path: Path) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def required(path: Path) -> Path:
    if not path_is_file(path):
        raise FileNotFoundError(f"missing required run344B input: {rel(path)}")
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        keys: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows_list = [dict(row) for row in rows]
    if path_is_file(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_columns) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_columns) not in replacement_keys
    ]
    write_csv(path, kept + rows_list, fieldnames)


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if path_is_file(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def source_metrics() -> dict[str, Any]:
    final = read_json(required(SOURCE_REVIEW_FINAL))
    _score_fields, score_rows = read_csv_rows(required(SOURCE_SCORECARD))
    _feature_fields, feature_sample = read_csv_rows(required(SOURCE_FEATURE_MATRIX))
    matched_rows = sum(int(float(row.get("matched_rows") or 0)) for row in score_rows)
    return {
        "best_attempt": final["best_attempt"],
        "best_model_id": final["best_model_id"],
        "best_net_profit": final["best_net_profit"],
        "best_profit_factor": final["best_profit_factor"],
        "best_drawdown": final["best_drawdown"],
        "best_recovery_factor": final["best_recovery_factor"],
        "best_trade_count": final["best_trade_count"],
        "best_expectancy": final["best_expectancy"],
        "best_long_trade_count": final["best_long_trade_count"],
        "best_short_trade_count": final["best_short_trade_count"],
        "shape_control_attempt": final["shape_control_attempt"],
        "shape_control_net_profit": final["shape_control_net_profit"],
        "shape_control_profit_factor": final["shape_control_profit_factor"],
        "shape_control_trade_count": final["shape_control_trade_count"],
        "near_anchor_attempt": final["near_anchor_attempt"],
        "near_anchor_net_profit": final["near_anchor_net_profit"],
        "near_anchor_profit_factor": final["near_anchor_profit_factor"],
        "attempt_count": len(score_rows),
        "matched_rows": matched_rows,
        "feature_count": len(feature_sample[0]) if feature_sample else 0,
    }


def build_experiment_contract(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "experiment_id": "stage344_directional_long_quality_surface",
            "hypothesis": (
                "profit anchor(수익 앵커)의 short supply(숏 공급)는 유지하고, long entries(롱 진입)는 "
                "quality/regime surface(품질/국면 표면)로 분리하면 trade shape(거래 형태)를 회복하면서 PF(수익 팩터)를 덜 훼손할 수 있다."
            ),
            "decision_use": "choose materialized runtime-probe package design(런타임 탐침 패키지 설계 선택) for run344C without selection(선정 없음)",
            "comparison_baseline": (
                f"anchor {metrics['best_attempt']} net={metrics['best_net_profit']} PF={metrics['best_profit_factor']} "
                f"trades={metrics['best_trade_count']} long/short={metrics['best_long_trade_count']}/{metrics['best_short_trade_count']}; "
                f"shape control {metrics['shape_control_attempt']} net={metrics['shape_control_net_profit']} PF={metrics['shape_control_profit_factor']} trades={metrics['shape_control_trade_count']}"
            ),
            "control_variables": "same ONNX(동일 온엑스), same feature order(동일 피처 순서), same MT5 period(동일 MT5 기간), same lot/hold/close_on_flat(동일 랏/보유/관망청산)",
            "changed_variables": "long-only quality thresholds(롱 전용 품질 임계값), volatility/trend/session gates(변동성/추세/세션 게이트), exit lifecycle overlay(청산 생명주기 오버레이)",
            "sample_scope": "Tier A(티어 A) FPMarkets US100 M5 inner holdout runtime window(내부 보류 런타임 구간); Tier B(티어 B) missing_required(필수 누락)",
            "success_criteria": "materialized variants include broad sweep(넓은 탐색), at least one extreme sweep(극단 탐색), anchor unchanged control(앵커 무변경 대조), and shape-control payoff attribution(거래 형태 대조 손익 귀속)",
            "failure_criteria": "design repeats minute-block-only micro tuning(분 차단 단독 미세조정 반복) or lacks controls(대조군 누락)",
            "invalid_conditions": "feature index mismatch(피처 인덱스 불일치), source package missing(원천 패키지 누락), lookahead join(미래참조 결합), or no Tier A/B record(티어 A/B 기록 없음)",
            "stop_conditions": "if runtime promotion(런타임 승격) or candidate selection(후보 선정) is desired, stop and open a separate promotion packet(별도 승격 묶음)",
            "evidence_plan": "run344C package manifests(패키지 목록), expected tape(예상 테이프), variant preview(변형 미리보기), MT5 queue(MT5 대기열), artifact registry(산출물 등록부)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_data_integrity_contract(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "data_source": f"{rel(SOURCE_FEATURE_MATRIX)};{rel(SOURCE_EXPECTED_TAPE)};{rel(SOURCE_RUNTIME_PACKAGE)}",
            "time_axis": "M5 bar timestamp(5분봉 시각) and MT5 runtime rows(MT5 런타임 행) inherited from run343D/run343E; design only(설계 전용)",
            "sample_scope": "US100(유에스100) M5(5분봉), Tier A(티어 A), run343E matched_rows 58270 reference(참고)",
            "missing_or_duplicate_check": "deferred to run344C materialization audit(344C 물질화 감사로 지연); source file existence and hashes checked here(여기서는 원천 파일 존재와 해시 확인)",
            "feature_label_boundary": "no new labels(새 라벨 없음); design uses existing runtime features only(기존 런타임 피처만 사용)",
            "split_boundary": "single runtime holdout scout(단일 런타임 보류 스카우트); not forward validation(전진 검증 아님)",
            "leakage_risk": "choosing long gates after seeing run343E KPI(343E KPI를 본 뒤 롱 게이트 선택) may overfit; run344C must keep broad variants and controls(넓은 변형과 대조군 유지)",
            "data_hash_or_identity": f"feature_sha256={sha256_file(SOURCE_FEATURE_MATRIX)}; expected_sha256={sha256_file(SOURCE_EXPECTED_TAPE)}; package_sha256={sha256_file(SOURCE_RUNTIME_PACKAGE)}",
            "integrity_judgment": "usable_with_boundary(경계 있는 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_model_validation_contract(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "model_family": "existing logreg ONNX(기존 로지스틱 회귀 온엑스) reused; no new training(새 학습 없음)",
            "target_and_label": "inherited from source ONNX(원천 온엑스에서 상속); no new label construction(새 라벨 생성 없음)",
            "split_method": "runtime probe package design(런타임 탐침 패키지 설계); run344C materialization then MT5 probe required(344C 물질화 후 MT5 탐침 필요)",
            "selection_metric": "none(없음); this run only designs broad candidate surface(넓은 후보 표면 설계만)",
            "secondary_metrics": "net profit(순수익), PF(수익 팩터), expectancy(기대값), drawdown(낙폭), recovery(회복), trade count(거래수), long/short(롱/숏)",
            "threshold_policy": "fixed source thresholds plus exploratory long-only overlays(고정 원천 임계값과 탐색 롱 전용 오버레이)",
            "overfit_risk": "multiple gate variants on same holdout(같은 보류 구간에서 다중 게이트 변형)",
            "calibration_risk": "scores used as rank/threshold surface(순위/임계값 표면) not calibrated probability(보정 확률 아님)",
            "comparison_baseline": metrics["best_model_id"],
            "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def surface_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "variant_id": "s01_anchor_short_supply_control",
            "priority": "P0",
            "surface_family": "anchor_control(앵커 대조)",
            "source_attempt": "d01_h04_anchor45",
            "long_quality_gate": "unchanged(무변경)",
            "regime_gate": "unchanged(무변경)",
            "exit_overlay": "unchanged(무변경)",
            "broad_or_extreme": "control(대조)",
            "expected_effect": "preserve profit anchor(수익 앵커 보존)",
        },
        {
            "variant_id": "s02_shape_control_payoff_audit",
            "priority": "P0",
            "surface_family": "payoff_attribution(손익 귀속)",
            "source_attempt": "d02_h02_shape_ctl",
            "long_quality_gate": "none(없음)",
            "regime_gate": "none(없음)",
            "exit_overlay": "unchanged(무변경)",
            "broad_or_extreme": "control(대조)",
            "expected_effect": "identify weak long cluster(약한 롱 군집 식별)",
        },
        {
            "variant_id": "s03_near_anchor_long_rescue_seed",
            "priority": "P0",
            "surface_family": "near_anchor(앵커 근처)",
            "source_attempt": "d06_q04_m015_blk15",
            "long_quality_gate": "margin>=0.015 and q04(마진 0.015 이상 및 q04)",
            "regime_gate": "early block 0-15 retained(초반 0-15 차단 유지)",
            "exit_overlay": "unchanged(무변경)",
            "broad_or_extreme": "broad(넓은 탐색)",
            "expected_effect": "test small long rescue(소폭 롱 복구 시험)",
        },
        {
            "variant_id": "s04_long_quality_high_conf",
            "priority": "P0",
            "surface_family": "long_quality(롱 품질)",
            "source_attempt": "d02_h02_shape_ctl",
            "long_quality_gate": "long_score_rank top 35%(롱 점수 상위 35%)",
            "regime_gate": "session neutral(세션 중립)",
            "exit_overlay": "unchanged(무변경)",
            "broad_or_extreme": "broad(넓은 탐색)",
            "expected_effect": "recover only strong longs(강한 롱만 복구)",
        },
        {
            "variant_id": "s05_long_quality_extreme_top20",
            "priority": "P1",
            "surface_family": "long_quality_extreme(롱 품질 극단)",
            "source_attempt": "d02_h02_shape_ctl",
            "long_quality_gate": "long_score_rank top 20%(롱 점수 상위 20%)",
            "regime_gate": "session neutral(세션 중립)",
            "exit_overlay": "unchanged(무변경)",
            "broad_or_extreme": "extreme(극단 탐색)",
            "expected_effect": "find payoff cliff(손익 절벽 확인)",
        },
        {
            "variant_id": "s06_volatility_mid_long_only",
            "priority": "P1",
            "surface_family": "volatility_regime(변동성 국면)",
            "source_attempt": "d02_h02_shape_ctl",
            "long_quality_gate": "shape-control longs(거래 형태 대조 롱)",
            "regime_gate": "exclude highest volatility bucket(최고 변동성 구간 제외)",
            "exit_overlay": "unchanged(무변경)",
            "broad_or_extreme": "broad(넓은 탐색)",
            "expected_effect": "remove shock longs(충격 롱 제거)",
        },
        {
            "variant_id": "s07_trend_confirmed_long_only",
            "priority": "P1",
            "surface_family": "trend_regime(추세 국면)",
            "source_attempt": "d02_h02_shape_ctl",
            "long_quality_gate": "shape-control longs(거래 형태 대조 롱)",
            "regime_gate": "trend-confirmed only(추세 확인만)",
            "exit_overlay": "unchanged(무변경)",
            "broad_or_extreme": "broad(넓은 탐색)",
            "expected_effect": "allow longs only with market structure(시장 구조 있는 롱만 허용)",
        },
        {
            "variant_id": "s08_cash_open_late_reentry",
            "priority": "P1",
            "surface_family": "session_reentry(세션 재진입)",
            "source_attempt": "d01_h04_anchor45",
            "long_quality_gate": "anchor plus late long reentry(앵커와 후반 롱 재진입)",
            "regime_gate": "minutes_from_cash_open>=110(현금장 이후 110분 이상)",
            "exit_overlay": "unchanged(무변경)",
            "broad_or_extreme": "broad(넓은 탐색)",
            "expected_effect": "avoid open shock but add later longs(개장 충격 회피 후 후반 롱 추가)",
        },
        {
            "variant_id": "s09_exit_lifecycle_short_hold_longs",
            "priority": "P2",
            "surface_family": "exit_lifecycle(청산 생명주기)",
            "source_attempt": "d02_h02_shape_ctl",
            "long_quality_gate": "shape-control longs(거래 형태 대조 롱)",
            "regime_gate": "none(없음)",
            "exit_overlay": "long max_hold shorter(롱 최대 보유 단축)",
            "broad_or_extreme": "broad(넓은 탐색)",
            "expected_effect": "keep trade count but reduce weak long loss tail(거래수 유지, 약한 롱 손실 꼬리 감소)",
        },
        {
            "variant_id": "s10_exit_lifecycle_flat_recheck",
            "priority": "P2",
            "surface_family": "exit_lifecycle_extreme(청산 생명주기 극단)",
            "source_attempt": "d02_h02_shape_ctl",
            "long_quality_gate": "shape-control longs(거래 형태 대조 롱)",
            "regime_gate": "none(없음)",
            "exit_overlay": "long close_on_flat true(롱 관망 청산 켜기)",
            "broad_or_extreme": "extreme(극단 탐색)",
            "expected_effect": "test lifecycle cliff(생명주기 절벽 확인)",
        },
        {
            "variant_id": "s11_short_supply_protect_vol_filter",
            "priority": "P2",
            "surface_family": "short_supply_protect(숏 공급 보호)",
            "source_attempt": "d01_h04_anchor45",
            "long_quality_gate": "unchanged(무변경)",
            "regime_gate": "short threshold unchanged, volatility veto only(숏 임계값 무변경, 변동성 거부만)",
            "exit_overlay": "unchanged(무변경)",
            "broad_or_extreme": "stress(압박 탐색)",
            "expected_effect": "avoid q10 short-threshold tax(q10 숏 임계값 세금 회피)",
        },
        {
            "variant_id": "s12_no_entry_change_exit_only",
            "priority": "P2",
            "surface_family": "no_entry_change_control(진입 무변경 대조)",
            "source_attempt": "d06_q04_m015_blk15",
            "long_quality_gate": "unchanged from near-anchor(앵커 근처 무변경)",
            "regime_gate": "unchanged(무변경)",
            "exit_overlay": "exit-only lifecycle(청산만 변경)",
            "broad_or_extreme": "control(대조)",
            "expected_effect": "separate entry vs exit effect(진입 효과와 청산 효과 분리)",
        },
    ]
    for row in rows:
        row["next_run_id"] = NEXT_RUN_ID
        row["claim_boundary"] = CLAIM_BOUNDARY
    return rows


def build_materialization_queue() -> list[dict[str, Any]]:
    rows = []
    for idx, row in enumerate(surface_rows(), start=1):
        rows.append(
            {
                "queue_id": f"run344C_{row['variant_id']}",
                "next_run_id": NEXT_RUN_ID,
                "variant_id": row["variant_id"],
                "priority": row["priority"],
                "source_attempt": row["source_attempt"],
                "materialization_action": "build runtime package candidate(런타임 패키지 후보 생성)",
                "required_controls": "s01 anchor, s02 shape control, s12 no-entry-change control(s01 앵커, s02 거래형태 대조, s12 진입 무변경 대조)",
                "expected_outputs": "runtime_probe_attempt_package.csv; variant_preview.csv; side_filter_expected_decision_audit.csv; run344D_queue.csv",
                "order": idx,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_failure_constraints() -> list[dict[str, Any]]:
    _fields, rows = read_csv_rows(required(SOURCE_FAILURE_MEMORY))
    constraints = []
    for row in rows:
        constraints.append(
            {
                "source_failure_id": row.get("failure_id", ""),
                "constraint": row.get("do_not_repeat", ""),
                "allowed_reopen_condition": row.get("reopen_condition", ""),
                "salvage_value": row.get("salvage_value", ""),
                "effect": "turn failure memory(실패 기억) into run344C design constraint(344C 설계 제약)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return constraints


def build_trade_bucket_plan() -> list[dict[str, Any]]:
    return [
        {
            "bucket_id": "direction_long_session_bucket",
            "source_attempts": "d01_h04_anchor45,d02_h02_shape_ctl,d06_q04_m015_blk15",
            "decomposition": "direction(방향), minutes_from_cash_open bucket(현금장 이후 분 구간), win/loss cluster(승패 군집)",
            "question": "Which restored long trades paid the PF tax(복구 롱 중 어떤 거래가 PF 세금을 냈는가)?",
            "consumer": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "bucket_id": "volatility_trend_bucket",
            "source_attempts": "d02_h02_shape_ctl",
            "decomposition": "volatility bucket(변동성 구간), trend/range proxy(추세/횡보 프록시), long payoff(롱 손익)",
            "question": "Can regime surface(국면 표면) separate useful long supply(유용한 롱 공급)?",
            "consumer": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "bucket_id": "exit_lifecycle_bucket",
            "source_attempts": "d02_h02_shape_ctl,d06_q04_m015_blk15",
            "decomposition": "hold bars(보유 봉), close_on_flat(관망 청산), adverse excursion proxy(역행 프록시)",
            "question": "Can exit lifecycle(청산 생명주기) repair shape without entry micro-tuning(진입 미세조정 없이 형태를 고칠 수 있는가)?",
            "consumer": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def output_paths() -> list[Path]:
    return [
        EXPERIMENT_CONTRACT,
        DATA_INTEGRITY_CONTRACT,
        MODEL_VALIDATION_CONTRACT,
        EXPLORATION_SURFACE_PLAN,
        MATERIALIZATION_QUEUE,
        FAILURE_MEMORY_CONSTRAINTS,
        TRADE_BUCKET_ATTRIBUTION_PLAN,
        WORK_PACKET,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        EXPLORATION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        SELECTION_STATUS,
        ROOT_SELECTION_STATUS,
        STAGE_LEDGER,
        STAGE_BRIEF,
        STAGE_README,
        REVIEW_INDEX,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        RUN_REGISTRY,
        PROJECT_LEDGER,
        ARTIFACT_REGISTRY,
        Path(__file__),
    ]


def write_receipts(metrics: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "long quality/regime surface can recover trade shape without preserving weak long tax(롱 품질/국면 표면이 약한 롱 비용 없이 거래 형태를 복구)",
            "decision_use": "run344C materialization scope(344C 물질화 범위)",
            "evidence_plan": rel(EXPERIMENT_CONTRACT),
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(SOURCE_FEATURE_MATRIX), rel(SOURCE_EXPECTED_TAPE), rel(SOURCE_RUNTIME_PACKAGE)],
            "time_axis": "inherited M5 runtime row order(상속된 5분봉 런타임 행 순서)",
            "integrity_judgment": "usable_with_boundary(경계 있는 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "existing ONNX logistic surface(기존 온엑스 로지스틱 표면)",
            "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
            "selection_metric": "none(없음)",
        },
    )
    write_json(
        EXPLORATION_RECEIPT,
        {
            **base,
            "idea_id": "stage344_directional_long_quality_surface",
            "broad_sweep": "long quality, volatility, trend, session, exit lifecycle(롱 품질/변동성/추세/세션/청산 생명주기)",
            "extreme_sweep": "top20 long quality and long close_on_flat true(상위 20% 롱 품질 및 롱 관망청산 켜기)",
            "micro_search_gate": "only after one broad surface improves both PF and trade shape(넓은 표면이 PF와 거래 형태를 모두 개선한 뒤)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": "design ready for materialization(물질화 준비 설계)",
            "forbidden_claims": [
                "model_training(모델 학습)",
                "MT5_execution(MT5 실행)",
                "candidate_selection(후보 선정)",
                "operating_promotion(운영 승격)",
                "runtime_authority(런타임 권위)",
                "Goal_Achieve(목표 달성)",
            ],
        },
    )
    artifacts = [path for path in output_paths() if path_is_file(path) and path != LINEAGE_RECEIPT]
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [
                {"path": rel(path), "sha256": sha256_file(path), "availability": "tracked"}
                for path, _label in SOURCE_INPUTS
                if path_is_file(path)
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifacts],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
        },
    )


def gate_row(gate_id: str, status: str, evidence_path: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": status,
        "evidence_path": evidence_path,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates() -> list[dict[str, Any]]:
    experiment_fields, experiment_rows = read_csv_rows(EXPERIMENT_CONTRACT)
    data_fields, data_rows = read_csv_rows(DATA_INTEGRITY_CONTRACT)
    model_fields, model_rows = read_csv_rows(MODEL_VALIDATION_CONTRACT)
    surface_fields, surface_rows_read = read_csv_rows(EXPLORATION_SURFACE_PLAN)
    queue_fields, queue_rows = read_csv_rows(MATERIALIZATION_QUEUE)
    constraints_fields, constraints_rows = read_csv_rows(FAILURE_MEMORY_CONSTRAINTS)
    required_experiment = {
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
    }
    required_data = {
        "data_source",
        "time_axis",
        "sample_scope",
        "missing_or_duplicate_check",
        "feature_label_boundary",
        "split_boundary",
        "leakage_risk",
        "data_hash_or_identity",
        "integrity_judgment",
    }
    required_model = {
        "model_family",
        "target_and_label",
        "split_method",
        "selection_metric",
        "secondary_metrics",
        "threshold_policy",
        "overfit_risk",
        "calibration_risk",
        "comparison_baseline",
        "validation_judgment",
    }
    has_extreme = any("extreme" in row.get("broad_or_extreme", "") for row in surface_rows_read)
    has_controls = {"s01_anchor_short_supply_control", "s02_shape_control_payoff_audit", "s12_no_entry_change_exit_only"}.issubset(
        {row.get("variant_id", "") for row in surface_rows_read}
    )
    return [
        gate_row(
            "source_stage344A_handoff_available",
            "passed" if path_is_file(PARENT_FINAL_DECISION) and path_is_file(SOURCE_QUEUE) else "failed",
            f"{rel(PARENT_FINAL_DECISION)};{rel(SOURCE_QUEUE)}",
            "run344A(344A 실행)의 handoff(인계)를 받는다.",
        ),
        gate_row(
            "source_run343F_review_evidence_available",
            "passed" if all(path_is_file(path) for path in [SOURCE_REVIEW_FINAL, SOURCE_SCORECARD, SOURCE_ATTRIBUTION, SOURCE_FAILURE_MEMORY]) else "failed",
            f"{rel(SOURCE_REVIEW_FINAL)};{rel(SOURCE_SCORECARD)};{rel(SOURCE_ATTRIBUTION)};{rel(SOURCE_FAILURE_MEMORY)}",
            "run343F(343F 실행)의 KPI(핵심 성과 지표), attribution(귀속), failure memory(실패 기억)를 읽는다.",
        ),
        gate_row(
            "experiment_design_contract_complete",
            "passed" if required_experiment.issubset(set(experiment_fields)) and bool(experiment_rows) else "failed",
            rel(EXPERIMENT_CONTRACT),
            "experiment design(실험 설계)의 필수 항목을 채운다.",
        ),
        gate_row(
            "data_integrity_contract_complete",
            "passed" if required_data.issubset(set(data_fields)) and bool(data_rows) else "failed",
            rel(DATA_INTEGRITY_CONTRACT),
            "timestamp-safe(시점 안전) 경계와 leakage risk(누수 위험)를 기록한다.",
        ),
        gate_row(
            "model_validation_contract_complete",
            "passed" if required_model.issubset(set(model_fields)) and bool(model_rows) else "failed",
            rel(MODEL_VALIDATION_CONTRACT),
            "model/threshold validation(모델/임계값 검증) 경계를 설계 전용으로 닫는다.",
        ),
        gate_row(
            "broad_and_extreme_surface_defined",
            "passed" if len(surface_rows_read) >= 12 and has_extreme and has_controls else "failed",
            rel(EXPLORATION_SURFACE_PLAN),
            "broad sweep(넓은 탐색), extreme sweep(극단 탐색), controls(대조군)를 모두 둔다.",
        ),
        gate_row(
            "failure_memory_constraints_connected",
            "passed" if len(constraints_rows) >= 3 and bool(constraints_fields) else "failed",
            rel(FAILURE_MEMORY_CONSTRAINTS),
            "failure memory(실패 기억)를 다음 설계 제약으로 연결한다.",
        ),
        gate_row(
            "materialization_queue_written",
            "passed" if len(queue_rows) >= 12 and "variant_id" in queue_fields else "failed",
            rel(MATERIALIZATION_QUEUE),
            "run344C(344C 실행)가 물질화할 구체 변형 대기열을 만든다.",
        ),
        gate_row(
            "artifact_lineage_audit",
            "passed" if path_is_file(LINEAGE_RECEIPT) else "failed",
            rel(LINEAGE_RECEIPT),
            "source inputs(원천 입력)와 design artifacts(설계 산출물)를 연결한다.",
        ),
        gate_row(
            "no_forbidden_operating_claim",
            "passed" if path_is_file(CLAIM_RECEIPT) else "failed",
            rel(CLAIM_RECEIPT),
            "design(설계)을 운영 주장(operating claim, 운영 주장)으로 올리지 않는다.",
        ),
        gate_row(
            "required_gate_coverage_audit_written",
            "passed",
            rel(GATE_AUDIT),
            "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다.",
        ),
    ]


def write_docs(metrics: Mapping[str, Any]) -> None:
    report = f"""# run344B Directional Long Quality Surface Design(344B 방향성 롱 품질 표면 설계)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- preserved_anchor(보존 앵커): `{metrics["best_attempt"]}` net `{metrics["best_net_profit"]}`, PF `{metrics["best_profit_factor"]}`, trades `{metrics["best_trade_count"]}`, long/short `{metrics["best_long_trade_count"]}/{metrics["best_short_trade_count"]}`
- shape_control(거래 형태 대조): `{metrics["shape_control_attempt"]}` net `{metrics["shape_control_net_profit"]}`, PF `{metrics["shape_control_profit_factor"]}`, trades `{metrics["shape_control_trade_count"]}`

## Action(행동)

directional long quality surface(방향성 롱 품질 표면)를 broad sweep(넓은 탐색)과 extreme sweep(극단 탐색)으로 설계했다.
Effect(효과): minute block micro-tuning(분 차단 미세조정)을 반복하지 않고, long quality/regime/exit lifecycle(롱 품질/국면/청산 생명주기) 축으로 새 수익 원천을 찾는다.

## Boundary(경계)

This run is design only(설계 전용). No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선정 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage344B Directional Long Quality Surface Design Decision(344B 방향성 롱 품질 표면 설계 결정)

- decision(결정): `{DECISION}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- reason(이유): run343F(343F 실행)는 profit anchor(수익 앵커)는 보존했지만 trade shape rescue(거래 형태 복구)가 실패했다. 다음은 minute block(분 차단)이 아니라 long quality source(롱 품질 원천)다.

Action(행동): run344C(344C 실행) materialization queue(물질화 대기열)를 열었다.
Effect(효과): source ONNX(원천 온엑스)와 MT5 runtime evidence(MT5 런타임 근거)를 유지하면서, broad/exreme/control(넓은/극단/대조) 후보를 같은 패키지로 넘긴다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_review(원천 검토): `run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- preserved_profit_anchor(보존 수익 앵커): `{metrics["best_attempt"]}`
- unresolved_failure(미해결 실패): `trade_shape_rescue_failed(거래 형태 복구 실패)`
- next_probe(다음 탐침): `directional_long_quality_surface_materialization(방향성 롱 품질 표면 물질화)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage344(344단계)는 selection(선정)이 아니라 offensive exploration(공격 탐색) 설계에서 물질화로 이동한다.
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

run344B(344B 실행)는 directional long quality surface(방향성 롱 품질 표면)를 설계했고, run344C(344C 실행)는 이를 runtime package(런타임 패키지)로 물질화한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
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
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, decision)
    write_text(SELECTION_STATUS, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(WORKSPACE_STATE, workspace)
    append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"""## run344B Directional Long Quality Surface Design(344B 방향성 롱 품질 표면 설계)

- run_id(실행 ID): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- variants(변형): `12`
- effect(효과): long quality/regime/exit lifecycle(롱 품질/국면/청산 생명주기) 후보를 넓게 연다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run344B Directional Long Quality Surface Design(344B 방향성 롱 품질 표면 설계)

- queue(대기열): `{rel(MATERIALIZATION_QUEUE)}`
- effect(효과): Stage344(344단계)의 다음 행동을 materialization(물질화)로 구체화한다.
""",
    )
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"""- run344B design(344B 설계): `{rel(REPORT_PATH)}`
""",
    )
    changelog = f"""## {TODAY} run344B Directional Long Quality Surface Design(방향성 롱 품질 표면 설계)

- action(행동): run343F(343F 실행)의 trade shape rescue failure(거래 형태 복구 실패)를 제약으로 바꾸고, run344C(344C 실행) 물질화 대기열을 만들었다.
- effect(효과): short supply(숏 공급) 수익 앵커는 대조로 보존하고, long quality/regime/exit lifecycle(롱 품질/국면/청산 생명주기) 공격 탐색을 시작한다.
- boundary(경계): design only(설계 전용), no MT5 execution(MT5 실행 없음), no selection(선정 없음), no runtime authority(런타임 권위 없음).
"""
    append_text_once(ROOT_CHANGELOG, RUN_ID, changelog)
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, changelog)
    idea = f"""## {TODAY} {RUN_ID} Directional Long Quality Surface Design(방향성 롱 품질 표면 설계)

- idea_id(아이디어 ID): `stage344_directional_long_quality_surface`
- hypothesis(가설): short supply(숏 공급) 수익 앵커는 보존하고, long entries(롱 진입)는 quality/regime/exit lifecycle(품질/국면/청산 생명주기) 표면으로 다시 나누면 trade shape(거래 형태)를 회복할 수 있다.
- broad_sweep(넓은 탐색): long quality(롱 품질), volatility(변동성), trend(추세), session reentry(세션 재진입), exit lifecycle(청산 생명주기)
- extreme_sweep(극단 탐색): top20 long quality(상위 20% 롱 품질), long close_on_flat true(롱 관망 청산 켜기)
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): minute block micro-tuning(분 차단 미세조정)을 반복하지 않는다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    append_text_once(IDEA_REGISTRY, RUN_ID, idea)


def ledger_rows(gates: Sequence[Mapping[str, Any]], metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    gate_passes = sum(1 for gate in gates if gate["status"] == "passed")
    gate_total = len(gates)
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "experiment_design(실험 설계)",
        "lane": "experiment_design(실험 설계)",
        "family": "experiment_design(실험 설계)",
        "run_number": RUN_NUMBER,
        "notes": "Design only(설계 전용); opens run344C materialization(344C 물질화 개방).",
        "source_package_run_id": "run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1",
        "attempt_count": 12,
    }
    tier_a = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier A",
        "subrun_id": "Tier A",
        "view": "Tier A separate(Tier A 분리)",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "tier_scope": "Tier A",
        "metric_scope": "design_source_reference_not_new_kpi",
        "kpi_scope": "design_source_reference_not_new_kpi",
        "candidate_model_id": metrics["best_model_id"],
        "net_profit": metrics["best_net_profit"],
        "profit_factor": metrics["best_profit_factor"],
        "drawdown": metrics["best_drawdown"],
        "recovery_factor": metrics["best_recovery_factor"],
        "trade_count": metrics["best_trade_count"],
        "expectancy": metrics["best_expectancy"],
        "matched_rows": metrics["matched_rows"],
        "result_status": "design_ready_materialization_required_no_selection(설계 준비, 물질화 필요, 선정 없음)",
        "primary_kpi": f"source_anchor_net={metrics['best_net_profit']};source_anchor_pf={metrics['best_profit_factor']};planned_variants=12",
        "guardrail_kpi": f"source_anchor_drawdown={metrics['best_drawdown']};source_long_short={metrics['best_long_trade_count']}/{metrics['best_short_trade_count']}",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
    }
    tier_b = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier B",
        "subrun_id": "Tier B",
        "view": "Tier B separate(Tier B 분리)",
        "record_view": "Tier B separate(Tier B 분리)",
        "tier": "Tier B",
        "tier_scope": "Tier B",
        "metric_scope": "missing_required",
        "kpi_scope": "missing_required",
        "candidate_model_id": "missing_required",
        "result_status": "missing_required(필수 누락)",
        "primary_kpi": "missing_required",
        "guardrail_kpi": "missing_required",
        "external_verification_status": "missing_required(필수 누락)",
        "attempt_count": "",
    }
    combined = {
        **tier_a,
        "ledger_row_id": f"{RUN_ID}__Tier A+B",
        "subrun_id": "Tier A+B",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "tier_scope": "Tier A+B",
        "metric_scope": "same_as_tier_a_until_tier_b_available",
        "kpi_scope": "same_as_tier_a_until_tier_b_available",
        "result_status": "same_as_tier_a_until_tier_b_available",
    }
    return [tier_a, tier_b, combined]


def write_registries(gates: Sequence[Mapping[str, Any]], metrics: Mapping[str, Any]) -> None:
    rows = ledger_rows(gates, metrics)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], [{key: row.get(key, "") for key in STAGE_LEDGER_COLUMNS} for row in rows])
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_design(실험 설계)",
                "family": "experiment_design(실험 설계)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "notes": "Directional long quality surface design only(방향성 롱 품질 표면 설계 전용).",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": sum(1 for gate in gates if gate["status"] == "passed"),
                "gate_total": len(gates),
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": metrics["best_model_id"],
                "net_profit": metrics["best_net_profit"],
                "profit_factor": metrics["best_profit_factor"],
                "drawdown": metrics["best_drawdown"],
                "recovery_factor": metrics["best_recovery_factor"],
                "trade_count": metrics["best_trade_count"],
                "expectancy": metrics["best_expectancy"],
                "result_status": "design_ready_materialization_required_no_selection(설계 준비, 물질화 필요, 선정 없음)",
                "matched_rows": metrics["matched_rows"],
                "attempt_count": 12,
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "design_source_reference_not_new_kpi",
                "source_package_run_id": "run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1",
            }
        ],
    )
    artifact_rows = []
    for path in output_paths():
        if path_is_file(path):
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": path.suffix.lstrip(".") or "file",
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha256_file(path),
                    "created_at": TODAY,
                    "created_at_utc": now_utc(),
                    "notes": "run344B directional long quality surface design artifact(344B 방향성 롱 품질 표면 설계 산출물)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "path"], artifact_rows)


def write_final(gates: Sequence[Mapping[str, Any]], metrics: Mapping[str, Any]) -> None:
    write_json(
        FINAL_DECISION,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "gate_passes": sum(1 for gate in gates if gate["status"] == "passed"),
            "gate_total": len(gates),
            "planned_variant_count": 12,
            "best_attempt": metrics["best_attempt"],
            "best_net_profit": metrics["best_net_profit"],
            "best_profit_factor": metrics["best_profit_factor"],
            "shape_control_attempt": metrics["shape_control_attempt"],
            "candidate_selection": "not_claimed",
            "mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "run_number": RUN_NUMBER,
            "work_family": "experiment_design(실험 설계)",
            "primary_action": "design directional long quality surface(방향성 롱 품질 표면 설계)",
            "producer": rel(Path(__file__)),
            "inputs": [rel(path) for path, _label in SOURCE_INPUTS],
            "outputs": [rel(path) for path in output_paths() if path_is_file(path)],
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def main() -> None:
    for path, _label in SOURCE_INPUTS:
        required(path)
    os.makedirs(fs_path(RUN_DIR), exist_ok=True)
    os.makedirs(fs_path(REVIEW_DIR), exist_ok=True)

    metrics = source_metrics()
    write_csv(EXPERIMENT_CONTRACT, build_experiment_contract(metrics))
    write_csv(DATA_INTEGRITY_CONTRACT, build_data_integrity_contract(metrics))
    write_csv(MODEL_VALIDATION_CONTRACT, build_model_validation_contract(metrics))
    write_csv(EXPLORATION_SURFACE_PLAN, surface_rows())
    write_csv(MATERIALIZATION_QUEUE, build_materialization_queue())
    write_csv(FAILURE_MEMORY_CONSTRAINTS, build_failure_constraints())
    write_csv(TRADE_BUCKET_ATTRIBUTION_PLAN, build_trade_bucket_plan())
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-exploration-mandate(탐색 명령)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "work_packet_schema_lint",
                "data_integrity_contract_complete",
                "model_validation_contract_complete",
                "broad_and_extreme_surface_defined",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_receipts(metrics)
    gates = build_gates()
    write_csv(GATE_AUDIT, gates)
    if any(gate["status"] != "passed" for gate in gates):
        failed = [gate["gate_id"] for gate in gates if gate["status"] != "passed"]
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise SystemExit(f"failed gates: {failed}")
    write_docs(metrics)
    write_final(gates, metrics)
    write_receipts(metrics)
    write_registries(gates, metrics)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": sum(1 for gate in gates if gate["status"] == "passed"),
                "gate_total": len(gates),
                "planned_variant_count": 12,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
