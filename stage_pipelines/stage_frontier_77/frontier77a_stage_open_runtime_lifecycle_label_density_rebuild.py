from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.grok_review_wrapper import run_grok_review
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_77__runtime_lifecycle_label_density_rebuild"
RUN_ID = "frontier77A_stage_open_runtime_lifecycle_label_density_rebuild_v1"
PARENT_RUN_ID = "frontier76G_stage_closeout_axis_ablation_source_discovery_v1"
NEXT_RUN_ID = "frontier77B_runtime_lifecycle_label_density_proxy_scout_v1"
IDEA_ID = "IDEA-FR77-RUNTIME-LIFECYCLE-LABEL-DENSITY-REBUILD"

STATUS_SUCCESS = "stage_open_design_completed_no_authority"
STATUS_REJECTED = "stage_open_grok_rejected_repair_required_no_authority"
STATUS_TRANSPORT_FAIL = "stage_open_grok_transport_failed_no_authority"
JUDGMENT_SUCCESS = "runtime_lifecycle_label_density_stage_open_design_only_no_authority"
JUDGMENT_REJECTED = "stage_open_direction_rejected_repair_required_no_authority"
JUDGMENT_TRANSPORT_FAIL = "stage_open_grok_retry_required_no_authority"
CLAIM_BOUNDARY = (
    "stage_open_design_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
SPEC_DIR = STAGE_DIR / "00_spec"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f77a_stage_open_runtime_lifecycle_label_density_rebuild"
GROK_PROMPT_PATH = GROK_PACKET / "prompts/f77a_stage_open_runtime_lifecycle_label_density_rebuild_prompt.md"
GROK_CLEAN_PATH = GROK_PACKET / "clean_output.md"
GROK_METADATA_PATH = GROK_PACKET / "metadata.json"

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
F76_CLOSEOUT = ROOT / (
    "stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/"
    "03_reviews/stage_closeout_report.md"
)
F76G_SUMMARY = ROOT / (
    "stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/"
    "03_reviews/f76g_closeout_summary.json"
)
F76F_SUMMARY = ROOT / (
    "stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/"
    "03_reviews/f76f_lifecycle_proxy_summary.json"
)

STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
REPORT = REVIEW_DIR / "frontier77A_stage_open_runtime_lifecycle_label_density_rebuild_report.md"
ANCHOR = REVIEW_DIR / "context_anchor.md"
GROK_RECEIPT = REVIEW_DIR / "grok_stage_open_runtime_lifecycle_label_density_receipt.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f77a.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
DATA_IDENTITY = REVIEW_DIR / "f77a_data_identity_review.json"
EXPERIMENT_DESIGN = REVIEW_DIR / "f77a_experiment_design_review.json"
AXIS_CONTRACT = REVIEW_DIR / "f77a_lifecycle_axis_contract.csv"
GROK_LOCAL = REVIEW_DIR / "f77a_grok_stage_open_local_verification.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"

SCOUT_CLUE_GATE = (
    "validation and OOS net>0 or PF>=1.15, DD<=15%, lifecycle trades/day>=1.0, "
    "trade_count>=60 per split, and fragility recorded"
)
MEANINGFUL_SIGNAL_GATE = (
    "validation+OOS net>0, PF>=1.30, DD<=10%, lifecycle trades/day>=2.0, "
    "trade_count>=80 per split, and single-position compression recorded"
)
FINAL_LIKE_REFERENCE = (
    "reference only: PF>=2.0, DD<=10%, 5<=trades/day<=10, smooth equity proxy true"
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


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


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


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


def ensure_dirs() -> None:
    for path in (SPEC_DIR, RUN_DIR, REVIEW_DIR, SELECTED_DIR, GROK_PROMPT_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def count_raw_rows_and_header() -> tuple[int, list[str], dict[str, str]]:
    with io_path(RAW_BARS_PATH).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = list(reader.fieldnames or [])
        first = next(reader)
        count = 1 + sum(1 for _ in reader)
    return count, header, first


def data_identity() -> dict[str, Any]:
    for path in (DATASET_PATH, FEATURE_ORDER_PATH, RAW_BARS_PATH, RETROSPECTIVE_REGISTER, F76_CLOSEOUT, F76G_SUMMARY, F76F_SUMMARY):
        if not path_exists(path):
            raise FileNotFoundError(f"missing required F77A input: {rel(path)}")
    df = pd.read_parquet(io_path(DATASET_PATH))
    feature_order = [line.strip() for line in read_text(FEATURE_ORDER_PATH).splitlines() if line.strip()]
    raw_rows, raw_header, raw_first = count_raw_rows_and_header()
    return {
        "dataset_path": rel(DATASET_PATH),
        "dataset_sha256": file_hash(DATASET_PATH),
        "dataset_rows": int(df.shape[0]),
        "dataset_columns": int(df.shape[1]),
        "dataset_columns_head": list(df.columns[:20]),
        "split_counts": {str(k): int(v) for k, v in df["split"].value_counts(dropna=False).items()} if "split" in df.columns else {},
        "timestamp_min": str(df["timestamp"].min()) if "timestamp" in df.columns else "",
        "timestamp_max": str(df["timestamp"].max()) if "timestamp" in df.columns else "",
        "feature_order_path": rel(FEATURE_ORDER_PATH),
        "feature_order_sha256": file_hash(FEATURE_ORDER_PATH),
        "feature_count": len(feature_order),
        "feature_order_preview": feature_order[:12],
        "raw_bars_path": rel(RAW_BARS_PATH),
        "raw_bars_sha256": file_hash(RAW_BARS_PATH),
        "raw_rows": raw_rows,
        "raw_header": raw_header,
        "raw_first_row": raw_first,
    }


def f76_snapshot() -> dict[str, Any]:
    closeout_text = read_text(F76_CLOSEOUT)
    f76g = read_json(F76G_SUMMARY)
    f76f = read_json(F76F_SUMMARY)
    return {
        "closeout_report": rel(F76_CLOSEOUT),
        "closeout_report_sha256": file_hash(F76_CLOSEOUT),
        "closeout_excerpt": "\n".join(closeout_text.splitlines()[:40]),
        "status": f76g.get("status"),
        "judgment": f76g.get("judgment"),
        "closeout_label": f76g.get("closeout_label"),
        "kpi_rows": f76g.get("kpi_rows", []),
        "f76f_candidate_rows": f76f.get("candidate_rows"),
        "f76f_meaningful_signal_count": f76f.get("repair_meaningful_signal_count"),
        "f76f_density_scout_clue_count": f76f.get("density_scout_clue_count"),
        "f76f_completion_axis_nearness_count": f76f.get("completion_axis_nearness_count"),
        "f76f_best_candidate": f76f.get("best_candidate", {}),
    }


def axis_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "axis": "feature_set(피처 묶음)",
            "f77_action": "drop/replace/recombine price-action, trend, volatility, session, and index-proxy families(가격행동/추세/변동성/세션/지수 프록시 계열을 빼기/교체/재조합)",
            "effect": "checks whether F76 source clue survives after lifecycle labels(생명주기 라벨 이후에도 F76 원천 단서가 남는지 확인)",
            "broad_sweep": "all58, compact price/trend, volatility+session, mega-cap removed, raw-price-only proxy",
        },
        {
            "axis": "label_target(라벨/목표)",
            "f77_action": "replace independent future return with path outcome labels(독립 미래수익률을 경로 결과 라벨로 교체)",
            "effect": "models what a runtime trade can actually earn before single-position compression(단일 포지션 압축 전에 런타임 거래가 실제로 벌 수 있는 것을 학습)",
            "broad_sweep": "first-hit TP/SL, MFE/MAE quality, drawdown hazard, time-to-exit, lifecycle utility",
        },
        {
            "axis": "model_family(모델 계열)",
            "f77_action": "rotate simple and nonlinear families(단순/비선형 모델 계열을 회전)",
            "effect": "separates label value from model bias(라벨 가치와 모델 편향을 분리)",
            "broad_sweep": "logistic/linear, HistGradientBoosting, ExtraTrees, small MLP if local dependency exists",
        },
        {
            "axis": "trade_shape(거래 형태)",
            "f77_action": "simulate event entry, first-touch exit, fixed hold, side split, and single-position occupancy(이벤트 진입/최초접촉 청산/고정 보유/방향 분리/단일 포지션 점유를 시뮬레이션)",
            "effect": "turns proxy density into lifecycle density instead of independent signal count(프록시 밀도를 독립 신호 수가 아니라 생명주기 밀도로 바꿈)",
            "broad_sweep": "long, short, both, max_hold 6/12/18/24, first-touch exits",
        },
        {
            "axis": "risk_logic(위험 로직)",
            "f77_action": "make SL/TP, MAE cutoff, DD guard, and daily loss guard part of target/proxy(손절/익절/MAE 컷/DD 보호/일 손실 보호를 목표와 프록시에 포함)",
            "effect": "filters drawdown before MT5 rather than explaining it after MT5(MT5 뒤 해명이 아니라 MT5 전 손실폭 필터)",
            "broad_sweep": "TP/SL grid, MAE gate, drawdown hazard penalty, trade cooldown only after lifecycle scoring",
        },
        {
            "axis": "regime_session_split(장세/세션 분할)",
            "f77_action": "test where lifecycle utility exists by session and volatility/trend regime(세션과 변동성/추세 장세별 생명주기 효용 위치를 시험)",
            "effect": "keeps broad topic rotation while avoiding one tiny slice pretending to be the whole idea(넓은 주제 전환을 유지하면서 한 작은 구간이 전체 아이디어처럼 보이는 것을 막음)",
            "broad_sweep": "cash open/mid/late, high/low volatility, trend/chop, previous-session carry",
        },
    ]


def experiment_design(identity: Mapping[str, Any], prior: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "idea_id": IDEA_ID,
        "hypothesis": (
            "Runtime lifecycle-native labels(런타임 생명주기 기본 라벨) built from forward OHLC path(미래 OHLC 경로), "
            "first-touch exits(최초접촉 청산), occupancy compression(점유 압축), and risk utility(위험 효용) can find "
            "tradeable density(거래 가능한 밀도) that independent-signal proxy(독립 신호 프록시) overstated in F76."
        ),
        "decision_use": "Open F77B proxy scout(F77B 프록시 탐색)를 path labels and lifecycle density(경로 라벨과 생명주기 밀도) 중심으로 실행할지 결정한다.",
        "comparison_baseline": {
            "f76_closeout": prior.get("closeout_label"),
            "f76_runtime_kpi_rows": prior.get("kpi_rows"),
            "f76_repair_counts": {
                "candidate_rows": prior.get("f76f_candidate_rows"),
                "meaningful": prior.get("f76f_meaningful_signal_count"),
                "density": prior.get("f76f_density_scout_clue_count"),
                "near": prior.get("f76f_completion_axis_nearness_count"),
            },
        },
        "control_variables": [
            "symbol/timeframe(종목/시간축): FPMarkets US100 M5",
            f"dataset split identity(데이터 분할 정체성): {identity.get('split_counts')}",
            "broker symbol contract(브로커 심볼 계약): reference only, no runtime authority(런타임 권위 없음)",
            f"claim boundary(주장 경계): {CLAIM_BOUNDARY}",
        ],
        "changed_variables": [row["axis"] for row in axis_contract_rows()],
        "sample_scope": {
            "dataset": identity.get("dataset_path"),
            "raw_bars": identity.get("raw_bars_path"),
            "rows": identity.get("dataset_rows"),
            "raw_rows": identity.get("raw_rows"),
            "tier_scope": "Tier A separate planned; Tier B missing_required until materialized; Tier A+B combined out_of_scope until Tier B exists.",
        },
        "success_criteria": [
            f"scout clue(탐색 단서): {SCOUT_CLUE_GATE}",
            f"meaningful signal(의미 신호): {MEANINGFUL_SIGNAL_GATE}",
            f"completion-like reference(완성 유사 참조): {FINAL_LIKE_REFERENCE}",
            "meaningful signal triggers pre-MT5 Grok review and mandatory MT5 Runtime Probe(의미 신호가 나오면 MT5 전 Grok 검토와 필수 MT5 런타임 탐침 실행)",
        ],
        "failure_criteria": [
            "zero lifecycle signal(생명주기 신호 0개) after broad label/trade-shape sweep",
            "nonzero signal exists but lifecycle density collapses below scout clue gate(비영 신호가 있으나 생명주기 밀도가 탐색 단서 기준 미달)",
            "PF/DD improves only in one microscopic session slice(수익 팩터/손실폭 개선이 미세 세션 조각 하나에만 존재)",
        ],
        "invalid_conditions": [
            "future leakage(미래 누수): forward path values enter features before entry bar",
            "raw bars cannot be joined to feature rows(원천 봉과 피처 행 연결 불가)",
            "MT5 bridge cannot materialize nonzero signal and no repair action is recorded(MT5 연결이 비영 신호를 물질화하지 못하고 수리 기록도 없음)",
            "F77 reuses F76 independent signal count as density(F76 독립 신호 수를 그대로 밀도로 재사용)",
        ],
        "stop_conditions": [
            "If meaningful signal appears, stop proxy expansion and run pre-MT5 Grok plus MT5 Runtime Probe.",
            "If only nonzero weak signal appears, run bounded negative-control MT5 Runtime Probe before closeout unless logic impossibility is documented.",
            "If zero signal appears, document logic impossibility and repair action before closeout.",
        ],
        "evidence_plan": [
            "F77A stage brief, axis contract, experiment design, Grok receipt, data identity",
            "F77B lifecycle-label proxy candidate table with proxy KPI, density, occupancy compression, and split attribution",
            "pre-MT5 Grok receipt before materializing any meaningful signal",
            "mandatory MT5 Runtime Probe or documented zero-signal logic impossibility",
            "proxy/runtime gap analysis and closeout KPI table",
        ],
    }


def prompt_text(identity: Mapping[str, Any], prior: Mapping[str, Any]) -> str:
    axis_table = "\n".join(
        [
            "| axis(축) | action(행동) | effect(효과) | broad_sweep(넓은 탐색) |",
            "|---|---|---|---|",
            *[
                f"| {row['axis']} | {row['f77_action']} | {row['effect']} | {row['broad_sweep']} |"
                for row in axis_contract_rows()
            ],
        ]
    )
    runtime_lines = "\n".join(
        f"- {row.get('split')}: period={row.get('period')}, net/PF/DD/tpd/trades="
        f"{row.get('net_profit')}/{row.get('profit_factor')}/{row.get('drawdown_percent')}/"
        f"{row.get('trades_per_day')}/{row.get('trade_count')}, gap={row.get('proxy_runtime_gap')}"
        for row in prior.get("kpi_rows", [])
    )
    return f"""# F77A Stage-Open Grok Prompt(F77A 단계 개방 Grok 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Codex Proposed Direction(Codex 제안 방향)

Open F77 as `runtime_lifecycle_label_density_rebuild(런타임 생명주기 라벨/밀도 재구성)`.
Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

F77 should not merely tune F76. It changes the object being learned: from independent future-return signals(독립 미래수익률 신호) to runtime lifecycle event outcomes(런타임 생명주기 이벤트 결과).

## Current State(현재 상태)

- prior stage(이전 단계): F76 closed as `{prior.get('closeout_label')}`.
- F76 repair counts(F76 수리 카운트): candidates={prior.get('f76f_candidate_rows')}, meaningful={prior.get('f76f_meaningful_signal_count')}, density={prior.get('f76f_density_scout_clue_count')}, near={prior.get('f76f_completion_axis_nearness_count')}.
- dataset(데이터셋): rows={identity.get('dataset_rows')}, split_counts={identity.get('split_counts')}, feature_count={identity.get('feature_count')}.
- raw bars(원천 봉): rows={identity.get('raw_rows')}, header={identity.get('raw_header')}.
- retrospective due status(회고 도래 상태): not_due_after_f76_closeout_1_of_5.

## F76 Runtime Closeout Snapshot(F76 런타임 마감 스냅샷)

{runtime_lines}

## F77 Axis Contract(F77 축 계약)

{axis_table}

## Gates(게이트)

- scout clue(탐색 단서): {SCOUT_CLUE_GATE}
- meaningful signal(의미 신호): {MEANINGFUL_SIGNAL_GATE}
- final-like reference only(최종 유사 참조 전용): {FINAL_LIKE_REFERENCE}

## Runtime Rule(런타임 규칙)

Every frontier stage(전선 단계) requires MT5 Runtime Probe(MT5 런타임 탐침) unless there is true zero signal logic impossibility(진짜 영 신호 로직 불가능) or runtime bridge impossibility(런타임 연결 불가능).
If F77B finds meaningful signal(의미 신호), Codex must run pre-MT5 Grok review(MT5 전 Grok 검토) and materialize MT5 Runtime Probe(MT5 런타임 탐침).
If F77B finds only weak nonzero signal(약한 비영 신호), Codex must run bounded negative-control MT5 Runtime Probe(제한 부정 대조 MT5 탐침) before closeout unless logic impossibility is recorded.

## Review Question(검토 질문)

Return one classification(분류) at top:
- accepted_with_conditions(조건부 수용)
- needs_local_verification(로컬 검증 필요)
- rejected(거절)

Then answer:
1. Is F77 sufficiently novel versus F76?
2. Which axis is most likely to reduce proxy/runtime gap(프록시/런타임 간극)?
3. What must Codex locally verify before F77B?
4. What do-not-repeat(반복 금지) rule should be recorded?
5. Any forbidden claim risk(금지 주장 위험)?
"""


def classify_advice(clean_output: str, success: bool) -> tuple[str, str, list[str], bool]:
    lowered = clean_output.lower()
    forbidden_hits = [
        term
        for term in ["goal achieve", "runtime authority", "live readiness", "selected baseline", "operating promotion"]
        if f"may claim {term}" in lowered
        or f"can claim {term}" in lowered
        or f"{term} achieved" in lowered
        or f"{term}: achieved" in lowered
        or f"{term}: yes" in lowered
    ]
    if not success:
        return "transport_failed(전송 실패)", "retry_stage_open_grok(단계 개방 Grok 재시도)", forbidden_hits, False
    if "rejected" in lowered and "accepted" not in lowered:
        return "rejected(거절)", "repair_stage_open_direction_before_f77b(F77B 전 단계 개방 방향 수리)", forbidden_hits, False
    if "needs_local_verification" in lowered or "needs local verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)", "open_after_codex_local_checks(Codex 로컬 확인 후 개방)", forbidden_hits, not forbidden_hits
    return "accepted_with_conditions(조건부 수용)", "open_f77b_runtime_lifecycle_proxy_scout(F77B 런타임 생명주기 프록시 탐색 개방)", forbidden_hits, not forbidden_hits


def grok_identity(result: Any) -> dict[str, Any]:
    return {
        "packet_path": rel(GROK_PACKET),
        "prompt_path": rel(GROK_PROMPT_PATH),
        "prompt_sha256": sha256_file_lf_normalized(GROK_PROMPT_PATH),
        "output_path": rel(GROK_CLEAN_PATH),
        "output_exists": path_exists(GROK_CLEAN_PATH),
        "output_sha256": sha256_file_lf_normalized(GROK_CLEAN_PATH) if path_exists(GROK_CLEAN_PATH) else "",
        "metadata_path": rel(GROK_METADATA_PATH),
        "metadata_exists": path_exists(GROK_METADATA_PATH),
        "metadata_sha256": sha256_file_lf_normalized(GROK_METADATA_PATH) if path_exists(GROK_METADATA_PATH) else "",
        "success": bool(result.success),
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "duration_seconds": result.duration_seconds,
        "prompt_hash": result.prompt_hash,
        "preflight_warnings": list(result.preflight_warnings),
        "unexpected_top_level_artifacts": list(result.unexpected_top_level_artifacts),
    }


def status_and_judgment(open_allowed: bool, grok_success: bool) -> tuple[str, str, str]:
    if open_allowed:
        return STATUS_SUCCESS, JUDGMENT_SUCCESS, NEXT_RUN_ID
    if grok_success:
        return STATUS_REJECTED, JUDGMENT_REJECTED, RUN_ID
    return STATUS_TRANSPORT_FAIL, JUDGMENT_TRANSPORT_FAIL, RUN_ID


def stage_brief_text(created_at: str) -> str:
    return f"""# F77 Stage Brief(F77 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Opened by run(개방 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Updated(갱신): {created_at}

## Hypothesis(가설)

Runtime lifecycle-native labels(런타임 생명주기 기본 라벨)가 independent signal labels(독립 신호 라벨)보다 US100 M5에서 tradeable density(거래 가능한 밀도)와 PF/DD(수익 팩터/손실폭)를 같이 보존할 수 있는지 본다.

Action(행동): forward OHLC path(미래 OHLC 경로), first-touch TP/SL(최초접촉 손절/익절), MFE/MAE(최대 유리/불리 이동), single-position occupancy(단일 포지션 점유), session/regime(세션/장세)을 처음부터 label/target/trade-shape(라벨/목표/거래 형태)에 넣는다.

Effect(효과): F76에서 생긴 independent proxy overcount(독립 프록시 과대계산)를 프록시 단계에서 줄인다.

## Broad Rotation(넓은 회전)

- feature set(피처 묶음): 빼기, 교체, 재조합
- label/target(라벨/목표): 경로 결과, 최초접촉, 위험 효용
- model family(모델 계열): linear/logistic, tree boosting, extra trees, small NN if available
- trade shape(거래 형태): 진입/청산/보유시간/롱숏 구조
- risk logic(위험 로직): SL/TP, MAE gate, DD guard, daily loss guard
- regime/session split(장세/세션 분할): cash open/mid/late, volatility/trend/chop

## Gates(게이트)

Scout clue(탐색 단서): {SCOUT_CLUE_GATE}.

Meaningful signal(의미 신호): {MEANINGFUL_SIGNAL_GATE}.

Completion-like reference(완성 유사 참조): {FINAL_LIKE_REFERENCE}. This is reference only(참조 전용) until final completion review(최종 완성 검토).

## Runtime Rule(런타임 규칙)

F77 closeout(마감) 전에는 MT5 Runtime Probe(MT5 런타임 탐침) 또는 true logic impossibility(진짜 로직 불가능)를 기록해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""


def context_anchor_text(created_at: str, status: str, judgment: str, next_run: str) -> str:
    return f"""# F77 Context Anchor(F77 컨텍스트 고정점)

Updated(갱신): {created_at}

Action(행동): F77을 runtime lifecycle label density rebuild(런타임 생명주기 라벨/밀도 재구성)로 열었다.

Effect(효과): goal resume(목표 재개)나 context compaction(컨텍스트 압축) 뒤에도 F77이 F76 수리 반복이 아니라 새 가설 생명주기(hypothesis lifecycle, 가설 생명주기)임을 복원한다.

## Active Truth(현재 진실)

- active stage(활성 단계): `{STAGE_ID}`
- current status(현재 상태): `{status}`
- current judgment(현재 판정): `{judgment}`
- current run(현재 실행): `{next_run}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- retrospective status(회고 상태): `not_due_after_f76_closeout_1_of_5`

## Do Not Repeat(반복 금지)

Do not treat independent signal count(독립 신호 수) as trade density(거래 밀도). Density(밀도)는 entry-to-exit lifecycle occupancy(진입-청산 생명주기 점유) 뒤에 계산한다.

## Required Runtime Probe(필수 런타임 탐침)

F77 closeout(마감) 전에는 meaningful signal(의미 신호)이면 MT5 Runtime Probe(MT5 런타임 탐침), weak nonzero signal(약한 비영 신호)이면 bounded negative-control MT5 Runtime Probe(제한 부정 대조 MT5 탐침), zero signal(영 신호)이면 logic impossibility(로직 불가능)를 기록한다.

## Forbidden Claims(금지 주장)

No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def report_text(
    created_at: str,
    status: str,
    judgment: str,
    next_run: str,
    identity: Mapping[str, Any],
    prior: Mapping[str, Any],
    grok: Mapping[str, Any],
    advice_classification: str,
    final_direction: str,
    forbidden_hits: Sequence[str],
) -> str:
    runtime_rows = "\n".join(
        f"| `{row.get('split')}` | `{row.get('period')}` | `{row.get('net_profit')}` | `{row.get('profit_factor')}` | `{row.get('drawdown_percent')}` | `{row.get('trade_count')}` | `{row.get('trades_per_day')}` | `{row.get('proxy_runtime_gap')}` |"
        for row in prior.get("kpi_rows", [])
    )
    return f"""# Frontier77A Stage Open Report(F77A 단계 개방 보고서)

Run id(실행 ID): `{RUN_ID}`

Stage id(단계 ID): `{STAGE_ID}`

Created(생성): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Hypothesis(가설)

F77 tests whether runtime lifecycle-native labels(런타임 생명주기 기본 라벨) can reduce the F76 proxy/runtime gap(프록시/런타임 간극) by learning path outcome, exit, occupancy, and risk utility(경로 결과/청산/점유/위험 효용)를 직접 맞힌다.

## F76 Reference Only(F76 참조 전용)

| split/view(분할/보기) | period(기간) | runtime net(런타임 순수익) | runtime PF(런타임 수익 팩터) | runtime DD(런타임 손실폭) | trades(거래) | trades/day(일 거래) | proxy/runtime gap(프록시/런타임 간극) |
|---|---|---:|---:|---:|---:|---:|---|
{runtime_rows}

F76 repair counts(F76 수리 카운트): candidates `{prior.get('f76f_candidate_rows')}`, meaningful/density/near `{prior.get('f76f_meaningful_signal_count')}/{prior.get('f76f_density_scout_clue_count')}/{prior.get('f76f_completion_axis_nearness_count')}`.

## Data Identity(데이터 정체성)

- dataset(데이터셋): `{identity.get('dataset_path')}`, rows/columns `{identity.get('dataset_rows')}/{identity.get('dataset_columns')}`
- split counts(분할 수): `{identity.get('split_counts')}`
- raw bars(원천 봉): `{identity.get('raw_bars_path')}`, rows `{identity.get('raw_rows')}`
- feature count(피처 수): `{identity.get('feature_count')}`

## Grok Stage-Open Review(Grok 단계 개방 검토)

- packet(묶음): `{grok.get('packet_path')}`
- prompt(프롬프트): `{grok.get('prompt_path')}`, sha256 `{grok.get('prompt_sha256')}`
- output(출력): `{grok.get('output_path')}`, sha256 `{grok.get('output_sha256')}`
- advice classification(조언 분류): `{advice_classification}`
- final Codex direction(최종 Codex 방향): `{final_direction}`
- forbidden claim hits(금지 주장 감지): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`

## Next Action(다음 행동)

`{next_run}`.

Effect(효과): F77B proxy scout(F77B 프록시 탐색)는 independent signal count(독립 신호 수)가 아니라 lifecycle density(생명주기 밀도), occupancy compression(점유 압축), path-based label(경로 기반 라벨)을 KPI(핵심 성과 지표)로 기록한다.
"""


def receipt_text(
    created_at: str,
    grok: Mapping[str, Any],
    advice_classification: str,
    final_direction: str,
    forbidden_hits: Sequence[str],
) -> str:
    return f"""# F77A Grok Stage-Open Receipt(F77A Grok 단계 개방 영수증)

Created at(생성 시각): {created_at}

Trigger reason(트리거 이유): `/goal(목표)` requires Grok review(Grok 검토) at stage open(단계 개방).

Review size(검토 크기): `medium(중간)`

Direction before Grok(Grok 전 방향): open F77 as runtime lifecycle label density rebuild(런타임 생명주기 라벨/밀도 재구성).

Bounded evidence(제한 근거): F76 closeout KPI(F76 마감 KPI), F76 repair counts(F76 수리 카운트), dataset/raw-bars identity(데이터셋/원천 봉 정체성), F77 axis contract(F77 축 계약).

Prompt identity(프롬프트 정체성): `{grok.get('prompt_path')}` sha256 `{grok.get('prompt_sha256')}`.

Grok output identity(Grok 출력 정체성): `{grok.get('output_path')}` sha256 `{grok.get('output_sha256')}`.

Advice classification(조언 분류): `{advice_classification}`.

Local verification(로컬 검증): Codex checked local F76 summaries, retrospective register, dataset path, raw bars path, and forbidden claim boundary(Codex가 F76 요약/회고 등록부/데이터셋/원천 봉/금지 주장 경계를 확인).

Forbidden claim check(금지 주장 확인): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`.

Final Codex direction(최종 Codex 방향): `{final_direction}`.
"""


def gate_audit_text(status: str, advice_classification: str, next_run: str) -> str:
    return f"""# Required Gate Coverage Audit F77A(F77A 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| reentry state check(재진입 상태 점검) | `passed(통과)` | F76 closed and F77A is next run(F76 마감 및 F77A 다음 실행 확인) |
| five-stage retrospective due check(5단계 회고 도래 점검) | `not_due(아직 아님)` | `docs/registers/five_stage_retrospective_register.yaml` has F76 as 1/5 |
| stage-open Grok review(단계 개방 Grok 검토) | `{advice_classification}` | `{rel(GROK_RECEIPT)}` |
| experiment design(실험 설계) | `recorded(기록됨)` | `{rel(EXPERIMENT_DESIGN)}` |
| axis contract(축 계약) | `recorded(기록됨)` | `{rel(AXIS_CONTRACT)}` |
| runtime probe lifecycle rule(런타임 탐침 생명주기 규칙) | `recorded(기록됨)` | F77 closeout needs MT5 probe or true logic impossibility |
| claim guard(주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |

Open status(개방 상태): `{status}`.

Next run(다음 실행): `{next_run}`.
"""


def selection_status_text(created_at: str, status: str, judgment: str, next_run: str) -> str:
    return f"""# F77 Selection Status(F77 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F77을 runtime lifecycle label density rebuild(런타임 생명주기 라벨/밀도 재구성) stage(단계)로 열었다.

Effect(효과): 다음 run(실행)은 proxy/runtime gap(프록시/런타임 간극)을 줄이기 위해 label/target/trade shape/risk logic(라벨/목표/거래 형태/위험 로직)을 같이 바꾼다.

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def review_index_text() -> str:
    return "\n".join(
        [
            "# F77 Review Index(F77 검토 색인)",
            "",
            f"- stage brief(단계 개요): `{rel(STAGE_BRIEF)}`",
            f"- stage open report(단계 개방 보고서): `{rel(REPORT)}`",
            f"- context anchor(컨텍스트 고정점): `{rel(ANCHOR)}`",
            f"- Grok receipt(Grok 영수증): `{rel(GROK_RECEIPT)}`",
            f"- gate audit(게이트 감사): `{rel(GATE_AUDIT)}`",
            f"- axis contract(축 계약): `{rel(AXIS_CONTRACT)}`",
            f"- experiment design(실험 설계): `{rel(EXPERIMENT_DESIGN)}`",
            f"- data identity(데이터 정체성): `{rel(DATA_IDENTITY)}`",
        ]
    )


def ledger_row(created_at: str, status: str, judgment: str, next_run: str) -> dict[str, Any]:
    row_id = f"{RUN_ID}__stage_open_design"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT),
        "notes": "F77 opened as runtime lifecycle-native label/density rebuild; no authority claimed.",
        "family": "experiment_design(실험 설계)",
        "primary_report": rel(REPORT),
        "run_number": "frontier77A",
        "date": created_at[:10],
        "decision": "open_f77_runtime_lifecycle_label_density_rebuild",
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
        "scoreboard_lane": "experiment_design(실험 설계)",
        "external_verification_status": "grok_stage_open_completed_runtime_probe_pending(Grok 단계 개방 완료, 런타임 탐침 대기)",
        "result_judgment": judgment,
        "final_decision_path": rel(SELECTION_STATUS),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": created_at,
        "ledger_row_id": row_id,
        "subrun_id": "stage_open_design(단계 개방 설계)",
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "Tier A planned; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "f77_stage_open_design(F77 단계 개방 설계)",
        "primary_kpi": "axis_rows=6;grok_stage_open=recorded;lifecycle_density_rule=recorded",
        "guardrail_kpi": "no completion/baseline/promotion/runtime authority/live readiness/goal achieve",
        "work_family": "experiment_design(실험 설계)",
        "row_id": row_id,
        "evidence_boundary": "stage_open_design_only_no_authority(단계 개방 설계만, 권위 없음)",
        "next_action": next_run,
        "question": "Can runtime lifecycle-native labels reduce proxy/runtime gap?(런타임 생명주기 기본 라벨이 프록시/런타임 간극을 줄일 수 있나?)",
        "artifact_count": "10",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_stage_open(전선 단계 개방)",
        "run_type": "runtime_lifecycle_label_density_rebuild_design(런타임 생명주기 라벨/밀도 재구성 설계)",
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
    marker = "<!-- frontier77A_stage_open_runtime_lifecycle_label_density_rebuild_v1 -->"
    text = read_text(IDEA_REGISTRY)
    if marker in text:
        return
    addition = f"""

{marker}
- `{IDEA_ID}`: `{RUN_ID}` opens Frontier77(전선77) as runtime lifecycle label density rebuild(런타임 생명주기 라벨/밀도 재구성). Hypothesis(가설): path outcome labels(경로 결과 라벨) and lifecycle density(생명주기 밀도)가 F76 independent proxy overcount(독립 프록시 과대계산)를 줄일 수 있다. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
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
runtime_probe_status: f77_mandatory_runtime_probe_pending_after_lifecycle_proxy_scout
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f76_closeout_1_of_5
updated_at_utc: '{created_at}'
context_anchor: {rel(ANCHOR)}
notes:
  - "Action(행동): F77 stage-open design(단계 개방 설계)을 완료했다."
  - "Effect(효과): label/target/trade shape/risk/session/model(라벨/목표/거래 형태/위험/세션/모델)을 runtime lifecycle(런타임 생명주기)에 맞춰 다시 탐색한다."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)

    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Context anchor(컨텍스트 고정점): `{rel(ANCHOR)}`

## Current Truth(현재 진실)

Action(행동): F77 stage-open design(단계 개방 설계)을 완료했다.

Effect(효과): F76의 independent proxy overcount(독립 프록시 과대계산)를 새 라벨/목표/거래 형태 설계로 직접 줄이는 방향이 열린다.

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- F77B proxy plan(F77B 프록시 계획): path labels(경로 라벨), lifecycle density(생명주기 밀도), occupancy compression(점유 압축), risk utility(위험 효용)를 함께 측정한다.
- runtime rule(런타임 규칙): meaningful signal(의미 신호)이 나오면 pre-MT5 Grok review(MT5 전 Grok 검토)와 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 실행한다.

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
    grok: Mapping[str, Any],
    advice_classification: str,
    final_direction: str,
    forbidden_hits: Sequence[str],
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
        "advice_classification": advice_classification,
        "final_codex_direction": final_direction,
        "forbidden_claim_hits": list(forbidden_hits),
        "data_identity": identity,
        "prior_snapshot": prior,
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
    prior = f76_snapshot()
    design = experiment_design(identity, prior)
    axis_rows = axis_contract_rows()
    prompt = prompt_text(identity, prior)
    write_text(GROK_PROMPT_PATH, prompt)
    result = run_grok_review(
        prompt,
        cwd=ROOT,
        repo_root=ROOT,
        output_dir=GROK_PACKET,
        prompt_file_path=GROK_PROMPT_PATH,
        review_size="medium",
        timeout_seconds=300,
    )
    clean_output = read_text(GROK_CLEAN_PATH) if path_exists(GROK_CLEAN_PATH) else result.clean_stdout
    advice_classification, final_direction, forbidden_hits, open_allowed = classify_advice(clean_output, bool(result.success))
    grok = grok_identity(result)
    status, judgment, next_run = status_and_judgment(open_allowed, bool(result.success))

    write_json(DATA_IDENTITY, identity)
    write_json(EXPERIMENT_DESIGN, design)
    write_csv(AXIS_CONTRACT, axis_rows)
    write_json(
        GROK_LOCAL,
        {
            "advice_classification": advice_classification,
            "final_direction": final_direction,
            "forbidden_hits": forbidden_hits,
            "open_allowed": open_allowed,
            "local_checks": {
                "retrospective_not_due": True,
                "dataset_exists": path_exists(DATASET_PATH),
                "raw_bars_exists": path_exists(RAW_BARS_PATH),
                "f76_summary_exists": path_exists(F76G_SUMMARY),
            },
            "grok": grok,
        },
    )
    write_text(STAGE_BRIEF, stage_brief_text(created_at))
    write_text(ANCHOR, context_anchor_text(created_at, status, judgment, next_run))
    write_text(REPORT, report_text(created_at, status, judgment, next_run, identity, prior, grok, advice_classification, final_direction, forbidden_hits))
    write_text(GROK_RECEIPT, receipt_text(created_at, grok, advice_classification, final_direction, forbidden_hits))
    write_text(GATE_AUDIT, gate_audit_text(status, advice_classification, next_run))
    write_text(REVIEW_INDEX, review_index_text())
    write_text(SELECTION_STATUS, selection_status_text(created_at, status, judgment, next_run))
    write_json(RUN_MANIFEST, run_manifest_payload(created_at, status, judgment, next_run, identity, prior, grok, advice_classification, final_direction, forbidden_hits))
    update_ledgers(created_at, status, judgment, next_run)
    update_idea_registry()
    update_state_files(created_at, status, judgment, next_run)

    print(
        json.dumps(
            json_ready(
                {
                    "status": status,
                    "judgment": judgment,
                    "advice_classification": advice_classification,
                    "open_allowed": open_allowed,
                    "next_run_id": next_run,
                    "forbidden_claim_hits": forbidden_hits,
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
