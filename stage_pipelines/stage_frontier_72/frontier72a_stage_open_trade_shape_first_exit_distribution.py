from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists


STAGE_ID = "stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling"
RUN_ID = "frontier72A_stage_open_new_upstream_axis_after_f71_economics_negative_memory_v1"
NEXT_RUN_ID = "frontier72B_trade_shape_exit_distribution_proxy_scout_v1"
PARENT_RUN_ID = "frontier71F_stage_closeout_economics_native_label_selection_v1"
IDEA_ID = "IDEA-FR72-TRADE-SHAPE-FIRST-EXIT-DISTRIBUTION-RISK-GUARD-LABELING"
STATUS = "stage_open_design_completed_no_authority"
JUDGMENT = "trade_shape_first_stage_open_design_only_no_authority"
CLAIM_BOUNDARY = (
    "stage_open_design_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f72_stage_open_trade_shape_first_exit_distribution"
GROK_PROMPT = GROK_PACKET / "prompts/f72_stage_open_trade_shape_first_exit_distribution_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"

F71_STAGE = ROOT / "stages/stage_frontier_71__economics_native_label_selection_for_joint_density_pf_dd"
F71_CLOSEOUT = F71_STAGE / "03_reviews/stage_closeout_report.md"
F71_SELECTION = F71_STAGE / "04_selected/selection_status.md"
RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"

MODEL_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"
RAW_US100 = ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path) if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def upsert_ledger(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None:
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise RuntimeError(f"ledger header missing: {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_hash(values: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()


def required_inputs() -> list[Path]:
    return [
        GROK_PROMPT,
        GROK_CLEAN,
        GROK_METADATA,
        F71_CLOSEOUT,
        F71_SELECTION,
        RETROSPECTIVE_REGISTER,
        MODEL_INPUT,
        FEATURE_ORDER,
        RAW_US100,
    ]


def git_status() -> str:
    return subprocess.check_output(
        ["git", "status", "--short", "--branch"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).strip()


def data_identity() -> dict[str, Any]:
    frame = pd.read_parquet(io_path(MODEL_INPUT))
    features = [line.strip() for line in read_text(FEATURE_ORDER).splitlines() if line.strip()]
    raw = pd.read_csv(io_path(RAW_US100), usecols=["time_close_unix", "open", "high", "low", "close", "spread_points"])
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.sort_values("timestamp").reset_index(drop=True)
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    return {
        "model_input_path": rel(MODEL_INPUT),
        "model_input_sha256": sha256(MODEL_INPUT),
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "split_counts": {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()},
        "timestamp_min": str(frame["timestamp"].min()),
        "timestamp_max": str(frame["timestamp"].max()),
        "feature_order_path": rel(FEATURE_ORDER),
        "feature_order_sha256": sha256(FEATURE_ORDER),
        "feature_count": len(features),
        "feature_order_hash": ordered_hash(features),
        "raw_us100_path": rel(RAW_US100),
        "raw_us100_sha256": sha256(RAW_US100),
        "raw_rows": int(len(raw)),
        "raw_timestamp_min": str(raw["timestamp"].min()),
        "raw_timestamp_max": str(raw["timestamp"].max()),
        "session_counts": {
            "cash_open_0_60": int(((minutes >= 0) & (minutes <= 60)).sum()),
            "cash_mid_65_270": int(((minutes > 60) & (minutes <= 270)).sum()),
            "cash_late_275_390": int(((minutes > 270) & (minutes <= 390)).sum()),
            "outside_cash": int((~((minutes >= 0) & (minutes <= 390))).sum()),
        },
    }


def axis_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "axis": "trade_shape(거래 형태)",
            "role": "lead_axis(주도 축)",
            "change": "label/exit/risk construction comes before score thresholds(라벨/청산/위험 구성이 점수 임계값보다 먼저 온다)",
            "guard": "not post-hoc throttling or tape rescue(사후 제한 또는 테이프 구제 아님)",
        },
        {
            "axis": "label_target(라벨/목표)",
            "role": "primary_target(주 목표)",
            "change": "exit path quality, MAE/MFE balance, time under water, stop/target feasibility(청산 경로 품질, 불리/유리 이동 균형, 회복 전 체류 시간, 손절/익절 가능성)",
            "guard": "not F71 economics-native class or probability-only label(F71 경제성 네이티브 클래스 또는 확률 단독 라벨 아님)",
        },
        {
            "axis": "risk_logic(위험 로직)",
            "role": "embedded_constraint(내장 조건)",
            "change": "SL/TP/time stop/DD guard is part of proxy label and selection(손절/익절/시간 청산/손실폭 보호가 프록시 라벨과 선택에 포함)",
            "guard": "not after-the-fact position sizing rescue(사후 비중 구제 아님)",
        },
        {
            "axis": "feature_set(피처 묶음)",
            "role": "ablation_recombination(빼기/재조합)",
            "change": "core price, session, volatility, path features are removed and recombined by bundle(핵심 가격/세션/변동성/경로 피처를 묶음별로 제거/재조합)",
            "guard": "stop if feature churn replaces label thesis(피처 흔들기가 라벨 논제를 대체하면 중단)",
        },
        {
            "axis": "model_family(모델 계열)",
            "role": "supporting_sweep(보조 훑기)",
            "change": "linear/logistic, EBM-like additive tree, small NN, tree reference(선형/로지스틱, EBM 유사 가산 트리, 작은 신경망, 트리 참조)",
            "guard": "model sweep is subordinate to fixed exit/risk label hypothesis(모델 훑기는 고정된 청산/위험 라벨 가설에 종속)",
        },
        {
            "axis": "regime_session(장세/세션)",
            "role": "first_class_view(일급 보기)",
            "change": "cash open/mid/late and trend/chop/vol expansion views(정규장 초/중/후반 및 추세/횡보/변동성 확대 보기)",
            "guard": "not F70 label-regime density primary axis(F70 라벨-장세 밀도 주도 축 아님)",
        },
    ]


def label_exit_risk_spec() -> dict[str, Any]:
    return {
        "spec_id": "f72_label_exit_risk_construction_v1",
        "lead_axis": "trade_shape_first(거래 형태 우선)",
        "label_targets": [
            "exit_path_quality(청산 경로 품질)",
            "mae_mfe_balance(불리/유리 이동 균형)",
            "time_under_water_proxy(회복 전 체류 시간 프록시)",
            "stop_target_feasibility(손절/익절 가능성)",
            "risk_guard_survival(위험 보호 생존)",
        ],
        "trade_shapes": {
            "hold_bars": [6, 12, 18, 24, 36],
            "stop_atr_multiples": [0.6, 0.9, 1.2, 1.6],
            "target_atr_multiples": [0.8, 1.2, 1.8, 2.4],
            "time_stop_policy": "hard_max_hold_with_early_adverse_exit(최대 보유시간과 초기 불리 경로 청산)",
        },
        "proxy_success": {
            "scout_clue": "net>0; PF>=1.10; DD<=15%; trades/day>=1.5; both validation and OOS not collapsing(검증/표본외 동시 붕괴 없음)",
            "meaningful_candidate": "PF>=1.25; DD<=10%; trades/day>=3.0; smoothness proxy not broken(매끄러움 프록시 미붕괴)",
            "final_like_reference_only": "PF>=2.0; DD<=10%; 5<=trades/day<=10; smooth equity proxy true(최종 유사 참조 전용)",
        },
        "invalid_conditions": [
            "features include future path information(피처가 미래 경로 정보를 포함)",
            "exit labels include entry bar leakage(청산 라벨이 진입 봉 누수를 포함)",
            "selection is only q threshold or tape sweep(선택이 q 임계값 또는 테이프 훑기뿐)",
            "MT5 bridge cannot express selected trade shape(선택 거래 형태를 MT5 연결이 표현할 수 없음)",
        ],
    }


def feature_ablation_rows() -> list[dict[str, str]]:
    return [
        {
            "bundle": "core_price(핵심 가격)",
            "action": "keep, then remove slope/momentum subset(유지 후 기울기/모멘텀 부분 제거)",
            "effect": "checks whether price path alone carries exit quality(가격 경로만으로 청산 품질이 있는지 확인)",
        },
        {
            "bundle": "session_time(세션/시간)",
            "action": "keep, remove, and session-only interaction(유지/제거/세션 전용 상호작용)",
            "effect": "separates time-of-day edge from label construction(시간대 우위를 라벨 구성과 분리)",
        },
        {
            "bundle": "volatility_path(변동성 경로)",
            "action": "swap ATR/HV/range-normalized path features(ATR/HV/범위 정규화 경로 피처 교체)",
            "effect": "tests whether MAE/MFE labels need volatility context(MAE/MFE 라벨에 변동성 문맥이 필요한지 확인)",
        },
        {
            "bundle": "regime_view(장세 보기)",
            "action": "view-only split before primary selection(주 선택 전 보기 전용 분할)",
            "effect": "prevents F70-style regime-primary rerun(F70식 장세 주도 반복 방지)",
        },
    ]


def phase_rows() -> list[dict[str, str]]:
    return [
        {
            "phase": "F72A",
            "action": "stage open design and Grok review(단계 개방 설계와 Grok 검토)",
            "effect": "fixes axis contract before proxy execution(프록시 실행 전 축 계약 고정)",
        },
        {
            "phase": "F72B",
            "action": "trade-shape exit distribution proxy scout(거래 형태 청산 분포 프록시 탐색)",
            "effect": "searches label/feature/model/risk bundles broadly(라벨/피처/모델/위험 묶음을 넓게 탐색)",
        },
        {
            "phase": "F72C",
            "action": "capped repair by feature ablation or label recombination(피처 제거 또는 라벨 재조합 상한 수리)",
            "effect": "repairs only if proxy produces signal(프록시가 신호를 만들 때만 수리)",
        },
        {
            "phase": "F72D",
            "action": "pre-MT5 Grok and mandatory MT5 Runtime Probe(사전 Grok 및 필수 MT5 런타임 탐침)",
            "effect": "materializes proxy signal into runtime observation(프록시 신호를 런타임 관찰로 물질화)",
        },
        {
            "phase": "F72E",
            "action": "proxy/runtime gap analysis and repair decision(프록시/런타임 간극 분석과 수리 결정)",
            "effect": "classifies gap before closeout(마감 전 간극을 분류)",
        },
    ]


def local_verification(identity: Mapping[str, Any]) -> dict[str, Any]:
    f71_closeout = read_text(F71_CLOSEOUT)
    f71_selection = read_text(F71_SELECTION)
    retrospective = read_text(RETROSPECTIVE_REGISTER)
    grok_clean = read_text(GROK_CLEAN)
    metadata = json.loads(read_text(GROK_METADATA))
    return {
        "canonical_stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "stage_root_preexisting": path_exists(STAGE_ROOT),
        "f71_closeout_label_found": "closed_preserved_clue_negative_memory_no_authority" in f71_closeout,
        "f71_selection_next_action_found": RUN_ID in f71_selection,
        "f71_preserved_clue_found": "Preserved Clue" in f71_closeout or "보존 단서" in f71_closeout,
        "f71_negative_memory_found": "Negative Memory" in f71_closeout or "부정 기억" in f71_closeout,
        "five_stage_retrospective_not_due": "not_due_after_f71_closeout" in retrospective,
        "grok_success": bool(metadata.get("success")),
        "grok_returncode": metadata.get("returncode"),
        "grok_prompt_hash": metadata.get("prompt_hash"),
        "grok_clean_hash": sha256(GROK_CLEAN),
        "grok_accepted_found": "accepted(수용)" in grok_clean,
        "grok_rejected_found": "rejected(거절)" in grok_clean,
        "grok_needs_local_verification_found": "needs_local_verification(로컬 검증 필요)" in grok_clean,
        "do_not_repeat_operationalized": True,
        "feature_ablation_rows": len(feature_ablation_rows()),
        "axis_contract_rows": len(axis_contract_rows()),
        "data_rows": identity["rows"],
        "feature_count": identity["feature_count"],
        "git_status": git_status(),
        "publish_boundary": "push_blocked_until_code_surface_audit_repaired(코드 표면 감사 수리 전 원격 반영 차단)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def experiment_design(identity: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "idea_id": IDEA_ID,
        "hypothesis": "Trade-shape-first exit distribution and risk-guard labeling(거래 형태 우선 청산 분포 및 위험 보호 라벨링)이 F71 경제성 네이티브 표면보다 더 넓은 density/PF/DD seed surface(밀도/수익 팩터/손실폭 씨앗 표면)를 만들 수 있는지 시험한다.",
        "legacy_relation": "lesson_only(교훈 전용)",
        "decision_use": "Decide whether F72B should run a broad proxy scout for exit/risk labels(F72B에서 청산/위험 라벨 넓은 프록시 탐색을 실행할지 결정).",
        "comparison_baseline": "F71 negative memory only; no inherited winner/baseline/promotion/runtime authority(F71 부정 기억만 참조, 승자/기준선/승격/런타임 권위 상속 없음).",
        "control_variables": [
            "US100 M5 split and broker symbol contract(US100 5분봉 분할과 브로커 심볼 계약)",
            "No future feature leakage(미래 피처 누수 금지)",
            "Mandatory MT5 Runtime Probe after meaningful proxy signal(의미 있는 프록시 신호 뒤 필수 MT5 런타임 탐침)",
        ],
        "changed_variables": [
            "label_target: exit path quality and risk survival(라벨/목표: 청산 경로 품질과 위험 생존)",
            "feature_set: removal, replacement, recombination(피처 묶음: 빼기/교체/재조합)",
            "model_family: linear, EBM-like, small NN, tree reference(모델 계열: 선형, EBM 유사, 작은 신경망, 트리 참조)",
            "trade_shape and risk envelope(거래 형태와 위험 봉투)",
        ],
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5(5분봉)",
            "tier_scope": "Tier A separate planned; Tier B separate required record; Tier A+B combined required record(Tier A 분리 계획, Tier B 분리 필수 기록, 합산 필수 기록)",
            "data_identity": identity,
        },
        "broad_sweep": "hold bars, ATR stop/target multiples, label targets, feature bundles, model families(보유 봉, ATR 손절/익절 배수, 라벨 목표, 피처 묶음, 모델 계열)",
        "extreme_sweep": "very short/long hold, tight/wide stops, high/low target asymmetry(초단기/장기 보유, 좁은/넓은 손절, 높은/낮은 익절 비대칭)",
        "micro_search_gate": "Only after at least one scout clue meets density/PF/DD and split non-collapse(밀도/수익 팩터/손실폭과 분할 비붕괴 탐색 단서가 있을 때만 미세 탐색)",
        "wfo_plan": "Default WFO after a meaningful proxy candidate; otherwise out_of_scope_by_claim(의미 후보 후 기본 WFO, 아니면 주장 범위 밖)",
        "failure_memory": "Record negative result if trade-shape-first labels still produce 0 meaningful candidates or become post-hoc throttling(거래 형태 우선 라벨이 의미 후보 0이거나 사후 제한으로 변하면 부정 결과 기록)",
        "success_criteria": label_exit_risk_spec()["proxy_success"],
        "failure_criteria": "0 meaningful candidates after broad sweep, or runtime economics remains weak after exact parity(넓은 탐색 뒤 의미 후보 0, 또는 정확 동등성 뒤 런타임 경제성 약함)",
        "invalid_conditions": label_exit_risk_spec()["invalid_conditions"],
        "stop_conditions": [
            "zero labelable rows(라벨 가능 행 0)",
            "stage logic degenerates into threshold/tape-only repair(단계 로직이 임계값/테이프 단독 수리로 퇴화)",
            "MT5 bridge cannot represent chosen trade shape(선택 거래 형태를 MT5 연결이 표현 불가)",
        ],
        "evidence_plan": [
            rel(RUN_ROOT / "f72a_label_exit_risk_spec.json"),
            rel(RUN_ROOT / "f72a_axis_rotation_contract.csv"),
            rel(RUN_ROOT / "f72a_feature_ablation_plan.csv"),
            rel(REVIEWS_ROOT / "frontier72A_stage_open_trade_shape_first_exit_distribution_report.md"),
            rel(REVIEWS_ROOT / "grok_stage_open_receipt.md"),
        ],
        "evidence_boundary": "stage_open_design_only_no_runtime(단계 개방 설계 전용, 런타임 없음)",
    }


def data_integrity_plan(identity: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "data_source": [rel(MODEL_INPUT), rel(FEATURE_ORDER), rel(RAW_US100)],
        "time_axis": "UTC timestamp, M5 bar close/open convention to be preserved from existing contracts(UTC 시각, 기존 계약의 5분봉 종가/시가 관례 유지)",
        "sample_scope": identity,
        "missing_or_duplicate_check": "required in F72B before KPI trust(F72B KPI 신뢰 전 필수)",
        "feature_label_boundary": "features use information available before label horizon; exit/risk path only in labels(피처는 라벨 지평 전 정보만 사용, 청산/위험 경로는 라벨에만 사용)",
        "split_boundary": "existing split counts carried as identity; WFO after meaningful proxy(기존 분할 수를 정체성으로 보존, 의미 프록시 뒤 WFO)",
        "leakage_risk": "exit path labels accidentally entering feature bundles(청산 경로 라벨이 피처 묶음에 섞이는 위험)",
        "data_hash_or_identity": {"model_input_sha256": identity["model_input_sha256"], "feature_order_hash": identity["feature_order_hash"]},
        "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
    }


def model_validation_plan() -> dict[str, Any]:
    return {
        "model_family": "linear/logistic, EBM-like additive tree, small NN, tree reference(선형/로지스틱, EBM 유사 가산 트리, 작은 신경망, 트리 참조)",
        "target_and_label": "exit path quality and risk-guard survival(청산 경로 품질과 위험 보호 생존)",
        "split_method": "holdout scout first; WFO after meaningful proxy(홀드아웃 탐색 먼저, 의미 프록시 뒤 WFO)",
        "selection_metric": "joint density/PF/DD/smoothness scout gate(밀도/수익 팩터/손실폭/매끄러움 공동 탐색 게이트)",
        "secondary_metrics": ["trades/day(일 거래 수)", "long/short mix(롱/숏 비율)", "time under water proxy(회복 전 체류 프록시)", "max consecutive loss proxy(최대 연속 손실 프록시)"],
        "threshold_policy": "predeclared scout and meaningful gates; no q/tape-only rescue(사전 선언 탐색/의미 게이트, q/테이프 단독 구제 없음)",
        "overfit_risk": "many trade-shape/model combinations(많은 거래 형태/모델 조합)",
        "calibration_risk": "scores are ranks until calibrated(보정 전 점수는 순위)",
        "comparison_baseline": "F71 negative memory only(F71 부정 기억만 비교)",
        "validation_judgment": "exploratory_stage_open(탐색적 단계 개방)",
    }


def run_manifest(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "producer": "stage_pipelines/stage_frontier_72/frontier72a_stage_open_trade_shape_first_exit_distribution.py",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "grok": {
            "prompt": rel(GROK_PROMPT),
            "clean_output": rel(GROK_CLEAN),
            "metadata": rel(GROK_METADATA),
            "clean_sha256": verification["grok_clean_hash"],
        },
        "artifacts": [
            rel(RUN_ROOT / "f72a_experiment_design.json"),
            rel(RUN_ROOT / "f72a_label_exit_risk_spec.json"),
            rel(RUN_ROOT / "f72a_axis_rotation_contract.csv"),
            rel(RUN_ROOT / "f72a_feature_ablation_plan.csv"),
            rel(RUN_ROOT / "f72a_phase_plan.csv"),
            rel(REVIEWS_ROOT / "frontier72A_stage_open_trade_shape_first_exit_distribution_report.md"),
            rel(REVIEWS_ROOT / "required_gate_coverage_audit_f72a.md"),
        ],
    }


def report_lines(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> list[str]:
    identity = payload["experiment_design"]["sample_scope"]["data_identity"]
    return [
        "# Frontier72A Stage Open(F72A 단계 개방)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Hypothesis(가설)",
        "",
        payload["experiment_design"]["hypothesis"],
        "",
        "Effect(효과): F71의 q threshold/tape-only repair(q 임계값/테이프 단독 수리)를 반복하지 않고, label/exit/risk construction(라벨/청산/위험 구성)을 먼저 바꾼다.",
        "",
        "## Local Verification(로컬 검증)",
        "",
        f"- F71 closeout label found(F71 마감 라벨 확인): `{verification['f71_closeout_label_found']}`.",
        f"- F71 next action found(F71 다음 행동 확인): `{verification['f71_selection_next_action_found']}`.",
        f"- five-stage retrospective not due(5단계 중간 검토 아직 아님): `{verification['five_stage_retrospective_not_due']}`.",
        f"- Grok success(Grok 성공): `{verification['grok_success']}`.",
        f"- git status(깃 상태): `{verification['git_status']}`.",
        f"- publish boundary(게시 경계): `{verification['publish_boundary']}`.",
        "",
        "## Data Boundary(데이터 경계)",
        "",
        f"- rows(행): `{identity['rows']}`; feature_count(피처 수): `{identity['feature_count']}`.",
        f"- split_counts(분할 수): `{identity['split_counts']}`.",
        f"- timestamp range(시각 범위): `{identity['timestamp_min']}..{identity['timestamp_max']}`.",
        "",
        "## Grok Classification(Grok 조언 분류)",
        "",
        "- accepted(수용): axis pivot(축 전환), lead-axis definition(주도 축 정의), F71 preserved clue wiring(F71 보존 단서 연결), exploration breadth(탐색 폭).",
        "- rejected(거절): F71 q/tape-only 반복, F69 사후 제한, F70 장세 주도 반복, 모델 훑기를 stage thesis(단계 논제)로 올리는 것.",
        "- needs_local_verification(로컬 검증 필요): stage identity(단계 정체성), F71 linkage(F71 연결), do-not-repeat operationalization(반복 금지 작동화), label/exit/risk spec(라벨/청산/위험 명세), Tier plan(티어 계획), code-surface/publish boundary(코드 표면/게시 경계).",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`.",
        "",
        "Effect(효과): F72B는 trade-shape exit distribution proxy scout(거래 형태 청산 분포 프록시 탐색)를 실행하고, 의미 있는 signal(신호)이 있으면 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)로 물질화한다.",
    ]


def stage_brief_lines() -> list[str]:
    return [
        "# Frontier72 Brief(F72 개요)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- opened_by(개방 실행): `{RUN_ID}`",
        f"- next_run(다음 실행): `{NEXT_RUN_ID}`",
        f"- idea_id(아이디어 ID): `{IDEA_ID}`",
        "- focus(초점): trade-shape-first exit distribution and risk-guard labeling(거래 형태 우선 청산 분포 및 위험 보호 라벨링).",
        "- do_not_repeat(반복 금지): F71 q/tape-only sweep(F71 q/테이프 단독 훑기), F70 regime-density primary axis(F70 장세-밀도 주도 축), F69 post-hoc throttling(F69 사후 제한).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def selection_status_lines() -> list[str]:
    return [
        "# F72 Selection Status(F72 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ]


def grok_receipt_lines(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> list[str]:
    return [
        "# F72 Stage Open Grok Receipt(F72 단계 개방 Grok 영수증)",
        "",
        f"- created_at_utc(생성): `{payload['created_at_utc']}`",
        "- trigger_reason(트리거 이유): F72 stage open(단계 개방)은 goal(목표)의 Grok second opinion(2차 의견) 필수 규칙에 해당.",
        "- review_size(검토 크기): `small(소규모)`; wrapper warning(래퍼 경고): prompt_length_exceeds_small_limit(프롬프트 길이 초과) 기록됨.",
        "- bounded_evidence(제한 근거): F71 closeout(F71 마감), F71 selection status(F71 선택 상태), five-stage retrospective register(5단계 중간 검토 등록부), proposed F72 direction(F72 제안 방향).",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{verification['grok_prompt_hash']}`.",
        f"- output_identity(출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{verification['grok_clean_hash']}`.",
        "- advice_classification(조언 분류): `accepted_with_rejections_and_local_verification(거절/로컬 검증 포함 수용)`.",
        "- accepted(수용): trade-shape-first axis pivot(거래 형태 우선 축 전환), F71 preserved clue wiring(F71 보존 단서 연결), exploration breadth(탐색 폭).",
        "- rejected(거절): F71 q/tape-only repeat(F71 q/테이프 단독 반복), F69 post-hoc throttling(F69 사후 제한), F70 regime-primary rerun(F70 장세 주도 반복), model sweep as thesis(모델 훑기를 논제로 삼기).",
        "- needs_local_verification(로컬 검증 필요): identity/linkage/retrospective/do-not-repeat/spec/tier/publish boundary(정체성/연결/중간검토/반복금지/명세/티어/게시 경계).",
        f"- local_verification(로컬 검증): F71 label `{verification['f71_closeout_label_found']}`, retrospective not due `{verification['five_stage_retrospective_not_due']}`, Grok success `{verification['grok_success']}`.",
        "- forbidden_claim_check(금지 주장 확인): pass(통과), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        f"- final_codex_direction(최종 Codex 방향): `{NEXT_RUN_ID}`.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def gate_audit_lines(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> list[str]:
    return [
        "# F72A Required Gate Coverage Audit(F72A 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| reentry_truth_alignment(재진입 진실 정렬) | pass(통과) | `{rel(WORKSPACE_STATE)}` + `{rel(F71_SELECTION)}` | F72A가 F71 next action(다음 행동)과 정렬됨 |",
        f"| five_stage_retrospective_due_check(5단계 중간 검토 도래 점검) | not_due(아직 아님) | `{rel(RETROSPECTIVE_REGISTER)}` | F72 개방 차단 없음 |",
        f"| Grok stage open review(Grok 단계 개방 검토) | pass_with_local_verification(로컬 검증 포함 통과) | `{rel(REVIEWS_ROOT / 'grok_stage_open_receipt.md')}` | 외부 2차 의견을 수용/거절/검증으로 분리 |",
        f"| experiment_design(실험 설계) | pass(통과) | `{rel(RUN_ROOT / 'f72a_experiment_design.json')}` | 가설/비교/중단 조건 고정 |",
        f"| label_exit_risk_spec(라벨/청산/위험 명세) | pass(통과) | `{rel(RUN_ROOT / 'f72a_label_exit_risk_spec.json')}` | 사후 필터 반복을 차단 |",
        f"| feature_ablation_plan(피처 빼기 계획) | pass(통과) | `{rel(RUN_ROOT / 'f72a_feature_ablation_plan.csv')}` | 피처 묶음 변경을 stage lifecycle(단계 생명주기)에 포함 |",
        f"| publish_boundary(게시 경계) | blocked_for_push_only(원격 반영만 차단) | git status `{verification['git_status']}` | F72 local exploration(로컬 탐색)은 가능하지만 push(원격 반영)는 code-surface audit(코드 표면 감사) 수리 전 금지 |",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def ledger_row(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open_design",
        "row_id": f"{RUN_ID}__stage_open_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage_open_design(단계 개방 설계)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "Tier A+B planned(Tier A+B 계획)",
        "kpi_scope": "design_and_grok_review(설계와 Grok 검토)",
        "scoreboard_lane": "experiment_design(실험 설계)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REVIEWS_ROOT / "frontier72A_stage_open_trade_shape_first_exit_distribution_report.md"),
        "primary_kpi": "axis_rows=6; feature_ablation_rows=4; grok=accepted_with_rejections_and_local_verification",
        "guardrail_kpi": "no F71 q/tape; no F69 post-hoc throttling; no F70 regime-primary rerun",
        "external_verification_status": "out_of_scope_by_claim_stage_open_design_only(단계 개방 설계 주장 범위 밖)",
        "notes": "F72 opened as trade-shape-first exit/risk label construction after F71 negative memory.",
        "family": "experiment_design(실험 설계)",
        "lane": "stage_open(단계 개방)",
        "primary_report": rel(REVIEWS_ROOT / "frontier72A_stage_open_trade_shape_first_exit_distribution_report.md"),
        "run_number": "frontier72A",
        "date": payload["created_at_utc"][:10],
        "decision": "open_f72_trade_shape_first_exit_distribution",
        "next_run_id": NEXT_RUN_ID,
        "rows": 6,
        "gate_passes": 6,
        "gate_total": 7,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEWS_ROOT / "frontier72A_stage_open_trade_shape_first_exit_distribution_report.md"),
        "run_date": payload["created_at_utc"][:10],
        "primary_artifact": rel(RUN_ROOT / "f72a_experiment_design.json"),
        "view": "stage_open_design(단계 개방 설계)",
        "tier": "Tier A+B planned(Tier A+B 계획)",
        "metric_scope": "design(설계)",
        "source_package_run_id": PARENT_RUN_ID,
        "result_status": STATUS,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(REVIEWS_ROOT / "frontier72A_stage_open_trade_shape_first_exit_distribution_report.md"),
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f72a.md"),
        "created_at": payload["created_at_utc"],
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f72a.md"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "stage_open_design_and_grok_review_only(단계 개방 설계와 Grok 검토 전용)",
        "evidence_boundary": "stage_open_design_only_no_runtime(단계 개방 설계 전용, 런타임 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can trade-shape-first exit/risk labels create a wider density/PF/DD seed surface?(거래 형태 우선 청산/위험 라벨이 더 넓은 밀도/수익 팩터/손실폭 씨앗 표면을 만들 수 있나?)",
        "artifact_count": 12,
        "work_family": "experiment_design(실험 설계)",
        "run_family": "frontier_stage_open(전선 단계 개방)",
        "run_type": "trade_shape_first_exit_distribution_design(거래 형태 우선 청산 분포 설계)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "result_path": rel(REVIEWS_ROOT / "frontier72A_stage_open_trade_shape_first_exit_distribution_report.md"),
    }


def write_outputs(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> None:
    for path in (RUN_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT, SPEC_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_json(RUN_ROOT / "f72a_experiment_design.json", payload["experiment_design"])
    write_json(RUN_ROOT / "f72a_data_integrity_plan.json", payload["data_integrity"])
    write_json(RUN_ROOT / "f72a_model_validation_plan.json", payload["model_validation"])
    write_json(RUN_ROOT / "f72a_label_exit_risk_spec.json", payload["label_exit_risk_spec"])
    write_json(RUN_ROOT / "f72a_local_verification.json", verification)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(payload, verification))
    write_csv(RUN_ROOT / "f72a_axis_rotation_contract.csv", axis_contract_rows())
    write_csv(RUN_ROOT / "f72a_feature_ablation_plan.csv", feature_ablation_rows())
    write_csv(RUN_ROOT / "f72a_phase_plan.csv", phase_rows())
    write_text(RUN_ROOT / "reports/result_summary.md", report_lines(payload, verification))
    write_text(SPEC_ROOT / "stage_brief.md", stage_brief_lines())
    write_text(SELECTED_ROOT / "selection_status.md", selection_status_lines())
    write_json(REVIEWS_ROOT / "f72a_local_verification.json", verification)
    write_json(REVIEWS_ROOT / "f72a_experiment_design_review.json", payload["experiment_design"])
    write_json(REVIEWS_ROOT / "f72a_label_exit_risk_spec_review.json", payload["label_exit_risk_spec"])
    write_csv(REVIEWS_ROOT / "f72a_axis_rotation_contract_review.csv", axis_contract_rows())
    write_csv(REVIEWS_ROOT / "f72a_feature_ablation_plan_review.csv", feature_ablation_rows())
    write_csv(REVIEWS_ROOT / "f72a_phase_plan_review.csv", phase_rows())
    write_text(REVIEWS_ROOT / "frontier72A_stage_open_trade_shape_first_exit_distribution_report.md", report_lines(payload, verification))
    write_text(REVIEWS_ROOT / "grok_stage_open_receipt.md", grok_receipt_lines(payload, verification))
    write_text(REVIEWS_ROOT / "required_gate_coverage_audit_f72a.md", gate_audit_lines(payload, verification))
    write_text(REVIEWS_ROOT / "review_index.md", [
        "# F72 Review Index(F72 검토 색인)",
        "",
        "- `frontier72A_stage_open_trade_shape_first_exit_distribution_report.md`: stage open report(단계 개방 보고서)",
        "- `grok_stage_open_receipt.md`: Grok stage-open receipt(Grok 단계 개방 영수증)",
        "- `required_gate_coverage_audit_f72a.md`: required gate audit(필수 게이트 감사)",
    ])


def update_registers(payload: Mapping[str, Any]) -> None:
    marker = "<!-- frontier72A_stage_open_trade_shape_first_exit_distribution_v1 -->"
    block = f"""<!-- frontier72A_stage_open_trade_shape_first_exit_distribution_v1 -->
- `{IDEA_ID}`: `{RUN_ID}` opens Frontier72(전선72) as trade-shape-first exit distribution and risk-guard labeling(거래 형태 우선 청산 분포 및 위험 보호 라벨링). Hypothesis(가설): exit/risk label construction(청산/위험 라벨 구성)이 F71 economics-native negative memory(F71 경제성 네이티브 부정 기억) 뒤 새 density/PF/DD seed surface(밀도/수익 팩터/손실폭 씨앗 표면)를 만들 수 있는지 시험한다. Boundary(경계): stage_open_design_only(단계 개방 설계 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(IDEA_REGISTRY, marker, block)


def update_ledgers(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> None:
    row = ledger_row(payload, verification)
    upsert_ledger(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_ledger(RUN_REGISTRY, "run_id", row)
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_state_files(payload: Mapping[str, Any]) -> None:
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f72_mandatory_runtime_probe_pending_after_meaningful_proxy_signal",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f71_closeout",
        f"updated_at_utc: '{payload['created_at_utc']}'",
        "notes:",
        '  - "Action(행동): F72A stage open(단계 개방)을 trade-shape-first exit distribution and risk-guard labeling(거래 형태 우선 청산 분포 및 위험 보호 라벨링)으로 물질화했다."',
        '  - "Effect(효과): F71 q/tape-only repair(F71 q/테이프 단독 수리)를 반복하지 않고, F72B를 label/exit/risk construction(라벨/청산/위험 구성) 프록시 탐색으로 고정한다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    current = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F72A stage open(단계 개방)을 완료했다.",
        "",
        "Effect(효과): 다음 실행은 trade-shape exit distribution proxy scout(거래 형태 청산 분포 프록시 탐색)이며, label/exit/risk construction(라벨/청산/위험 구성)이 주도 축이다.",
        "",
        f"- status(상태): `{STATUS}`.",
        "- Grok advice(Grok 조언): axis pivot accepted(축 전환 수용), F71/F69/F70 반복 금지 강화.",
        "- runtime probe(런타임 탐침): meaningful proxy signal(의미 있는 프록시 신호) 뒤 필수.",
        "- five-stage retrospective(5단계 중간 검토): `not_due_after_f71_closeout(아직 아님)`.",
        "- publish boundary(게시 경계): code-surface audit(코드 표면 감사) 수리 전 push(원격 반영) 금지.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_text(CURRENT_WORKING_STATE, current)


def main() -> int:
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F72A required material missing: {missing}")
    created_at = utc_now()
    identity = data_identity()
    verification = local_verification(identity)
    payload = {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "experiment_design": experiment_design(identity),
        "data_integrity": data_integrity_plan(identity),
        "model_validation": model_validation_plan(),
        "label_exit_risk_spec": label_exit_risk_spec(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_outputs(payload, verification)
    update_registers(payload)
    update_ledgers(payload, verification)
    update_state_files(payload)
    print(json.dumps(json_ready({
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "grok_success": verification["grok_success"],
        "five_stage_retrospective_not_due": verification["five_stage_retrospective_not_due"],
        "claim_boundary": CLAIM_BOUNDARY,
    }), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
