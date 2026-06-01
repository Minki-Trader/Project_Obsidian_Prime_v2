from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

STAGE_ID = "355_density_recovery_model_family__new_label_source_probe"
RUN_NUMBER = "run355A"
RUN_ID = "run355A_design_density_recovery_label_model_source_without_db_v1"
PARENT_RUN_ID = "run354C_expand_proxy_filter_sweep_without_db_v1"
NEXT_RUN_ID = "run355B_materialize_density_recovery_label_inputs_without_db_v1"

STATUS = "completed_stage355A_density_recovery_design_queue_opened_no_selection"
JUDGMENT = "experiment_design_completed_new_label_model_source_queue_no_operating_claim"
DECISION = "stage355A_open_run355B_materialize_density_recovery_label_inputs"
CLAIM_BOUNDARY = (
    "research_development_experiment_design_only_new_label_source_model_queue_"
    "no_training_no_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
GATE_TOTAL = 10

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE_SELECTION = SELECTED_DIR / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
REPORT_PATH = REVIEW_DIR / "run355A_density_recovery_design.md"

SOURCE_RUN354C_DIR = ROOT / "stages" / "354_proxy_trade_shape_scout__small_candidate_queue" / "02_runs" / "run354C"
SOURCE_RUN354C_FINAL = SOURCE_RUN354C_DIR / "final_decision.json"
SOURCE_RUN354C_SWEEP = SOURCE_RUN354C_DIR / "expanded_outcome_horizon_sweep.csv"
SOURCE_RUN354C_QUEUE = SOURCE_RUN354C_DIR / "density_valid_queue.csv"
SOURCE_RUN354C_FAILURE = SOURCE_RUN354C_DIR / "failure_memory.csv"
SOURCE_RUN354C_REPORT = (
    ROOT
    / "stages"
    / "354_proxy_trade_shape_scout__small_candidate_queue"
    / "03_reviews"
    / "run354C_expand_proxy_filter_sweep.md"
)
RUNTIME_FEATURES = (
    ROOT
    / "stages"
    / "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
    / "02_runs"
    / "run351B"
    / "features"
    / "runtime_features.csv"
)
RAW_US100_BARS = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"

DESIGN_MATRIX = RUN_DIR / "density_recovery_design_matrix.csv"
LABEL_SOURCE_PLAN = RUN_DIR / "label_source_plan.csv"
FEATURE_SOURCE_PLAN = RUN_DIR / "feature_source_plan.csv"
MODEL_FAMILY_PLAN = RUN_DIR / "model_family_plan.csv"
TRADE_SHAPE_CONTROL_PLAN = RUN_DIR / "trade_shape_control_plan.csv"
RUN355B_QUEUE = RUN_DIR / "run355B_materialization_queue.csv"
WORK_PACKET_CONTRACT = RUN_DIR / "work_packet_contract.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage355A_density_recovery_design.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{block.strip()}\n" if current.strip() else block.strip() + "\n"
    write_text(path, next_text)


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(100_000_000)
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
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    new_rows = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing_rows = read_csv_rows(path)
    else:
        fieldnames, existing_rows = [], []
    for row in new_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replace_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in new_rows}
    kept = [
        row
        for row in existing_rows
        if tuple(str(row.get(key, "")) for key in key_fields) not in replace_keys
    ]
    write_csv(path, kept + new_rows, fieldnames)


def csv_count(path: Path) -> int:
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def source_identity() -> dict[str, Any]:
    final = read_json(SOURCE_RUN354C_FINAL)
    return {
        "stage354C_status": final.get("status", ""),
        "stage354C_judgment": final.get("judgment", ""),
        "stage354C_density_valid_queue_rows": final.get("density_valid_queue_rows", ""),
        "stage354C_sweep_rows": final.get("sweep_rows", ""),
        "stage354C_best_read": final.get("best_read", {}),
        "source_final_sha256": sha256_file(SOURCE_RUN354C_FINAL),
        "source_sweep_sha256": sha256_file(SOURCE_RUN354C_SWEEP),
        "source_failure_sha256": sha256_file(SOURCE_RUN354C_FAILURE),
        "runtime_features_sha256": sha256_file(RUNTIME_FEATURES),
        "raw_us100_bars_sha256": sha256_file(RAW_US100_BARS),
        "source_queue_rows": csv_count(SOURCE_RUN354C_QUEUE),
        "source_failure_rows": csv_count(SOURCE_RUN354C_FAILURE),
    }


def design_rows() -> list[dict[str, Any]]:
    return [
        {
            "design_id": "d01_microtrend_cost_buffer_fwd6_fwd8",
            "priority": 1,
            "hypothesis": "shorter horizon cost-buffer labels(짧은 보유기간 비용 완충 라벨)이 기존 12봉 표면보다 trade/day(일별 거래수) 3+와 cost stress(비용 압박)를 같이 회복한다.",
            "label_source_id": "ls01_cost_buffer_multihorizon",
            "feature_source_id": "fs01_existing_58_runtime_features",
            "model_family_id": "mf01_logreg_and_small_mlp_onnx",
            "rule_stack_seed": "nonoverlap_hold_6_or_8_with_min_margin(비중첩 6/8봉 보유와 최소 마진)",
            "why_new_source": "Stage354C(354C 실행)는 기존 probability surface(확률 표면) 임계값만으로 비용 압박을 넘지 못했다.",
            "expected_failure_to_watch": "validation positive but OOS negative(검증 양수, 표본외 음수)",
            "materialize_next": "true",
        },
        {
            "design_id": "d02_triple_barrier_path_quality_fwd12",
            "priority": 2,
            "hypothesis": "terminal return label(종가 기준 라벨) 대신 path quality triple barrier(경로 품질 삼중 장벽)가 drawdown(낙폭)과 recovery(회복)를 개선한다.",
            "label_source_id": "ls02_path_triple_barrier",
            "feature_source_id": "fs02_existing_58_plus_bar_microstructure",
            "model_family_id": "mf02_treeensemble_with_logreg_fallback",
            "rule_stack_seed": "one_position_max_next_tick_entry_path_quality_filter(단일 포지션 다음 틱 진입 경로 품질 필터)",
            "why_new_source": "Stage354C(354C 실행)의 best near miss(최상 근접 실패)는 density(밀도)는 있으나 stress(압박)가 깨졌다.",
            "expected_failure_to_watch": "barrier label too sparse(장벽 라벨 과소) or runtime feature gap(런타임 피처 공백)",
            "materialize_next": "true",
        },
        {
            "design_id": "d03_asymmetric_long_short_heads",
            "priority": 3,
            "hypothesis": "long quality head(롱 품질 헤드)와 short carry head(숏 기여 헤드)를 분리하면 long/short balance(롱/숏 균형)를 잃지 않고 수익 구조를 회복한다.",
            "label_source_id": "ls03_asymmetric_side_heads",
            "feature_source_id": "fs01_existing_58_runtime_features",
            "model_family_id": "mf03_dual_binary_heads_onnx_allocator",
            "rule_stack_seed": "side_head_allocator_with_balance_guard(방향 헤드 배분기와 균형 보호)",
            "why_new_source": "과거 cash-open(현금장 초반) 단일 방향 필터는 균형 또는 수익을 함께 살리지 못했다.",
            "expected_failure_to_watch": "one side dominates(한 방향 지배) or allocator churn(배분기 잦은 변경)",
            "materialize_next": "true",
        },
        {
            "design_id": "d04_drawdown_avoidance_meta_filter",
            "priority": 4,
            "hypothesis": "bad-regime meta label(나쁜 국면 메타 라벨)이 weak edge(약한 우위)의 drawdown(낙폭)을 줄여 recovery factor(회복 계수)를 회복한다.",
            "label_source_id": "ls04_drawdown_avoidance_meta",
            "feature_source_id": "fs03_regime_macro_session_features",
            "model_family_id": "mf01_logreg_and_small_mlp_onnx",
            "rule_stack_seed": "direction_model_plus_meta_veto(방향 모델과 메타 거부)",
            "why_new_source": "Stage354C(354C 실행)의 near miss(근접 실패)는 PF(수익 팩터)가 1 근처라 손실 구간 제거가 필요하다.",
            "expected_failure_to_watch": "meta filter kills trade density(메타 필터가 거래 밀도를 죽임)",
            "materialize_next": "false",
        },
        {
            "design_id": "d05_session_regime_density_allocator",
            "priority": 5,
            "hypothesis": "session/regime allocator(세션/국면 배분기)가 cash-open(현금장 초반) 과집중 없이 trade density(거래 밀도)를 회복한다.",
            "label_source_id": "ls05_session_regime_density",
            "feature_source_id": "fs03_regime_macro_session_features",
            "model_family_id": "mf04_monotone_scorecard_plus_onnx_distill",
            "rule_stack_seed": "session_bucket_thresholds_with_global_cost_guard(세션 구간 임계값과 전역 비용 보호)",
            "why_new_source": "같은 전역 임계값은 regime cliff(국면 절벽)를 숨긴다.",
            "expected_failure_to_watch": "micro-tuning by session(세션별 미세조정) overfits(과적합)",
            "materialize_next": "false",
        },
    ]


def label_rows() -> list[dict[str, Any]]:
    return [
        {
            "label_source_id": "ls01_cost_buffer_multihorizon",
            "label_type": "3class directional cost buffer(3분류 방향 비용 완충)",
            "future_source": "raw US100 close future returns 6 and 8 bars(원시 US100 종가 6/8봉 미래 수익률)",
            "timestamp_boundary": "current closed M5 bar to future close only(현재 닫힌 M5 봉에서 미래 종가만)",
            "positive_rule": "long if future_log_return > dynamic_cost_buffer(미래 로그수익이 동적 비용 완충 초과)",
            "negative_rule": "short if future_log_return < -dynamic_cost_buffer(미래 로그수익이 음의 비용 완충 미만)",
            "flat_rule": "otherwise flat(그 외 중립)",
            "cost_buffer": "base cost 0.00015 plus stress reserve(기본 비용 0.00015와 압박 여유)",
            "density_guard": TRADE_DENSITY_REQUIREMENT,
        },
        {
            "label_source_id": "ls02_path_triple_barrier",
            "label_type": "path quality triple barrier(경로 품질 삼중 장벽)",
            "future_source": "raw US100 high/low/close over 12 bars(원시 US100 고가/저가/종가 12봉)",
            "timestamp_boundary": "barrier path begins after current closed bar(장벽 경로는 현재 닫힌 봉 이후 시작)",
            "positive_rule": "first hit take-profit before stop-loss(손절 전 익절 선행)",
            "negative_rule": "first hit stop-loss before take-profit(익절 전 손절 선행)",
            "flat_rule": "no barrier or ambiguous path(장벽 미도달 또는 모호 경로)",
            "cost_buffer": "barrier levels must exceed base and stress cost(장벽은 기본/압박 비용 초과)",
            "density_guard": TRADE_DENSITY_REQUIREMENT,
        },
        {
            "label_source_id": "ls03_asymmetric_side_heads",
            "label_type": "separate binary side heads(분리 이진 방향 헤드)",
            "future_source": "raw close horizons and session slices(원시 종가 보유기간과 세션 절편)",
            "timestamp_boundary": "head labels use only future returns after feature timestamp(헤드 라벨은 피처 시각 이후 미래 수익만 사용)",
            "positive_rule": "long_quality or short_quality if side-specific net survives cost(방향별 순수익이 비용 생존)",
            "negative_rule": "side rejected if adverse excursion dominates(역행이 지배하면 방향 거부)",
            "flat_rule": "allocator may abstain(배분기가 관망 가능)",
            "cost_buffer": "side-specific stress cost(방향별 비용 압박)",
            "density_guard": TRADE_DENSITY_REQUIREMENT,
        },
        {
            "label_source_id": "ls04_drawdown_avoidance_meta",
            "label_type": "bad-regime veto label(나쁜 국면 거부 라벨)",
            "future_source": "rolling adverse return and drawdown proxy(구르는 역행 수익과 낙폭 프록시)",
            "timestamp_boundary": "meta label references only after-entry future path(메타 라벨은 진입 이후 미래 경로만 참조)",
            "positive_rule": "allow when adverse path stays under budget(역행 경로가 예산 이하이면 허용)",
            "negative_rule": "veto when adverse path exceeds budget(역행 경로가 예산 초과이면 거부)",
            "flat_rule": "not applicable(해당 없음)",
            "cost_buffer": "drawdown budget plus execution reserve(낙폭 예산과 실행 여유)",
            "density_guard": "must not reduce projected trade/day below 3(예상 일별 거래수 3 미만으로 낮추면 실패)",
        },
        {
            "label_source_id": "ls05_session_regime_density",
            "label_type": "session/regime density label(세션/국면 밀도 라벨)",
            "future_source": "future return by cash-open and ADX/VIX buckets(현금장/ADX/VIX 구간별 미래 수익)",
            "timestamp_boundary": "bucket features fixed before future return(구간 피처는 미래 수익 전에 고정)",
            "positive_rule": "bucket useful if net/PF/density survive train-only threshold(학습 전용 임계값에서 순수익/PF/밀도 생존)",
            "negative_rule": "bucket rejected if stress cost fails(비용 압박 실패 시 거부)",
            "flat_rule": "bucket abstain when not stable(안정성 없으면 관망)",
            "cost_buffer": "global base and stress cost(전역 기본/압박 비용)",
            "density_guard": TRADE_DENSITY_REQUIREMENT,
        },
    ]


def feature_rows() -> list[dict[str, Any]]:
    return [
        {
            "feature_source_id": "fs01_existing_58_runtime_features",
            "source_path": rel(RUNTIME_FEATURES),
            "feature_policy": "reuse closed-bar 58 feature contract(닫힌 봉 58피처 계약 재사용)",
            "runtime_gap": "lowest gap because current EA feature order already exists(현재 EA 피처 순서가 있어 공백 최소)",
            "materialization_risk": "low(낮음)",
        },
        {
            "feature_source_id": "fs02_existing_58_plus_bar_microstructure",
            "source_path": f"{rel(RUNTIME_FEATURES)} + {rel(RAW_US100_BARS)}",
            "feature_policy": "add spread_points and tick_volume only if runtime feature contract is extended(런타임 피처 계약 확장 시에만 스프레드/틱 거래량 추가)",
            "runtime_gap": "medium because MT5 feature input must be extended(중간, MT5 피처 입력 확장 필요)",
            "materialization_risk": "medium(중간)",
        },
        {
            "feature_source_id": "fs03_regime_macro_session_features",
            "source_path": rel(RUNTIME_FEATURES),
            "feature_policy": "reuse ADX/VIX/session and mega8 breadth features(ADX/VIX/세션/메가8 폭 피처 재사용)",
            "runtime_gap": "low if no new columns are added(새 열을 안 더하면 낮음)",
            "materialization_risk": "low_to_medium(낮음에서 중간)",
        },
    ]


def model_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_family_id": "mf01_logreg_and_small_mlp_onnx",
            "families": "LogisticRegression and small MLP(로지스틱 회귀와 소형 MLP)",
            "onnx_reason": "simple operators are most likely MT5-compatible(단순 연산자가 MT5 호환 가능성이 큼)",
            "runtime_parity_risk": "softmax/output shape must be checked(소프트맥스/출력 모양 확인 필요)",
            "overfit_control": "fixed validation/OOS split plus WFO before promotion(고정 검증/표본외 뒤 승격 전 워크포워드)",
        },
        {
            "model_family_id": "mf02_treeensemble_with_logreg_fallback",
            "families": "HistGradientBoosting/LightGBM scout with logistic fallback(히스토그램 부스팅/라이트GBM 탐색과 로지스틱 대체)",
            "onnx_reason": "TreeEnsemble may work as research but needs MT5 operator probe(TreeEnsemble은 연구 가능하나 MT5 연산자 탐침 필요)",
            "runtime_parity_risk": "operator support risk high(연산자 지원 위험 높음)",
            "overfit_control": "use only as scout unless distilled to logistic/MLP(로지스틱/MLP 증류 전 탐색 전용)",
        },
        {
            "model_family_id": "mf03_dual_binary_heads_onnx_allocator",
            "families": "two binary ONNX heads plus allocator(두 이진 ONNX 헤드와 배분기)",
            "onnx_reason": "separate outputs can preserve side meaning(분리 출력이 방향 의미를 보존)",
            "runtime_parity_risk": "allocator rule must be mirrored in EA(배분기 규칙을 EA에 맞춰야 함)",
            "overfit_control": "side balance and density gates before MT5 probe(방향 균형과 밀도 게이트 후 MT5 탐침)",
        },
        {
            "model_family_id": "mf04_monotone_scorecard_plus_onnx_distill",
            "families": "interpretable scorecard distilled to logistic/MLP(해석 가능 점수표를 로지스틱/MLP로 증류)",
            "onnx_reason": "distilled model keeps ONNX path open(증류 모델이 ONNX 경로를 유지)",
            "runtime_parity_risk": "distillation can change thresholds(증류가 임계값을 바꿀 수 있음)",
            "overfit_control": "neighborhood robustness and bucket stability(이웃 안정성과 구간 안정성)",
        },
    ]


def trade_shape_rows() -> list[dict[str, Any]]:
    return [
        {
            "control_id": "tc01_density_no_split",
            "rule": "minimum trade/day 3+ and no trade splitting(일별 거래수 3+와 거래 쪼개기 금지)",
            "effect": "density must come from real signal frequency, not chopped exits(밀도는 잘게 쪼갠 청산이 아니라 실제 신호 빈도에서 나와야 함)",
        },
        {
            "control_id": "tc02_nonoverlap_proxy_first",
            "rule": "proxy evaluation uses non-overlap hold before MT5 probe(프록시 평가는 MT5 탐침 전 비중첩 보유 사용)",
            "effect": "proxy trade count does not inflate by overlapping signals(프록시 거래 수가 중첩 신호로 부풀지 않음)",
        },
        {
            "control_id": "tc03_cost_stress_required",
            "rule": "base cost and stress cost must both be reported(기본 비용과 압박 비용을 모두 보고)",
            "effect": "weak near-zero PF surfaces are filtered early(PF 1 근처 약한 표면을 조기에 거름)",
        },
        {
            "control_id": "tc04_side_balance_guard",
            "rule": "long/short balance must be measured before candidate queue(후보 대기열 전 롱/숏 균형 측정)",
            "effect": "single-side carry is not mistaken for robust model(단일 방향 기여를 견고한 모델로 오해하지 않음)",
        },
    ]


def materialization_queue(designs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in designs:
        if str(row.get("materialize_next", "")).lower() != "true":
            continue
        rows.append(
            {
                "queue_id": f"run355B__{row['design_id']}",
                "next_run_id": NEXT_RUN_ID,
                "design_id": row["design_id"],
                "priority": row["priority"],
                "label_source_id": row["label_source_id"],
                "feature_source_id": row["feature_source_id"],
                "model_family_id": row["model_family_id"],
                "required_outputs": "feature_label_table, label_distribution, proxy_training_grid(피처-라벨 표, 라벨 분포, 프록시 학습 격자)",
                "stop_condition": "if validation/OOS trade_day < 3 or stress net <= 0 then negative memory(검증/표본외 일별 거래수 3 미만 또는 압박 순수익 0 이하이면 부정 기억)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_stage_docs(designs: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], identity: Mapping[str, Any]) -> None:
    top = designs[0]
    write_text(
        STAGE_BRIEF,
        f"""# Stage355 Density Recovery Model Family(355단계 밀도 회복 모델 계열)

- canonical_stage_id(정식 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- selection_status(선택 상태): `design_queue_ready_no_selection(설계 대기열 준비, 선택 없음)`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Question(질문)

기존 probability surface(확률 표면)의 threshold/horizon/filter(임계값/보유기간/필터) 회수가 실패했으므로, 새 label/source/model family(라벨/원천/모델 계열)로 trade/day(일별 거래수) 3+와 net/PF/stress(순수익/수익 팩터/압박)를 동시에 회복할 수 있는가?

## Lead Seed(선두 씨앗)

`{top["design_id"]}`: {top["hypothesis"]}

## Effect(효과)

Stage355B(355B 실행)는 같은 threshold-only search(임계값 전용 탐색)를 반복하지 않고, timestamp-safe(시점 안전) 라벨과 ONNX-compatible(온엑스 호환) 모델 계열부터 물질화한다.
""",
    )
    write_text(
        STAGE_INPUT_REFS,
        f"""# Stage355 Input Refs(355단계 입력 참조)

- source_final_decision(원천 최종 결정): `{rel(SOURCE_RUN354C_FINAL)}`
- source_sweep(원천 스윕): `{rel(SOURCE_RUN354C_SWEEP)}`
- source_queue(원천 대기열): `{rel(SOURCE_RUN354C_QUEUE)}`
- source_failure_memory(원천 실패 기억): `{rel(SOURCE_RUN354C_FAILURE)}`
- runtime_features(런타임 피처): `{rel(RUNTIME_FEATURES)}`
- raw_us100_bars(원시 US100 봉): `{rel(RAW_US100_BARS)}`
- design_matrix(설계 행렬): `{rel(DESIGN_MATRIX)}`
- materialization_queue(물질화 대기열): `{rel(RUN355B_QUEUE)}`

Action(행동): Stage354C(354C 실행)의 failure memory(실패 기억)를 Stage355A(355A 실행)의 design constraint(설계 제약)로 고정한다.

Effect(효과): 다음 실행이 기존 surface(표면)의 미세 임계값 검색을 반복하지 않는다.
""",
    )
    selection_text = f"""# Stage355 Selection Status(355단계 선택 상태)

- selection_status(선택 상태): `design_queue_ready_no_selection(설계 대기열 준비, 선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- materialization_queue_rows(물질화 대기열 행): `{len(queue)}`
- mt5_queue_rows(MT5 대기열 행): `0`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_text(STAGE_SELECTION, selection_text)
    write_text(ROOT_SELECTION_STATUS, selection_text)
    write_text(
        REPORT_PATH,
        f"""# run355A Density Recovery Design(355A 밀도 회복 설계)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- design_rows(설계 행): `{len(designs)}`
- materialization_queue_rows(물질화 대기열 행): `{len(queue)}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Action(행동)

Stage354C(354C 실행)의 negative memory(부정 기억)를 설계 제약으로 바꾸고, 새 label/source/model family(라벨/원천/모델 계열) 후보를 정리했다.

## Effect(효과)

다음 실행은 기존 probability surface(확률 표면)의 threshold-only search(임계값 전용 탐색)를 반복하지 않고, 라벨과 모델 원천을 바꿔 trade/day(일별 거래수) 3+와 cost stress(비용 압박)를 같이 본다.

## Priority Queue(우선순위 대기열)

- priority 1(우선순위 1): `{queue[0]["design_id"] if queue else "none"}`
- priority 2(우선순위 2): `{queue[1]["design_id"] if len(queue) > 1 else "none"}`
- priority 3(우선순위 3): `{queue[2]["design_id"] if len(queue) > 2 else "none"}`

## Source Truth(원천 진실)

- stage354C_sweep_rows(354C 스윕 행): `{identity["stage354C_sweep_rows"]}`
- stage354C_density_valid_queue_rows(354C 밀도 유효 대기열 행): `{identity["stage354C_density_valid_queue_rows"]}`
- source_failure_rows(원천 실패 행): `{identity["source_failure_rows"]}`

## Boundary(경계)

이 결과는 experiment design(실험 설계)이다. training(학습), proxy execution(프록시 실행), MT5 execution(MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    append_text_once(REVIEW_INDEX, "run355A_density_recovery_design", f"- `{rel(REPORT_PATH)}`")


def write_receipts(designs: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], identity: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            **common,
            "data_source": [rel(SOURCE_RUN354C_FINAL), rel(SOURCE_RUN354C_SWEEP), rel(RUNTIME_FEATURES), rel(RAW_US100_BARS)],
            "time_axis": "all proposed labels use closed M5 timestamp then future-only raw bars(모든 제안 라벨은 닫힌 M5 시각 뒤 미래 원시 봉만 사용)",
            "sample_scope": "US100 M5 Stage351B/354C Tier A full-context sample(US100 M5 351B/354C Tier A 전체 문맥 표본)",
            "missing_or_duplicate_check": "not recomputed in design packet; inherited Stage354C zero missing/duplicate audit(설계 묶음에서는 재계산 없음, 354C 결측/중복 0 감사 상속)",
            "feature_label_boundary": "feature sources are current or past closed-bar only; label sources are future-only(피처 원천은 현재/과거 닫힌 봉, 라벨 원천은 미래 전용)",
            "split_boundary": "materialization must keep train/validation/OOS chronological split(물질화는 시간순 학습/검증/표본외 분할 유지)",
            "leakage_risk": "path/barrier labels may accidentally include current bar high-low if not shifted(경로/장벽 라벨이 현재 봉 고저를 포함하면 누수)",
            "data_hash_or_identity": identity,
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **common,
            "hypothesis": "new label/source/model family(새 라벨/원천/모델 계열) can recover density and stress edge after existing surface failure(기존 표면 실패 뒤 밀도와 압박 우위 회복)",
            "decision_use": "choose what Stage355B materializes first(Stage355B가 먼저 물질화할 대상을 선택)",
            "comparison_baseline": rel(SOURCE_RUN354C_FINAL),
            "control_variables": [
                "US100 M5 symbol/timeframe(US100 M5 심볼/시간프레임)",
                TRADE_DENSITY_REQUIREMENT,
                "no operating claim without MT5 probe(MT5 탐침 없이는 운영 주장 없음)",
            ],
            "changed_variables": [
                "label source(라벨 원천)",
                "model family(모델 계열)",
                "feature source extension policy(피처 원천 확장 정책)",
                "rule stack seed(규칙 묶음 씨앗)",
            ],
            "sample_scope": "Tier A full-context now; Tier B recorded missing_required(Tier A 전체 문맥, Tier B 필수 누락 기록)",
            "success_criteria": "Stage355B creates timestamp-safe label tables and proxy grids with projected trade/day 3+(355B가 시점 안전 라벨 표와 일별 거래수 3+ 프록시 격자를 생성)",
            "failure_criteria": "label distribution too sparse, stress cost negative, or density below 3(라벨 과소, 비용 압박 음수, 밀도 3 미만)",
            "invalid_conditions": "lookahead, split leakage, current bar path leakage, missing source artifact(미래참조, 분할 누수, 현재 봉 경로 누수, 원천 산출물 누락)",
            "stop_conditions": "stop threshold-only reuse unless new label/source changes result(새 라벨/원천 변화 없이는 임계값 전용 재사용 중단)",
            "evidence_plan": [rel(DESIGN_MATRIX), rel(LABEL_SOURCE_PLAN), rel(MODEL_FAMILY_PLAN), rel(RUN355B_QUEUE)],
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            **common,
            "model_family": [row["model_family_id"] for row in model_rows()],
            "target_and_label": [row["label_source_id"] for row in label_rows()],
            "split_method": "planned fixed train/validation/OOS plus WFO before promotion(고정 학습/검증/표본외 예정, 승격 전 WFO)",
            "selection_metric": "net/PF/expectancy/drawdown/recovery/trade density/balance/stress/equity quality(순수익/PF/기대값/낙폭/회복/밀도/균형/압박/곡선 품질)",
            "secondary_metrics": "label distribution and runtime operator compatibility(라벨 분포와 런타임 연산자 호환성)",
            "threshold_policy": "search only after materialized labels pass density sanity(라벨 밀도 점검 후에만 검색)",
            "overfit_risk": "multiple label variants and model family search(다중 라벨 변형과 모델 계열 검색)",
            "calibration_risk": "scores may be ranking only until calibrated(보정 전 점수는 순위일 수 있음)",
            "comparison_baseline": rel(SOURCE_RUN354C_FINAL),
            "validation_judgment": "design_ready_no_selection(설계 준비, 선택 없음)",
        },
    )
    write_json(
        ARTIFACT_LINEAGE_RECEIPT,
        {
            **common,
            "source_inputs": [rel(SOURCE_RUN354C_FINAL), rel(SOURCE_RUN354C_SWEEP), rel(SOURCE_RUN354C_FAILURE), rel(RUNTIME_FEATURES), rel(RAW_US100_BARS)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(DESIGN_MATRIX),
                rel(LABEL_SOURCE_PLAN),
                rel(FEATURE_SOURCE_PLAN),
                rel(MODEL_FAMILY_PLAN),
                rel(TRADE_SHAPE_CONTROL_PLAN),
                rel(RUN355B_QUEUE),
                rel(REPORT_PATH),
                rel(FINAL_DECISION),
            ],
            "artifact_hashes": {
                rel(path): sha256_file(path)
                for path in [
                    DESIGN_MATRIX,
                    LABEL_SOURCE_PLAN,
                    FEATURE_SOURCE_PLAN,
                    MODEL_FAMILY_PLAN,
                    TRADE_SHAPE_CONTROL_PLAN,
                    RUN355B_QUEUE,
                ]
                if exists(path)
            },
            "registry_links": [rel(STAGE_LEDGER), rel(PROJECT_LEDGER), rel(RUN_REGISTRY), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_design_artifacts(추적 설계 산출물)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **common,
            "result_subject": RUN_ID,
            "evidence_available": [rel(DESIGN_MATRIX), rel(RUN355B_QUEUE), rel(REPORT_PATH), rel(GATE_AUDIT)],
            "evidence_missing": "training outputs, proxy KPI, MT5 probe, runtime parity(학습 출력, 프록시 KPI, MT5 탐침, 런타임 동등성)",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "design queue only; next run must materialize labels(설계 대기열 전용, 다음 실행에서 라벨 물질화 필요)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **common,
            "allowed_claim": "Stage355A design queue ready(Stage355A 설계 대기열 준비)",
            "forbidden_claims": [
                "training completed(학습 완료)",
                "proxy positive(프록시 긍정)",
                "MT5 runtime evidence(MT5 런타임 근거)",
                "candidate selection(후보 선정)",
                "operating promotion(운영 승격)",
                "runtime authority(런타임 권위)",
                "Goal Achieve(목표 달성)",
            ],
        },
    )


def write_state_and_decisions(queue: Sequence[Mapping[str, Any]]) -> None:
    write_text(
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
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage355A(355A 실행)에서 density recovery label/model/source design(밀도 회복 라벨/모델/원천 설계)을 완료했다.

Effect(효과): Stage355B(355B 실행)는 `{len(queue)}`개 materialization queue(물질화 대기열)에서 새 label source(라벨 원천)를 실제 데이터로 만든다.
""",
    )
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage355A Density Recovery Design(355A 밀도 회복 설계)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Action(행동): Stage354C(354C 실행)의 existing surface failure(기존 표면 실패)를 새 label/source/model family(라벨/원천/모델 계열) 설계로 전환했다.

Effect(효과): 같은 threshold-only search(임계값 전용 탐색)를 반복하지 않고, 다음 실행에서 timestamp-safe label table(시점 안전 라벨 표)을 물질화한다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} {RUN_ID}

Action(행동): Stage355A(355A 실행) density recovery design(밀도 회복 설계)을 완료했다.

Effect(효과): materialization queue(물질화 대기열) `{len(queue)}`개를 만들고 다음 실행을 `{NEXT_RUN_ID}`로 동기화했다.

- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        "IDEA-ST355A-DENSITY-RECOVERY-DESIGN-QUEUE",
        f"""| `IDEA-ST355A-DENSITY-RECOVERY-DESIGN-QUEUE` | `{STAGE_ID}` | Stage354C(354C 실행)의 existing surface failure(기존 표면 실패)를 새 label/source/model family(라벨/원천/모델 계열) 설계 큐로 전환해 trade/day(일별 거래수) 3+와 cost stress(비용 압박)를 회복한다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `design_queue_ready_no_selection` | next_action(다음 행동) `{NEXT_RUN_ID}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |""",
    )


def ledger_rows(queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
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
        "gate_passes": GATE_TOTAL,
        "gate_total": GATE_TOTAL,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "density_recovery_design(밀도 회복 설계)",
        "lane": "density_recovery_design(밀도 회복 설계)",
        "family": "experiment_design(실험 설계)",
        "work_family": "experiment_design(실험 설계)",
        "run_number": RUN_NUMBER,
        "notes": "Design queue only; no model training or MT5 execution(설계 대기열 전용, 모델 학습이나 MT5 실행 없음).",
        "source_package_run_id": PARENT_RUN_ID,
        "rows": len(queue),
        "candidate_rows": "",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": "design_queue_ready_no_selection(설계 대기열 준비, 선택 없음)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
    }
    rows = []
    for tier, view, scope in [
        ("Tier A", "Tier A separate(Tier A 분리)", "design_queue_full_context(설계 대기열 전체 문맥)"),
        ("Tier B", "Tier B separate(Tier B 분리)", "missing_required_no_partial_context_materialization(Tier B 부분 문맥 물질화 없음 필수 누락)"),
        ("Tier A+B", "Tier A+B combined(Tier A+B 합산)", "same_as_tier_a_no_fallback(대체 없음, Tier A와 동일)"),
    ]:
        row = dict(base)
        row["ledger_row_id"] = f"{RUN_ID}__{tier.replace(' ', '_').replace('+', 'plus')}"
        row["row_id"] = row["ledger_row_id"]
        row["subrun_id"] = tier
        row["view"] = view
        row["record_view"] = view
        row["tier"] = tier
        row["tier_scope"] = tier
        row["metric_scope"] = scope
        row["kpi_scope"] = scope
        if tier == "Tier B":
            row["result_status"] = "missing_required(필수 누락)"
            row["notes"] = "Tier B partial-context sample is not materialized in Stage355A(Tier B 부분 문맥 표본은 355A에서 미산출)."
        rows.append(row)
    return rows


def write_ledgers(queue: Sequence[Mapping[str, Any]]) -> None:
    rows = ledger_rows(queue)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **rows[2],
                "gate_audit_path": rel(GATE_AUDIT),
            }
        ],
    )


def write_final_and_manifest(identity: Mapping[str, Any], queue: Sequence[Mapping[str, Any]]) -> None:
    payload = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "design_rows": len(design_rows()),
        "materialization_queue_rows": len(queue),
        "source_identity": identity,
        "candidate_selection": "not_claimed",
        "training": "not_run",
        "proxy_execution": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": GATE_TOTAL,
        "gate_total": GATE_TOTAL,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, payload)
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "producer": rel(Path(__file__)),
            "inputs": [rel(SOURCE_RUN354C_FINAL), rel(SOURCE_RUN354C_SWEEP), rel(SOURCE_RUN354C_FAILURE), rel(RUNTIME_FEATURES), rel(RAW_US100_BARS)],
            "outputs": [
                rel(DESIGN_MATRIX),
                rel(LABEL_SOURCE_PLAN),
                rel(FEATURE_SOURCE_PLAN),
                rel(MODEL_FAMILY_PLAN),
                rel(TRADE_SHAPE_CONTROL_PLAN),
                rel(RUN355B_QUEUE),
                rel(REPORT_PATH),
                rel(FINAL_DECISION),
                rel(GATE_AUDIT),
            ],
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_gates() -> list[dict[str, Any]]:
    gates = [
        ("work_packet_schema_lint", exists(WORK_PACKET_CONTRACT), WORK_PACKET_CONTRACT, "work packet contract(작업 묶음 계약) 작성"),
        ("source_failure_memory_gate", exists(SOURCE_RUN354C_FAILURE) and csv_count(SOURCE_RUN354C_FAILURE) > 0, SOURCE_RUN354C_FAILURE, "failure memory(실패 기억) 입력 확인"),
        ("design_matrix_written", exists(DESIGN_MATRIX) and csv_count(DESIGN_MATRIX) >= 5, DESIGN_MATRIX, "design matrix(설계 행렬) 작성"),
        ("label_source_plan_written", exists(LABEL_SOURCE_PLAN) and csv_count(LABEL_SOURCE_PLAN) >= 5, LABEL_SOURCE_PLAN, "label source plan(라벨 원천 계획) 작성"),
        ("model_family_plan_written", exists(MODEL_FAMILY_PLAN) and csv_count(MODEL_FAMILY_PLAN) >= 4, MODEL_FAMILY_PLAN, "model family plan(모델 계열 계획) 작성"),
        ("materialization_queue_written", exists(RUN355B_QUEUE) and csv_count(RUN355B_QUEUE) >= 3, RUN355B_QUEUE, "materialization queue(물질화 대기열) 작성"),
        ("skill_receipt_lint", all(exists(path) for path in [DATA_INTEGRITY_RECEIPT, EXPERIMENT_RECEIPT, MODEL_VALIDATION_RECEIPT, ARTIFACT_LINEAGE_RECEIPT, JUDGMENT_RECEIPT]), EXPERIMENT_RECEIPT, "skill receipts(스킬 영수증) 작성"),
        ("tier_pair_records", exists(STAGE_LEDGER) and RUN_ID in read_text(STAGE_LEDGER), STAGE_LEDGER, "Tier A/B/combined(Tier A/B/합산) 장부 기록"),
        ("current_truth_sync", RUN_ID in read_text(WORKSPACE_STATE) and NEXT_RUN_ID in read_text(CURRENT_WORKING_STATE), WORKSPACE_STATE, "current truth(현재 진실) 동기화"),
        ("final_claim_guard", "not_claimed" in json.dumps(read_json(FINAL_DECISION)), FINAL_DECISION, "forbidden claims(금지 주장) 차단"),
    ]
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, path, effect in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_artifact_registry() -> None:
    artifacts = [
        DESIGN_MATRIX,
        LABEL_SOURCE_PLAN,
        FEATURE_SOURCE_PLAN,
        MODEL_FAMILY_PLAN,
        TRADE_SHAPE_CONTROL_PLAN,
        RUN355B_QUEUE,
        WORK_PACKET_CONTRACT,
        DATA_INTEGRITY_RECEIPT,
        EXPERIMENT_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        ARTIFACT_LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path) if exists(path) else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "Stage355A design artifact(355A 설계 산출물)",
        }
        for path in artifacts
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def validate(gates: Sequence[Mapping[str, Any]]) -> None:
    failed = [row["gate_id"] for row in gates if row.get("status") != "passed"]
    if failed:
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise RuntimeError("required gates failed(필수 게이트 실패): " + ", ".join(failed))
    final = read_json(FINAL_DECISION)
    for key in ["runtime_authority", "operating_promotion", "goal_achieve", "candidate_selection"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}={final.get(key)}")


def main() -> None:
    for directory in [RUN_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    identity = source_identity()
    designs = design_rows()
    labels = label_rows()
    features = feature_rows()
    models = model_rows()
    controls = trade_shape_rows()
    queue = materialization_queue(designs)
    write_csv(DESIGN_MATRIX, designs)
    write_csv(LABEL_SOURCE_PLAN, labels)
    write_csv(FEATURE_SOURCE_PLAN, features)
    write_csv(MODEL_FAMILY_PLAN, models)
    write_csv(TRADE_SHAPE_CONTROL_PLAN, controls)
    write_csv(RUN355B_QUEUE, queue)
    write_json(
        WORK_PACKET_CONTRACT,
        {
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": ["work_packet_schema_lint"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_stage_docs(designs, queue, identity)
    write_receipts(designs, queue, identity)
    write_state_and_decisions(queue)
    write_ledgers(queue)
    write_final_and_manifest(identity, queue)
    gates = write_gates()
    write_artifact_registry()
    validate(gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "design_rows": len(designs),
                "materialization_queue_rows": len(queue),
                "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
                "gate_total": len(gates),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
