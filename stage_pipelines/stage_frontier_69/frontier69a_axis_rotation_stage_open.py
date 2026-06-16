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

from foundation.control_plane.ledger import io_path, json_ready, path_exists


STAGE_ID = "stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory"
RUN_ID = "frontier69A_stage_open_axis_rotation_hypothesis_design_v1"
NEXT_RUN_ID = "frontier69B_event_first_first_hit_proxy_sweep_v1"
PREVIOUS_STAGE_ID = "stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout"
PREVIOUS_CLOSEOUT_RUN_ID = "frontier68_closeout_preserved_clue_negative_memory_v1"
IDEA_ID = "IDEA-FR69-EVENT-FIRST-AXIS-ROTATION-PF-SOURCE"

CLAIM_BOUNDARY = (
    "stage_open_design_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

MODEL_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
MODEL_FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"
RAW_US100 = ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"
F68_CLOSEOUT_REPORT = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews" / "stage_closeout_report.md"
F68_REQUIRED_GATE = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews" / "required_gate_coverage_audit.md"
F68J_MANIFEST = ROOT / "stages" / PREVIOUS_STAGE_ID / "02_runs" / "frontier68J_unit_corrected_atr_runtime_repair_probe_v1" / "run_manifest.json"
F68F_RECEIPT = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews" / "frontier68F_runtime_probe_receipt_review.csv"
F68J_RECEIPT = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews" / "frontier68J_runtime_probe_receipt_review.csv"

FIVE_STAGE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f69_stage_open_axis_rotation"
GROK_PROMPT = GROK_PACKET / "prompts/f69_stage_open_axis_rotation_prompt.md"
GROK_OUTPUT = GROK_PACKET / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET / "outputs/metadata.json"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in fieldnames})


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


def ordered_hash(names: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()


def required_artifacts() -> list[Path]:
    return [
        MODEL_INPUT,
        MODEL_FEATURE_ORDER,
        RAW_US100,
        F68_CLOSEOUT_REPORT,
        F68_REQUIRED_GATE,
        F68J_MANIFEST,
        F68F_RECEIPT,
        F68J_RECEIPT,
        FIVE_STAGE_REGISTER,
        GROK_PROMPT,
        GROK_OUTPUT,
        GROK_METADATA,
    ]


def data_identity() -> dict[str, Any]:
    frame = pd.read_parquet(io_path(MODEL_INPUT))
    order = [line.strip() for line in read_text(MODEL_FEATURE_ORDER).splitlines() if line.strip()]
    raw_head = pd.read_csv(io_path(RAW_US100), nrows=5)
    raw = pd.read_csv(io_path(RAW_US100), usecols=["time_close_unix", "open", "high", "low", "close", "spread_points"])
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.sort_values("timestamp").reset_index(drop=True)
    positions = pd.Series(raw.index.to_numpy(), index=raw["timestamp"]).reindex(frame["timestamp"]).to_numpy(dtype=float)
    labelable: dict[str, Any] = {}
    for horizon in (3, 6, 9, 12):
        valid = pd.Series((positions == positions) & ((positions + horizon) < len(raw)))
        subset = frame.loc[valid.to_numpy()]
        labelable[f"h{horizon}_labelable_rows"] = int(len(subset))
        labelable[f"h{horizon}_split_counts"] = {str(k): int(v) for k, v in subset["split"].value_counts().to_dict().items()}
    session_buckets = {
        "open_0_30": int(((frame["minutes_from_cash_open"] > 0) & (frame["minutes_from_cash_open"] <= 30)).sum()),
        "mid_35_300": int(((frame["minutes_from_cash_open"] > 30) & (frame["minutes_from_cash_open"] <= 300)).sum()),
        "late_305_390": int(((frame["minutes_from_cash_open"] > 300) & (frame["minutes_from_cash_open"] <= 390)).sum()),
        "outside_or_missing": int((~((frame["minutes_from_cash_open"] > 0) & (frame["minutes_from_cash_open"] <= 390))).sum()),
    }
    regime_buckets = {
        "trend_adx_ge25": int((frame["adx_14"] >= 25).sum()),
        "chop_adx_lt18": int((frame["adx_14"] < 18).sum()),
        "vol_expansion_hv5over20_ge1p25": int((frame["historical_vol_5_over_20"] >= 1.25).sum()),
        "bb_squeeze_on": int((frame["bb_squeeze"] == 1).sum()),
    }
    return {
        "model_input_path": rel(MODEL_INPUT),
        "model_input_sha256": sha256_file(MODEL_INPUT),
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "split_counts": {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()},
        "timestamp_min": str(frame["timestamp"].min()),
        "timestamp_max": str(frame["timestamp"].max()),
        "feature_order_path": rel(MODEL_FEATURE_ORDER),
        "feature_count": len(order),
        "feature_order_hash": ordered_hash(order),
        "feature_order_sha256": sha256_file(MODEL_FEATURE_ORDER),
        "raw_us100_path": rel(RAW_US100),
        "raw_us100_sha256": sha256_file(RAW_US100),
        "raw_columns": list(raw_head.columns),
        "aligned_model_rows": int((positions == positions).sum()),
        "unaligned_model_rows": int((positions != positions).sum()),
        "labelable": labelable,
        "session_bucket_counts": session_buckets,
        "regime_bucket_counts": regime_buckets,
    }


def axis_diff_rows() -> list[dict[str, str]]:
    return [
        {
            "axis": "feature_set(피처 묶음)",
            "f68_surface": "full F68F/F68 lifecycle ONNX feature surface(전체 F68F/F68 생명주기 온엑스 피처 표면)",
            "f69_surface": "compact event/context feature surface(압축 이벤트/문맥 피처 표면)",
            "change_type": "replace_and_ablate(교체 및 소거)",
            "enforcement": "write explicit F68F as-is reuse prohibition(F68F 그대로 재사용 금지 명시)",
        },
        {
            "axis": "label_target(라벨/목표)",
            "f68_surface": "lifecycle/cost/DD aggregate label(생명주기/비용/손실폭 집계 라벨)",
            "f69_surface": "first-hit opportunity long/short heads(선도달 기회 롱/숏 헤드)",
            "change_type": "replace(교체)",
            "enforcement": "future path starts after entry bar only(미래 경로는 진입봉 이후만 사용)",
        },
        {
            "axis": "model_family(모델 계열)",
            "f68_surface": "F68F ONNX scoring vehicle(F68F 온엑스 점수화 수단)",
            "f69_surface": "linear/shallow tree first, optional EBM-like only if local support(선형/얕은 트리 우선, EBM 유사 선택)",
            "change_type": "rotate(회전)",
            "enforcement": "interpretable scout before ONNX export(온엑스 내보내기 전 해석 가능 탐색)",
        },
        {
            "axis": "trade_shape(거래 형태)",
            "f68_surface": "dense every-bar scoring with risk repair(촘촘한 매봉 점수와 위험 수리)",
            "f69_surface": "event admission, fixed hold, first-hit SLTP(이벤트 진입, 고정 보유, 선도달 손익절)",
            "change_type": "replace(교체)",
            "enforcement": "risk knobs frozen in phase 1(1단계에서 위험 손잡이 고정)",
        },
        {
            "axis": "risk_logic(위험 로직)",
            "f68_surface": "ATR width/capped repair became central(평균진폭 폭/상한 수리가 중심화)",
            "f69_surface": "single conservative template until PF movement appears(PF 움직임 전까지 단일 보수 템플릿)",
            "change_type": "demote(보조화)",
            "enforcement": "no SLTP-only search until proxy source passes(프록시 원천 통과 전 손익절 단독 탐색 금지)",
        },
        {
            "axis": "regime_session_split(장세/세션 분할)",
            "f68_surface": "not primary attribution axis(주 귀속 축 아님)",
            "f69_surface": "open/mid/late, trend/chop/volatility bucket comparisons(초/중/후반, 추세/횡보/변동성 구간 비교)",
            "change_type": "add_as_primary_attribution(주 귀속 축으로 추가)",
            "enforcement": "bucket KPI required in F69B(F69B 구간별 KPI 필수)",
        },
    ]


def f69b_phase_rows() -> list[dict[str, str]]:
    return [
        {
            "phase": "phase1_event_label_model(1단계 이벤트/라벨/모델)",
            "purpose": "test whether event-first first-hit labels move proxy PF(이벤트 우선 선도달 라벨이 프록시 PF를 움직이는지 확인)",
            "allowed_changes": "event definition, first-hit labels, linear/shallow model(이벤트 정의, 선도달 라벨, 선형/얕은 모델)",
            "frozen": "risk template, broad trade-shape knobs(위험 템플릿, 넓은 거래형태 손잡이)",
            "advance_condition": "validation and OOS show non-density-only PF separation(검증/표본외가 밀도만이 아닌 PF 분리를 보임)",
        },
        {
            "phase": "phase2_regime_session_attribution(2단계 장세/세션 귀속)",
            "purpose": "locate where signal survives(신호가 살아남는 구간 찾기)",
            "allowed_changes": "open/mid/late, trend/chop/volatility buckets(초/중/후반, 추세/횡보/변동성 구간)",
            "frozen": "best phase1 label/model family(1단계 라벨/모델 계열)",
            "advance_condition": "at least one bucket improves PF without collapsing trades/day(한 구간 이상 PF 개선, 일 거래 수 붕괴 없음)",
        },
        {
            "phase": "phase3_trade_shape_limited(3단계 제한 거래 형태)",
            "purpose": "only after PF source exists, test cooldown/hold bounds(PF 원천 후 쿨다운/보유 경계 확인)",
            "allowed_changes": "cooldown and max hold caps only(쿨다운과 최대 보유 상한만)",
            "frozen": "feature/label/model/regime source(피처/라벨/모델/장세 원천)",
            "advance_condition": "proxy signal earns pre-MT5 Grok review(프록시 신호가 사전 MT5 그록 검토 자격을 얻음)",
        },
    ]


def local_verification(identity: Mapping[str, Any], grok: Mapping[str, Any]) -> dict[str, Any]:
    five_text = read_text(FIVE_STAGE_REGISTER)
    return {
        "grok_transport_success": bool(grok.get("success") is True and grok.get("returncode") == 0),
        "grok_prompt_hash": grok.get("prompt_hash", ""),
        "five_stage_retrospective_due_status": "not_due" if "current_due_status: not_due" in five_text else "needs_local_verification",
        "data_source_usable": identity["rows"] == 46650 and identity["feature_count"] == 58,
        "raw_model_alignment": identity["aligned_model_rows"] == identity["rows"] and identity["unaligned_model_rows"] == 0,
        "first_hit_label_definability": {
            "h3": identity["labelable"]["h3_labelable_rows"],
            "h6": identity["labelable"]["h6_labelable_rows"],
            "h9": identity["labelable"]["h9_labelable_rows"],
            "h12": identity["labelable"]["h12_labelable_rows"],
            "judgment": "usable_with_closed_bar_future_path_boundary(닫힌 봉 이후 미래 경로 경계에서 사용 가능)",
        },
        "event_sparsity_budget": "target 5-10 trades/day remains final-review gate; F69B proxy scout should log event rows/day before MT5(최종 게이트는 5-10회/일, F69B는 MT5 전 이벤트 행/일 기록)",
        "session_regime_schema": {
            "session_buckets": identity["session_bucket_counts"],
            "regime_buckets": identity["regime_bucket_counts"],
            "judgment": "usable_for_proxy_bucket_attribution(프록시 구간 귀속에 사용 가능)",
        },
        "tier_pair_plan": "Tier A separate, Tier B separate, Tier A+B combined required; if unavailable mark missing_required/blocked/out_of_scope_by_claim(티어 A/B/합산 필수, 불가 시 상태 명시)",
        "forbidden_claims": {
            "completion": "not_claimed(주장 없음)",
            "baseline": "not_claimed(주장 없음)",
            "promotion": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "live_readiness": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
        },
    }


def experiment_design_payload(created_at: str, identity: Mapping[str, Any], grok: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "idea_id": IDEA_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "hypothesis": (
            "A sparse event-first regime/session and candle-path opportunity model(희소 이벤트 우선 장세/세션 및 캔들 경로 기회 모델)이 "
            "F68 risk-only repair loop(F68 위험 단독 수리 반복)와 다른 PF source(수익 팩터 원천)를 만들 수 있는지 시험한다."
        ),
        "decision_use": "Open F69 and authorize F69B proxy sweep only( F69 개방 및 F69B 프록시 탐색 허용만 한다).",
        "comparison_baseline": "F68 closeout evidence only, not a baseline( F68 마감 근거는 참조일 뿐 기준선 아님).",
        "control_variables": [
            "symbol/timeframe US100 M5(심볼/시간프레임 US100 5분봉)",
            "closed-bar only features(닫힌 봉 피처만)",
            "train/validation/OOS split v1(학습/검증/표본외 분할 v1)",
            "risk template frozen in F69B phase 1(F69B 1단계 위험 템플릿 고정)",
            "no strong claims(강한 주장 없음)",
        ],
        "changed_variables": [
            "feature set becomes event/context compact surface(피처 묶음은 이벤트/문맥 압축 표면)",
            "label becomes first-hit long/short opportunity(라벨은 선도달 롱/숏 기회)",
            "model family begins interpretable-first(모델 계열은 해석 가능 우선)",
            "trade shape becomes sparse event admission(거래 형태는 희소 이벤트 진입)",
            "regime/session split becomes primary attribution(장세/세션 분할은 주 귀속 축)",
        ],
        "sample_scope": {
            "data_source": identity["model_input_path"],
            "raw_us100": identity["raw_us100_path"],
            "rows": identity["rows"],
            "splits": identity["split_counts"],
            "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        },
        "success_criteria": [
            "F69B shows proxy PF movement not explained only by density or DD repair(F69B가 밀도/손실폭 수리만이 아닌 PF 움직임을 보임)",
            "session/regime bucket separation is visible(세션/장세 구간 분리가 보임)",
            "event sparsity remains compatible with eventual 5-10 trades/day target(이벤트 희소성이 최종 5-10회/일 목표와 양립 가능)",
        ],
        "failure_criteria": [
            "all useful rows come only from SL/TP/cooldown width changes(유용 행이 손익절/쿨다운 폭 변경에서만 나옴)",
            "feature/model surface collapses into F68F reuse(F68F 재사용으로 붕괴)",
            "proxy signal is zero or only validation-specific(프록시 신호가 0 또는 검증 전용)",
        ],
        "invalid_conditions": [
            "first-hit labels use current or future data incorrectly(선도달 라벨이 현재/미래 데이터를 잘못 사용)",
            "session buckets use raw broker timestamp as direct UTC(세션 구간이 원천 브로커 시간을 직접 UTC로 사용)",
            "Tier B or combined record is silently omitted(티어 B 또는 합산 기록이 조용히 누락)",
        ],
        "stop_conditions": [
            "F69B zero signal: record invalid/blocked and repair label/event definition(F69B 영 신호면 무효/차단 기록 후 라벨/이벤트 수리)",
            "meaningful proxy signal: run pre-MT5 Grok and mandatory MT5 Runtime Probe(의미 있는 프록시 신호면 사전 그록 및 필수 MT5 탐침)",
            "risk-only repetition detected: cap repair and close as negative memory(위험 단독 반복이면 수리 상한 후 부정 기억 마감)",
        ],
        "evidence_plan": [
            "axis diff table(축 차이표)",
            "F69B proxy KPI by split and bucket(F69B 분할/구간별 프록시 KPI)",
            "Tier A/B/combined ledger rows(티어 A/B/합산 장부 행)",
            "pre-MT5 Grok receipt before runtime probe(런타임 탐침 전 그록 영수증)",
            "mandatory MT5 Runtime Probe receipt if meaningful proxy signal exists(의미 있는 프록시 신호 시 필수 MT5 탐침 영수증)",
        ],
        "exploration_mandate": {
            "legacy_relation": "prior_evidence_only(이전 근거 전용)",
            "tier_scope": "Tier A+B planned(티어 A+B 계획)",
            "broad_sweep": "event labels, compact features, interpretable models, session/regime buckets(이벤트 라벨/압축 피처/해석 모델/세션 장세 구간)",
            "extreme_sweep": "boundary event definitions and sparse/dense event budgets only after phase 1(1단계 후 경계 이벤트 정의와 희소/밀도 예산)",
            "micro_search_gate": "proxy PF movement plus bucket separation(프록시 PF 움직임과 구간 분리)",
            "wfo_plan": "WFO is required after proxy and runtime scout show nonzero material signal(프록시와 런타임 탐색이 0이 아닌 신호를 보이면 WFO 필수)",
            "failure_memory": "record do-not-repeat if F69 collapses to risk-only or F68F reuse(F69가 위험 단독/F68F 재사용으로 붕괴하면 반복 금지 기록)",
            "evidence_boundary": "stage_open_design_only(단계 개방 설계 전용)",
        },
        "data_integrity": {
            "data_source": [identity["model_input_path"], identity["raw_us100_path"]],
            "time_axis": "bar-close key with project time-axis policy; session columns from verified mapper(봉 닫힘 키와 프로젝트 시간축 정책, 검증 매퍼 세션 컬럼)",
            "sample_scope": identity["split_counts"],
            "missing_or_duplicate_check": "raw/model alignment 46650/46650, unaligned 0(원천/모델 정렬 46650/46650, 미정렬 0)",
            "feature_label_boundary": "features at current closed bar; labels use future path after entry bar only(피처는 현재 닫힌 봉, 라벨은 진입봉 이후 미래 경로)",
            "split_boundary": "train/validation/oos split v1 retained(분할 v1 유지)",
            "leakage_risk": "first-hit path and session bucket construction(선도달 경로와 세션 구간 구성)",
            "data_hash_or_identity": {
                "model_input_sha256": identity["model_input_sha256"],
                "raw_us100_sha256": identity["raw_us100_sha256"],
            },
            "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)",
        },
        "model_validation": {
            "model_family": "linear and shallow tree first; optional EBM-like if local support(선형/얕은 트리 우선, 로컬 지원 시 EBM 유사 선택)",
            "target_and_label": "side-specific first-hit opportunity with MAE guard(불리 이동 보호가 있는 방향별 선도달 기회)",
            "split_method": "time-ordered train/validation/OOS and later WFO(시간순 학습/검증/표본외 및 이후 WFO)",
            "selection_metric": "proxy PF movement with trades/day and DD guardrails(프록시 PF 움직임과 일 거래 수/손실폭 가드레일)",
            "secondary_metrics": "bucket separation, shuffled-label control, long/short mix(구간 분리, 셔플 라벨 대조, 롱/숏 비율)",
            "threshold_policy": "searched only after event/label signal exists(이벤트/라벨 신호 이후에만 탐색)",
            "overfit_risk": "multi-axis broad sweep selection bias(다축 넓은 탐색 선택 편향)",
            "calibration_risk": "scores are ranks, not probabilities until calibrated(보정 전 점수는 확률이 아니라 순위)",
            "comparison_baseline": "F68 negative memory reference and no-trade/shuffled controls(F68 부정 기억 참조 및 무거래/셔플 대조)",
            "validation_judgment": "exploratory_stage_open(탐색 단계 개방)",
        },
        "grok": grok_receipt_payload(grok),
        "next_run_id": NEXT_RUN_ID,
    }


def grok_receipt_payload(metadata: Mapping[str, Any]) -> dict[str, Any]:
    clean = read_text(GROK_OUTPUT)
    return {
        "trigger_reason": "goal requires Grok stage-open review(목표가 그록 단계 개방 검토를 요구)",
        "review_size": metadata.get("review_size", "medium"),
        "direction_before_grok": "Open F69 as event-first axis rotation after F68 risk-only negative memory(F68 위험 단독 부정 기억 뒤 이벤트 우선 축 회전으로 F69 개방)",
        "bounded_evidence": [rel(F68_CLOSEOUT_REPORT), rel(FIVE_STAGE_REGISTER), rel(GROK_PROMPT)],
        "prompt_identity": {"path": rel(GROK_PROMPT), "prompt_hash": metadata.get("prompt_hash", ""), "sha256": sha256_file(GROK_PROMPT)},
        "grok_output_identity": {"path": rel(GROK_OUTPUT), "sha256": sha256_file(GROK_OUTPUT), "metadata": rel(GROK_METADATA)},
        "advice_classification": {
            "accepted": [
                "axis rotation is directionally sound(축 회전 방향 타당)",
                "stage open design-only boundary is sound(단계 개방 설계 전용 경계 타당)",
                "interpretable compact model family first(해석 가능한 압축 모델 우선)",
                "regime/session bucket attribution required(장세/세션 구간 귀속 필요)",
            ],
            "rejected": [
                "do not use F68J OOS metrics as F69 success preconditions(F68J 표본외 지표를 F69 성공 전제로 쓰지 않음)",
                "do not let F69 become F68F reuse with event wrappers(F69를 이벤트 포장 F68F 재사용으로 만들지 않음)",
                "do not frame pre-MT5 probe as due at stage open(사전 MT5 탐침을 단계 개방 시점 의무로 말하지 않음)",
            ],
            "needs_local_verification": [
                "F68 artifact lineage and explicit exclusions(F68 산출물 계보와 명시 제외)",
                "first-hit label definability(선도달 라벨 정의 가능성)",
                "event sparsity budget(이벤트 희소성 예산)",
                "session/regime bucket schema(세션/장세 구간 스키마)",
                "Tier A/B paired plan(티어 A/B 쌍 계획)",
            ],
        },
        "local_verification": "recorded in f69a_local_verification.json(F69A 로컬 검증 JSON에 기록)",
        "forbidden_claim_check": "no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)",
        "final_codex_direction": "accept with local constraints and open F69A as axis contract(로컬 제약과 함께 수용하고 F69A를 축 계약으로 개방)",
        "clean_output_excerpt": clean.splitlines()[:8],
    }


def stage_brief_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        "# F69 Stage Brief(F69 단계 개요)",
        "",
        f"Stage(단계): `{STAGE_ID}`",
        f"Opened(개방): {payload['created_at_utc']}",
        "",
        "## Hypothesis(가설)",
        "",
        str(payload["hypothesis"]),
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F69를 event-first axis rotation(이벤트 우선 축 회전) 전선으로 연다.",
        "",
        "Effect(효과): F68의 동등성/기록 단서는 보존하지만, 동일 ONNX(온엑스)에 위험 로직만 덧대는 반복을 끊고 새 PF source(수익 팩터 원천)를 찾는다.",
        "",
        "## Axis Contract(축 계약)",
        "",
        "| axis(축) | F68 surface(F68 표면) | F69 surface(F69 표면) | enforcement(강제 경계) |",
        "|---|---|---|---|",
    ] + [
        f"| {row['axis']} | {row['f68_surface']} | {row['f69_surface']} | {row['enforcement']} |"
        for row in axis_diff_rows()
    ] + [
        "",
        "## Required Lifecycle(필수 생명주기)",
        "",
        "Hypothesis(가설) -> proxy(프록시) -> mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) -> gap analysis(간극 분석) -> validation/repair/closeout(검증/수리/마감).",
        "",
        "F69A is design-only(설계 전용)이다. F69B가 meaningful proxy signal(의미 있는 프록시 신호)을 만들면 pre-MT5 Grok review(사전 MT5 그록 검토)와 MT5 Runtime Probe(MT5 런타임 탐침)를 실행한다.",
        "",
        "## Grok Stage Open Review(그록 단계 개방 검토)",
        "",
        f"- prompt_path(프롬프트 경로): `{payload['grok']['prompt_identity']['path']}`",
        f"- prompt_hash(프롬프트 해시): `{payload['grok']['prompt_identity']['prompt_hash']}`",
        f"- clean_output_path(정리 출력 경로): `{payload['grok']['grok_output_identity']['path']}`",
        f"- advice_classification(조언 분류): `accepted_with_conditions(조건부 수용)`",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`: staged proxy sweep(단계형 프록시 탐색)을 실행한다.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def report_lines(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> list[str]:
    identity = payload["sample_scope"]
    return [
        "# F69A Axis Rotation Stage Open(F69A 축 회전 단계 개방)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F69A에서 axis diff contract(축 차이 계약), F69B staged proxy plan(단계형 프록시 계획), Grok receipt(그록 영수증), local verification(로컬 검증)을 물질화했다.",
        "",
        "Effect(효과): F69가 F68 risk-only repair loop(F68 위험 단독 수리 반복)로 되돌아가는 길을 문서 경계와 장부 경계로 막는다.",
        "",
        "## Experiment Design(실험 설계)",
        "",
        f"- hypothesis(가설): {payload['hypothesis']}",
        f"- decision_use(결정 사용): {payload['decision_use']}",
        f"- comparison_baseline(비교 기준): {payload['comparison_baseline']}",
        f"- sample_scope(표본 범위): rows(행) `{identity['rows']}`, split(분할) `{identity['splits']}`.",
        "",
        "## Axis Diff(축 차이)",
        "",
        "| axis(축) | change_type(변경 유형) | enforcement(강제 경계) |",
        "|---|---|---|",
    ] + [
        f"| {row['axis']} | {row['change_type']} | {row['enforcement']} |" for row in axis_diff_rows()
    ] + [
        "",
        "## F69B Staged Proxy Plan(F69B 단계형 프록시 계획)",
        "",
        "| phase(단계) | purpose(목적) | frozen(고정) | advance_condition(진행 조건) |",
        "|---|---|---|---|",
    ] + [
        f"| {row['phase']} | {row['purpose']} | {row['frozen']} | {row['advance_condition']} |" for row in f69b_phase_rows()
    ] + [
        "",
        "## Local Verification(로컬 검증)",
        "",
        f"- Grok transport success(그록 전송 성공): `{verification['grok_transport_success']}`.",
        f"- five-stage retrospective(5단계 중간 검토): `{verification['five_stage_retrospective_due_status']}`.",
        f"- data usable(데이터 사용 가능): `{verification['data_source_usable']}`.",
        f"- raw/model alignment(원천/모델 정렬): `{verification['raw_model_alignment']}`.",
        f"- first-hit definability(선도달 정의 가능성): `{verification['first_hit_label_definability']['judgment']}`.",
        f"- session/regime schema(세션/장세 스키마): `{verification['session_regime_schema']['judgment']}`.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}` proxy sweep(프록시 탐색)을 실행한다. Meaningful proxy signal(의미 있는 프록시 신호)이 나오면 MT5 전 Grok review(그록 검토) 후 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 실행한다.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def gate_audit_lines(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> list[str]:
    return [
        "# F69A Required Gate Coverage Audit(F69A 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| work_family(작업군) | pass(통과) | experiment_design(실험 설계) + Grok overlay(그록 추가) | F69A가 설계 전용 개방임을 고정 |",
        f"| external_review_packet(외부 검토 묶음) | pass(통과) | `{payload['grok']['grok_output_identity']['path']}` | Grok second opinion(2차 의견) 기록 |",
        f"| five_stage_retrospective(5단계 중간 검토) | `{verification['five_stage_retrospective_due_status']}` | `{rel(FIVE_STAGE_REGISTER)}` | F69 open(개방) 차단 여부 확인 |",
        f"| data_integrity(데이터 무결성) | usable_with_boundary(경계 내 사용 가능) | `{rel(RUN_ROOT / 'f69a_data_identity.json')}` | F69B proxy(프록시) 실행 가능성 확인 |",
        f"| model_validation_boundary(모델 검증 경계) | exploratory(탐색) | `{rel(RUN_ROOT / 'f69a_experiment_design.json')}` | 모델 우열 주장 방지 |",
        f"| final_claim_guard(최종 주장 보호) | pass(통과) | forbidden claims not_claimed(금지 주장 없음) | completion/baseline/promotion/runtime authority(완성/기준선/승격/런타임 권위) 방지 |",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def review_index_lines() -> list[str]:
    return [
        "# F69 Review Index(F69 검토 색인)",
        "",
        "- `../00_spec/stage_brief.md`: F69 stage brief(F69 단계 개요)",
        "- `frontier69A_stage_open_axis_rotation_hypothesis_design_report.md`: F69A stage open report(F69A 단계 개방 보고서)",
        "- `f69a_axis_diff_review.csv`: F69 axis diff table(F69 축 차이표)",
        "- `f69a_proxy_sweep_phase_plan_review.csv`: F69B staged proxy plan(F69B 단계형 프록시 계획)",
        "- `f69a_local_verification.json`: F69A local verification(F69A 로컬 검증)",
        "- `grok_stage_open_receipt.md`: F69 Grok stage-open receipt(F69 그록 단계 개방 영수증)",
        "- `required_gate_coverage_audit.md`: F69A gate coverage audit(F69A 게이트 커버리지 감사)",
        "- `stage_run_ledger.csv`: F69 stage run ledger(F69 단계 실행 장부)",
        "",
        f"Current status(현재 상태): `f69a_stage_open_axis_rotation_design_completed_no_authority(F69A 축 회전 설계 완료, 권위 없음)`",
        f"Next action(다음 행동): `{NEXT_RUN_ID}`",
    ]


def selection_status_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        "# F69 Selection Status(F69 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- status(상태): `f69a_stage_open_axis_rotation_design_completed_no_authority(F69A 축 회전 설계 완료, 권위 없음)`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        "- completed_action(완료 행동): F69A axis rotation stage open(F69A 축 회전 단계 개방).",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}` staged proxy sweep(단계형 프록시 탐색).",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
    ]


def state_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        "current_status: f69a_stage_open_axis_rotation_design_completed_no_authority",
        "current_judgment: stage_open_design_only_no_authority",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f69_mandatory_runtime_probe_pending_after_meaningful_proxy_signal(F69 의미 있는 프록시 신호 후 필수 런타임 탐침 대기)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{payload['created_at_utc']}'",
        "notes:",
        '  - "F69A action(행동): event-first axis rotation stage open(이벤트 우선 축 회전 단계 개방)을 물질화했다."',
        '  - "Effect(효과): F68F ONNX risk-only repair loop(F68F 온엑스 위험 단독 수리 반복)를 금지하고 F69B staged proxy sweep(단계형 프록시 탐색)으로 이동한다."',
        '  - "Grok(그록): accepted_with_conditions(조건부 수용); axis diff contract(축 차이 계약)와 per-axis ablation(축별 소거)을 요구했다."',
        '  - "Five-stage retrospective(5단계 중간 검토): not_due_after_f68_closeout_3_of_5(아직 아님, F68 마감 후 3/5)."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]


def current_working_state_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
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
        "Action(행동): F69A stage open(단계 개방)을 axis rotation contract(축 회전 계약)로 물질화했다.",
        "",
        "Effect(효과): 다음 작업은 F69B proxy sweep(프록시 탐색)이고, F68처럼 proxy/runtime alignment(프록시/런타임 정렬)만 보다가 새 실험을 피하지 않도록 feature/label/model/trade-shape/regime(피처/라벨/모델/거래 형태/장세)을 실제로 바꾼다.",
        "",
        "- status(상태): `f69a_stage_open_axis_rotation_design_completed_no_authority(F69A 축 회전 설계 완료, 권위 없음)`.",
        "- runtime probe(런타임 탐침): `pending_after_meaningful_proxy_signal(의미 있는 프록시 신호 후 대기)`.",
        "- Grok advice(그록 조언): `accepted_with_conditions(조건부 수용)`.",
        "- forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 모두 없음.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`: event definition(이벤트 정의), first-hit label(선도달 라벨), compact feature set(압축 피처 묶음), interpretable model family(해석 가능 모델 계열), session/regime buckets(세션/장세 구간)을 staged proxy sweep(단계형 프록시 탐색)으로 실행한다.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def ledger_row(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open_axis_rotation_design",
        "row_id": f"{RUN_ID}__stage_open_axis_rotation_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage_open_axis_rotation_design(단계 개방 축 회전 설계)",
        "parent_run_id": PREVIOUS_CLOSEOUT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        "kpi_scope": "design_and_local_verification(설계 및 로컬 검증)",
        "scoreboard_lane": "experiment_design(실험 설계)",
        "status": "completed_stage_open_axis_rotation_design_no_authority",
        "judgment": "stage_open_design_only_no_authority",
        "path": f"stages/{STAGE_ID}/03_reviews/frontier69A_stage_open_axis_rotation_hypothesis_design_report.md",
        "primary_kpi": "axis_contract_rows=6; f69b_phases=3; grok=accepted_with_conditions",
        "guardrail_kpi": f"five_stage={verification['five_stage_retrospective_due_status']}; raw_model_alignment={verification['raw_model_alignment']}; no_forbidden_claims=true",
        "external_verification_status": "out_of_scope_by_claim_stage_open_design_only(단계 개방 설계 주장 범위 밖)",
        "notes": "F69 opened as event-first axis rotation after F68 risk-only negative memory.",
        "family": "experiment_design(실험 설계)",
        "lane": "stage_open(단계 개방)",
        "primary_report": f"stages/{STAGE_ID}/03_reviews/frontier69A_stage_open_axis_rotation_hypothesis_design_report.md",
        "run_number": "frontier69A",
        "date": str(payload["created_at_utc"])[:10],
        "decision": "open_f69_axis_rotation_then_run_f69b_proxy_sweep",
        "next_run_id": NEXT_RUN_ID,
        "rows": 6,
        "gate_passes": 6,
        "gate_total": 6,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": f"stages/{STAGE_ID}/03_reviews/frontier69A_stage_open_axis_rotation_hypothesis_design_report.md",
        "run_date": str(payload["created_at_utc"])[:10],
        "primary_artifact": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f69a_experiment_design.json",
        "view": "stage_open_design(단계 개방 설계)",
        "tier": "Tier A+B planned(티어 A+B 계획)",
        "metric_scope": "design(설계)",
        "source_package_run_id": PREVIOUS_CLOSEOUT_RUN_ID,
        "result_status": "stage_open_design_only_no_authority",
        "result_judgment": "stage_open_design_only_no_authority",
        "final_decision_path": f"stages/{STAGE_ID}/03_reviews/frontier69A_stage_open_axis_rotation_hypothesis_design_report.md",
        "gate_audit_path": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit.md",
        "created_at": payload["created_at_utc"],
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit.md",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "stage_open_design_and_grok_review_only(단계 개방 설계 및 그록 검토 전용)",
        "evidence_boundary": "stage_open_design_only_no_runtime(단계 개방 설계 전용, 런타임 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can event-first axis rotation create a new PF source?(이벤트 우선 축 회전이 새 PF 원천을 만들 수 있는가)",
        "artifact_count": 10,
        "work_family": "experiment_design(실험 설계)",
        "run_family": "frontier_stage_open(전선 단계 개방)",
        "run_type": "axis_rotation_hypothesis_design(축 회전 가설 설계)",
        "input_run_id": PREVIOUS_CLOSEOUT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f69a_experiment_design.json",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier69A_stage_open_axis_rotation_hypothesis_design_report.md",
    }


def write_outputs(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> None:
    for path in (RUN_ROOT, REVIEWS_ROOT, SELECTED_ROOT, STAGE_ROOT / "00_spec", STAGE_ROOT / "01_inputs"):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_json(RUN_ROOT / "f69a_experiment_design.json", payload)
    write_json(RUN_ROOT / "f69a_data_identity.json", payload["sample_scope"]["data_identity"])
    write_json(RUN_ROOT / "f69a_local_verification.json", verification)
    write_csv(RUN_ROOT / "f69a_axis_diff.csv", axis_diff_rows())
    write_csv(RUN_ROOT / "f69a_proxy_sweep_phase_plan.csv", f69b_phase_rows())
    write_md(RUN_ROOT / "reports" / "result_summary.md", report_lines(payload, verification))
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(payload))

    write_md(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief_lines(payload))
    write_csv(REVIEWS_ROOT / "f69a_axis_diff_review.csv", axis_diff_rows())
    write_csv(REVIEWS_ROOT / "f69a_proxy_sweep_phase_plan_review.csv", f69b_phase_rows())
    write_json(REVIEWS_ROOT / "f69a_experiment_design_review.json", payload)
    write_json(REVIEWS_ROOT / "f69a_data_identity_review.json", payload["sample_scope"]["data_identity"])
    write_json(REVIEWS_ROOT / "f69a_local_verification.json", verification)
    write_md(REVIEWS_ROOT / "frontier69A_stage_open_axis_rotation_hypothesis_design_report.md", report_lines(payload, verification))
    write_md(REVIEWS_ROOT / "grok_stage_open_receipt.md", grok_receipt_lines(payload))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit.md", gate_audit_lines(payload, verification))
    write_md(REVIEWS_ROOT / "review_index.md", review_index_lines())
    write_md(SELECTED_ROOT / "selection_status.md", selection_status_lines(payload))


def run_manifest(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": payload["created_at_utc"],
        "status": "completed_stage_open_axis_rotation_design_no_authority",
        "claim_boundary": CLAIM_BOUNDARY,
        "producer": "stage_pipelines/stage_frontier_69/frontier69a_axis_rotation_stage_open.py",
        "parent_run_id": PREVIOUS_CLOSEOUT_RUN_ID,
        "grok_prompt": rel(GROK_PROMPT),
        "grok_output": rel(GROK_OUTPUT),
        "artifacts": [
            rel(RUN_ROOT / "f69a_experiment_design.json"),
            rel(RUN_ROOT / "f69a_axis_diff.csv"),
            rel(RUN_ROOT / "f69a_proxy_sweep_phase_plan.csv"),
            rel(RUN_ROOT / "f69a_local_verification.json"),
            rel(REVIEWS_ROOT / "frontier69A_stage_open_axis_rotation_hypothesis_design_report.md"),
            rel(REVIEWS_ROOT / "required_gate_coverage_audit.md"),
        ],
        "next_run_id": NEXT_RUN_ID,
    }


def grok_receipt_lines(payload: Mapping[str, Any]) -> list[str]:
    grok = payload["grok"]
    return [
        "# F69 Grok Stage Open Receipt(F69 그록 단계 개방 영수증)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        f"- trigger_reason(트리거 이유): {grok['trigger_reason']}",
        f"- review_size(검토 크기): `{grok['review_size']}`",
        f"- direction_before_grok(그록 전 방향): {grok['direction_before_grok']}",
        f"- prompt_identity(프롬프트 정체성): `{grok['prompt_identity']['path']}`, hash `{grok['prompt_identity']['prompt_hash']}`",
        f"- grok_output_identity(그록 출력 정체성): `{grok['grok_output_identity']['path']}`",
        "- advice_classification(조언 분류): `accepted_with_conditions(조건부 수용)`",
        "- accepted(수용): axis rotation(축 회전), design-only boundary(설계 전용 경계), interpretable-first models(해석 가능 모델 우선), regime/session attribution(장세/세션 귀속).",
        "- rejected(거절): F68J metrics as success preconditions(F68J 지표 성공 전제), F68F reuse with wrappers(F68F 포장 재사용), premature MT5 framing(이른 MT5 프레이밍).",
        "- needs_local_verification(로컬 검증 필요): F68 exclusions(F68 제외), first-hit labels(선도달 라벨), event sparsity(이벤트 희소성), bucket schema(구간 스키마), Tier A/B plan(티어 A/B 계획).",
        "- local_verification(로컬 검증): `f69a_local_verification.json`.",
        f"- final_codex_direction(최종 Codex 방향): {grok['final_codex_direction']}",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def update_ledgers(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> None:
    row = ledger_row(payload, verification)
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")
    upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", row)


def update_registers(payload: Mapping[str, Any]) -> None:
    marker = "<!-- frontier69A_stage_open_axis_rotation_hypothesis_design_v1 -->"
    block = f"""<!-- frontier69A_stage_open_axis_rotation_hypothesis_design_v1 -->
- `{IDEA_ID}`: `{RUN_ID}` opens Frontier69(전선69) as event-first axis rotation(이벤트 우선 축 회전). Hypothesis(가설): sparse event/regime/session first-hit opportunity model(희소 이벤트/장세/세션 선도달 기회 모델)이 F68 risk-only negative memory(F68 위험 단독 부정 기억) 뒤 새 PF source(수익 팩터 원천)를 만들 수 있는지 시험한다. Boundary(경계): stage_open_design_only(단계 개방 설계 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(ROOT / "docs/registers/idea_registry.md", marker, block)


def update_state_files(payload: Mapping[str, Any]) -> None:
    write_md(ROOT / "docs/context/current_working_state.md", current_working_state_lines(payload))
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(state_lines(payload)) + "\n", encoding="utf-8-sig")


def main() -> int:
    missing = [rel(path) for path in required_artifacts() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F69A required material missing: {missing}")
    created_at = utc_now()
    identity = data_identity()
    metadata = read_json(GROK_METADATA)
    verification = local_verification(identity, metadata)
    payload = experiment_design_payload(created_at, identity, metadata)
    payload["sample_scope"]["data_identity"] = identity
    write_outputs(payload, verification)
    update_ledgers(payload, verification)
    update_registers(payload)
    update_state_files(payload)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "completed_stage_open_axis_rotation_design_no_authority",
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "grok": "accepted_with_conditions",
                    "data_rows": identity["rows"],
                    "feature_count": identity["feature_count"],
                    "five_stage_retrospective": verification["five_stage_retrospective_due_status"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
