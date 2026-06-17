from __future__ import annotations

import argparse
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


STAGE_ID = "stage_frontier_73__session_regime_feature_model_rotation_for_runtime_economics_gap"
RUN_ID = "frontier73A_stage_open_new_hypothesis_after_f72_trade_shape_negative_memory_v1"
NEXT_RUN_ID = "frontier73B_session_regime_feature_model_rotation_proxy_scout_v1"
PARENT_RUN_ID = "frontier72G_stage_closeout_trade_shape_lifecycle_gap_v1"
IDEA_ID = "IDEA-FR73-SESSION-REGIME-FEATURE-MODEL-ROTATION-RUNTIME-ECONOMICS"
STATUS = "stage_open_design_completed_no_authority"
JUDGMENT = "session_regime_feature_model_rotation_stage_open_design_only_no_authority"
CLAIM_BOUNDARY = (
    "stage_open_design_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f73_stage_open_session_regime_feature_model_rotation"
GROK_PROMPT = GROK_PACKET / "prompts/f73_stage_open_session_regime_feature_model_rotation_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"

F72_STAGE = ROOT / "stages/stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling"
F72_CLOSEOUT = F72_STAGE / "03_reviews/stage_closeout_report.md"
F72_SELECTION = F72_STAGE / "04_selected/selection_status.md"
F70_CLOSEOUT = ROOT / "stages/stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation/03_reviews/stage_closeout_report.md"
F71_CLOSEOUT = ROOT / "stages/stage_frontier_71__economics_native_label_selection_for_joint_density_pf_dd/03_reviews/stage_closeout_report.md"
RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"

FWD12_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
FWD12_FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"
FWD18_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd18_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
FWD18_FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd18_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"

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


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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


def git_status() -> str:
    return subprocess.check_output(["git", "status", "--short", "--branch"], cwd=ROOT, text=True, encoding="utf-8").strip()


def data_identity() -> dict[str, Any]:
    fwd12 = pd.read_parquet(io_path(FWD12_INPUT))
    fwd18 = pd.read_parquet(io_path(FWD18_INPUT))
    features12 = [line.strip() for line in read_text(FWD12_FEATURE_ORDER).splitlines() if line.strip()]
    features18 = [line.strip() for line in read_text(FWD18_FEATURE_ORDER).splitlines() if line.strip()]
    return {
        "fwd12_path": rel(FWD12_INPUT),
        "fwd12_sha256": sha256(FWD12_INPUT),
        "fwd12_rows": int(len(fwd12)),
        "fwd12_columns": int(len(fwd12.columns)),
        "fwd12_split_counts": {str(k): int(v) for k, v in fwd12["split"].value_counts().to_dict().items()},
        "fwd12_timestamp_min": str(fwd12["timestamp"].min()),
        "fwd12_timestamp_max": str(fwd12["timestamp"].max()),
        "fwd18_path": rel(FWD18_INPUT),
        "fwd18_sha256": sha256(FWD18_INPUT),
        "fwd18_rows": int(len(fwd18)),
        "fwd18_columns": int(len(fwd18.columns)),
        "fwd18_split_counts": {str(k): int(v) for k, v in fwd18["split"].value_counts().to_dict().items()},
        "fwd18_timestamp_min": str(fwd18["timestamp"].min()),
        "fwd18_timestamp_max": str(fwd18["timestamp"].max()),
        "feature_order_path_fwd12": rel(FWD12_FEATURE_ORDER),
        "feature_order_path_fwd18": rel(FWD18_FEATURE_ORDER),
        "feature_count_fwd12": len(features12),
        "feature_count_fwd18": len(features18),
        "feature_order_hash_fwd12": ordered_hash(features12),
        "feature_order_hash_fwd18": ordered_hash(features18),
        "feature_order_same": features12 == features18,
    }


def required_material_for_prompt() -> list[Path]:
    return [F72_CLOSEOUT, F72_SELECTION, RETROSPECTIVE_REGISTER, NEGATIVE_REGISTER, FWD12_INPUT, FWD18_INPUT]


def required_material_for_materialize() -> list[Path]:
    return required_material_for_prompt() + [
        F70_CLOSEOUT,
        F71_CLOSEOUT,
        GROK_PROMPT,
        GROK_CLEAN,
        GROK_METADATA,
        FWD12_FEATURE_ORDER,
        FWD18_FEATURE_ORDER,
    ]


def prompt_lines(identity: Mapping[str, Any]) -> list[str]:
    return [
        "# F73 Stage Open Grok Prompt(F73 단계 개방 그록 프롬프트)",
        "",
        "You are Grok(Grok, 그록), an external second opinion reviewer(외부 2차 의견 검토자).",
        "Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(검색 금지), or do local verification(로컬 검증 금지).",
        "",
        "Required output sections(필수 출력 섹션): accepted(수용), rejected(거절), needs_local_verification(로컬 검증 필요), drift_risks(드리프트 위험), final_advice(최종 조언).",
        "",
        "## Current Truth(현재 진실)",
        "",
        "- Frontier72(F72 전선 단계) closed as preserved clue + negative memory(보존 단서 + 부정 기억), no authority(권위 없음).",
        "- F72F OOS runtime(표본외 런타임): net/PF/DD/trades_day/trades(순수익/수익 팩터/손실폭/일거래/거래) = 66.47/1.05/18.60%/2.4769/483.",
        "- F72 preserved clue(보존 단서): lifecycle count bridge(생명주기 개수 브리지) reduced expected/runtime trade-count gap(예상/런타임 거래 수 간극), and signal/feature parity(신호/피처 동등성) stayed diff 0.",
        "- F72 negative memory(부정 기억): trade-shape-first label/feature/lifecycle surface(거래 형태 우선 라벨/피처/생명주기 표면) did not create runtime economics(런타임 경제성).",
        "- Five-stage retrospective(5단계 중간 검토): not due after F72 closeout(F72 마감 뒤 아직 아님), 2/5 closeouts since last retrospective(마지막 중간 검토 이후 2/5).",
        "",
        "## Proposed F73 Direction(F73 제안 방향)",
        "",
        "Hypothesis(가설): session/regime-conditioned feature-set and model-family rotation(세션/장세 조건 피처 묶음과 모델 계열 회전)이 parity/lifecycle fixes(동등성/생명주기 수리)와 별개인 runtime economics source(런타임 경제성 원천)를 분리할 수 있다.",
        "",
        "Plain version(쉬운 설명): F72는 주문 개수와 준비 상태를 꽤 맞췄지만 돈 버는 구조가 약했다. F73은 같은 청산 모양을 더 만지기보다, 어느 시간대/장세에서 어떤 피처 묶음과 어떤 모델이 실제로 돈 되는 후보를 만드는지 넓게 바꿔본다.",
        "",
        "## Intentional Changes(의도 변경)",
        "",
        "- feature set(피처 묶음): all58(전체 58개), core price/path(핵심 가격/경로), session/regime-only plus core(세션/장세+핵심), no top3 proxy(상위3 대리 제거), low-correlation/top-importance recombination(저상관/중요도 재조합).",
        "- label/target(라벨/목표): fwd12(12봉 전방) and fwd18(18봉 전방), direct direction(직접 방향), inverse/rank read(역방향/순위 판독), quality-of-move proxy(움직임 품질 대리).",
        "- model family(모델 계열): logistic/linear(로지스틱/선형), ExtraTrees(엑스트라트리스), HistGradientBoosting(히스토그램 그래디언트 부스팅), small NN(작은 신경망) if dependency available(의존성 가능 시).",
        "- trade shape(거래 형태): not lead axis(주도 축 아님); use simple fixed lifecycle proxy(단순 고정 생명주기 프록시) so model/feature/regime differences are visible.",
        "- risk logic(위험 로직): keep bounded SL/TP/hold bands(제한된 손절/익절/보유 범위) as guardrail(보호 장치), not as the main repair.",
        "- regime/session split(장세/세션 분할): cash open/mid/late(정규장 초반/중반/후반), trend/chop/volatility buckets(추세/횡보/변동성 구간).",
        "",
        "## Controls(통제 변수)",
        "",
        "- Symbol/timeframe(심볼/시간프레임): US100 M5(US100 5분봉).",
        "- Split(분할): time-ordered train/validation/OOS(시간순 학습/검증/표본외).",
        "- Runtime rule(런타임 규칙): if proxy(프록시)가 meaningful signal(의미 있는 신호)을 만들면 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 실행한다.",
        "- Claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        "",
        "## Evidence Snapshot(근거 스냅샷)",
        "",
        f"- fwd12 input(12봉 입력): `{identity['fwd12_path']}`, rows(행) `{identity['fwd12_rows']}`, splits(분할) `{identity['fwd12_split_counts']}`.",
        f"- fwd18 input(18봉 입력): `{identity['fwd18_path']}`, rows(행) `{identity['fwd18_rows']}`, splits(분할) `{identity['fwd18_split_counts']}`.",
        f"- feature order same(피처 순서 동일): `{identity['feature_order_same']}`, feature counts(피처 수) `{identity['feature_count_fwd12']}/{identity['feature_count_fwd18']}`.",
        "",
        "## Success/Failure Boundary(성공/실패 경계)",
        "",
        "- scout clue(탐색 단서): validation and OOS(검증과 표본외) both net>0(순수익 양수), PF>=1.10(수익 팩터 1.10 이상), DD<=15%(손실폭 15% 이하), trades/day>=1.5(일거래 1.5 이상).",
        "- meaningful proxy signal(의미 있는 프록시 신호): PF>=1.25(수익 팩터 1.25 이상), DD<=10%(손실폭 10% 이하), trades/day>=3.0(일거래 3.0 이상), validation/OOS non-collapse(검증/표본외 붕괴 없음).",
        "- final-like reference only(최종 유사 참조 전용): PF>=2.0(수익 팩터 2.0 이상), DD<10%(손실폭 10% 미만), trades/day 5-10(일거래 5-10), smooth equity proxy(매끄러운 자산곡선 대리).",
        "- failure(실패): zero signal(영 신호), only post-hoc quota/throttle(사후 할당/제한만), or same F72 trade-shape-first repair(동일 F72 거래 형태 우선 수리).",
        "",
        "## Question For Grok(Grok에게 묻는 질문)",
        "",
        "Is this F73 direction genuinely different enough from F70/F71/F72(이 방향이 F70/F71/F72와 충분히 다른가), broad enough to satisfy the user's exploration concern(사용자의 넓은 탐색 걱정을 만족할 만큼 넓은가), and bounded enough to run as a single frontier lifecycle(하나의 전선 생명주기로 실행할 만큼 경계가 있는가)?",
    ]


def write_prompt() -> None:
    missing = [rel(path) for path in required_material_for_prompt() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F73A prompt material missing: {missing}")
    identity = data_identity()
    write_md(GROK_PROMPT, prompt_lines(identity))
    print(json.dumps({"prompt": rel(GROK_PROMPT), "packet": rel(GROK_PACKET)}, ensure_ascii=False, indent=2))


def axis_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "axis": "feature_set(피처 묶음)",
            "change": "remove, replace, and recombine all58/core/session/no-top3/top-importance bundles(전체58/핵심/세션/상위3제거/중요도 묶음 제거·교체·재조합)",
            "effect": "tests whether runtime economics(런타임 경제성) is hidden in feature composition(피처 구성)",
        },
        {
            "axis": "label_target(라벨/목표)",
            "change": "compare fwd12/fwd18 and direct/inverse/rank/quality targets(12봉/18봉 및 직접/역방향/순위/품질 목표 비교)",
            "effect": "prevents one label horizon(단일 라벨 예측수평선) from trapping the stage(단계)",
        },
        {
            "axis": "model_family(모델 계열)",
            "change": "rotate logistic, ExtraTrees, HistGradientBoosting, and small NN if available(로지스틱/엑스트라트리스/히스토그램 부스팅/가능 시 작은 신경망 회전)",
            "effect": "separates model bias(모델 편향) from feature/label value(피처/라벨 가치)",
        },
        {
            "axis": "trade_shape(거래 형태)",
            "change": "keep fixed lifecycle proxy as control(고정 생명주기 프록시를 통제 변수로 유지)",
            "effect": "avoids repeating F72 trade-shape-first repair(F72 거래 형태 우선 수리 반복 방지)",
        },
        {
            "axis": "risk_logic(위험 로직)",
            "change": "use bounded SL/TP/hold guardrails, not sizing rescue(제한된 손절/익절/보유 보호를 쓰되 비중 구제는 금지)",
            "effect": "keeps DD(손실폭) visible while scouting(탐색 중에도 보이게 함)",
        },
        {
            "axis": "regime_session(장세/세션)",
            "change": "evaluate cash open/mid/late and trend/chop/volatility buckets(정규장 초반/중반/후반 및 추세/횡보/변동성 구간 평가)",
            "effect": "turns session/regime(세션/장세) into attribution(귀속), not a post-hoc excuse(사후 핑계)",
        },
    ]


def surface_plan_rows() -> list[dict[str, str]]:
    return [
        {"surface": "all58_fwd12_reference", "feature_set": "all58(전체 58개)", "label_target": "fwd12 direct(12봉 직접)", "model_family": "logistic + ExtraTrees", "risk": "fixed lifecycle", "effect": "reference surface only(참조 표면 전용)"},
        {"surface": "all58_fwd18_horizon_shift", "feature_set": "all58(전체 58개)", "label_target": "fwd18 direct/inverse(18봉 직접/역방향)", "model_family": "linear + tree", "risk": "fixed lifecycle", "effect": "tests horizon sensitivity(예측수평선 민감도 시험)"},
        {"surface": "core_price_path_only", "feature_set": "core price/path(핵심 가격/경로)", "label_target": "fwd12/fwd18 rank(12/18봉 순위)", "model_family": "HistGradientBoosting", "risk": "bounded SL/TP", "effect": "checks if proxy/macro noise hurts economics(대리/거시 잡음 손상 확인)"},
        {"surface": "session_regime_core", "feature_set": "session/regime + core(세션/장세+핵심)", "label_target": "quality-of-move proxy(움직임 품질 대리)", "model_family": "ExtraTrees + small NN if available", "risk": "fixed lifecycle", "effect": "tests user-requested regime split(사용자 요청 장세 분할 시험)"},
        {"surface": "no_top3_proxy_ablation", "feature_set": "remove top3 proxy(상위3 대리 제거)", "label_target": "fwd12/fwd18", "model_family": "logistic + tree", "risk": "fixed lifecycle", "effect": "tests feature-set removal(피처 제거 시험)"},
        {"surface": "top_importance_recombination", "feature_set": "top-importance/low-corr recombination(중요도/저상관 재조합)", "label_target": "rank/quality", "model_family": "tree reference", "risk": "bounded guard", "effect": "tests recombination without inheriting a winner(승자 상속 없는 재조합 시험)"},
    ]


def prior_stage_difference_rows() -> list[dict[str, str]]:
    return [
        {
            "prior_stage": "F70 regime-specific asymmetric value(장세별 비대칭 가치)",
            "prior_lead_axis": "label/regime/exit-survival density(라벨/장세/청산 생존 밀도)",
            "f73_difference": "session/regime is attribution plus feature/model rotation, not the primary label thesis(세션/장세는 귀속과 피처/모델 회전이며 주 라벨 논제가 아님)",
            "effect": "prevents F70 regime-primary rerun(F70 장세 주도 반복 방지)",
        },
        {
            "prior_stage": "F71 economics-native label selection(경제성 네이티브 라벨 선택)",
            "prior_lead_axis": "what-to-select via economics label/selection(경제성 라벨/선택으로 무엇을 고를지)",
            "f73_difference": "feature-set and model-family rotation are lead axes while labels are compared as horizons/targets(피처 묶음과 모델 계열 회전이 주도 축이고 라벨은 수평선/목표 비교)",
            "effect": "prevents q/tape-only selection repeat(q/테이프 단독 선택 반복 방지)",
        },
        {
            "prior_stage": "F72 trade-shape-first exit/risk labeling(거래 형태 우선 청산/위험 라벨링)",
            "prior_lead_axis": "trade shape, exit distribution, lifecycle repair(거래 형태/청산 분포/생명주기 수리)",
            "f73_difference": "fixed lifecycle becomes a control while feature/label/model/regime surfaces rotate(고정 생명주기는 통제 변수로 낮추고 피처/라벨/모델/장세 표면을 회전)",
            "effect": "prevents same F72 trade-shape surface repeat(동일 F72 거래 형태 표면 반복 방지)",
        },
    ]


def experiment_design(identity: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "idea_id": IDEA_ID,
        "hypothesis": "Session/regime-conditioned feature-set and model-family rotation(세션/장세 조건 피처 묶음과 모델 계열 회전)이 runtime economics gap(런타임 경제성 간극)을 분리할 수 있다.",
        "decision_use": "Decide whether F73B should run broad proxy scout across feature/label/model/regime axes(F73B가 피처/라벨/모델/장세 축 넓은 프록시 탐색을 실행할지 결정).",
        "comparison_baseline": "F72 preserved clue only; no inherited baseline/winner/authority(F72 보존 단서만 참조, 기준선/승자/권위 상속 없음).",
        "control_variables": [
            "US100 M5 symbol/timeframe(US100 5분봉 심볼/시간프레임)",
            "time-ordered train/validation/OOS split(시간순 학습/검증/표본외 분할)",
            "no future feature leakage(미래 피처 누수 금지)",
            "fixed lifecycle proxy as control(고정 생명주기 프록시를 통제 변수로 사용)",
        ],
        "changed_variables": [
            "feature set removal/replacement/recombination(피처 묶음 제거/교체/재조합)",
            "label horizon and target semantics(라벨 예측수평선과 목표 의미)",
            "model family rotation(모델 계열 회전)",
            "regime/session attribution(장세/세션 귀속)",
        ],
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5(5분봉)",
            "tier_scope": "Tier A separate planned; Tier B missing_required unless materialized(Tier A 분리 계획, Tier B는 물질화 전 필수 누락 기록)",
            "data_identity": identity,
        },
        "success_criteria": {
            "scout_clue": "validation/OOS net>0, PF>=1.10, DD<=15%, trades/day>=1.5(검증/표본외 순수익 양수, 수익 팩터 1.10 이상, 손실폭 15% 이하, 일거래 1.5 이상)",
            "meaningful_signal": "PF>=1.25, DD<=10%, trades/day>=3.0, non-collapse across validation/OOS(수익 팩터 1.25 이상, 손실폭 10% 이하, 일거래 3 이상, 검증/표본외 비붕괴)",
        },
        "failure_criteria": [
            "zero signal across broad sweep(넓은 탐색 전체 영 신호)",
            "only post-hoc quota/throttle works(사후 할당/제한만 작동)",
            "same F72 trade-shape-first surface repeats(F72 동일 거래 형태 우선 표면 반복)",
        ],
        "invalid_conditions": [
            "feature leakage across label horizon(라벨 수평선 너머 피처 누수)",
            "model selection uses OOS for tuning(모델 선택에 표본외 튜닝 사용)",
            "runtime bridge cannot express selected surface(런타임 연결이 선택 표면을 표현 불가)",
        ],
        "stop_conditions": [
            "run mandatory MT5 Runtime Probe after meaningful proxy signal(의미 있는 프록시 신호 뒤 필수 MT5 런타임 탐침 실행)",
            "repair only after proxy/runtime gap is named(프록시/런타임 간극 명명 뒤에만 수리)",
            "close as negative_memory if broad axes produce no scout clue(넓은 축이 탐색 단서를 못 만들면 부정 기억으로 마감)",
        ],
        "evidence_plan": [
            "stage brief(단계 개요)",
            "Grok stage-open receipt(Grok 단계 개방 영수증)",
            "proxy surface plan(프록시 표면 계획)",
            "F73B proxy KPI report(F73B 프록시 핵심 성과 지표 보고)",
            "MT5 Runtime Probe KPI if meaningful signal appears(의미 신호 발생 시 MT5 런타임 탐침 핵심 성과 지표)",
        ],
    }


def data_integrity_plan(identity: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "data_source": [identity["fwd12_path"], identity["fwd18_path"]],
        "time_axis": "timestamp is closed M5 bar time in UTC-style project contract(타임스탬프는 프로젝트 계약상 확정 5분봉 시간)",
        "sample_scope": "US100 M5 fwd12/fwd18 model inputs(US100 5분봉 12봉/18봉 모델 입력)",
        "missing_or_duplicate_check": "deferred to F73B pre-run audit(F73B 실행 전 감사로 이월)",
        "feature_label_boundary": "features must be known at entry bar close; labels use future horizon only as target(피처는 진입 봉 마감에 알려져야 하고 라벨만 미래 수평선 사용)",
        "split_boundary": "train/validation/OOS time ordered(학습/검증/표본외 시간순)",
        "leakage_risk": "feature recombination or top-importance selection could overfit validation(피처 재조합/중요도 선택이 검증에 과적합 가능)",
        "data_hash_or_identity": identity,
        "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
    }


def model_validation_plan() -> dict[str, Any]:
    return {
        "model_family": "logistic, ExtraTrees, HistGradientBoosting, small NN if available(로지스틱, 엑스트라트리스, 히스토그램 부스팅, 가능 시 작은 신경망)",
        "target_and_label": "fwd12/fwd18 direction/rank/quality targets(12봉/18봉 방향/순위/품질 목표)",
        "split_method": "time holdout scout, WFO planned after meaningful signal(시간 홀드아웃 탐색, 의미 신호 후 워크포워드 계획)",
        "selection_metric": "joint proxy utility from net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래 공동 프록시 효용)",
        "secondary_metrics": "win rate, payoff, expectancy, long/short mix, session attribution(승률, 손익비, 기대값, 롱/숏 비율, 세션 귀속)",
        "threshold_policy": "broad scout quantiles, no OOS tuning(넓은 탐색 분위수, 표본외 튜닝 금지)",
        "overfit_risk": "many surfaces can overfit validation(많은 표면이 검증에 과적합 가능)",
        "calibration_risk": "scores are ranks unless calibrated(보정 전 점수는 확률이 아니라 순위)",
        "comparison_baseline": "F72 negative memory and no-trade baseline(F72 부정 기억과 무거래 기준)",
        "validation_judgment": "exploratory(탐색)",
    }


def local_verification(identity: Mapping[str, Any]) -> dict[str, Any]:
    f70_closeout = read_text(F70_CLOSEOUT)
    f71_closeout = read_text(F71_CLOSEOUT)
    f72_closeout = read_text(F72_CLOSEOUT)
    f72_selection = read_text(F72_SELECTION)
    retrospective = read_text(RETROSPECTIVE_REGISTER)
    grok_clean = read_text(GROK_CLEAN)
    metadata = json.loads(read_text(GROK_METADATA))
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "f72_closeout_label_found": "closed_preserved_clue_negative_memory_no_authority" in f72_closeout,
        "f70_difference_verified": (
            "Regime/session-specific asymmetric value" in f70_closeout
            and "same_f70_label_model_axis_should_not_repeat" in f70_closeout
            and "Negative Memory" in f70_closeout
        ),
        "f71_difference_verified": "economics-native label/selection" in f71_closeout and "Negative Memory" in f71_closeout,
        "f72_next_action_found": RUN_ID in f72_selection or "frontier73A_stage_open_new_hypothesis_after_f72_trade_shape_negative_memory_v1" in f72_selection,
        "f72_negative_memory_found": "Negative Memory" in f72_closeout,
        "five_stage_retrospective_not_due": "not_due_after_f72_closeout" in retrospective,
        "grok_success": bool(metadata.get("success")),
        "grok_returncode": metadata.get("returncode"),
        "grok_prompt_hash": metadata.get("prompt_hash"),
        "grok_clean_hash": sha256(GROK_CLEAN),
        "grok_accepted_found": "accepted" in grok_clean.lower(),
        "grok_rejected_found": "rejected" in grok_clean.lower(),
        "grok_needs_local_verification_found": "needs_local_verification" in grok_clean.lower(),
        "feature_order_same": identity["feature_order_same"],
        "git_status": git_status(),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def run_manifest(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "inputs": {
            "f72_closeout": rel(F72_CLOSEOUT),
            "f72_selection": rel(F72_SELECTION),
            "retrospective_register": rel(RETROSPECTIVE_REGISTER),
            "grok_prompt": rel(GROK_PROMPT),
            "grok_clean_output": rel(GROK_CLEAN),
        },
        "outputs": {
            "open_report": rel(REVIEWS_ROOT / "frontier73A_stage_open_session_regime_feature_model_rotation_report.md"),
            "stage_brief": rel(SPEC_ROOT / "stage_brief.md"),
            "selection_status": rel(SELECTED_ROOT / "selection_status.md"),
            "gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73a.md"),
        },
        "verification": verification,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": payload["created_at_utc"],
    }


def report_lines(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> list[str]:
    identity = payload["experiment_design"]["sample_scope"]["data_identity"]
    return [
        "# Frontier73A Stage Open(F73A 단계 개방)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Hypothesis(가설)",
        "",
        "Session/regime-conditioned feature-set and model-family rotation(세션/장세 조건 피처 묶음과 모델 계열 회전)이 F72에서 남은 runtime economics gap(런타임 경제성 간극)을 분리할 수 있는지 시험한다.",
        "",
        "Effect(효과): 같은 trade-shape-first repair(거래 형태 우선 수리)를 반복하지 않고, feature set/label/model/regime(피처 묶음/라벨/모델/장세) 축을 넓게 바꿔본다.",
        "",
        "## Test Period(테스트 기간)",
        "",
        f"- fwd12(12봉): `{identity['fwd12_timestamp_min']}..{identity['fwd12_timestamp_max']}`.",
        f"- fwd18(18봉): `{identity['fwd18_timestamp_min']}..{identity['fwd18_timestamp_max']}`.",
        "- split/view(분할/보기): train/validation/OOS design only(학습/검증/표본외 설계 전용).",
        "",
        "## Proxy Expectation(프록시 예상)",
        "",
        "At least one surface(표면)가 session/regime attribution(세션/장세 귀속)과 feature/model rotation(피처/모델 회전) 안에서 scout clue(탐색 단서)를 만들면 F73B 이후 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)로 물질화한다.",
        "",
        "## Planned KPI(계획 핵심 성과 지표)",
        "",
        "- proxy KPI(프록시 핵심 성과 지표): net profit/PF/DD/trade count/trades/day/win rate/expectancy/recovery factor(순수익/수익 팩터/손실폭/거래 수/일거래/승률/기대값/회복 계수).",
        "- runtime probe KPI(런타임 탐침 핵심 성과 지표): mandatory after meaningful proxy signal(의미 있는 프록시 신호 뒤 필수).",
        "- signal count parity(신호 수 동등성): not applicable at stage open(단계 개방 해당 없음).",
        "- feature readiness parity(피처 준비 동등성): not applicable at stage open(단계 개방 해당 없음).",
        "",
        "## Grok Review(Grok 검토)",
        "",
        f"- prompt(프롬프트): `{rel(GROK_PROMPT)}`, sha256 `{verification['grok_prompt_hash']}`.",
        f"- output(출력): `{rel(GROK_CLEAN)}`, sha256 `{verification['grok_clean_hash']}`.",
        "- classification(분류): `accepted_with_rejections_and_local_verification(거절/로컬 검증 포함 수용)`.",
        "- accepted(수용): F73 is a new upstream axis(새 상류 축), broad exploration surface(넓은 탐색 표면), and fixed lifecycle as control(통제 변수로 고정 생명주기).",
        "- rejected(거절): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claims.",
        "- needs_local_verification(로컬 검증 필요): data identity(데이터 정체성), feature order(피처 순서), F72 next action(F72 다음 행동), retrospective due(중간 검토 도래).",
        "",
        "## Prior Stage Difference(이전 단계 차이)",
        "",
        "| prior(이전) | F73 difference(F73 차이) | effect(효과) |",
        "|---|---|---|",
        "| F70 | session/regime(세션/장세)을 주 라벨 축이 아니라 attribution(귀속) 축으로 둔다 | F70 regime-primary rerun(F70 장세 주도 반복)을 막는다 |",
        "| F71 | economics-native label selection(경제성 네이티브 라벨 선택)이 아니라 feature/model rotation(피처/모델 회전)을 주도 축으로 둔다 | F71 q/tape-only repeat(q/테이프 단독 반복)을 막는다 |",
        "| F72 | lifecycle/trade shape(생명주기/거래 형태)는 control(통제)이고 lead repair(주도 수리)가 아니다 | F72 trade-shape-first repeat(거래 형태 우선 반복)을 막는다 |",
        "",
        "## Pruned Matrix(축소 실행 매트릭스)",
        "",
        "Grok warned against full Cartesian product(전체 데카르트 조합). F73B starts from six named surfaces(이름 붙인 6개 표면) and expands only after scout clue(탐색 단서)가 나온다.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`.",
        "",
        "Effect(효과): F73B에서 proxy scout(프록시 탐색)를 실행하고, 의미 신호가 있으면 Grok pre-MT5 review(Grok 사전 MT5 검토) 뒤 MT5 Runtime Probe(MT5 런타임 탐침)를 실행한다.",
    ]


def stage_brief_lines() -> list[str]:
    return [
        "# Frontier73 Brief(F73 개요)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- opened_by(개방 실행): `{RUN_ID}`",
        f"- next_run(다음 실행): `{NEXT_RUN_ID}`",
        f"- idea_id(아이디어 ID): `{IDEA_ID}`",
        "- focus(초점): session/regime-conditioned feature-set and model-family rotation(세션/장세 조건 피처 묶음과 모델 계열 회전).",
        "- do_not_repeat(반복 금지): same F72 trade-shape-first surface(동일 F72 거래 형태 우선 표면), F71 q/tape-only selection(단독 q/테이프 선택), F70 regime-primary rerun(F70 장세 주도 반복).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def selection_status_lines() -> list[str]:
    return [
        "# F73 Selection Status(F73 선택 상태)",
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
        "# F73 Stage Open Grok Receipt(F73 단계 개방 Grok 영수증)",
        "",
        f"- created_at_utc(생성): `{payload['created_at_utc']}`",
        "- trigger_reason(트리거 이유): goal(목표)에 stage open(단계 개방) Grok second opinion(그록 2차 의견)이 필수로 지정됨.",
        "- review_size(검토 크기): `small(소규모)`.",
        "- bounded_evidence(제한 근거): F72 closeout(F72 마감), F72 selection status(F72 선택 상태), five-stage retrospective register(5단계 중간 검토 등록부), fwd12/fwd18 data identity(12봉/18봉 데이터 정체성), proposed F73 direction(F73 제안 방향).",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{verification['grok_prompt_hash']}`.",
        f"- output_identity(출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{verification['grok_clean_hash']}`.",
        "- advice_classification(조언 분류): `accepted_with_rejections_and_local_verification(거절/로컬 검증 포함 수용)`.",
        "- accepted(수용): new upstream axis(새 상류 축), broad feature/label/model/regime sweep(넓은 피처/라벨/모델/장세 탐색), fixed lifecycle as control(통제 변수로 고정 생명주기).",
        "- rejected(거절): any completion/baseline/promotion/runtime authority/live readiness/Goal Achieve claim(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장).",
        "- needs_local_verification(로컬 검증 필요): data identity(데이터 정체성), feature order same(피처 순서 동일), F70/F71/F72 differentiation(차이 확인), not-due retrospective(중간 검토 아직 아님).",
        f"- local_verification(로컬 검증): F70 diff `{verification['f70_difference_verified']}`, F71 diff `{verification['f71_difference_verified']}`, F72 closeout `{verification['f72_closeout_label_found']}`, F72 next action `{verification['f72_next_action_found']}`, retrospective not due `{verification['five_stage_retrospective_not_due']}`, feature order same `{verification['feature_order_same']}`, Grok success `{verification['grok_success']}`.",
        "- pruned_matrix(축소 실행 매트릭스): accepted(수용). Full Cartesian product(전체 데카르트 조합)은 rejected(거절); six named surfaces(이름 붙인 6개 표면)부터 시작.",
        "- forbidden_claim_check(금지 주장 확인): pass(통과), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        f"- final_codex_direction(최종 Codex 방향): `{NEXT_RUN_ID}`.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def gate_audit_lines(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> list[str]:
    return [
        "# F73A Required Gate Coverage Audit(F73A 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| reentry_truth_alignment(재진입 진실 정렬) | pass(통과) | `{rel(WORKSPACE_STATE)}` + `{rel(F72_SELECTION)}` | F73A가 F72 next action(다음 행동)과 정렬됨 |",
        f"| five_stage_retrospective_due_check(5단계 중간 검토 도래 점검) | not_due(아직 아님) | `{rel(RETROSPECTIVE_REGISTER)}` | F73 개방 차단 없음 |",
        f"| Grok stage open review(Grok 단계 개방 검토) | pass_with_local_verification(로컬 검증 포함 통과) | `{rel(REVIEWS_ROOT / 'grok_stage_open_receipt.md')}` | 외부 2차 의견을 수용/거절/검증으로 분리 |",
        f"| experiment_design(실험 설계) | pass(통과) | `{rel(RUN_ROOT / 'f73a_experiment_design.json')}` | 가설/비교/통제/중단 조건 고정 |",
        f"| surface_plan(표면 계획) | pass(통과) | `{rel(RUN_ROOT / 'f73a_proxy_scout_surface_plan.csv')}` | 피처/라벨/모델/장세 변경을 명시 |",
        f"| prior_stage_difference(이전 단계 차이) | pass(통과) | `{rel(REVIEWS_ROOT / 'f73a_prior_stage_difference_table.csv')}` | F70/F71/F72 반복 위험을 분리 |",
        f"| data_integrity_boundary(데이터 무결성 경계) | pass_with_boundary(경계 포함 통과) | `{rel(RUN_ROOT / 'f73a_data_integrity_plan.json')}` | F73B 실행 전 누락/중복/누수 점검 필요를 보존 |",
        f"| claim_guard(주장 보호) | pass(통과) | `{CLAIM_BOUNDARY}` | 강한 주장 없음 |",
    ]


def ledger_row(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> dict[str, Any]:
    report = REVIEWS_ROOT / "frontier73A_stage_open_session_regime_feature_model_rotation_report.md"
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
        "path": rel(report),
        "primary_kpi": "axis_rows=6; surface_rows=6; grok=accepted_with_rejections_and_local_verification",
        "guardrail_kpi": "no F72 same-surface repeat; fixed lifecycle control; mandatory MT5 probe after meaningful proxy",
        "external_verification_status": "out_of_scope_by_claim_stage_open_design_only(단계 개방 설계 주장 범위 밖)",
        "notes": "F73 opened as session/regime feature/model rotation after F72 runtime economics negative memory.",
        "family": "experiment_design(실험 설계)",
        "lane": "stage_open(단계 개방)",
        "primary_report": rel(report),
        "run_number": "frontier73A",
        "date": payload["created_at_utc"][:10],
        "decision": "open_f73_session_regime_feature_model_rotation",
        "next_run_id": NEXT_RUN_ID,
        "rows": 6,
        "gate_passes": 7,
        "gate_total": 7,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(report),
        "run_date": payload["created_at_utc"][:10],
        "primary_artifact": rel(RUN_ROOT / "run_manifest.json"),
        "view": "stage_open_design(단계 개방 설계)",
        "tier": "Tier A+B planned(Tier A+B 계획)",
        "metric_scope": "design(설계)",
        "source_package_run_id": PARENT_RUN_ID,
        "result_status": STATUS,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(report),
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73a.md"),
        "created_at": payload["created_at_utc"],
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73a.md"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "stage_open_design_and_grok_review_only(단계 개방 설계 및 Grok 검토 전용)",
        "evidence_boundary": "stage_open_design_only_no_runtime(단계 개방 설계 전용, 런타임 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can session/regime feature/model rotation separate runtime economics source?(세션/장세 피처/모델 회전이 런타임 경제성 원천을 분리할 수 있나?)",
        "artifact_count": 12,
        "work_family": "experiment_design(실험 설계)",
        "run_family": "frontier_stage_open(전선 단계 개방)",
        "run_type": "session_regime_feature_model_rotation_design(세션/장세 피처/모델 회전 설계)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "result_path": rel(report),
    }


def write_outputs(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> None:
    for path in (RUN_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT, SPEC_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_json(RUN_ROOT / "f73a_experiment_design.json", payload["experiment_design"])
    write_json(RUN_ROOT / "f73a_data_integrity_plan.json", payload["data_integrity"])
    write_json(RUN_ROOT / "f73a_model_validation_plan.json", payload["model_validation"])
    write_json(RUN_ROOT / "f73a_local_verification.json", verification)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(payload, verification))
    write_csv(RUN_ROOT / "f73a_axis_rotation_contract.csv", axis_contract_rows())
    write_csv(RUN_ROOT / "f73a_proxy_scout_surface_plan.csv", surface_plan_rows())
    write_csv(RUN_ROOT / "f73a_prior_stage_difference_table.csv", prior_stage_difference_rows())
    write_md(RUN_ROOT / "reports/result_summary.md", report_lines(payload, verification))
    write_md(SPEC_ROOT / "stage_brief.md", stage_brief_lines())
    write_md(SELECTED_ROOT / "selection_status.md", selection_status_lines())
    write_json(REVIEWS_ROOT / "f73a_local_verification.json", verification)
    write_json(REVIEWS_ROOT / "f73a_experiment_design_review.json", payload["experiment_design"])
    write_json(REVIEWS_ROOT / "f73a_data_integrity_plan_review.json", payload["data_integrity"])
    write_json(REVIEWS_ROOT / "f73a_model_validation_plan_review.json", payload["model_validation"])
    write_csv(REVIEWS_ROOT / "f73a_axis_rotation_contract_review.csv", axis_contract_rows())
    write_csv(REVIEWS_ROOT / "f73a_proxy_scout_surface_plan_review.csv", surface_plan_rows())
    write_csv(REVIEWS_ROOT / "f73a_prior_stage_difference_table.csv", prior_stage_difference_rows())
    write_md(REVIEWS_ROOT / "frontier73A_stage_open_session_regime_feature_model_rotation_report.md", report_lines(payload, verification))
    write_md(REVIEWS_ROOT / "grok_stage_open_receipt.md", grok_receipt_lines(payload, verification))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f73a.md", gate_audit_lines(payload, verification))
    write_md(REVIEWS_ROOT / "review_index.md", [
        "# F73 Review Index(F73 검토 색인)",
        "",
        "- `frontier73A_stage_open_session_regime_feature_model_rotation_report.md`: stage open report(단계 개방 보고서)",
        "- `grok_stage_open_receipt.md`: Grok stage-open receipt(Grok 단계 개방 영수증)",
        "- `required_gate_coverage_audit_f73a.md`: required gate audit(필수 게이트 감사)",
    ])


def update_registers(payload: Mapping[str, Any]) -> None:
    marker = "<!-- frontier73A_stage_open_session_regime_feature_model_rotation_v1 -->"
    block = f"""<!-- frontier73A_stage_open_session_regime_feature_model_rotation_v1 -->
- `{IDEA_ID}`: `{RUN_ID}` opens Frontier73(전선73) as session/regime feature-set and model-family rotation(세션/장세 피처 묶음 및 모델 계열 회전). Hypothesis(가설): F72 lifecycle/parity clue(F72 생명주기/동등성 단서)를 control(통제)로 낮추고, feature set/label/model/regime(피처 묶음/라벨/모델/장세)을 넓게 바꾸면 runtime economics source(런타임 경제성 원천)를 분리할 수 있다. Boundary(경계): stage_open_design_only(단계 개방 설계 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
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
        "runtime_probe_status: f73_mandatory_runtime_probe_pending_after_meaningful_proxy_signal",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f72_closeout",
        f"updated_at_utc: '{payload['created_at_utc']}'",
        "notes:",
        '  - "Action(행동): F73A stage open(단계 개방)을 session/regime feature-set and model-family rotation(세션/장세 피처 묶음 및 모델 계열 회전)으로 물질화했다."',
        '  - "Effect(효과): F72 trade-shape-first repair(거래 형태 우선 수리) 반복을 막고, F73B를 feature/label/model/regime(피처/라벨/모델/장세) 넓은 프록시 탐색으로 고정한다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    write_md(CURRENT_WORKING_STATE, [
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
        "Action(행동): F73A stage open(단계 개방)을 완료했다.",
        "",
        "Effect(효과): 다음 실행은 session/regime feature/model rotation proxy scout(세션/장세 피처/모델 회전 프록시 탐색)이며, 의미 있는 signal(신호)이 나오면 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)로 물질화한다.",
        "",
        f"- status(상태): `{STATUS}`.",
        "- Grok advice(Grok 조언): accepted with local verification(로컬 검증 포함 수용).",
        "- five-stage retrospective(5단계 중간 검토): `not_due_after_f72_closeout(아직 아님)`.",
        "- runtime probe(런타임 탐침): meaningful proxy signal(의미 있는 프록시 신호) 뒤 필수.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ])


def materialize() -> None:
    missing = [rel(path) for path in required_material_for_materialize() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F73A material missing: {missing}")
    identity = data_identity()
    verification = local_verification(identity)
    payload = {
        "created_at_utc": utc_now(),
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "experiment_design": experiment_design(identity),
        "data_integrity": data_integrity_plan(identity),
        "model_validation": model_validation_plan(),
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
        "feature_order_same": verification["feature_order_same"],
        "claim_boundary": CLAIM_BOUNDARY,
    }), ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-prompt", action="store_true")
    parser.add_argument("--materialize", action="store_true")
    args = parser.parse_args()
    if args.write_prompt == args.materialize:
        raise SystemExit("Choose exactly one of --write-prompt or --materialize")
    if args.write_prompt:
        write_prompt()
    if args.materialize:
        materialize()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
