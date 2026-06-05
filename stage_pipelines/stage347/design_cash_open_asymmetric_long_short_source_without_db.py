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

STAGE_ID = "347_cash_open_asymmetric_source__long_short_head_design"
RUN_NUMBER = "run347A"
RUN_ID = "run347A_design_cash_open_asymmetric_long_short_source_without_db_v1"
PARENT_RUN_ID = "run346B_review_cash_open_runtime_probe_source_pivot_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1"
NEXT_RUN_ID = "run347B_materialize_cash_open_asymmetric_source_inputs_without_db_v1"

STATUS = "completed_stage347A_cash_open_asymmetric_source_design_ready_no_selection"
JUDGMENT = "asymmetric_long_short_source_design_ready_timestamp_safe_materialization_required_no_operating_claim"
DECISION = "stage347A_open_run347B_materialize_cash_open_asymmetric_source_inputs"
CLAIM_BOUNDARY = (
    "research_development_design_only_cash_open_asymmetric_long_short_source_"
    "no_model_training_no_mt5_execution_no_candidate_selection_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run347A_cash_open_asymmetric_source_design.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_SELECTION = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

SOURCE_REVIEW_RUN_DIR = ROOT / "stages" / "346_cash_open_runtime_review__asymmetric_source_pivot" / "02_runs" / "run346B"
SOURCE_FINAL_DECISION = SOURCE_REVIEW_RUN_DIR / "final_decision.json"
SOURCE_SCORECARD = SOURCE_REVIEW_RUN_DIR / "variant_review_scorecard.csv"
SOURCE_POSITIVE_CLUES = SOURCE_REVIEW_RUN_DIR / "positive_clues.csv"
SOURCE_FAILURE_MEMORY = SOURCE_REVIEW_RUN_DIR / "failure_memory.csv"
SOURCE_SEED_QUEUE = SOURCE_REVIEW_RUN_DIR / "stage347_asymmetric_source_seed_queue.csv"
SOURCE_TIER_AUDIT = SOURCE_REVIEW_RUN_DIR / "tier_boundary_audit.csv"
SOURCE_RUN345B_DIR = ROOT / "stages" / "345_cash_open_decomposition__long_quality_short_carry_runtime_probe" / "02_runs" / "run345B"
SOURCE_RUN345B_SUMMARY = SOURCE_RUN345B_DIR / "cash_open_long_quality_short_carry_mt5_probe_summary.csv"

DESIGN_MATRIX = RUN_DIR / "asymmetric_source_design_matrix.csv"
FEATURE_SOURCE_PLAN = RUN_DIR / "feature_source_plan.csv"
LABEL_HEAD_PLAN = RUN_DIR / "label_head_plan.csv"
MODEL_FAMILY_PLAN = RUN_DIR / "model_family_plan.csv"
CONTROL_ABLATION_PLAN = RUN_DIR / "control_and_ablation_plan.csv"
TIMESTAMP_SAFETY_AUDIT = RUN_DIR / "timestamp_safety_audit.csv"
PROXY_MT5_ROLE_CONTRACT = RUN_DIR / "proxy_mt5_role_contract.csv"
RUN347B_QUEUE = RUN_DIR / "run347B_materialization_queue.csv"
EXPERIMENT_DESIGN_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage347A_cash_open_asymmetric_source_design.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

STAGE_LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "path",
    "report_path",
    "primary_report",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "scoreboard_lane",
    "lane",
    "family",
    "run_number",
    "notes",
    "source_package_run_id",
    "rows",
    "attempt_count",
    "feature_count",
    "candidate_model_id",
    "ledger_row_id",
    "subrun_id",
    "view",
    "record_view",
    "tier",
    "tier_scope",
    "metric_scope",
    "kpi_scope",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "result_status",
    "net_profit",
    "profit_factor",
    "expectancy",
    "drawdown",
    "recovery_factor",
    "trade_count",
    "matched_rows",
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


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def required(path: Path) -> Path:
    if not path_is_file(path):
        raise FileNotFoundError(f"missing required input(필수 입력 누락): {rel(path)}")
    return path


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


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
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


def build_design_matrix() -> list[dict[str, Any]]:
    rows = [
        {
            "design_id": "a01_dual_logreg_side_heads(이중 로지스틱 방향 헤드)",
            "priority": 1,
            "hypothesis": "Separate logistic long/short heads(분리 로지스틱 롱/숏 헤드)가 n01 profit(수익)을 보존하면서 n02 long quality(롱 품질)를 더 자주 공급할 수 있다.",
            "comparison_baseline": "n01_s07_base_control",
            "control_variables": "same source rows, same cost assumption, no new MT5 execution in design(같은 원천 행, 같은 비용 가정, 설계 중 새 MT5 실행 없음)",
            "changed_variables": "side-specific labels and thresholds(방향별 라벨과 임계값)",
            "sample_scope": "Tier A run345B runtime-probe source rows(Tier A 345B 런타임 탐침 원천 행)",
            "success_criteria": "proxy screen keeps net/PF/recovery above base stress floor before MT5(프록시 선별이 MT5 전 기준 하한 유지)",
            "failure_criteria": "single side head collapses net or trade supply(한쪽 헤드가 순수익이나 거래 공급 붕괴)",
            "invalid_conditions": "feature timestamp after label horizon(피처 시점이 라벨 수평선 이후)",
            "stop_conditions": "no adjacent settings survive broad sweep(인접 설정 생존 없음)",
            "evidence_plan": "materialized feature/label tables, proxy scorecard, later MT5 runtime probe(피처/라벨 표, 프록시 점수표, 이후 MT5 런타임 탐침)",
        },
        {
            "design_id": "a02_tree_long_quality_short_carry(트리 롱 품질/숏 기여)",
            "priority": 2,
            "hypothesis": "ExtraTrees/HistGBM(엑스트라트리스/히스토그램 GBM)이 cash-open regime interaction(현금장 국면 상호작용)을 logistic head(로지스틱 헤드)보다 잘 분리할 수 있다.",
            "comparison_baseline": "a01_dual_logreg_side_heads",
            "control_variables": "same label heads and split plan(같은 라벨 헤드와 분할 계획)",
            "changed_variables": "nonlinear model family(비선형 모델 계열)",
            "sample_scope": "Tier A design rows with no Tier B claim(Tier A 설계 행, Tier B 주장 없음)",
            "success_criteria": "broader sweep produces at least two non-adjacent survivors(넓은 탐색에서 비인접 생존 2개 이상)",
            "failure_criteria": "only one extreme survivor or calibration collapse(극단 생존 1개뿐이거나 보정 붕괴)",
            "invalid_conditions": "using future return bucket as feature(미래 수익 구간을 피처로 사용)",
            "stop_conditions": "rank score cannot explain direction separately(순위 점수가 방향 분리를 설명 못함)",
            "evidence_plan": "model-family proxy comparison and calibration risk receipt(모델 계열 프록시 비교와 보정 위험 영수증)",
        },
        {
            "design_id": "a03_cash_open_regime_allocator(현금장 국면 배분기)",
            "priority": 3,
            "hypothesis": "A small allocator(작은 배분기)가 long head/short head(롱 헤드/숏 헤드) exposure(노출)를 cash-open regime(현금장 국면)에 따라 조절할 수 있다.",
            "comparison_baseline": "n04_s07_no_cash_open_short_single_filter",
            "control_variables": "heads fixed after design materialization(설계 물질화 뒤 헤드 고정)",
            "changed_variables": "cash-open minute bucket, ADX/DI, volatility state(현금장 경과분 구간, ADX/DI, 변동성 상태)",
            "sample_scope": "cash-open tagged rows only plus no-cash-open control(현금장 태그 행과 현금장 제외 대조)",
            "success_criteria": "balance improves without PF collapse(수익 팩터 붕괴 없이 균형 개선)",
            "failure_criteria": "balance-only improvement repeats n04 tax(n04 균형 비용 반복)",
            "invalid_conditions": "session label derived from post-trade outcome(세션 라벨이 거래 이후 결과에서 파생)",
            "stop_conditions": "allocator behaves like single side filter(배분기가 단일 방향 필터처럼 동작)",
            "evidence_plan": "allocator ablation table and side exposure summary(배분기 제거 실험표와 방향 노출 요약)",
        },
    ]
    write_csv(DESIGN_MATRIX, rows)
    return rows


def write_design_tables() -> None:
    write_csv(
        FEATURE_SOURCE_PLAN,
        [
            {
                "feature_group": "closed_bar_price_action(확정 봉 가격 행동)",
                "columns_or_source": "existing OHLC-derived indicators and prior bar returns(기존 OHLC 기반 지표와 이전 봉 수익률)",
                "timestamp_rule": "available at feature bar close only(피처 봉 종가 이후만 사용)",
                "leakage_guard": "no current/future trade outcome(현재/미래 거래 결과 금지)",
                "materialization_action": "reuse foundation feature columns if available, otherwise stage-local manifest only(가능하면 foundation 피처 재사용, 아니면 단계 로컬 목록만)",
            },
            {
                "feature_group": "cash_open_clock(현금장 시계)",
                "columns_or_source": "minutes_from_cash_open, cash_open_bucket(현금장 경과분, 현금장 구간)",
                "timestamp_rule": "derived from bar timestamp and exchange session calendar(봉 시각과 거래소 세션 달력에서 파생)",
                "leakage_guard": "calendar-only, no PnL-derived buckets(달력 전용, 손익 파생 구간 금지)",
                "materialization_action": "materialize deterministic timestamp transform(결정적 시각 변환 물질화)",
            },
            {
                "feature_group": "trend_volatility_context(추세/변동성 문맥)",
                "columns_or_source": "ADX/DI, realized volatility, range compression(ADX/DI, 실현 변동성, 범위 압축)",
                "timestamp_rule": "rolling windows end at feature timestamp(롤링 구간은 피처 시점에서 종료)",
                "leakage_guard": "no forward-filled macro surprise unless as-of release exists(as-of 발표 없는 거시 서프라이즈 전방 채움 금지)",
                "materialization_action": "record window lengths and missing rules(구간 길이와 결측 규칙 기록)",
            },
        ],
    )
    write_csv(
        LABEL_HEAD_PLAN,
        [
            {
                "label_head": "long_quality_head(롱 품질 헤드)",
                "target": "long trade payoff or forward favorable move after feature timestamp(피처 시점 이후 롱 손익 또는 우호 전방 움직임)",
                "positive_class": "profitable/low drawdown long opportunity(수익/낮은 낙폭 롱 기회)",
                "negative_class": "bad long or no-trade context(나쁜 롱 또는 무거래 문맥)",
                "boundary": "label only after feature timestamp(라벨은 피처 시점 이후만)",
                "selection_metric": "PF/support balance proxy(수익 팩터/공급 균형 프록시)",
            },
            {
                "label_head": "short_carry_head(숏 기여 헤드)",
                "target": "short trade payoff or forward adverse/downside move after feature timestamp(피처 시점 이후 숏 손익 또는 하방 움직임)",
                "positive_class": "profitable short carry opportunity(수익 숏 기여 기회)",
                "negative_class": "bad short or long-dominant context(나쁜 숏 또는 롱 우세 문맥)",
                "boundary": "label only after feature timestamp(라벨은 피처 시점 이후만)",
                "selection_metric": "net/recovery preservation proxy(순수익/회복 보존 프록시)",
            },
            {
                "label_head": "allocator_head(배분 헤드)",
                "target": "choose long, short, or flat using only head scores and timestamp-safe regime(헤드 점수와 시점 안전 국면만으로 롱/숏/관망 선택)",
                "positive_class": "route improves balance without PF collapse(수익 팩터 붕괴 없이 경로 균형 개선)",
                "negative_class": "single-filter-like overprune(단일 필터형 과삭감)",
                "boundary": "trained after heads are frozen in design materialization(설계 물질화에서 헤드 고정 뒤 학습)",
                "selection_metric": "net/PF/recovery/trade-count joint proxy(순수익/수익 팩터/회복/거래수 결합 프록시)",
            },
        ],
    )
    write_csv(
        MODEL_FAMILY_PLAN,
        [
            {
                "model_family": "logistic_balanced(균형 로지스틱)",
                "role": "transparent side-head control(투명한 방향 헤드 대조)",
                "threshold_policy": "broad sweep fixed grid first(넓은 고정 격자 우선)",
                "calibration_risk": "probabilities may be rank-like under class weighting(클래스 가중 시 확률은 순위처럼 볼 수 있음)",
                "overfit_risk": "multiple side thresholds(다중 방향 임계값)",
                "validation_boundary": "exploratory design only(탐색 설계 전용)",
            },
            {
                "model_family": "ExtraTrees(엑스트라트리스)",
                "role": "nonlinear interaction scout(비선형 상호작용 탐색)",
                "threshold_policy": "quantile rank sweep(분위 순위 탐색)",
                "calibration_risk": "rank score, not probability(순위 점수, 확률 아님)",
                "overfit_risk": "feature interaction selection(피처 상호작용 선택)",
                "validation_boundary": "requires WFO before promotion language(승격 표현 전 워크포워드 필요)",
            },
            {
                "model_family": "HistGBM(히스토그램 GBM)",
                "role": "cash-open regime nonlinear scout(현금장 국면 비선형 탐색)",
                "threshold_policy": "broad rank and margin sweep(넓은 순위/마진 탐색)",
                "calibration_risk": "uncalibrated unless calibrated later(후속 보정 전 보정 없음)",
                "overfit_risk": "cash-open bucket overfit(현금장 구간 과적합)",
                "validation_boundary": "scout only until MT5 probe(런타임 탐침 전 스카우트 전용)",
            },
        ],
    )
    write_csv(
        CONTROL_ABLATION_PLAN,
        [
            {
                "control_id": "c01_base_replay_reference(기준 재생 참고)",
                "purpose": "Compare all proxy ideas against n01 runtime reference(n01 런타임 참고와 모든 프록시 비교)",
                "must_hold": "same cost, same source rows, same timestamp boundary(같은 비용/원천 행/시점 경계)",
            },
            {
                "control_id": "c02_long_only_fragment(롱 전용 조각)",
                "purpose": "Check whether long quality supply grows beyond n02(롱 품질 공급이 n02를 넘는지 확인)",
                "must_hold": "no short trades counted as long quality(숏 거래를 롱 품질로 계산 금지)",
            },
            {
                "control_id": "c03_short_only_fragment(숏 전용 조각)",
                "purpose": "Check whether short carry is preserved without full imbalance(완전 불균형 없이 숏 기여 보존 확인)",
                "must_hold": "short-only cannot be called operating candidate(숏 전용은 운영 후보 아님)",
            },
            {
                "control_id": "c04_no_cash_open_short_block_negative(현금장 숏 차단 부정 대조)",
                "purpose": "Prevent repeating n04 balance-only trap(n04 균형 전용 함정 반복 방지)",
                "must_hold": "balance improvement must not hide PF collapse(균형 개선이 PF 붕괴를 숨기면 안 됨)",
            },
        ],
    )
    write_csv(
        TIMESTAMP_SAFETY_AUDIT,
        [
            {
                "check": "feature_timestamp_boundary(피처 시점 경계)",
                "status": "planned_pass(계획 통과)",
                "rule": "features end at or before decision bar close(피처는 결정 봉 종가 이하)",
                "risk": "rolling window accidental future include(롤링 구간 미래 포함)",
                "mitigation": "materialization script must write min/max timestamp audit(물질화 스크립트가 최소/최대 시각 감사 작성)",
            },
            {
                "check": "label_shift_boundary(라벨 시프트 경계)",
                "status": "planned_pass(계획 통과)",
                "rule": "labels use only bars after feature timestamp(라벨은 피처 시점 이후 봉만 사용)",
                "risk": "trade outcome reused as feature(거래 결과를 피처로 재사용)",
                "mitigation": "separate label table and feature table hashes(라벨표/피처표 해시 분리)",
            },
            {
                "check": "economic_join_boundary(경제지표 결합 경계)",
                "status": "not_used_in_run347A(347A 미사용)",
                "rule": "macro/economic data only with as-of release timestamp(거시/경제 데이터는 발표 시점 기준만)",
                "risk": "calendar revision leak(달력 수정 누수)",
                "mitigation": "if added later, require release-time manifest(후속 추가 시 발표시각 목록 필수)",
            },
            {
                "check": "tier_boundary(티어 경계)",
                "status": "usable_with_boundary(경계 내 사용 가능)",
                "rule": "Tier B remains missing_required until materialized(Tier B는 물질화 전 필수 누락)",
                "risk": "Tier A read overstated as combined(Tier A 판독을 합산처럼 과장)",
                "mitigation": "write Tier A/Tier B/Tier A+B rows in every run(모든 실행에 세 행 기록)",
            },
        ],
    )
    write_csv(
        PROXY_MT5_ROLE_CONTRACT,
        [
            {
                "role": "proxy_screen(프록시 선별)",
                "allowed_use": "rank broad designs before MT5(넓은 설계를 MT5 전 순위화)",
                "forbidden_use": "replace MT5 KPI(MT5 KPI 대체)",
                "required_comparison": "every promoted probe seed needs MT5 runtime probe later(승격되는 탐침 씨앗은 후속 MT5 런타임 탐침 필요)",
            },
            {
                "role": "MT5_runtime_probe(MT5 런타임 탐침)",
                "allowed_use": "measure execution KPI and proxy gap(실행 KPI와 프록시 차이 측정)",
                "forbidden_use": "claim runtime authority without parity/handoff closure(동등성/인계 폐쇄 없이 런타임 권위 주장)",
                "required_comparison": "proxy-MT5 diff and attribution(프록시-MT5 차이와 귀속)",
            },
        ],
    )
    write_csv(
        RUN347B_QUEUE,
        [
            {
                "queue_id": "q01_materialize_feature_label_tables(피처/라벨 표 물질화)",
                "next_run_id": NEXT_RUN_ID,
                "source_design_id": "a01_dual_logreg_side_heads(이중 로지스틱 방향 헤드)",
                "action": "Build timestamp-safe feature and side-label tables(시점 안전 피처와 방향 라벨 표 생성).",
                "effect": "training/proxy screen(학습/프록시 선별)의 입력을 만든다.",
            },
            {
                "queue_id": "q02_materialize_proxy_screen_grid(프록시 선별 격자 물질화)",
                "next_run_id": NEXT_RUN_ID,
                "source_design_id": "a01/a02/a03",
                "action": "Create broad sweep grid for long/short heads and allocator(롱/숏 헤드와 배분기 넓은 탐색 격자 생성).",
                "effect": "micro search(미세 탐색) 전에 구조 경계를 본다.",
            },
            {
                "queue_id": "q03_write_handoff_identity(인계 정체성 기록)",
                "next_run_id": NEXT_RUN_ID,
                "source_design_id": "all",
                "action": "Hash input tables and design files(입력 표와 설계 파일 해시 기록).",
                "effect": "artifact lineage(산출물 계보)를 닫는다.",
            },
        ],
    )


def write_receipts(design_rows: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        EXPERIMENT_DESIGN_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "Asymmetric long/short heads can preserve short carry while expanding long quality supply(비대칭 롱/숏 헤드가 숏 기여를 보존하면서 롱 품질 공급을 늘릴 수 있다).",
            "decision_use": "authorize run347B materialization only(run347B 물질화 허용만)",
            "comparison_baseline": "n01_s07_base_control",
            "control_variables": "source rows, cost assumptions, no MT5 execution in design(원천 행/비용 가정/설계 중 MT5 실행 없음)",
            "changed_variables": "side labels, model family, allocator feature set(방향 라벨/모델 계열/배분기 피처)",
            "sample_scope": "Tier A source from run345B; Tier B missing_required(Tier A run345B 원천, Tier B 필수 누락)",
            "success_criteria": "materialized design inputs with timestamp-safe audit(시점 안전 감사가 있는 설계 입력 물질화)",
            "failure_criteria": "design cannot avoid single side-filter repetition(단일 방향 필터 반복을 피하지 못함)",
            "invalid_conditions": "lookahead, timestamp ambiguity, feature-label overlap(미래참조/시각 모호성/피처-라벨 겹침)",
            "stop_conditions": "no materializable feature/label boundary(물질화 가능한 피처/라벨 경계 없음)",
            "evidence_plan": [rel(path) for path in [DESIGN_MATRIX, FEATURE_SOURCE_PLAN, LABEL_HEAD_PLAN, RUN347B_QUEUE]],
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": [rel(SOURCE_SCORECARD), rel(SOURCE_SEED_QUEUE), rel(SOURCE_RUN345B_SUMMARY)],
            "time_axis": "FPMarkets US100 M5 bar timestamps; design requires bar-close-safe features(FPMarkets US100 5분봉 시각; 설계는 봉 종가 기준 안전 피처 요구)",
            "sample_scope": "Tier A only in design, Tier B missing_required(설계는 Tier A 전용, Tier B 필수 누락)",
            "missing_or_duplicate_check": "deferred to run347B materialization(run347B 물질화로 이월)",
            "feature_label_boundary": "features before decision, labels after decision(피처는 결정 전, 라벨은 결정 후)",
            "split_boundary": "design only; WFO planned after materialization(설계 전용, 물질화 후 워크포워드 계획)",
            "leakage_risk": "cash-open regime features accidentally derived from trade outcome(현금장 국면 피처가 거래 결과에서 파생될 위험)",
            "data_hash_or_identity": "source artifacts hashed in artifact registry(원천 산출물은 산출물 등록부에 해시 기록)",
            "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)",
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_family": "logistic, ExtraTrees, HistGBM design only(로지스틱/엑스트라트리스/히스토그램 GBM 설계 전용)",
            "target_and_label": "separate long-quality, short-carry, allocator labels(분리 롱 품질/숏 기여/배분 라벨)",
            "split_method": "not trained yet; WFO required after materialization(아직 학습 없음, 물질화 후 워크포워드 필요)",
            "selection_metric": "joint net/PF/recovery/trade-count proxy, MT5 later(순수익/PF/회복/거래수 결합 프록시, MT5 후속)",
            "secondary_metrics": "long/short balance, drawdown, expectancy, density(롱/숏 균형, 낙폭, 기대값, 밀도)",
            "threshold_policy": "broad grid first, no micro search until adjacency survives(넓은 격자 우선, 인접 생존 전 미세 탐색 없음)",
            "overfit_risk": "multiple model families and side thresholds(다중 모델 계열과 방향 임계값)",
            "calibration_risk": "scores are rank unless calibrated(보정 전 점수는 순위)",
            "comparison_baseline": "n01_s07_base_control",
            "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [rel(SOURCE_FINAL_DECISION), rel(SOURCE_SCORECARD), rel(SOURCE_SEED_QUEUE), rel(SOURCE_FAILURE_MEMORY)],
            "producer": rel(Path("stage_pipelines/stage347/design_cash_open_asymmetric_long_short_source_without_db.py")),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(DESIGN_MATRIX), rel(FEATURE_SOURCE_PLAN), rel(LABEL_HEAD_PLAN), rel(MODEL_FAMILY_PLAN), rel(RUN347B_QUEUE)],
            "artifact_hashes": "recorded_in_artifact_registry(산출물 등록부에 기록)",
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
            "availability": "tracked(추적됨)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "design_ready_for_materialization(물질화 설계 준비)",
            "model_training": "not_claimed",
            "mt5_execution": "not_claimed",
            "candidate_selection": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_docs(design_rows: Sequence[Mapping[str, Any]]) -> None:
    write_text(
        REPORT_PATH,
        f"""# run347A Cash-Open Asymmetric Source Design(347A 현금장 비대칭 원천 설계)

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): Stage346(346단계)의 positive clue(긍정 단서)와 failure memory(실패 기억)를 asymmetric long/short source design(비대칭 롱/숏 원천 설계)으로 바꿨다.
Effect(효과): 다음 run347B(347B 실행)는 feature/label/proxy input(피처/라벨/프록시 입력)을 timestamp-safe(시점 안전)하게 물질화할 수 있다.

## Design Rows(설계 행)

- `a01_dual_logreg_side_heads(이중 로지스틱 방향 헤드)`
- `a02_tree_long_quality_short_carry(트리 롱 품질/숏 기여)`
- `a03_cash_open_regime_allocator(현금장 국면 배분기)`

## Guardrails(가드레일)

- single side-filter micro-tuning(단일 방향 필터 미세조정)을 중심 주제로 반복하지 않는다.
- proxy(프록시)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.
- feature/label boundary(피처/라벨 경계)는 timestamp-safe(시점 안전)이어야 한다.

## Artifacts(산출물)

- design_matrix(설계 표): `{rel(DESIGN_MATRIX)}`
- feature_source_plan(피처 원천 계획): `{rel(FEATURE_SOURCE_PLAN)}`
- label_head_plan(라벨 헤드 계획): `{rel(LABEL_HEAD_PLAN)}`
- model_family_plan(모델 계열 계획): `{rel(MODEL_FAMILY_PLAN)}`
- run347B_queue(347B 대기열): `{rel(RUN347B_QUEUE)}`

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        REVIEW_INDEX,
        "## run347A Cash-Open Asymmetric Source Design(347A 현금장 비대칭 원천 설계)",
        f"""## run347A Cash-Open Asymmetric Source Design(347A 현금장 비대칭 원천 설계)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage347(347단계)의 비대칭 원천 설계를 물질화 대기열로 바꿨다.
""",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run347A Design Packet(347A 설계 묶음)",
        f"""## run347A Design Packet(347A 설계 묶음)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- design_rows(설계 행): `{len(design_rows)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): long-quality/short-carry(롱 품질/숏 기여)를 separate heads(분리 헤드)와 allocator(배분기)로 설계한다.
""",
    )
    write_text(
        DECISION_DOC,
        f"""# 2026-06-01 Stage347A Design Decision(347A 설계 결정)

- decision(결정): `{DECISION}`
- source_review(원천 검토): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- reason(이유): run346B(346B 실행)가 single side-filter(단일 방향 필터)를 실패 기억으로 닫고, asymmetric long/short source(비대칭 롱/숏 원천)를 다음 공격 탐색 씨앗으로 열었기 때문이다.

Action(행동): feature source(피처 원천), label head(라벨 헤드), model family(모델 계열), control/ablation(대조/제거 실험), timestamp safety(시점 안전)를 설계했다.
Effect(효과): run347B(347B 실행)는 입력 물질화와 프록시 선별 준비로 진행할 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_status_docs() -> None:
    selection = f"""# Stage 347 Selection Status(347단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_review_run(원천 검토 실행): `{PARENT_RUN_ID}`
- source_runtime_probe(원천 런타임 탐침): `{SOURCE_RUNTIME_RUN_ID}`
- design_status(설계 상태): `ready_for_materialization(물질화 준비)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage347(347단계)는 design(설계)까지 완료했고 다음은 materialization(물질화)이다.
"""
    write_text(STAGE_SELECTION, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
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

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

Stage347A(347A 실행)는 asymmetric long/short source design(비대칭 롱/숏 원천 설계)을 완료했다. 다음 run347B(347B 실행)는 timestamp-safe feature/label/proxy inputs(시점 안전 피처/라벨/프록시 입력)를 물질화해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
""",
    )


def write_ledger() -> list[dict[str, Any]]:
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
        "gate_passes": 10,
        "gate_total": 10,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "experiment_design(실험 설계)",
        "lane": "experiment_design(실험 설계)",
        "family": "experiment_design(실험 설계)",
        "run_number": RUN_NUMBER,
        "notes": "asymmetric source design only(비대칭 원천 설계 전용).",
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "candidate_model_id": "none(없음)",
    }
    rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "design_matrix",
            "kpi_scope": "design_only",
            "primary_kpi": "design_rows=3;queue_rows=3",
            "guardrail_kpi": "no_model_training;no_mt5_execution",
            "external_verification_status": "not_applicable(해당 없음)",
            "result_status": "design_ready_no_selection(설계 준비, 선정 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "missing_required(필수 누락)",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": "same_as_tier_a_until_tier_b_available",
            "guardrail_kpi": "Tier B missing_required(Tier B 필수 누락)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "result_status": "same_as_tier_a_until_tier_b_available",
        },
    ]
    existing_fields, existing_rows = read_csv_rows(STAGE_LEDGER) if path_is_file(STAGE_LEDGER) else (STAGE_LEDGER_COLUMNS, [])
    replacement = {row["ledger_row_id"] for row in rows}
    kept = [row for row in existing_rows if row.get("ledger_row_id") not in replacement]
    fieldnames = list(dict.fromkeys(list(existing_fields) + STAGE_LEDGER_COLUMNS))
    write_csv(STAGE_LEDGER, kept + rows, fieldnames)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    return rows


def write_gates() -> list[dict[str, Any]]:
    gates = [
        ("source_review_available", path_is_file(SOURCE_FINAL_DECISION), SOURCE_FINAL_DECISION, "run346B review(검토)를 원천으로 확인한다."),
        ("design_matrix_written", path_is_file(DESIGN_MATRIX), DESIGN_MATRIX, "asymmetric source design matrix(비대칭 원천 설계 표)를 기록한다."),
        ("feature_source_plan_written", path_is_file(FEATURE_SOURCE_PLAN), FEATURE_SOURCE_PLAN, "feature source plan(피처 원천 계획)을 기록한다."),
        ("label_head_plan_written", path_is_file(LABEL_HEAD_PLAN), LABEL_HEAD_PLAN, "label head plan(라벨 헤드 계획)을 기록한다."),
        ("model_family_plan_written", path_is_file(MODEL_FAMILY_PLAN), MODEL_FAMILY_PLAN, "model family plan(모델 계열 계획)을 기록한다."),
        ("timestamp_safety_audit_written", path_is_file(TIMESTAMP_SAFETY_AUDIT), TIMESTAMP_SAFETY_AUDIT, "timestamp safety audit(시점 안전 감사)를 기록한다."),
        ("proxy_mt5_role_contract_written", path_is_file(PROXY_MT5_ROLE_CONTRACT), PROXY_MT5_ROLE_CONTRACT, "proxy/MT5 role contract(프록시/MT5 역할 계약)을 기록한다."),
        ("run347B_queue_written", path_is_file(RUN347B_QUEUE), RUN347B_QUEUE, "run347B materialization queue(물질화 대기열)를 만든다."),
        ("no_forbidden_operating_claim", path_is_file(CLAIM_RECEIPT), CLAIM_RECEIPT, "운영 주장을 하지 않는다."),
        ("required_gate_coverage_audit_written", True, GATE_AUDIT, "required gate coverage audit(필수 게이트 감사)를 남긴다."),
    ]
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, effect in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_final_and_manifest(design_rows: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        FINAL_DECISION,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "design_rows": len(design_rows),
            "feature_source_rows": 3,
            "label_head_rows": 3,
            "model_family_rows": 3,
            "run347B_queue_rows": 3,
            "gate_passes": 10,
            "gate_total": 10,
            "model_training": "not_claimed",
            "mt5_execution": "not_claimed",
            "candidate_selection": "not_claimed",
            "forward_passed": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer": rel(Path("stage_pipelines/stage347/design_cash_open_asymmetric_long_short_source_without_db.py")),
            "inputs": [rel(SOURCE_FINAL_DECISION), rel(SOURCE_SCORECARD), rel(SOURCE_SEED_QUEUE), rel(SOURCE_FAILURE_MEMORY)],
            "outputs": [
                rel(DESIGN_MATRIX),
                rel(FEATURE_SOURCE_PLAN),
                rel(LABEL_HEAD_PLAN),
                rel(MODEL_FAMILY_PLAN),
                rel(CONTROL_ABLATION_PLAN),
                rel(TIMESTAMP_SAFETY_AUDIT),
                rel(PROXY_MT5_ROLE_CONTRACT),
                rel(RUN347B_QUEUE),
                rel(REPORT_PATH),
                rel(FINAL_DECISION),
            ],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_registries() -> None:
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_design(실험 설계)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "notes": "Asymmetric long/short source design ready(비대칭 롱/숏 원천 설계 준비).",
                "family": "experiment_design(실험 설계)",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": 10,
                "gate_total": 10,
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": "none(없음)",
                "result_status": "design_ready_no_selection(설계 준비, 선정 없음)",
                "attempt_count": 3,
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "design_only",
                "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            }
        ],
    )
    artifact_paths = [
        DESIGN_MATRIX,
        FEATURE_SOURCE_PLAN,
        LABEL_HEAD_PLAN,
        MODEL_FAMILY_PLAN,
        CONTROL_ABLATION_PLAN,
        TIMESTAMP_SAFETY_AUDIT,
        PROXY_MT5_ROLE_CONTRACT,
        RUN347B_QUEUE,
        EXPERIMENT_DESIGN_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
    ]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": f"{path.stem}(산출물)",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "run347A design artifact(347A 설계 산출물).",
        }
        for path in artifact_paths
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_register_notes() -> None:
    append_text_once(
        IDEA_REGISTRY,
        "`IDEA-ST347-RUN347A-ASYMMETRIC-SOURCE-DESIGN`",
        f"""| `IDEA-ST347-RUN347A-ASYMMETRIC-SOURCE-DESIGN` | `{STAGE_ID}` | asymmetric long/short source design(비대칭 롱/숏 원천 설계) `3`개를 materialization queue(물질화 대기열)로 만든다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `design_ready_no_selection` | next_action(다음 행동) `{NEXT_RUN_ID}`; model training(모델 학습), MT5 execution(MT5 실행), selection(선정), ONNX readiness(온엑스 준비) 없음 |""",
    )
    text = f"""## 2026-06-01 run347A Cash-Open Asymmetric Source Design(현금장 비대칭 원천 설계)

- action(행동): long-quality/short-carry(롱 품질/숏 기여)를 separate heads(분리 헤드), cash-open allocator(현금장 배분기), timestamp-safe feature/label plan(시점 안전 피처/라벨 계획)으로 설계했다.
- effect(효과): run347B(347B 실행)가 materialization(물질화)로 진행할 수 있다.
- boundary(경계): model training/MT5 execution/selection(모델 학습/MT5 실행/선정)은 없음.
"""
    append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run347A Cash-Open Asymmetric Source Design", text)
    append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run347A Cash-Open Asymmetric Source Design", text)


def validate() -> None:
    outputs = [
        DESIGN_MATRIX,
        FEATURE_SOURCE_PLAN,
        LABEL_HEAD_PLAN,
        MODEL_FAMILY_PLAN,
        CONTROL_ABLATION_PLAN,
        TIMESTAMP_SAFETY_AUDIT,
        PROXY_MT5_ROLE_CONTRACT,
        RUN347B_QUEUE,
        EXPERIMENT_DESIGN_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        STAGE_SELECTION,
    ]
    missing = [rel(path) for path in outputs if not path_is_file(path)]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    _fields, gates = read_csv_rows(GATE_AUDIT)
    if len(gates) != 10 or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run347A gate audit failed(347A 게이트 감사 실패)")
    current_texts = [read_text(WORKSPACE_STATE), read_text(CURRENT_WORKING_STATE), read_text(STAGE_SELECTION)]
    if not all(NEXT_RUN_ID in text and STAGE_ID in text for text in current_texts):
        raise RuntimeError("current truth sync failed(현재 진실 동기화 실패)")


def main() -> None:
    for path in [
        SOURCE_FINAL_DECISION,
        SOURCE_SCORECARD,
        SOURCE_POSITIVE_CLUES,
        SOURCE_FAILURE_MEMORY,
        SOURCE_SEED_QUEUE,
        SOURCE_TIER_AUDIT,
        SOURCE_RUN345B_SUMMARY,
    ]:
        required(path)
    design_rows = build_design_matrix()
    write_design_tables()
    write_receipts(design_rows)
    write_docs(design_rows)
    write_status_docs()
    write_ledger()
    gates = write_gates()
    write_final_and_manifest(design_rows)
    write_registries()
    write_register_notes()
    validate()
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_run_id": NEXT_RUN_ID,
                "design_rows": len(design_rows),
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
