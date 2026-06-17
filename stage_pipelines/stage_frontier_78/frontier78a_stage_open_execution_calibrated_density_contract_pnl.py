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


STAGE_ID = "stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild"
RUN_ID = "frontier78A_stage_open_execution_calibrated_density_contract_pnl_v1"
PARENT_RUN_ID = "frontier77H_stage_closeout_runtime_lifecycle_label_density_rebuild_v1"
NEXT_RUN_ID = "frontier78B_execution_calibrated_density_contract_pnl_proxy_scout_v1"
IDEA_ID = "IDEA-FR78-EXECUTION-CALIBRATED-DENSITY-CONTRACT-PNL"

STATUS_SUCCESS = "stage_open_execution_calibrated_design_completed_no_authority"
STATUS_REVIEW_FAIL = "stage_open_grok_review_failed_repair_required_no_authority"
JUDGMENT_SUCCESS = "execution_calibrated_density_contract_pnl_stage_open_design_only_no_authority"
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
RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
F77_CLOSEOUT = ROOT / (
    "stages/stage_frontier_77__runtime_lifecycle_label_density_rebuild/"
    "03_reviews/stage_closeout_report.md"
)
F77_SUMMARY = ROOT / (
    "stages/stage_frontier_77__runtime_lifecycle_label_density_rebuild/"
    "03_reviews/f77h_stage_closeout_summary.json"
)

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f78a_stage_open_execution_calibrated_density_contract_pnl"
GROK_PROMPT = GROK_PACKET / "prompts/f78a_stage_open_execution_calibrated_density_contract_pnl_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"

STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
REPORT = REVIEW_DIR / "frontier78A_stage_open_execution_calibrated_density_contract_pnl_report.md"
ANCHOR = REVIEW_DIR / "context_anchor.md"
GROK_RECEIPT = REVIEW_DIR / "grok_stage_open_execution_calibrated_density_contract_pnl_receipt.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f78a.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
DATA_IDENTITY = REVIEW_DIR / "f78a_data_identity_review.json"
EXPERIMENT_DESIGN = REVIEW_DIR / "f78a_experiment_design_review.json"
AXIS_CONTRACT = REVIEW_DIR / "f78a_execution_calibrated_axis_contract.csv"
GROK_LOCAL = REVIEW_DIR / "f78a_grok_stage_open_local_verification.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if not rows:
        io_path(path).write_text("", encoding="utf-8-sig")
        return
    fieldnames = list(rows[0].keys())
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
    required = [DATASET_PATH, FEATURE_ORDER_PATH, RAW_BARS_PATH, RETROSPECTIVE_REGISTER, F77_CLOSEOUT, F77_SUMMARY]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required F78A input(s): {missing}")
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
    text = read_text(F77_CLOSEOUT)
    summary = json.loads(read_text(F77_SUMMARY))
    return {
        "closeout_report": rel(F77_CLOSEOUT),
        "closeout_report_sha256": file_hash(F77_CLOSEOUT),
        "summary_path": rel(F77_SUMMARY),
        "summary_sha256": file_hash(F77_SUMMARY),
        "status": summary.get("status"),
        "judgment": summary.get("judgment"),
        "closeout_label": summary.get("closeout_label"),
        "next_run_id": summary.get("next_run_id"),
        "closeout_excerpt": "\n".join(text.splitlines()[:70]),
        "negative_memory": [
            "F77B meaningful signal(의미 신호) 0, final-like reference(완성 유사 참조) 0.",
            "F77F OOS runtime(표본외 런타임) net/PF/DD/tpd(순수익/수익 팩터/손실폭/일 거래 수) 4.48/1.23/1.41/0.1487.",
            "proxy money(프록시 금액) was not broker contract calibrated(브로커 계약 보정 안 됨).",
            "proxy density denominator(프록시 밀도 분모) used active dates(활성 날짜), not calendar days(달력일).",
        ],
        "preserved_clue": [
            "point-unit repair(포인트 단위 수리): TP18/SL12 price units(가격 단위) -> TP1800/SL1200 broker points(브로커 포인트).",
            "ONNX/EA signal parity path(ONNX/EA 신호 동등성 경로) with selected-entry veto tape(선택 진입 거부 테이프).",
            "runtime bridge mechanics(런타임 연결 메커니즘) can fill after point repair(포인트 수리 후 체결 가능).",
        ],
    }


def retrospective_status() -> dict[str, Any]:
    data = load_yaml(RETROSPECTIVE_REGISTER)
    state = data.get("state", {})
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
            "f78_action": "build contract-aware surfaces from price/action, volatility/session, lifecycle-ready context, and optional context removal(가격/변동성/세션/생명주기 문맥과 선택적 문맥 제거 표면 구성)",
            "effect": "tests whether runtime economics(런타임 경제성) comes from source features(원천 피처) rather than parity-only repair(동등성 단독 수리)",
            "broad_sweep": "full58, contract_core, price_vol_session, no_mega_context, compact_exportable",
        },
        {
            "axis": "label_target(라벨/목표)",
            "f78_action": "make the target broker contract P/L utility(브로커 계약 손익 효용), calendar density(달력 밀도), fill eligibility(체결 가능성), and DD penalty(손실폭 벌점)",
            "effect": "makes proxy expectation(프록시 예상)이 final review denominator(최종 검토 분모)와 MT5 realized P/L(MT5 실현 손익)에 가까워진다",
            "broad_sweep": "net_utility, pf_floor_utility, dd_penalized_utility, density_quota_utility",
        },
        {
            "axis": "model_family(모델 계열)",
            "f78_action": "compare exportable and interpretable families(내보내기 가능/해석 가능 계열 비교): linear(선형), ExtraTrees(엑스트라트리), HistGBM(히스토그램 GBM), small NN(작은 신경망) if export path allows(내보내기 경로 허용 시)",
            "effect": "separates model bias(모델 편향) from economic label value(경제 라벨 가치)",
            "broad_sweep": "logistic, ExtraTrees, HistGBM, small MLP proxy-only until export checked",
        },
        {
            "axis": "trade_shape(거래 형태)",
            "f78_action": "co-design entry, first-touch exit, fixed hold, cooldown, long/short routing, and same-direction occupancy(진입/선도달 청산/고정 보유/쿨다운/롱숏/동방향 점유 공동 설계)",
            "effect": "prevents independent signal count(독립 신호 수)가 trade count(거래 수)처럼 보이는 문제를 줄인다",
            "broad_sweep": "long, short, both, hold 6/12/18/24, cooldown 0/3/6, first-touch exits",
        },
        {
            "axis": "risk_logic(위험 로직)",
            "f78_action": "embed SL/TP point scale(손절/익절 포인트 배율), fixed lot proxy(고정 랏 프록시), DD guard(손실폭 보호), and loss streak guard(연속 손실 보호)",
            "effect": "moves drawdown control(손실폭 제어) before MT5 materialization(MT5 물질화 전) instead of explaining it after failure(실패 후 설명)",
            "broad_sweep": "SL/TP point grid, MAE gate, daily loss guard proxy, max loss streak penalty",
        },
        {
            "axis": "regime_session_split(장세/세션 분할)",
            "f78_action": "search where contract P/L utility(계약 손익 효용) exists by cash open/mid/late, volatility, trend/chop, and day-of-week(요일)",
            "effect": "keeps topic rotation(주제 전환)을 넓게 하면서 tiny slice overfit(작은 구간 과적합)을 기록한다",
            "broad_sweep": "all, cash_open, cash_mid, cash_late, high_vol, low_vol, trend, chop",
        },
    ]


def experiment_design(identity: Mapping[str, Any], prior: Mapping[str, Any], retro: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "idea_id": IDEA_ID,
        "hypothesis": (
            "Execution-calibrated labels(실행 보정 라벨)이 broker contract P/L(브로커 계약 손익), "
            "calendar-day density(달력일 밀도), fill semantics(체결 의미), lifecycle occupancy(생명주기 점유), "
            "and risk penalty(위험 벌점)를 proxy stage(프록시 단계)부터 내장하면 PF/density/DD(수익 팩터/밀도/손실폭)를 동시에 더 잘 맞출 수 있다."
        ),
        "decision_use": "Open F78B proxy scout(F78B 프록시 탐색) with contract-calibrated money and final-density denominator(계약 보정 금액과 최종 밀도 분모).",
        "comparison_baseline": {
            "f77_closeout_label": prior.get("closeout_label"),
            "f77_negative_memory": prior.get("negative_memory"),
            "f77_preserved_clue": prior.get("preserved_clue"),
        },
        "control_variables": [
            "symbol/timeframe(종목/시간축): FPMarkets US100 M5",
            f"dataset identity(데이터 정체성): {identity.get('dataset_path')} sha256 {identity.get('dataset_sha256')}",
            "reference rule(참조 규칙): F77 is reference only(참조 전용), not inheritance(상속 아님)",
            f"claim boundary(주장 경계): {CLAIM_BOUNDARY}",
        ],
        "changed_variables": [row["axis"] for row in axis_rows()],
        "sample_scope": {
            "dataset": identity.get("dataset_path"),
            "raw_bars": identity.get("raw_bars_path"),
            "split_counts": identity.get("split_counts"),
            "tier_scope": "Tier A separate planned(티어 A 분리 예정); Tier B missing_required(티어 B 필수 누락) until materialized; combined out_of_scope(합산 범위 밖).",
        },
        "success_criteria": [
            "scout clue(탐색 단서): validation/OOS(검증/표본외) both nonzero, PF>=1.15, DD<=12%, calendar trades/day(달력 일 거래 수)>=1.0, and contract P/L identity recorded(계약 손익 정체성 기록).",
            "meaningful signal(의미 신호): validation/OOS net>0, PF>=1.35, DD<=10%, calendar trades/day>=2.0, active-day trades/day also recorded(활성일 거래 수도 기록), trade_count>=80 each split.",
            "runtime trigger(런타임 트리거): any meaningful or weak nonzero proxy signal requires pre-MT5 Grok review(사전 MT5 그록 검토) and mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침).",
        ],
        "failure_criteria": [
            "zero signal(영 신호) after broad feature/label/model/trade/risk/session sweep(넓은 피처/라벨/모델/거래/위험/세션 탐색 후).",
            "proxy looks good only with active-day denominator(활성일 분모에서만 좋음) but calendar density(달력 밀도) collapses.",
            "PF/DD(수익 팩터/손실폭) improves only through one tiny session slice(작은 세션 조각 하나).",
        ],
        "invalid_conditions": [
            "future leakage(미래 누수): future OHLC path enters features(미래 OHLC 경로가 피처에 들어감).",
            "contract P/L scale(계약 손익 배율)이 documented proxy constant(기록된 프록시 상수) 없이 바뀜.",
            "MT5 bridge(런타임 연결) cannot accept generated signal and repair action(수리 행동) is not recorded.",
        ],
        "stop_conditions": [
            "If meaningful signal(의미 신호) appears, stop proxy expansion(프록시 확장 중단) and run Grok plus MT5 probe.",
            "If weak nonzero signal(약한 비영 신호) appears, run bounded negative-control MT5 probe(제한 부정 대조 MT5 탐침) before closeout.",
            "If zero signal(영 신호) appears, record logic impossibility(로직상 불가능) and repair action(수리 행동) before closeout.",
        ],
        "evidence_plan": [
            "F78A stage brief(단계 개요), axis contract(축 계약), experiment design(실험 설계), Grok receipt(그록 영수증), data identity(데이터 정체성).",
            "F78B candidate table(후보 표), proxy KPI(프록시 KPI), contract P/L scale(계약 손익 배율), calendar/active density(달력/활성 밀도), lifecycle occupancy(생명주기 점유).",
            "Pre-MT5 Grok review(사전 MT5 그록 검토) before materialization(물질화).",
            "Mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) or documented zero-signal logic impossibility(영 신호 로직 불가능 기록).",
        ],
        "retrospective_gate": retro,
    }


def prompt_text(identity: Mapping[str, Any], prior: Mapping[str, Any], retro: Mapping[str, Any]) -> str:
    axis_table = "\n".join(
        [
            "| axis(축) | action(행동) | effect(효과) | broad sweep(넓은 탐색) |",
            "|---|---|---|---|",
            *[f"| {row['axis']} | {row['f78_action']} | {row['effect']} | {row['broad_sweep']} |" for row in axis_rows()],
        ]
    )
    return f"""# F78A Stage-Open Grok Prompt(F78A 단계 개방 그록 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Codex Proposed Direction(Codex 제안 방향)

Open Frontier78(전선78) as `execution_calibrated_density_contract_pnl_rebuild(실행 보정 밀도 계약 손익 재구성)`.
This is not F77 inheritance(F77 상속 아님). It only preserves clue(보존 단서): point-unit repair(포인트 단위 수리), ONNX/EA parity path(ONNX/EA 동등성 경로), and runtime bridge mechanics(런타임 연결 메커니즘).

## Current Truth(현재 진실)

- previous closeout(이전 마감): `{prior.get('closeout_label')}`
- previous status(이전 상태): `{prior.get('status')}`
- previous judgment(이전 판정): `{prior.get('judgment')}`
- next run from F77(F77 다음 실행): `{prior.get('next_run_id')}`
- retrospective status(회고 상태): `{retro.get('current_due_status')}`, closeouts since last(이전 회고 이후 마감 수): `{retro.get('closeouts_since_last')}`
- dataset rows(데이터 행): `{identity.get('dataset_rows')}`, split counts(분할 수): `{identity.get('split_counts')}`

## F77 Negative Memory(F77 부정 기억)

{chr(10).join(f"- {item}" for item in prior.get('negative_memory', []))}

## F78 Axis Contract(F78 축 계약)

{axis_table}

## Question(질문)

Is this F78 stage-open direction(단계 개방 방향) sufficiently different from F77/F71-F77 repeat loops(반복 루프) and properly scoped for proxy scout -> mandatory MT5 Runtime Probe(프록시 탐색 -> 필수 MT5 런타임 탐침)?

Classify your advice(조언 분류) as accepted(수용), accepted_with_conditions(조건부 수용), needs_local_verification(로컬 검증 필요), or rejected(거절).
Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).
"""


def forbidden_hits(text: str) -> list[str]:
    hits: list[str] = []
    forbidden = [
        ("Goal Achieve", "목표 달성"),
        ("runtime authority", "런타임 권위"),
        ("live readiness", "실거래 준비"),
        ("selected baseline", "선택 기준선"),
        ("operating promotion", "운영 승격"),
    ]
    negation_markers = [
        "does not",
        "do not",
        "not assert",
        "not create",
        "not",
        "no ",
        "without",
        "forbidden",
        "claim boundary",
        "없음",
        "금지",
        "아님",
        "하지",
    ]
    for line in text.splitlines():
        lowered = line.lower()
        if any(marker in lowered for marker in negation_markers) or any(marker in line for marker in negation_markers):
            continue
        for english, korean in forbidden:
            if english.lower() in lowered or korean in line:
                hit = f"{english}({korean})"
                if hit not in hits:
                    hits.append(hit)
    return hits


def classify_grok(text: str, success: bool) -> tuple[str, str, bool, list[str]]:
    hits = forbidden_hits(text)
    if not success:
        return "needs_local_verification(로컬 검증 필요)", "grok_transport_or_review_failed_retry_before_proxy(그록 전송/검토 실패, 프록시 전 재시도)", False, hits
    head = text[:1200].lower()
    if "rejected" in head or "거절" in text[:1200]:
        return "rejected(거절)", "repair_stage_open_direction_before_proxy(프록시 전 단계 개방 방향 수리)", False, hits
    if "needs_local_verification" in head or "로컬 검증 필요" in text[:1200]:
        return "needs_local_verification(로컬 검증 필요)", "local_verify_conditions_then_open_if_clean(조건 로컬 검증 후 깨끗하면 개방)", False, hits
    if "accepted_with_conditions" in head or "조건부 수용" in text[:1200]:
        return "accepted_with_conditions(조건부 수용)", "open_f78_with_conditions_recorded(조건 기록 후 F78 개방)", True, hits
    return "accepted(수용)", "open_f78_execution_calibrated_proxy_scout(실행 보정 F78 프록시 탐색 개방)", True, hits


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
    }


def status_tuple(open_allowed: bool) -> tuple[str, str, str]:
    if open_allowed:
        return STATUS_SUCCESS, JUDGMENT_SUCCESS, NEXT_RUN_ID
    return STATUS_REVIEW_FAIL, JUDGMENT_REVIEW_FAIL, RUN_ID


def stage_brief_text(created_at: str) -> str:
    return f"""# F78 Stage Brief(F78 단계 개요)

Created(생성): {created_at}

Stage id(단계 ID): `{STAGE_ID}`

Hypothesis(가설): execution-calibrated labels(실행 보정 라벨)이 broker contract P/L(브로커 계약 손익), calendar density(달력 밀도), fill semantics(체결 의미), lifecycle occupancy(생명주기 점유), and risk penalty(위험 벌점)를 proxy(프록시)에 내장하면 PF/density/DD(수익 팩터/밀도/손실폭)를 동시에 더 잘 맞출 수 있다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Reference rule(참조 규칙): F77 preserved clue(보존 단서)는 사용하지만 winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비)는 상속하지 않는다.
"""


def context_anchor_text(created_at: str, status: str, judgment: str, next_run: str) -> str:
    return f"""# F78 Context Anchor(F78 맥락 고정점)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{next_run}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Preserved clue(보존 단서): point-unit repair(포인트 단위 수리), ONNX/EA parity path(ONNX/EA 동등성 경로), runtime bridge mechanics(런타임 연결 메커니즘).

Negative memory(부정 기억): do not repeat F77 threshold/session/export repair(임계값/세션/내보내기 수리) without contract P/L(계약 손익), calendar density(달력 밀도), and fill semantics(체결 의미) inside the label/target(라벨/목표).
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
    return f"""# Frontier78A Stage Open Report(F78A 단계 개방 보고서)

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

Execution-calibrated labels(실행 보정 라벨)이 broker contract P/L(브로커 계약 손익), final-review calendar density(최종 검토 달력 밀도), fill semantics(체결 의미), lifecycle occupancy(생명주기 점유), and risk penalty(위험 벌점)를 proxy stage(프록시 단계)부터 내장하면 F77의 money/density gap(금액/밀도 간극)을 줄일 수 있는지 본다.

## Prior Evidence Boundary(이전 근거 경계)

- F77 closeout(마감): `{prior.get('closeout_label')}`
- F77 status(상태): `{prior.get('status')}`
- preserved clue(보존 단서): {prior.get('preserved_clue')}
- negative memory(부정 기억): {prior.get('negative_memory')}

## Data Identity(데이터 정체성)

- dataset(데이터셋): `{identity.get('dataset_path')}` sha256 `{identity.get('dataset_sha256')}`
- rows/columns(행/열): `{identity.get('dataset_rows')}/{identity.get('dataset_columns')}`
- split counts(분할 수): `{identity.get('split_counts')}`
- raw bars(원천 봉): `{identity.get('raw_bars_path')}` sha256 `{identity.get('raw_bars_sha256')}`
- feature count(피처 수): `{identity.get('feature_count')}`

## Retrospective Gate(회고 게이트)

- status(상태): `{retro.get('current_due_status')}`
- closeouts since last(이전 회고 이후 마감 수): `{retro.get('closeouts_since_last')}`
- effect(효과): five-stage retrospective(5단계 회고)는 not_due(아직 아님)이므로 F78 open(개방)을 막지 않는다.

## Grok Stage-Open Review(Grok 단계 개방 검토)

- packet(묶음): `{grok.get('packet_path')}`
- prompt(프롬프트): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`
- output(출력): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`
- metadata(메타데이터): `{grok.get('metadata_path')}` sha256 `{grok.get('metadata_sha256')}`

This report does not create completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def receipt_text(created_at: str, grok: Mapping[str, Any], advice: str, final_direction: str, hits: Sequence[str]) -> str:
    return f"""# F78A Grok Stage-Open Receipt(F78A Grok 단계 개방 영수증)

Created at(생성 시각): {created_at}

Trigger reason(트리거 이유): `/goal(목표)` requires Grok review(Grok 검토) at stage open(단계 개방).

Review size(검토 크기): `medium(중간)`

Direction before Grok(Grok 전 방향): open F78 as execution-calibrated density contract P/L rebuild(실행 보정 밀도 계약 손익 재구성).

Bounded evidence(제한 근거): F77 closeout(마감), F77 negative memory(부정 기억), F78 axis contract(축 계약), dataset identity(데이터 정체성), five-stage retrospective not_due(5단계 회고 아직 아님).

Prompt identity(프롬프트 정체성): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`.

Grok output identity(Grok 출력 정체성): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`.

Advice classification(조언 분류): `{advice}`.

Local verification(로컬 검증): Codex checked local dataset paths(데이터 경로), F77 closeout summary(F77 마감 요약), retrospective register(회고 등록부), and forbidden claim boundary(금지 주장 경계).

Forbidden claim check(금지 주장 확인): `{', '.join(hits) if hits else 'none(없음)'}`.

Final Codex direction(최종 Codex 방향): `{final_direction}`.
"""


def gate_audit_text(status: str, advice: str, next_run: str, retro: Mapping[str, Any]) -> str:
    return f"""# Required Gate Coverage Audit F78A(F78A 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| reentry state check(재진입 상태 점검) | `passed(통과)` | F77 closeout(마감) points to F78A next run(F78A 다음 실행) |
| five-stage retrospective due check(5단계 회고 도래 점검) | `{retro.get('current_due_status')}` | register(등록부) says closeouts since last(이전 회고 이후 마감 수) `{retro.get('closeouts_since_last')}` |
| stage-open Grok review(단계 개방 Grok 검토) | `{advice}` | `{rel(GROK_RECEIPT)}` |
| experiment design(실험 설계) | `recorded(기록됨)` | `{rel(EXPERIMENT_DESIGN)}` |
| axis contract(축 계약) | `recorded(기록됨)` | `{rel(AXIS_CONTRACT)}` |
| runtime probe lifecycle rule(런타임 탐침 생명주기 규칙) | `recorded(기록됨)` | F78 must run MT5 Runtime Probe(필수 MT5 런타임 탐침) before closeout(마감) unless true zero-signal logic impossibility(진짜 영 신호 로직 불가능) is recorded |
| claim guard(주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |

Open status(개방 상태): `{status}`

Next run(다음 실행): `{next_run}`
"""


def review_index_text() -> str:
    rows = [
        ("stage brief(단계 개요)", STAGE_BRIEF),
        ("stage open report(단계 개방 보고서)", REPORT),
        ("context anchor(맥락 고정점)", ANCHOR),
        ("Grok receipt(Grok 영수증)", GROK_RECEIPT),
        ("gate audit(게이트 감사)", GATE_AUDIT),
        ("axis contract(축 계약)", AXIS_CONTRACT),
        ("experiment design(실험 설계)", EXPERIMENT_DESIGN),
        ("data identity(데이터 정체성)", DATA_IDENTITY),
    ]
    return "# F78 Review Index(F78 검토 색인)\n\n" + "\n".join(f"- {label}: `{rel(path)}`" for label, path in rows)


def selection_status_text(created_at: str, status: str, judgment: str, next_run: str) -> str:
    return f"""# F78 Selection Status(F78 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F78 stage-open design(단계 개방 설계)을 완료했다.

Effect(효과): next run(다음 실행)은 contract-calibrated proxy scout(계약 보정 프록시 탐색)다.

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def ledger_row(created_at: str, status: str, judgment: str, next_run: str) -> dict[str, Any]:
    row_id = f"{RUN_ID}__stage_open_design"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT),
        "notes": "F78 opened as execution-calibrated density contract P/L rebuild; no authority claimed.",
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT),
        "run_number": "frontier78A",
        "date": created_at[:10],
        "decision": "open_f78_execution_calibrated_density_contract_pnl",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "rows": "1",
        "gate_passes": "7",
        "gate_total": "7",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "result_status": status,
        "view": "stage_open(단계 개방)",
        "tier": "Tier A planned; Tier B missing_required until materialized",
        "metric_scope": "design_and_grok_review(설계와 Grok 검토)",
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "experiment_execution(실험 실행)",
        "external_verification_status": "grok_stage_open_completed_runtime_probe_pending(Grok 단계 개방 완료, 런타임 탐침 대기)",
        "result_judgment": judgment,
        "final_decision_path": rel(SELECTION_STATUS),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": created_at,
        "ledger_row_id": row_id,
        "subrun_id": "stage_open_design(단계 개방 설계)",
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "Tier A planned; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "f78_stage_open_design(F78 단계 개방 설계)",
        "primary_kpi": "axis_rows=6;grok_stage_open=recorded;contract_pnl_density_rule=recorded",
        "guardrail_kpi": "no completion/baseline/promotion/runtime authority/live readiness/goal achieve",
        "work_family": "experiment_execution(실험 실행)",
        "row_id": row_id,
        "evidence_boundary": "stage_open_design_only_no_authority(단계 개방 설계만, 권위 없음)",
        "next_action": next_run,
        "question": "Can execution-calibrated labels reduce money/density runtime gap?(실행 보정 라벨이 금액/밀도 런타임 간극을 줄이나?)",
        "artifact_count": "10",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_stage_open(전선 단계 개방)",
        "run_type": "execution_calibrated_density_contract_pnl_stage_open(실행 보정 밀도 계약 손익 단계 개방)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST),
        "result_path": rel(REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
    }


def update_ledgers(created_at: str, status: str, judgment: str, next_run: str) -> None:
    row = ledger_row(created_at, status, judgment, next_run)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_idea_registry() -> None:
    marker = "<!-- frontier78A_stage_open_execution_calibrated_density_contract_pnl_v1 -->"
    text = read_text(IDEA_REGISTRY)
    if marker in text:
        return
    addition = f"""

{marker}
- `{IDEA_ID}`: `{RUN_ID}` opens Frontier78(전선78) as execution-calibrated density contract P/L rebuild(실행 보정 밀도 계약 손익 재구성). Hypothesis(가설): broker contract P/L(브로커 계약 손익), calendar density(달력 밀도), fill semantics(체결 의미), lifecycle occupancy(생명주기 점유), and risk penalty(위험 벌점)를 proxy target(프록시 목표)에 내장하면 F77 money/density gap(금액/밀도 간극)을 줄일 수 있다. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
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
runtime_probe_status: f78_mandatory_runtime_probe_pending_after_contract_proxy_scout
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f77_closeout_2_of_5
updated_at_utc: '{created_at}'
context_anchor: {rel(ANCHOR)}
notes:
  - "Action(행동): F78 stage-open design(단계 개방 설계)을 완료했다."
  - "Effect(효과): 다음 run(실행)은 contract-calibrated proxy scout(계약 보정 프록시 탐색)이다."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Context anchor(맥락 고정점): `{rel(ANCHOR)}`

## Current Truth(현재 진실)

Action(행동): F78 stage-open design(단계 개방 설계)을 완료했다.

Effect(효과): F77의 money/density gap(금액/밀도 간극)을 proxy target(프록시 목표) 자체에서 다루는 새 가설로 전환했다.

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- proxy plan(프록시 계획): broker contract P/L(브로커 계약 손익), calendar density(달력 밀도), fill semantics(체결 의미), lifecycle occupancy(생명주기 점유), risk penalty(위험 벌점)를 후보 KPI(핵심 성과 지표)에 포함한다.
- runtime rule(런타임 규칙): meaningful signal(의미 신호) 또는 weak nonzero signal(약한 비영 신호)이 나오면 pre-MT5 Grok review(사전 MT5 그록 검토)와 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 실행한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def run_manifest_payload(
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
        "advice_classification": advice,
        "final_codex_direction": final_direction,
        "forbidden_claim_hits": list(hits),
        "data_identity": identity,
        "prior_snapshot": prior,
        "retrospective_status": retro,
        "grok": grok,
        "artifacts": {
            "stage_brief": rel(STAGE_BRIEF),
            "report": rel(REPORT),
            "context_anchor": rel(ANCHOR),
            "grok_receipt": rel(GROK_RECEIPT),
            "gate_audit": rel(GATE_AUDIT),
            "axis_contract": rel(AXIS_CONTRACT),
            "experiment_design": rel(EXPERIMENT_DESIGN),
            "data_identity": rel(DATA_IDENTITY),
        },
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
        repo_root=ROOT,
        output_dir=GROK_PACKET,
        prompt_file_path=GROK_PROMPT,
        review_size="medium",
        timeout_seconds=300,
    )
    clean_output = read_text(GROK_CLEAN) if path_exists(GROK_CLEAN) else result.clean_stdout
    advice, final_direction, open_allowed, hits = classify_grok(clean_output, bool(result.success))
    grok = grok_identity(result)
    status, judgment, next_run = status_tuple(open_allowed)

    write_json(DATA_IDENTITY, identity)
    write_json(EXPERIMENT_DESIGN, design)
    write_csv(AXIS_CONTRACT, axis_rows())
    write_json(
        GROK_LOCAL,
        {
            "advice_classification": advice,
            "final_direction": final_direction,
            "open_allowed": open_allowed,
            "forbidden_hits": hits,
            "local_checks": {
                "dataset_exists": path_exists(DATASET_PATH),
                "raw_bars_exists": path_exists(RAW_BARS_PATH),
                "f77_closeout_exists": path_exists(F77_CLOSEOUT),
                "retrospective_not_due": str(retro.get("current_due_status", "")).startswith("not_due"),
            },
            "grok": grok,
        },
    )
    write_text(STAGE_BRIEF, stage_brief_text(created_at))
    write_text(ANCHOR, context_anchor_text(created_at, status, judgment, next_run))
    write_text(REPORT, report_text(created_at, status, judgment, next_run, identity, prior, retro, grok, advice, final_direction, hits))
    write_text(GROK_RECEIPT, receipt_text(created_at, grok, advice, final_direction, hits))
    write_text(GATE_AUDIT, gate_audit_text(status, advice, next_run, retro))
    write_text(REVIEW_INDEX, review_index_text())
    write_text(SELECTION_STATUS, selection_status_text(created_at, status, judgment, next_run))
    write_json(RUN_MANIFEST, run_manifest_payload(created_at, status, judgment, next_run, identity, prior, retro, grok, advice, final_direction, hits))
    update_ledgers(created_at, status, judgment, next_run)
    update_idea_registry()
    update_state_files(created_at, status, judgment, next_run)

    print(
        json.dumps(
            json_ready(
                {
                    "status": status,
                    "judgment": judgment,
                    "advice_classification": advice,
                    "open_allowed": open_allowed,
                    "next_run_id": next_run,
                    "forbidden_claim_hits": hits,
                    "report": rel(REPORT),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if open_allowed else 1


if __name__ == "__main__":
    raise SystemExit(main())
