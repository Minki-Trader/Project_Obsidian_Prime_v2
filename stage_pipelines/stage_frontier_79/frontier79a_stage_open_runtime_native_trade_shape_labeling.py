from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.grok_review_wrapper import run_grok_review
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_79__runtime_native_trade_shape_labeling_from_fill_path"
RUN_ID = "frontier79A_stage_open_runtime_native_trade_shape_labeling_from_fill_path_v1"
PARENT_RUN_ID = "frontier78G_zero_signal_or_negative_repair_closeout_decision_v1"
NEXT_RUN_ID = "frontier79B_runtime_native_trade_shape_label_proxy_scout_v1"
IDEA_ID = "IDEA-FR79-RUNTIME-NATIVE-TRADE-SHAPE-LABELING-FROM-FILL-PATH"

STATUS_SUCCESS = "stage_open_runtime_native_trade_shape_labeling_completed_no_authority"
STATUS_REVIEW_FAIL = "stage_open_grok_review_failed_repair_required_no_authority"
JUDGMENT_SUCCESS = "runtime_native_trade_shape_labeling_stage_open_design_only_no_authority"
JUDGMENT_REVIEW_FAIL = "stage_open_direction_needs_repair_before_proxy_no_authority"
CLAIM_BOUNDARY = (
    "stage_open_design_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
SPEC_DIR = STAGE_DIR / "00_spec"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

DATASET_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_feature_order.txt"
)
RAW_BARS_PATH = ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"
F78_CLOSEOUT = ROOT / (
    "stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/"
    "03_reviews/stage_closeout_report.md"
)
F78_SELECTION = ROOT / (
    "stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/"
    "04_selected/selection_status.md"
)
RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f79a_stage_open_runtime_native_trade_shape_labeling"
GROK_PROMPT = GROK_PACKET / "prompts/f79a_stage_open_runtime_native_trade_shape_labeling_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"

STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
EXPERIMENT_DESIGN = REVIEW_DIR / "f79a_experiment_design_review.json"
AXIS_CONTRACT = REVIEW_DIR / "f79a_runtime_native_axis_contract.csv"
DATA_IDENTITY = REVIEW_DIR / "f79a_data_identity_review.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f79a_grok_stage_open_local_verification.json"
REPORT = REVIEW_DIR / "frontier79A_stage_open_runtime_native_trade_shape_labeling_report.md"
GROK_RECEIPT = REVIEW_DIR / "grok_stage_open_runtime_native_trade_shape_labeling_receipt.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f79a.md"
ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"

SCRIPT_REL = "stage_pipelines/stage_frontier_79/frontier79a_stage_open_runtime_native_trade_shape_labeling.py"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256_binary(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_hash(path: Path) -> str:
    if not path_exists(path):
        return ""
    if path.suffix.lower() in {".parquet", ".csv"}:
        return sha256_binary(path)
    return sha256_file_lf_normalized(path)


def ensure_dirs() -> None:
    for path in (SPEC_DIR, RUN_DIR, REVIEW_DIR, SELECTED_DIR, GROK_PROMPT.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(read_text(path)) or {}


def data_identity() -> dict[str, Any]:
    required = [DATASET_PATH, FEATURE_ORDER_PATH, RAW_BARS_PATH, F78_CLOSEOUT, F78_SELECTION, RETROSPECTIVE_REGISTER]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required F79A input(s): {missing}")
    df = pd.read_parquet(io_path(DATASET_PATH))
    features = [line.strip() for line in read_text(FEATURE_ORDER_PATH).splitlines() if line.strip()]
    raw_sample = pd.read_csv(io_path(RAW_BARS_PATH), nrows=5)
    return {
        "dataset_path": rel(DATASET_PATH),
        "dataset_sha256": file_hash(DATASET_PATH),
        "dataset_rows": int(df.shape[0]),
        "dataset_columns": int(df.shape[1]),
        "split_counts": {str(k): int(v) for k, v in df["split"].value_counts(dropna=False).items()} if "split" in df.columns else {},
        "timestamp_min": str(df["timestamp"].min()) if "timestamp" in df.columns else "",
        "timestamp_max": str(df["timestamp"].max()) if "timestamp" in df.columns else "",
        "feature_order_path": rel(FEATURE_ORDER_PATH),
        "feature_order_sha256": file_hash(FEATURE_ORDER_PATH),
        "feature_count": len(features),
        "feature_preview": features[:16],
        "raw_bars_path": rel(RAW_BARS_PATH),
        "raw_bars_sha256": file_hash(RAW_BARS_PATH),
        "raw_columns": list(raw_sample.columns),
        "raw_head": raw_sample.to_dict(orient="records"),
    }


def prior_snapshot() -> dict[str, Any]:
    closeout = read_text(F78_CLOSEOUT)
    selection = read_text(F78_SELECTION)
    return {
        "closeout_report": rel(F78_CLOSEOUT),
        "closeout_report_sha256": file_hash(F78_CLOSEOUT),
        "selection_status": rel(F78_SELECTION),
        "selection_status_sha256": file_hash(F78_SELECTION),
        "closeout_excerpt": "\n".join(closeout.splitlines()[:90]),
        "selection_excerpt": "\n".join(selection.splitlines()[:24]),
        "closed_status": "closed_negative_memory_no_authority",
        "closed_judgment": "negative_memory_with_preserved_clue_no_authority",
        "preserved_clue": [
            "ONNX/EA feature and signal parity(ONNX/EA 피처와 신호 동등성)는 정확히 맞출 수 있었다.",
            "Selected-entry veto tape(선택 진입 거부 테이프)는 proxy selected count(프록시 선택 수)와 runtime signal count(런타임 신호 수)를 맞추는 도구로 보존한다.",
            "Entry timing(진입 시각)과 DD denominator(손실폭 분모)는 proxy label(프록시 라벨) 설계 시작부터 명시해야 한다.",
        ],
        "negative_memory": [
            "Next-bar proxy(다음 봉 프록시)는 양수여도 MT5 same-bar execution(MT5 동일 봉 실행)에서는 음수가 될 수 있다.",
            "Runtime-aligned entry(런타임 정렬 진입)와 tester-deposit DD(테스터 예치금 손실폭) 수리 뒤 F78F는 scout clue(탐색 단서) 0, meaningful signal(의미 신호) 0이었다.",
            "F78은 threshold-only(임계값 단독)나 model-only(모델 단독) 수리로 계속 밀면 반복 수리가 된다.",
        ],
    }


def retrospective_status() -> dict[str, Any]:
    state = load_yaml(RETROSPECTIVE_REGISTER).get("state", {})
    return {
        "current_due_status": state.get("current_due_status"),
        "closeouts_since_last": state.get("closeouts_since_last"),
        "closed_frontier_ids_since_last_retrospective": state.get("closed_frontier_ids_since_last_retrospective", []),
        "next_numeric_trigger_frontier": state.get("next_numeric_trigger_frontier"),
    }


def axis_rows() -> list[dict[str, str]]:
    return [
        {
            "axis": "feature_set(피처 묶음)",
            "f79_action": "test full58, contract_core, price_vol_session, runtime_fill_context, and ablated no_external/no_session sets(전체58, 계약 핵심, 가격/변동성/세션, 런타임 체결 문맥, 외부/세션 제거 묶음 시험)",
            "effect": "separates actual source value(원천 가치) from F78 parity-only repair(동등성 단독 수리)",
            "broad_sweep": "full58, contract_core, price_vol_session, runtime_fill_context, no_external, no_session",
        },
        {
            "axis": "label_target(라벨/목표)",
            "f79_action": "build same-bar/next-tick fill-path labels with first-touch order, MAE/MFE, net utility, DD-normalized utility, and density quota(동일 봉/다음 틱 체결 경로, 선도달 순서, MAE/MFE, 순효용, 손실폭 정규화 효용, 밀도 할당)",
            "effect": "moves entry timing(진입 시각), fill ordering(체결 순서), and tester-deposit DD(테스터 예치금 손실폭)를 proxy expectation(프록시 예상)에 처음부터 넣는다",
            "broad_sweep": "fill_path_net, first_touch_utility, mae_mfe_asymmetry, dd_normalized_utility, density_quota",
        },
        {
            "axis": "model_family(모델 계열)",
            "f79_action": "compare LGBM-like HistGBM, linear/logistic, ExtraTrees, EBM-style shallow additive proxy, and small NN when exportable(히스토그램 GBM, 선형/로지스틱, ExtraTrees, EBM식 얕은 가산 프록시, 내보내기 가능한 작은 신경망)",
            "effect": "tests whether runtime-native labels(런타임 네이티브 라벨)이 특정 model bias(모델 편향)에만 걸리는지 분리한다",
            "broad_sweep": "logistic, ridge, HistGradientBoosting, ExtraTrees, shallow additive bins, small MLP proxy",
        },
        {
            "axis": "trade_shape(거래 형태)",
            "f79_action": "vary long/short/both, entry delay, SL/TP first-touch, max hold, opposite exit, cooldown, and one-position occupancy(롱/숏/양방향, 진입 지연, 손절/익절 선도달, 최대 보유, 반대 신호 청산, 쿨다운, 단일 포지션 점유)",
            "effect": "treats trade count(거래 수) as realized lifecycle(실현 생명주기), not independent signal count(독립 신호 수)",
            "broad_sweep": "short, long, both, hold 6/12/18/24, cooldown 0/3/6, SLTP grids",
        },
        {
            "axis": "risk_logic(위험 로직)",
            "f79_action": "score with Deposit=500 DD, fixed 0.1 lot, spread-aware cost, MAE gate, loss streak guard, and daily DD guard proxies(예치금 500 손실폭, 고정 0.1랏, 스프레드 비용, MAE 게이트, 연속 손실 보호, 일 손실 보호 프록시)",
            "effect": "brings drawdown control(손실폭 제어) before MT5 materialization(MT5 물질화)",
            "broad_sweep": "DD penalty, MAE gate, loss streak cap, daily stop proxy, recovery factor filter",
        },
        {
            "axis": "regime_session_split(장세/세션 분할)",
            "f79_action": "rotate all/cash_open/cash_mid/cash_late/high_vol/low_vol/trend/chop/day-of-week slices(전체, 현금장 초반/중반/후반, 고변동/저변동, 추세/횡보, 요일 구간)",
            "effect": "changes topic surface(주제 표면) without hiding overfit(과적합)를 tiny slice(작은 구간)에 숨기지 않는다",
            "broad_sweep": "all, cash_open, cash_mid, cash_late, high_vol, low_vol, trend, chop, dow",
        },
    ]


def experiment_design(identity: Mapping[str, Any], prior: Mapping[str, Any], retro: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "idea_id": IDEA_ID,
        "hypothesis": (
            "Runtime-native trade-shape labels(런타임 네이티브 거래 형태 라벨)이 actual fill path(실제 체결 경로), "
            "entry timing(진입 시각), tester-deposit risk(테스터 예치금 위험), and lifecycle occupancy(생명주기 점유)를 "
            "처음부터 label/target(라벨/목표)에 내장하면 F78의 signal parity without runtime economics(신호 동등성은 있으나 런타임 경제성 없음)를 줄일 수 있다."
        ),
        "decision_use": "Open F79B proxy scout(F79B 프록시 탐색)를 넓은 축 변화로 실행할지 결정한다.",
        "comparison_baseline": {
            "reference_only": "F78 closeout(마감)은 negative memory(부정 기억)와 preserved clue(보존 단서)로만 사용한다.",
            "f78_closeout_report": prior.get("closeout_report"),
            "f78_preserved_clue": prior.get("preserved_clue"),
            "f78_negative_memory": prior.get("negative_memory"),
        },
        "control_variables": [
            "symbol/timeframe(종목/시간봉): FPMarkets US100 M5",
            "tester defaults for later MT5(향후 MT5 기본): Deposit=500, Leverage=100, Every tick based on real ticks(실틱 기반 모든 틱), fixed 0.1 lot(고정 0.1랏)",
            f"dataset identity(데이터 정체성): {identity.get('dataset_path')} sha256 {identity.get('dataset_sha256')}",
            f"claim boundary(주장 경계): {CLAIM_BOUNDARY}",
        ],
        "changed_variables": [row["axis"] for row in axis_rows()],
        "sample_scope": {
            "dataset": identity.get("dataset_path"),
            "raw_bars": identity.get("raw_bars_path"),
            "split_counts": identity.get("split_counts"),
            "tier_scope": "Tier A separate(티어 A 분리); Tier B missing_required(티어 B 필수 누락); Tier A+B combined out_of_scope_by_claim(합산은 주장 범위 밖) until materialized.",
        },
        "success_criteria": [
            "scout clue(탐색 단서): validation/OOS(검증/표본외) 모두 nonzero(비영), PF>=1.15, DD<=12%, calendar trades/day(달력 일 거래 수)>=1.0, trade_count(거래 수)>=80.",
            "meaningful signal(의미 신호): validation/OOS net>0, PF>=1.35, DD<=10%, calendar trades/day>=2.0, trade_count>=120, and no single tiny session dependence(작은 세션 단독 의존 없음).",
            "runtime trigger(런타임 트리거): meaningful signal(의미 신호)나 weak nonzero signal(약한 비영 신호)이 있으면 pre-MT5 Grok(사전 MT5 그록) 뒤 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 실행한다.",
        ],
        "failure_criteria": [
            "broad sweep(넓은 탐색) 뒤 scout clue(탐색 단서) 0.",
            "positive proxy(양수 프록시)가 active-day density(활성일 밀도)나 tiny regime slice(작은 장세 조각)에만 기대는 경우.",
            "PF/DD/trades/day(수익 팩터/손실폭/일 거래 수) 중 한 축만 좋아지고 네 축 동시 접근이 없을 때.",
        ],
        "invalid_conditions": [
            "future OHLC path(미래 OHLC 경로)가 feature(피처)에 들어가면 invalid(무효).",
            "same-bar/next-tick entry semantics(동일 봉/다음 틱 진입 의미)가 MT5 handoff(MT5 인계)와 다르면 invalid(무효) 또는 repair required(수리 필요).",
            "contract P/L scale(계약 손익 배율), Deposit=500 DD denominator(예치금 500 손실폭 분모), spread cost(스프레드 비용)가 기록 없이 바뀌면 invalid(무효).",
        ],
        "stop_conditions": [
            "meaningful signal(의미 신호)이 나오면 proxy expansion(프록시 확장)을 멈추고 Grok plus MT5 probe(Grok 및 MT5 탐침)로 물질화한다.",
            "weak nonzero signal(약한 비영 신호)이 나오면 negative-control runtime probe(부정 대조 런타임 탐침)를 최소 1회 실행한다.",
            "zero signal(영 신호)이면 logic impossibility(로직상 불가능) 또는 repair action(수리 행동)을 기록하고 closeout(마감)으로 간다.",
        ],
        "evidence_plan": [
            "F79A stage brief(단계 개요), experiment design(실험 설계), axis contract(축 계약), Grok receipt(그록 영수증), data identity(데이터 정체성).",
            "F79B proxy KPI(프록시 핵심 성과 지표): net/PF/DD/trade count/trades per day/win rate/expectancy/recovery/long-short mix.",
            "If signal exists(신호가 있으면): pre-MT5 Grok(사전 MT5 그록), bundle/EA handoff(번들/EA 인계), mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침), proxy/runtime gap analysis(프록시/런타임 간극 분석).",
        ],
        "legacy_relation": "lesson_only(교훈 전용)",
        "tier_scope": "Tier A separate now(현재 티어 A 분리); Tier B and combined missing_required until materialized(티어 B와 합산은 물질화 전 필수 누락).",
        "broad_sweep": axis_rows(),
        "extreme_sweep": [
            "hold_bars(보유 봉) 3/6/12/24/36",
            "SL/TP point grid(손절/익절 포인트 격자) tight/medium/wide",
            "session all versus cash-only(전체 대비 현금장 전용)",
            "DD penalty off/soft/hard(손실폭 벌점 꺼짐/약함/강함)",
        ],
        "micro_search_gate": "Only after at least one scout clue(탐색 단서)가 validation/OOS both nonzero(검증/표본외 모두 비영)일 때.",
        "wfo_plan": "After proxy scout(프록시 탐색) finds a seed surface(씨앗 표면), run WFO/stress(워크포워드/스트레스) before any stronger claim(강한 주장).",
        "failure_memory": "If zero signal(영 신호), record which axis family failed and reopen only with new source/label/runtime representation(새 원천/라벨/런타임 표현).",
        "evidence_boundary": "stage_open_design_only(단계 개방 설계 전용)",
        "retrospective_gate": retro,
    }


def prompt_text(identity: Mapping[str, Any], prior: Mapping[str, Any], retro: Mapping[str, Any]) -> str:
    axis_table = "\n".join(
        [
            "| axis(축) | action(행동) | effect(효과) | broad sweep(넓은 탐색) |",
            "|---|---|---|---|",
            *[f"| {row['axis']} | {row['f79_action']} | {row['effect']} | {row['broad_sweep']} |" for row in axis_rows()],
        ]
    )
    negative = "\n".join(f"- {item}" for item in prior.get("negative_memory", []))
    clue = "\n".join(f"- {item}" for item in prior.get("preserved_clue", []))
    return f"""# F79A Stage-Open Grok Prompt(F79A 단계 개방 그록 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Codex Proposed Direction(Codex 제안 방향)

Open Frontier79(전선79) as `runtime_native_trade_shape_labeling_from_fill_path(체결 경로 기반 런타임 네이티브 거래 형태 라벨링)`.
This is a topic pivot(주제 전환), not F78 inheritance(F78 상속 아님).
The point is to vary feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), and regime/session split(장세/세션 분할), not only repair one F78 threshold(임계값).

## Current Truth(현재 진실)

- F78 status(상태): `{prior.get('closed_status')}`
- F78 judgment(판정): `{prior.get('closed_judgment')}`
- F78 closeout report(마감 보고서): `{prior.get('closeout_report')}` sha256 `{prior.get('closeout_report_sha256')}`
- five-stage retrospective status(5단계 회고 상태): `{retro.get('current_due_status')}`, closeouts since last(이전 회고 이후 마감 수): `{retro.get('closeouts_since_last')}`
- dataset rows(데이터 행): `{identity.get('dataset_rows')}`, split counts(분할 수): `{identity.get('split_counts')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## F78 Preserved Clue(F78 보존 단서)

{clue}

## F78 Negative Memory(F78 부정 기억)

{negative}

## F79 Axis Contract(F79 축 계약)

{axis_table}

## Question(질문)

Is this F79 stage-open direction(단계 개방 방향) broad and novel enough to address the user's concern that experiments must keep changing feature sets(피처 묶음), labels(라벨), model families(모델 계열), trade shapes(거래 형태), risk logic(위험 로직), and regimes/sessions(장세/세션)?

Also check whether it is properly scoped for proxy scout(프록시 탐색) -> mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) if signal exists(신호가 있으면).

Classify your advice(조언 분류) as accepted(수용), accepted_with_conditions(조건부 수용), needs_local_verification(로컬 검증 필요), or rejected(거절).
Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).
"""


def forbidden_hits(text: str) -> list[str]:
    hits: list[str] = []
    forbidden = [
        "Goal Achieve",
        "runtime authority",
        "live readiness",
        "selected baseline",
        "operating promotion",
        "completion achieved",
    ]
    negation_markers = ["do not", "does not", "not ", "no ", "without", "forbidden", "claim boundary", "금지", "아님", "없음", "주장하지"]
    for line in text.splitlines():
        lowered = line.lower()
        if any(marker in lowered for marker in negation_markers) or any(marker in line for marker in negation_markers):
            continue
        for phrase in forbidden:
            if phrase.lower() in lowered and phrase not in hits:
                hits.append(phrase)
    return hits


def classify_grok(text: str, success: bool) -> tuple[str, str, bool, list[str]]:
    hits = forbidden_hits(text)
    if not success:
        return "needs_local_verification(로컬 검증 필요)", "retry_or_repair_grok_transport_before_proxy(프록시 전 그록 전송 재시도 또는 수리)", False, hits
    head = text[:1800].lower()
    if "rejected" in head or "거절" in text[:1800]:
        return "rejected(거절)", "repair_stage_open_direction_before_proxy(프록시 전 단계 개방 방향 수리)", False, hits
    if "needs_local_verification" in head or "로컬 검증 필요" in text[:1800]:
        return "needs_local_verification(로컬 검증 필요)", "local_verify_conditions_before_proxy(프록시 전 조건 로컬 검증)", False, hits
    if "accepted_with_conditions" in head or "조건부 수용" in text[:1800]:
        return "accepted_with_conditions(조건부 수용)", "open_f79_with_conditions_recorded(조건 기록 후 F79 개방)", not hits, hits
    if "accepted" in head or "수용" in text[:1800]:
        return "accepted(수용)", "open_f79_runtime_native_proxy_scout(런타임 네이티브 F79 프록시 탐색 개방)", not hits, hits
    return "needs_local_verification(로컬 검증 필요)", "manual_review_grok_advice_before_proxy(프록시 전 그록 조언 수동 검토)", False, hits


def grok_identity(result: Any) -> dict[str, Any]:
    return {
        "packet_path": rel(GROK_PACKET),
        "prompt_path": rel(GROK_PROMPT),
        "prompt_sha256": file_hash(GROK_PROMPT),
        "output_path": rel(GROK_CLEAN) if path_exists(GROK_CLEAN) else "",
        "output_sha256": file_hash(GROK_CLEAN) if path_exists(GROK_CLEAN) else "",
        "metadata_path": rel(GROK_METADATA) if path_exists(GROK_METADATA) else "",
        "metadata_sha256": file_hash(GROK_METADATA) if path_exists(GROK_METADATA) else "",
        "success": bool(result.success),
        "returncode": result.returncode,
        "timed_out": bool(result.timed_out),
        "duration_seconds": result.duration_seconds,
    }


def status_tuple(open_allowed: bool) -> tuple[str, str, str]:
    if open_allowed:
        return STATUS_SUCCESS, JUDGMENT_SUCCESS, NEXT_RUN_ID
    return STATUS_REVIEW_FAIL, JUDGMENT_REVIEW_FAIL, RUN_ID


def stage_brief_text(created_at: str) -> str:
    axes = "\n".join(f"- {row['axis']}: {row['f79_action']}" for row in axis_rows())
    return f"""# F79 Stage Brief(F79 단계 개요)

Created(생성): {created_at}

Stage id(단계 ID): `{STAGE_ID}`

Run id(실행 ID): `{RUN_ID}`

## Hypothesis(가설)

Runtime-native trade-shape labels(런타임 네이티브 거래 형태 라벨)이 actual fill path(실제 체결 경로), entry timing(진입 시각), tester-deposit risk(테스터 예치금 위험), and lifecycle occupancy(생명주기 점유)를 처음부터 label/target(라벨/목표)에 넣으면 F78의 proxy/runtime gap(프록시/런타임 간극)을 줄일 수 있다.

## Novelty Delta(신규성 차이)

F78은 contract P/L(계약 손익)과 parity(동등성)를 맞춘 뒤 entry/deposit repair(진입/예치금 수리)를 했다. F79는 그 수리를 뒤에서 붙이지 않고, fill path(체결 경로)와 trade shape(거래 형태)를 label/target(라벨/목표)의 원천으로 삼는다.

## Axis Contract(축 계약)

{axes}

## Mandatory Lifecycle(필수 생명주기)

Hypothesis(가설) -> proxy scout(프록시 탐색) -> pre-MT5 Grok review(사전 MT5 그록 검토) -> mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) if signal exists(신호 존재 시) -> gap analysis(간극 분석) -> WFO/stress/repair(워크포워드/스트레스/수리) as needed(필요 시) -> closeout(마감).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def context_anchor_text(created_at: str, status: str, judgment: str, next_run: str) -> str:
    return f"""# F79 Context Anchor(F79 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{next_run}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Preserved clue(보존 단서): F78 signal/feature parity(신호/피처 동등성), selected-entry veto tape(선택 진입 거부 테이프), entry timing and DD denominator must be designed at label start(진입 시각과 손실폭 분모는 라벨 시작부터 설계).

Negative memory(부정 기억): do not repeat F78 threshold-only/model-only repair(F78 임계값/모델 단독 수리 반복 금지).
"""


def report_text(
    created_at: str,
    status: str,
    judgment: str,
    next_run: str,
    identity: Mapping[str, Any],
    prior: Mapping[str, Any],
    retro: Mapping[str, Any],
    grok: Mapping[str, Any],
    advice: str,
    final_direction: str,
    hits: Sequence[str],
) -> str:
    return f"""# Frontier79A Stage Open Report(F79A 단계 개방 보고서)

Updated(갱신): {created_at}

- run id(실행 ID): `{RUN_ID}`
- stage id(단계 ID): `{STAGE_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- Grok advice(Grok 조언): `{advice}`
- final Codex direction(최종 Codex 방향): `{final_direction}`
- forbidden claim hits(금지 주장 감지): `{', '.join(hits) if hits else 'none(없음)'}`
- next action(다음 행동): `{next_run}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Hypothesis(가설)

Runtime-native trade-shape labels(런타임 네이티브 거래 형태 라벨)이 actual fill path(실제 체결 경로), entry timing(진입 시각), tester-deposit risk(테스터 예치금 위험), and lifecycle occupancy(생명주기 점유)를 처음부터 label/target(라벨/목표)에 내장하면 F78의 signal parity without runtime economics(신호 동등성은 있으나 런타임 경제성 없음)를 줄일 수 있다.

## Test Period(테스트 기간)

- stage-open evidence(단계 개방 근거): F78 closeout(마감) and shared dataset identity(공유 데이터 정체성)
- proxy test period planned(예정 프록시 기간): split_v1 train/validation/OOS(훈련/검증/표본외)
- MT5 runtime probe(런타임 탐침): signal exists(신호 존재) 후 F79C/F79D에서 물질화

## Data Identity(데이터 정체성)

- dataset(데이터셋): `{identity.get('dataset_path')}` sha256 `{identity.get('dataset_sha256')}`
- rows(행): `{identity.get('dataset_rows')}`
- split counts(분할 수): `{identity.get('split_counts')}`
- raw bars(원천 봉): `{identity.get('raw_bars_path')}` sha256 `{identity.get('raw_bars_sha256')}`

## Prior Scan(이전 단계 점검)

- F78 closeout report(마감 보고서): `{prior.get('closeout_report')}` sha256 `{prior.get('closeout_report_sha256')}`
- preserved clue(보존 단서): `{'; '.join(prior.get('preserved_clue', []))}`
- negative memory(부정 기억): `{'; '.join(prior.get('negative_memory', []))}`
- five-stage retrospective(5단계 회고): `{retro.get('current_due_status')}` with `{retro.get('closeouts_since_last')}` closeouts since last(이전 이후 마감 수)

## Axis Sweep(축 탐색)

| axis(축) | broad sweep(넓은 탐색) | effect(효과) |
|---|---|---|
""" + "\n".join(f"| {row['axis']} | {row['broad_sweep']} | {row['effect']} |" for row in axis_rows()) + f"""

## Grok Review(Grok 검토)

- packet(묶음): `{grok.get('packet_path')}`
- prompt(프롬프트): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`
- output(출력): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`
- success(성공): `{grok.get('success')}`
- returncode(반환 코드): `{grok.get('returncode')}`

This report(보고서)는 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 만들지 않는다.
"""


def grok_receipt_text(
    advice: str,
    final_direction: str,
    grok: Mapping[str, Any],
    local: Mapping[str, Any],
) -> str:
    return f"""# F79A Grok Stage-Open Receipt(F79A 그록 단계 개방 영수증)

- trigger_reason(트리거 이유): stage open requires Grok second opinion(단계 개방은 Grok 2차 의견 필요)
- review_size(검토 크기): medium review(중간 검토)
- direction_before_grok(그록 전 방향): open F79 as runtime-native trade-shape label pivot(F79를 런타임 네이티브 거래 형태 라벨 전환으로 개방)
- bounded_evidence(제한 근거): F78 closeout(마감), five-stage retrospective status(5단계 회고 상태), dataset identity(데이터 정체성), F79 axis contract(축 계약)
- prompt_identity(프롬프트 정체성): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`
- grok_output_identity(그록 출력 정체성): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`
- advice_classification(조언 분류): `{advice}`
- local_verification(로컬 검증): `{local.get('passed')}`
- forbidden_claim_check(금지 주장 확인): `{local.get('forbidden_claim_hits')}`
- final_codex_direction(최종 Codex 방향): `{final_direction}`
"""


def gate_audit_text(status: str, open_allowed: bool, retro: Mapping[str, Any], local: Mapping[str, Any]) -> str:
    return f"""# F79A Required Gate Coverage Audit(F79A 필수 게이트 커버리지 감사)

Status(상태): `{status}`

| gate(게이트) | status(상태) | evidence(근거) |
|---|---|---|
| reentry truth(재진입 진실) | `passed(통과)` | workspace state(작업공간 상태), F78 selection(선택 상태), git status(깃 상태) checked before action(행동 전 확인) |
| five-stage retrospective due check(5단계 회고 도래 점검) | `{retro.get('current_due_status')}` | closeouts since last(이전 이후 마감 수) `{retro.get('closeouts_since_last')}` |
| stage open contract(단계 개방 계약) | `passed(통과)` | stage brief(단계 개요), novelty delta(신규성 차이), do-not-repeat(반복 금지), exit rule(종료 규칙), claim boundary(주장 경계) recorded(기록됨) |
| Grok external review(그록 외부 검토) | `{local.get('grok_success')}` | `{rel(GROK_CLEAN) if path_exists(GROK_CLEAN) else 'missing(누락)'}` |
| forbidden claim guard(금지 주장 보호) | `{not bool(local.get('forbidden_claim_hits'))}` | hits(감지) `{local.get('forbidden_claim_hits')}` |
| data identity(데이터 정체성) | `passed(통과)` | `{rel(DATA_IDENTITY)}` |
| next action(다음 행동) | `{open_allowed}` | next run(다음 실행) `{NEXT_RUN_ID if open_allowed else RUN_ID}` |

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def selection_status_text(created_at: str, status: str, judgment: str, next_run: str) -> str:
    return f"""# F79 Selection Status(F79 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F79A stage open(단계 개방)을 실행했다.

Effect(효과): F79는 runtime-native trade-shape labels(런타임 네이티브 거래 형태 라벨)을 feature/label/model/trade/risk/session(피처/라벨/모델/거래/위험/세션) 축으로 넓게 탐색하는 새 전선으로 열렸다.

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def review_index_text(created_at: str) -> str:
    return f"""# F79 Review Index(F79 검토 색인)

Updated(갱신): {created_at}

- stage brief(단계 개요): `{rel(STAGE_BRIEF)}`
- experiment design(실험 설계): `{rel(EXPERIMENT_DESIGN)}`
- axis contract(축 계약): `{rel(AXIS_CONTRACT)}`
- data identity(데이터 정체성): `{rel(DATA_IDENTITY)}`
- Grok receipt(그록 영수증): `{rel(GROK_RECEIPT)}`
- gate audit(게이트 감사): `{rel(GATE_AUDIT)}`
- report(보고서): `{rel(REPORT)}`
- context anchor(문맥 앵커): `{rel(ANCHOR)}`
"""


def local_verification_payload(
    result: Any,
    advice: str,
    hits: Sequence[str],
    retro: Mapping[str, Any],
    prior: Mapping[str, Any],
) -> dict[str, Any]:
    checks = {
        "grok_success": bool(result.success),
        "grok_returncode": result.returncode,
        "grok_timed_out": bool(result.timed_out),
        "forbidden_claim_hits": list(hits),
        "retrospective_not_due": str(retro.get("current_due_status", "")).startswith("not_due"),
        "f78_closed_negative_memory": prior.get("closed_status") == "closed_negative_memory_no_authority",
        "advice_classification": advice,
        "required_inputs_exist": all(path_exists(path) for path in [DATASET_PATH, FEATURE_ORDER_PATH, RAW_BARS_PATH, F78_CLOSEOUT, F78_SELECTION, RETROSPECTIVE_REGISTER]),
    }
    checks["passed"] = (
        checks["grok_success"]
        and not checks["forbidden_claim_hits"]
        and checks["retrospective_not_due"]
        and checks["f78_closed_negative_memory"]
        and checks["required_inputs_exist"]
        and advice in {"accepted(수용)", "accepted_with_conditions(조건부 수용)"}
    )
    return checks


def ledger_row(created_at: str, status: str, judgment: str, next_run: str) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "stage_open(단계 개방)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B combined out_of_scope",
        "kpi_scope": "stage_open_design(단계 개방 설계)",
        "scoreboard_lane": "experiment_design(실험 설계)",
        "lane": "stage_open(단계 개방)",
        "family": "experiment_design(실험 설계)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT),
        "primary_kpi": "hypothesis and axis contract recorded(가설과 축 계약 기록)",
        "guardrail_kpi": "Grok review, no authority claims, retrospective not_due(Grok 검토, 권위 주장 없음, 회고 아직 아님)",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": f"stage_open_axis_count={len(axis_rows())}; next={next_run}",
        "run_number": "frontier79A",
        "date": created_at[:10],
        "decision": judgment,
        "next_run_id": next_run,
        "rows": len(axis_rows()),
        "gate_passes": 7 if status == STATUS_SUCCESS else 5,
        "gate_total": 7,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "stage_open",
        "tier": "Tier A",
        "metric_scope": "design",
        "result_status": status,
        "feature_count": 58,
        "work_family": "experiment_design",
        "row_id": f"{RUN_ID}__stage_open",
        "evidence_boundary": "stage_open_design_only_no_authority(단계 개방 설계 전용, 권위 없음)",
        "next_action": next_run,
        "question": "Can runtime-native fill-path trade-shape labels reduce proxy/runtime economics gap?(런타임 네이티브 체결 경로 거래 형태 라벨이 프록시/런타임 경제성 간극을 줄이나?)",
        "artifact_count": 9,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "stage_open_design_only(단계 개방 설계 전용)",
        "run_family": "frontier_stage_open",
        "run_type": "stage_open",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(REPORT),
        "result_path": rel(REPORT),
    }


def update_ledgers(created_at: str, status: str, judgment: str, next_run: str) -> None:
    row = ledger_row(created_at, status, judgment, next_run)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_idea_registry(created_at: str, status: str, judgment: str, next_run: str) -> None:
    text = read_text(IDEA_REGISTRY) if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    if RUN_ID in text:
        return
    addition = f"""

## {IDEA_ID} Frontier79 runtime-native trade-shape labels(전선79 런타임 네이티브 거래 형태 라벨)

- `{RUN_ID}` opened F79 stage(단계 개방). Hypothesis(가설): fill path(체결 경로), entry timing(진입 시각), tester-deposit risk(테스터 예치금 위험), and lifecycle occupancy(생명주기 점유)를 label/target(라벨/목표)에 처음부터 넣으면 F78 proxy/runtime economics gap(프록시/런타임 경제성 간극)을 줄일 수 있다.
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- boundary(경계): `{CLAIM_BOUNDARY}`
- next(다음): `{next_run}`
- recorded_at(기록 시각): `{created_at}`
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_state_files(created_at: str, status: str, judgment: str, next_run: str) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run}
runtime_probe_status: f79_stage_open_runtime_probe_required_if_signal_exists
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f78_closeout_3_of_5
updated_at_utc: '{created_at}'
context_anchor: {rel(ANCHOR)}
notes:
  - "Action(행동): F79A stage open(단계 개방)을 실행했다."
  - "Effect(효과): F79는 runtime-native fill-path trade-shape label(런타임 네이티브 체결 경로 거래 형태 라벨) 가설로 열렸다."
  - "Next(다음): {next_run}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F79A stage open(단계 개방)을 실행했다.

Effect(효과): F79는 feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), regime/session split(장세/세션 분할)을 넓게 바꾸는 runtime-native trade-shape label(런타임 네이티브 거래 형태 라벨) 실험으로 열렸다.

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- next action(다음 행동): F79B proxy scout(프록시 탐색)를 구현하고 실행한다.
- mandatory rule(필수 규칙): meaningful signal(의미 신호) 또는 weak nonzero signal(약한 비영 신호)이 나오면 pre-MT5 Grok(사전 MT5 그록)과 MT5 Runtime Probe(MT5 런타임 탐침)를 실행한다.
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def run_manifest_payload(
    created_at: str,
    status: str,
    judgment: str,
    next_run: str,
    identity: Mapping[str, Any],
    grok: Mapping[str, Any],
    local: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "idea_id": IDEA_ID,
        "work_family": "experiment_design(실험 설계)",
        "data_identity": identity,
        "grok": grok,
        "local_verification": local,
        "artifacts": [
            rel(STAGE_BRIEF),
            rel(EXPERIMENT_DESIGN),
            rel(AXIS_CONTRACT),
            rel(DATA_IDENTITY),
            rel(LOCAL_VERIFICATION),
            rel(REPORT),
            rel(GROK_RECEIPT),
            rel(GATE_AUDIT),
            rel(SELECTION_STATUS),
        ],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
    }


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    identity = data_identity()
    prior = prior_snapshot()
    retro = retrospective_status()
    design = experiment_design(identity, prior, retro)
    prompt = prompt_text(identity, prior, retro)
    write_text(GROK_PROMPT, prompt)

    result = run_grok_review(
        prompt,
        cwd=ROOT,
        timeout_seconds=300,
        review_size="medium",
        output_dir=GROK_PACKET,
        repo_root=ROOT,
        prompt_file_path=GROK_PROMPT,
    )
    advice, final_direction, open_allowed, hits = classify_grok(result.clean_stdout, result.success)
    local = local_verification_payload(result, advice, hits, retro, prior)
    open_allowed = bool(open_allowed and local["passed"])
    status, judgment, next_run = status_tuple(open_allowed)
    grok = grok_identity(result)

    write_json(DATA_IDENTITY, identity)
    write_json(EXPERIMENT_DESIGN, design)
    write_csv(AXIS_CONTRACT, axis_rows())
    write_json(LOCAL_VERIFICATION, local)
    write_text(STAGE_BRIEF, stage_brief_text(created_at))
    write_text(ANCHOR, context_anchor_text(created_at, status, judgment, next_run))
    write_text(REPORT, report_text(created_at, status, judgment, next_run, identity, prior, retro, grok, advice, final_direction, hits))
    write_text(GROK_RECEIPT, grok_receipt_text(advice, final_direction, grok, local))
    write_text(GATE_AUDIT, gate_audit_text(status, open_allowed, retro, local))
    write_text(SELECTION_STATUS, selection_status_text(created_at, status, judgment, next_run))
    write_text(REVIEW_INDEX, review_index_text(created_at))
    write_json(RUN_MANIFEST, run_manifest_payload(created_at, status, judgment, next_run, identity, grok, local))

    update_ledgers(created_at, status, judgment, next_run)
    update_idea_registry(created_at, status, judgment, next_run)
    update_state_files(created_at, status, judgment, next_run)

    print(
        json.dumps(
            {
                "status": status,
                "judgment": judgment,
                "advice": advice,
                "open_allowed": open_allowed,
                "next_run": next_run,
                "report": rel(REPORT),
                "grok_output": grok.get("output_path"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if open_allowed else 1


if __name__ == "__main__":
    raise SystemExit(main())
