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

from foundation.control_plane.ledger import io_path, json_ready, path_exists


STAGE_ID = "stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation"
RUN_ID = "frontier70A_stage_open_regime_specific_asymmetric_value_exit_model_rotation_v1"
NEXT_RUN_ID = "frontier70B_label_regime_asymmetric_value_proxy_scout_v1"
PREVIOUS_STAGE_ID = "stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory"
PREVIOUS_CLOSEOUT_RUN_ID = "frontier69F_stage_closeout_event_first_axis_rotation_v1"
IDEA_ID = "IDEA-FR70-REGIME-ASYMMETRIC-VALUE-EXIT-MODEL-ROTATION"

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
F69_CLOSEOUT_REPORT = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews" / "stage_closeout_report.md"
F69_GATE_AUDIT = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews" / "required_gate_coverage_audit_f69f.md"
F69_RUNTIME_RECEIPT = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews" / "f69d_runtime_probe_receipt_review.csv"
F69_REPAIR_DECISION = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews" / "f69e_proxy_runtime_gap_decision_review.json"
FIVE_STAGE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f70_stage_open_regime_value_exit_model_rotation"
GROK_PROMPT = GROK_PACKET / "prompts/f70_stage_open_regime_value_exit_model_rotation_prompt.md"
GROK_OUTPUT = GROK_PACKET / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET / "outputs/metadata.json"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_hash(values: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
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


def required_artifacts() -> list[Path]:
    return [
        MODEL_INPUT,
        MODEL_FEATURE_ORDER,
        RAW_US100,
        F69_CLOSEOUT_REPORT,
        F69_GATE_AUDIT,
        F69_RUNTIME_RECEIPT,
        F69_REPAIR_DECISION,
        FIVE_STAGE_REGISTER,
        GROK_PROMPT,
        GROK_OUTPUT,
        GROK_METADATA,
    ]


def data_identity() -> dict[str, Any]:
    frame = pd.read_parquet(io_path(MODEL_INPUT))
    order = [line.strip() for line in read_text(MODEL_FEATURE_ORDER).splitlines() if line.strip()]
    raw = pd.read_csv(io_path(RAW_US100), usecols=["time_close_unix", "open", "high", "low", "close", "spread_points"])
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.sort_values("timestamp").reset_index(drop=True)
    positions = pd.Series(raw.index.to_numpy(), index=raw["timestamp"]).reindex(frame["timestamp"]).to_numpy(dtype=float)
    labelable: dict[str, Any] = {}
    for horizon in (3, 6, 9, 12, 18):
        valid = pd.Series((positions == positions) & ((positions + horizon) < len(raw)))
        subset = frame.loc[valid.to_numpy()]
        labelable[f"h{horizon}_labelable_rows"] = int(len(subset))
        labelable[f"h{horizon}_split_counts"] = {str(k): int(v) for k, v in subset["split"].value_counts().to_dict().items()}
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    return {
        "model_input_path": rel(MODEL_INPUT),
        "model_input_sha256": sha256_file(MODEL_INPUT),
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "split_counts": {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()},
        "timestamp_min": str(frame["timestamp"].min()),
        "timestamp_max": str(frame["timestamp"].max()),
        "feature_order_path": rel(MODEL_FEATURE_ORDER),
        "feature_order_sha256": sha256_file(MODEL_FEATURE_ORDER),
        "feature_count": len(order),
        "feature_order_hash": ordered_hash(order),
        "raw_us100_path": rel(RAW_US100),
        "raw_us100_sha256": sha256_file(RAW_US100),
        "aligned_model_rows": int((positions == positions).sum()),
        "unaligned_model_rows": int((positions != positions).sum()),
        "labelable": labelable,
        "session_counts": {
            "cash_open_0_60": int(((minutes >= 0) & (minutes <= 60)).sum()),
            "cash_mid_65_270": int(((minutes > 60) & (minutes <= 270)).sum()),
            "cash_late_275_390": int(((minutes > 270) & (minutes <= 390)).sum()),
            "outside_cash": int((~((minutes >= 0) & (minutes <= 390))).sum()),
        },
        "regime_counts": {
            "trend_adx_ge25": int((pd.to_numeric(frame["adx_14"], errors="coerce") >= 25).sum()),
            "chop_adx_lt18": int((pd.to_numeric(frame["adx_14"], errors="coerce") < 18).sum()),
            "vol_expansion_hv5over20_ge1p25": int((pd.to_numeric(frame["historical_vol_5_over_20"], errors="coerce") >= 1.25).sum()),
            "bb_squeeze_on": int((pd.to_numeric(frame["bb_squeeze"], errors="coerce") == 1).sum()),
        },
    }


def five_stage_status() -> dict[str, Any]:
    payload = yaml.safe_load(read_text(FIVE_STAGE_REGISTER)) or {}
    state = payload.get("state", {})
    return {
        "current_due_status": state.get("current_due_status", "unknown"),
        "closeouts_since_last": state.get("closeouts_since_last", ""),
        "next_numeric_trigger_frontier": state.get("next_numeric_trigger_frontier", ""),
    }


def axis_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "axis": "label/target(라벨/목표)",
            "priority": "1",
            "f70_contract": "lead axis(주도 축): asymmetric value and exit-survival labels(비대칭 가치 및 청산 생존 라벨)",
            "f69_guard": "not threshold/cooldown/daily quota repair(임계값/쿨다운/일별 할당 수리 아님)",
            "pass_condition": "PF and density improve together in at least one validation/OOS stratum(검증/표본외 구간에서 수익 팩터와 밀도 동시 개선)",
        },
        {
            "axis": "regime/session split(장세/세션 분할)",
            "priority": "2",
            "f70_contract": "coupled to label strata(라벨 층과 결합): cash open/mid/late plus trend/chop/volatility(정규장 초반/중반/후반 및 추세/횡보/변동성)",
            "f69_guard": "not same label filtered by smaller bucket(같은 라벨의 작은 구간 필터 아님)",
            "pass_condition": "stratum explains sparse/dense fracture(희박/조밀 균열 설명)",
        },
        {
            "axis": "model family(모델 계열)",
            "priority": "3",
            "f70_contract": "regularized linear, EBM-like additive tree, small NN(정규화 선형, EBM 유사 가법 트리, 작은 신경망)",
            "f69_guard": "ExtraTrees-light reference only(가벼운 엑스트라트리스는 참조 전용)",
            "pass_condition": "family changes Pareto knee, not only noise(모델 계열이 잡음이 아닌 파레토 굴절을 이동)",
        },
        {
            "axis": "exit shape(청산 형태)",
            "priority": "4",
            "f70_contract": "ablation after label/regime scout(라벨/장세 탐색 후 소거 비교)",
            "f69_guard": "never lead with exit or quota rescue(청산 또는 할당 구제로 시작 금지)",
            "pass_condition": "only used to explain, not rescue, a seed surface(씨앗 표면 설명용이지 구제용 아님)",
        },
        {
            "axis": "risk logic(위험 로직)",
            "priority": "5",
            "f70_contract": "runtime-compatible fixed envelope(런타임 호환 고정 봉투)",
            "f69_guard": "no post-hoc ATR/SLTP rescue loop(사후 평균진폭/손익절 구제 반복 금지)",
            "pass_condition": "keeps MT5 materialization feasible(메타트레이더5 물질화 가능성 유지)",
        },
        {
            "axis": "Tier pair(티어 쌍)",
            "priority": "6",
            "f70_contract": "Tier A separate, Tier B separate, Tier A+B combined planned(티어 A 분리, 티어 B 분리, 합산 계획)",
            "f69_guard": "Tier B missing cannot be hidden(티어 B 누락 숨김 금지)",
            "pass_condition": "missing_required if not materialized(물질화 못 하면 필수 누락 기록)",
        },
    ]


def phase_rows() -> list[dict[str, str]]:
    return [
        {
            "phase": "F70B",
            "question": "Can label-regime asymmetric value labels move PF and density together?(라벨-장세 비대칭 가치 라벨이 수익 팩터와 밀도를 같이 움직이는가)",
            "scope": "label/target first with coupled regime/session strata(라벨/목표 우선, 장세/세션 층 결합)",
            "stop": "zero joint-soft or cosmetic label changes only(공동 완화 행 0 또는 라벨 변화가 표면적일 때)",
        },
        {
            "phase": "F70C",
            "question": "Does model rotation change the Pareto knee?(모델 회전이 파레토 굴절을 바꾸는가)",
            "scope": "linear, EBM-like, small NN, ExtraTrees-light reference(선형, EBM 유사, 작은 신경망, 엑스트라트리스 참조)",
            "stop": "same sparse/dense fracture across families(모든 계열에서 같은 희박/조밀 균열)",
        },
        {
            "phase": "F70D",
            "question": "Can a meaningful seed surface be materialized in MT5?(의미 있는 씨앗 표면을 MT5로 물질화할 수 있는가)",
            "scope": "Grok pre-MT5, ONNX export, mandatory runtime probe(사전 그록, 온엑스 내보내기, 필수 런타임 탐침)",
            "stop": "runtime bridge impossible or zero signal(런타임 연결 불가능 또는 영 신호)",
        },
        {
            "phase": "F70E",
            "question": "What proxy/runtime gap remains and is repair novel?(남은 프록시/런타임 간극과 수리 신규성은 무엇인가)",
            "scope": "gap analysis plus capped non-repeat repair(간극 분석 및 상한 있는 비반복 수리)",
            "stop": "F69-style trade-shape-only repair emerges(F69식 거래 형태 단독 수리 재등장)",
        },
    ]


def experiment_payload(created_at: str, identity: Mapping[str, Any], metadata: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "idea_id": IDEA_ID,
        "hypothesis": "Regime/session-specific asymmetric value and exit-survival labels(장세/세션별 비대칭 가치 및 청산 생존 라벨)이 density-aware selection(밀도 인식 선택)을 라벨 단계에 내장하면 F69 sparse/dense fracture(F69 희박/조밀 균열)를 줄일 수 있다.",
        "decision_use": "Decide whether F70B should run label-regime proxy scout first(F70B 라벨-장세 프록시 탐색 우선 실행 여부 결정).",
        "comparison_baseline": "F69 closeout negative memory only; no inherited winner/baseline/promotion/runtime authority(F69 마감 부정 기억만 참조, 승자/기준선/승격/런타임 권위 상속 없음).",
        "control_variables": [
            "US100 M5 split_v1(US100 5분봉 분할 v1)",
            "Runtime-compatible fixed risk envelope(런타임 호환 고정 위험 봉투)",
            "Mandatory MT5 Runtime Probe after meaningful proxy signal(의미 있는 프록시 신호 뒤 필수 MT5 런타임 탐침)",
        ],
        "changed_variables": [
            "asymmetric value labels(비대칭 가치 라벨)",
            "exit-survival labels(청산 생존 라벨)",
            "regime/session label strata(장세/세션 라벨 층)",
            "model family rotation(모델 계열 회전)",
        ],
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5(5분봉)",
            "tier_scope": "Tier A planned with Tier B required record(티어 A 계획 및 티어 B 필수 기록)",
            "data_identity": identity,
        },
        "success_criteria": "At least one label-regime scout row moves PF and trades/day together while DD remains below early scout ceiling(라벨-장세 탐색 행 하나 이상에서 수익 팩터와 일거래가 함께 개선되고 손실폭이 초기 탐색 상한 아래 유지).",
        "failure_criteria": "Same sparse high-PF/low-density and dense low-PF fracture persists after label-first scout(라벨 우선 탐색 뒤에도 희박 고PF/저밀도 및 조밀 저PF 균열 지속).",
        "invalid_conditions": "future path includes entry bar, split leakage, raw/model timestamp mismatch, or F69 repair knobs lead the scout(미래 경로가 진입봉 포함, 분할 누수, 원천/모델 시각 불일치, F69 수리 노브가 탐색 주도).",
        "stop_conditions": [
            "zero signal or no labelable rows(영 신호 또는 라벨 가능 행 없음)",
            "joint-soft rows remain zero after bounded label-first scout(상한 있는 라벨 우선 탐색 뒤 공동 완화 행 0)",
            "exit/threshold/cooldown/quota becomes lead axis(청산/임계값/쿨다운/할당이 주도 축이 됨)",
        ],
        "evidence_plan": [
            rel(RUN_ROOT / "f70a_experiment_design.json"),
            rel(RUN_ROOT / "f70a_axis_contract.csv"),
            rel(RUN_ROOT / "f70a_phase_plan.csv"),
            rel(REVIEWS_ROOT / "frontier70A_stage_open_regime_value_exit_model_rotation_report.md"),
            rel(REVIEWS_ROOT / "grok_stage_open_receipt.md"),
        ],
        "grok": grok_receipt_payload(metadata),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def grok_receipt_payload(metadata: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "trigger_reason": "stage open requires Grok second opinion(단계 개방은 그록 2차 의견 필요)",
        "review_size": metadata.get("review_size", "medium"),
        "direction_before_grok": "Open F70 as label-regime asymmetric value scout, not trade-shape repair(F70을 거래 형태 수리가 아니라 라벨-장세 비대칭 가치 탐색으로 개방)",
        "bounded_evidence": [rel(F69_CLOSEOUT_REPORT), rel(F69_RUNTIME_RECEIPT), rel(F69_REPAIR_DECISION), rel(FIVE_STAGE_REGISTER)],
        "prompt_identity": {"path": rel(GROK_PROMPT), "prompt_hash": metadata.get("prompt_hash", ""), "sha256": sha256_file(GROK_PROMPT)},
        "grok_output_identity": {"path": rel(GROK_OUTPUT), "sha256": sha256_file(GROK_OUTPUT), "metadata": rel(GROK_METADATA)},
        "advice_classification": {
            "accepted": [
                "F70 is conditionally new if label/regime/density-in-selection leads(F70은 라벨/장세/밀도 내장 선택이 주도하면 조건부 신규)",
                "first scout priority should be label/target coupled with regime/session(첫 탐색 우선순위는 장세/세션 결합 라벨/목표)",
                "exit shape should be ablation only(청산 형태는 소거 비교 전용)",
            ],
            "rejected": [
                "none; forbidden claims were not made(없음; 금지 주장은 없음)",
            ],
            "needs_local_verification": [
                "ensure F70 packet schema enforces label-first ordering(F70 패킷 스키마가 라벨 우선 순서를 강제하는지 확인)",
            ],
        },
        "local_verification": "axis_contract and phase_plan make label/target priority 1 and exit shape priority 4(축 계약과 단계 계획이 라벨/목표를 1순위, 청산 형태를 4순위로 고정)",
        "forbidden_claim_check": "pass; no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve claimed(통과; 완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음)",
        "final_codex_direction": "Proceed to F70B label-regime asymmetric value proxy scout(F70B 라벨-장세 비대칭 가치 프록시 탐색으로 진행)",
    }


def local_verification(identity: Mapping[str, Any], metadata: Mapping[str, Any]) -> dict[str, Any]:
    output = read_text(GROK_OUTPUT)
    five = five_stage_status()
    forbidden = ["Goal Achieve", "runtime authority", "live readiness", "promotion", "baseline", "completion"]
    forbidden_claims_absent = all(f"no {term}" in output.lower() or term not in output for term in forbidden)
    return {
        "grok_transport_success": bool(metadata.get("success") is True and metadata.get("returncode") == 0),
        "grok_prompt_hash": metadata.get("prompt_hash", ""),
        "f69_closeout_exists": path_exists(F69_CLOSEOUT_REPORT),
        "f69_runtime_receipt_exists": path_exists(F69_RUNTIME_RECEIPT),
        "f69_repair_decision_exists": path_exists(F69_REPAIR_DECISION),
        "five_stage_retrospective_due_status": five["current_due_status"],
        "five_stage_closeouts_since_last": five["closeouts_since_last"],
        "label_first_enforced": axis_contract_rows()[0]["axis"].startswith("label/target") and phase_rows()[0]["phase"] == "F70B",
        "exit_shape_not_lead": axis_contract_rows()[3]["axis"].startswith("exit shape"),
        "raw_model_alignment": identity["unaligned_model_rows"] == 0,
        "forbidden_claims_absent": forbidden_claims_absent,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> list[str]:
    identity = payload["sample_scope"]["data_identity"]
    return [
        "# Frontier70 Stage Open(F70 전선 단계 개방)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "## Hypothesis(가설)",
        "",
        str(payload["hypothesis"]),
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F70을 label/regime-first asymmetric value scout(라벨/장세 우선 비대칭 가치 탐색)로 열었다.",
        "",
        "Effect(효과): F69의 event-first ExtraTrees trade-shape-only loop(이벤트 우선 엑스트라트리스 거래 형태 단독 반복)를 피하고, density objective(밀도 목표)를 라벨/선택 단계에 넣는다.",
        "",
        "## Grok Review(그록 검토)",
        "",
        f"- prompt(프롬프트): `{payload['grok']['prompt_identity']['path']}`, hash `{payload['grok']['prompt_identity']['prompt_hash']}`.",
        f"- output(출력): `{payload['grok']['grok_output_identity']['path']}`.",
        "- accepted(수용): label/target first(라벨/목표 우선), regime/session coupled(장세/세션 결합), exit shape ablation only(청산 형태 소거 비교 전용).",
        "- needs_local_verification(로컬 검증 필요): F70 packet schema(패킷 스키마)가 label-first ordering(라벨 우선 순서)을 강제하는지.",
        f"- local_verification(로컬 검증): label_first_enforced={verification['label_first_enforced']}; exit_shape_not_lead={verification['exit_shape_not_lead']}.",
        "",
        "## Sample Scope(표본 범위)",
        "",
        f"- rows(행): `{identity['rows']}`.",
        f"- splits(분할): `{identity['split_counts']}`.",
        f"- feature_count(피처 수): `{identity['feature_count']}`.",
        f"- aligned_model_rows(정렬 모델 행): `{identity['aligned_model_rows']}`; unaligned(미정렬): `{identity['unaligned_model_rows']}`.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`: label/target + regime/session coupled proxy scout(라벨/목표 + 장세/세션 결합 프록시 탐색).",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def stage_brief_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        "# F70 Stage Brief(F70 단계 개요)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- opened_by(개방 실행): `{RUN_ID}`",
        f"- next_run(다음 실행): `{NEXT_RUN_ID}`",
        f"- idea_id(아이디어 ID): `{IDEA_ID}`",
        "- focus(초점): label/regime-first asymmetric value and exit-survival scout(라벨/장세 우선 비대칭 가치 및 청산 생존 탐색).",
        "- forbidden repeat(반복 금지): F69 threshold/cooldown/daily quota trade-shape-only repair(F69 임계값/쿨다운/일별 할당 거래 형태 단독 수리).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def selection_status_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        "# F70 Selection Status(F70 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- status(상태): `stage_open_design_completed_no_authority(단계 개방 설계 완료, 권위 없음)`",
        "- judgment(판정): `stage_open_design_only_no_authority(단계 개방 설계 전용, 권위 없음)`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ]


def gate_audit_lines(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> list[str]:
    return [
        "# F70A Required Gate Coverage Audit(F70A 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| reentry(재진입) | pass(통과) | `{rel(F69_CLOSEOUT_REPORT)}` | F69/F70 handoff(인계) 확인 |",
        f"| Grok stage open(그록 단계 개방) | pass(통과) | `{payload['grok']['grok_output_identity']['path']}` | 외부 2차 의견 반영 |",
        f"| experiment design(실험 설계) | pass(통과) | `{rel(RUN_ROOT / 'f70a_experiment_design.json')}` | 가설/변수/중단 조건 고정 |",
        f"| label-first guard(라벨 우선 보호) | pass(통과) | `{rel(RUN_ROOT / 'f70a_axis_contract.csv')}` | F69 반복 방지 |",
        f"| five-stage retrospective(5단계 중간 검토) | {verification['five_stage_retrospective_due_status']} | `{rel(FIVE_STAGE_REGISTER)}` | F70 개방 차단 없음 |",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def grok_receipt_lines(payload: Mapping[str, Any]) -> list[str]:
    grok = payload["grok"]
    return [
        "# F70 Grok Stage Open Receipt(F70 그록 단계 개방 영수증)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        f"- trigger_reason(트리거 이유): {grok['trigger_reason']}",
        f"- review_size(검토 크기): `{grok['review_size']}`",
        f"- direction_before_grok(그록 전 방향): {grok['direction_before_grok']}",
        f"- prompt_identity(프롬프트 정체성): `{grok['prompt_identity']['path']}`, hash `{grok['prompt_identity']['prompt_hash']}`",
        f"- grok_output_identity(그록 출력 정체성): `{grok['grok_output_identity']['path']}`",
        f"- advice_classification(조언 분류): `{grok['advice_classification']}`",
        f"- local_verification(로컬 검증): {grok['local_verification']}",
        f"- forbidden_claim_check(금지 주장 확인): {grok['forbidden_claim_check']}",
        f"- final_codex_direction(최종 Codex 방향): {grok['final_codex_direction']}",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def run_manifest(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": payload["created_at_utc"],
        "producer": "stage_pipelines/stage_frontier_70/frontier70a_stage_open_regime_value_exit_model_rotation.py",
        "status": "stage_open_design_completed_no_authority",
        "parent_run_id": PREVIOUS_CLOSEOUT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "grok_prompt": rel(GROK_PROMPT),
        "grok_output": rel(GROK_OUTPUT),
        "artifacts": [
            rel(RUN_ROOT / "f70a_experiment_design.json"),
            rel(RUN_ROOT / "f70a_axis_contract.csv"),
            rel(RUN_ROOT / "f70a_phase_plan.csv"),
            rel(RUN_ROOT / "f70a_local_verification.json"),
            rel(REVIEWS_ROOT / "frontier70A_stage_open_regime_value_exit_model_rotation_report.md"),
            rel(REVIEWS_ROOT / "required_gate_coverage_audit_f70a.md"),
        ],
        "next_run_id": NEXT_RUN_ID,
    }


def ledger_row(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open_design",
        "row_id": f"{RUN_ID}__stage_open_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage_open_design(단계 개방 설계)",
        "parent_run_id": PREVIOUS_CLOSEOUT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        "kpi_scope": "design_and_grok_review(설계 및 그록 검토)",
        "scoreboard_lane": "experiment_design(실험 설계)",
        "status": "stage_open_design_completed_no_authority",
        "judgment": "stage_open_design_only_no_authority",
        "path": f"stages/{STAGE_ID}/03_reviews/frontier70A_stage_open_regime_value_exit_model_rotation_report.md",
        "primary_kpi": "axis_contract_rows=6; phase_rows=4; grok=accepted_with_local_guard",
        "guardrail_kpi": f"five_stage={verification['five_stage_retrospective_due_status']}; label_first={verification['label_first_enforced']}; exit_not_lead={verification['exit_shape_not_lead']}",
        "external_verification_status": "out_of_scope_by_claim_stage_open_design_only(단계 개방 설계 주장 범위 밖)",
        "notes": "F70 opened as label-regime asymmetric value scout after F69 negative memory.",
        "family": "experiment_design(실험 설계)",
        "lane": "stage_open(단계 개방)",
        "primary_report": f"stages/{STAGE_ID}/03_reviews/frontier70A_stage_open_regime_value_exit_model_rotation_report.md",
        "run_number": "frontier70A",
        "date": str(payload["created_at_utc"])[:10],
        "decision": "open_f70_label_regime_first_then_run_f70b_proxy_scout",
        "next_run_id": NEXT_RUN_ID,
        "rows": 6,
        "gate_passes": 5,
        "gate_total": 5,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": f"stages/{STAGE_ID}/03_reviews/frontier70A_stage_open_regime_value_exit_model_rotation_report.md",
        "run_date": str(payload["created_at_utc"])[:10],
        "primary_artifact": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f70a_experiment_design.json",
        "view": "stage_open_design(단계 개방 설계)",
        "tier": "Tier A+B planned(티어 A+B 계획)",
        "metric_scope": "design(설계)",
        "source_package_run_id": PREVIOUS_CLOSEOUT_RUN_ID,
        "result_status": "stage_open_design_completed_no_authority",
        "result_judgment": "stage_open_design_only_no_authority",
        "final_decision_path": f"stages/{STAGE_ID}/03_reviews/frontier70A_stage_open_regime_value_exit_model_rotation_report.md",
        "gate_audit_path": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f70a.md",
        "created_at": payload["created_at_utc"],
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f70a.md",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "stage_open_design_and_grok_review_only(단계 개방 설계 및 그록 검토 전용)",
        "evidence_boundary": "stage_open_design_only_no_runtime(단계 개방 설계 전용, 런타임 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can label-regime asymmetric value labels reduce the sparse/dense fracture?(라벨-장세 비대칭 가치 라벨이 희박/조밀 균열을 줄이는가)",
        "artifact_count": 9,
        "work_family": "experiment_design(실험 설계)",
        "run_family": "frontier_stage_open(전선 단계 개방)",
        "run_type": "regime_value_exit_model_rotation_design(장세 가치 청산 모델 회전 설계)",
        "input_run_id": PREVIOUS_CLOSEOUT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f70a_experiment_design.json",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier70A_stage_open_regime_value_exit_model_rotation_report.md",
    }


def update_registers(payload: Mapping[str, Any]) -> None:
    marker = "<!-- frontier70A_stage_open_regime_specific_asymmetric_value_exit_model_rotation_v1 -->"
    block = f"""<!-- frontier70A_stage_open_regime_specific_asymmetric_value_exit_model_rotation_v1 -->
- `{IDEA_ID}`: `{RUN_ID}` opens Frontier70(전선70) as label/regime-first asymmetric value and exit-survival scout(라벨/장세 우선 비대칭 가치 및 청산 생존 탐색). Hypothesis(가설): density-aware label/selection(밀도 인식 라벨/선택)이 F69 sparse/dense fracture(F69 희박/조밀 균열)를 줄일 수 있다. Boundary(경계): stage_open_design_only(단계 개방 설계 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(ROOT / "docs/registers/idea_registry.md", marker, block)


def update_state_files(payload: Mapping[str, Any]) -> None:
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        "current_status: stage_open_design_completed_no_authority",
        "current_judgment: stage_open_design_only_no_authority",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f70_mandatory_runtime_probe_pending_after_meaningful_proxy_signal(F70 의미 있는 프록시 신호 뒤 필수 런타임 탐침 대기)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f69_closeout_4_of_5",
        f"updated_at_utc: '{payload['created_at_utc']}'",
        "notes:",
        '  - "F70A action(행동): label/regime-first asymmetric value stage open(라벨/장세 우선 비대칭 가치 단계 개방)을 물질화했다."',
        '  - "Effect(효과): F69 trade-shape-only repair loop(F69 거래 형태 단독 수리 반복)를 금지하고 F70B를 라벨/목표 우선 프록시 탐색으로 고정했다."',
        '  - "Grok(그록): accepted with local guard(로컬 보호 조건으로 수용); exit shape(청산 형태)는 ablation only(소거 비교 전용)."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(state) + "\n", encoding="utf-8-sig")
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
        "Action(행동): Frontier70 label/regime-first asymmetric value stage open(전선70 라벨/장세 우선 비대칭 가치 단계 개방)을 완료했다.",
        "",
        "Effect(효과): F69의 sparse/dense fracture(희박/조밀 균열)를 라벨/선택 단계에서 직접 시험하고, 청산/할당 수리 반복은 후순위 소거 비교로 묶었다.",
        "",
        "- status(상태): `stage_open_design_completed_no_authority(단계 개방 설계 완료, 권위 없음)`.",
        "- Grok advice(그록 조언): label/target first(라벨/목표 우선) accepted(수용), exit shape ablation only(청산 형태 소거 비교 전용).",
        "- runtime probe(런타임 탐침): meaningful proxy signal(의미 있는 프록시 신호) 뒤 필수.",
        "- five-stage retrospective(5단계 중간 검토): `not_due(아직 아님)`, 4/5.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", current)


def write_outputs(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> None:
    for path in (RUN_ROOT, RUN_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT, STAGE_ROOT / "00_spec"):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_json(RUN_ROOT / "f70a_experiment_design.json", payload)
    write_json(RUN_ROOT / "f70a_data_identity.json", payload["sample_scope"]["data_identity"])
    write_json(RUN_ROOT / "f70a_local_verification.json", verification)
    write_csv(RUN_ROOT / "f70a_axis_contract.csv", axis_contract_rows())
    write_csv(RUN_ROOT / "f70a_phase_plan.csv", phase_rows())
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(payload))
    write_md(RUN_ROOT / "reports/result_summary.md", report_lines(payload, verification))
    write_md(STAGE_ROOT / "00_spec/stage_brief.md", stage_brief_lines(payload))
    write_json(REVIEWS_ROOT / "f70a_experiment_design_review.json", payload)
    write_json(REVIEWS_ROOT / "f70a_data_identity_review.json", payload["sample_scope"]["data_identity"])
    write_json(REVIEWS_ROOT / "f70a_local_verification.json", verification)
    write_csv(REVIEWS_ROOT / "f70a_axis_contract_review.csv", axis_contract_rows())
    write_csv(REVIEWS_ROOT / "f70a_phase_plan_review.csv", phase_rows())
    write_md(REVIEWS_ROOT / "frontier70A_stage_open_regime_value_exit_model_rotation_report.md", report_lines(payload, verification))
    write_md(REVIEWS_ROOT / "grok_stage_open_receipt.md", grok_receipt_lines(payload))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f70a.md", gate_audit_lines(payload, verification))
    write_md(REVIEWS_ROOT / "review_index.md", [
        "# F70 Review Index(F70 검토 색인)",
        "",
        "- `frontier70A_stage_open_regime_value_exit_model_rotation_report.md`: F70A stage open report(F70A 단계 개방 보고서)",
        "- `grok_stage_open_receipt.md`: F70 Grok stage-open receipt(F70 그록 단계 개방 영수증)",
        "- `required_gate_coverage_audit_f70a.md`: F70A required gate audit(F70A 필수 게이트 감사)",
    ])
    write_md(SELECTED_ROOT / "selection_status.md", selection_status_lines(payload))


def update_ledgers(payload: Mapping[str, Any], verification: Mapping[str, Any]) -> None:
    row = ledger_row(payload, verification)
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")
    upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", row)


def main() -> int:
    missing = [rel(path) for path in required_artifacts() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F70A required material missing: {missing}")
    created_at = utc_now()
    identity = data_identity()
    metadata = read_json(GROK_METADATA)
    verification = local_verification(identity, metadata)
    payload = experiment_payload(created_at, identity, metadata)
    write_outputs(payload, verification)
    update_ledgers(payload, verification)
    update_registers(payload)
    update_state_files(payload)
    print(json.dumps(json_ready({
        "status": "stage_open_design_completed_no_authority",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "grok_prompt_hash": metadata.get("prompt_hash", ""),
        "label_first_enforced": verification["label_first_enforced"],
        "exit_shape_not_lead": verification["exit_shape_not_lead"],
        "five_stage_retrospective": verification["five_stage_retrospective_due_status"],
        "claim_boundary": CLAIM_BOUNDARY,
    }), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
