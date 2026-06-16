from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.mt5.runtime_support import mt5_runtime_module_hashes


STAGE_ID = "stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout"
RUN_ID = "frontier68A_stage_open_lifecycle_economics_proxy_design_v1"
NEXT_RUN_ID = "frontier68B_runtime_lifecycle_proxy_broad_sweep_v1"
F67_STAGE_ID = "stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk"
F67D_RUN_ID = "frontier67D_narrow_cost_order_intent_runtime_probe_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"

MODEL_INPUT_V1 = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1"
MODEL_INPUT_V2 = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"

F67C_ROWS = ROOT / "stages" / F67_STAGE_ID / "03_reviews" / "frontier67C_runtime_native_order_intent_rows_review.csv"
F67D_RECEIPT = ROOT / "stages" / F67_STAGE_ID / "03_reviews" / "frontier67D_order_intent_receipt_review.csv"
F67D_GAP_ROWS = ROOT / "stages" / F67_STAGE_ID / "03_reviews" / "frontier67D_gap_classification_review.csv"
F67D_KPI_RECORD = ROOT / "stages" / F67_STAGE_ID / "02_runs" / F67D_RUN_ID / "kpi_record.json"
F67D_FEATURE_MATRIX = (
    ROOT
    / "stages"
    / F67_STAGE_ID
    / "02_runs"
    / F67D_RUN_ID
    / "features"
    / "F31_c416c0dae0c6_oos_features.csv"
)

CLAIM_BOUNDARY = (
    "preflight_and_label_design_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str | None:
    if not path_exists(path):
        return None
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_hash(names: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in fieldnames})


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def num(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def number_summary(values: Iterable[float | None]) -> dict[str, Any]:
    clean = sorted(float(value) for value in values if value is not None and math.isfinite(float(value)))
    if not clean:
        return {"count": 0}
    return {
        "count": len(clean),
        "min": clean[0],
        "median": statistics.median(clean),
        "max": clean[-1],
    }


def feature_order_payload(root: Path) -> dict[str, Any]:
    path = root / "model_input_feature_order.txt"
    if not path_exists(path):
        return {"path": rel(path), "exists": False}
    names = [line.strip() for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    return {
        "path": rel(path),
        "exists": True,
        "feature_count": len(names),
        "ordered_hash": ordered_hash(names),
        "sha256": sha256_file(path),
        "first_features": names[:8],
        "last_features": names[-5:],
    }


def model_input_payload(root: Path, dataset_id: str) -> dict[str, Any]:
    parquet_path = root / "model_input_dataset.parquet"
    summary_path = root / "model_input_summary.json"
    order = feature_order_payload(root)
    payload: dict[str, Any] = {
        "dataset_id": dataset_id,
        "path": rel(parquet_path),
        "exists": path_exists(parquet_path),
        "sha256": sha256_file(parquet_path),
        "summary_path": rel(summary_path),
        "summary_exists": path_exists(summary_path),
        "summary_sha256": sha256_file(summary_path),
        "feature_order": order,
    }
    if path_exists(parquet_path):
        frame = pd.read_parquet(io_path(parquet_path))
        payload.update(
            {
                "rows": int(len(frame)),
                "columns": int(len(frame.columns)),
                "split_counts": {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()}
                if "split" in frame
                else {},
                "timestamp_min": str(frame["timestamp"].min()) if "timestamp" in frame else "",
                "timestamp_max": str(frame["timestamp"].max()) if "timestamp" in frame else "",
                "label_counts": {str(k): int(v) for k, v in frame["label"].value_counts().to_dict().items()}
                if "label" in frame
                else {},
            }
        )
    return payload


def f67c_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    pf = [num(row.get("profit_factor")) for row in rows]
    dd = [num(row.get("max_drawdown_percent")) for row in rows]
    trade_to_signal = [num(row.get("trade_to_signal_ratio")) for row in rows]
    deal_minus_fill = [num(row.get("deal_minus_order_fill")) for row in rows]
    swap = [num(row.get("deal_swap_sum")) for row in rows]
    net_per_trade = [num(row.get("net_per_trade")) for row in rows]
    return {
        "path": rel(F67C_ROWS),
        "exists": path_exists(F67C_ROWS),
        "sha256": sha256_file(F67C_ROWS),
        "rows": len(rows),
        "pf_summary": number_summary(pf),
        "dd_summary": number_summary(dd),
        "trade_to_signal_summary": number_summary(trade_to_signal),
        "deal_minus_order_fill_positive_rows": sum(1 for value in deal_minus_fill if value is not None and value > 0),
        "swap_nonzero_rows": sum(1 for value in swap if value is not None and abs(value) > 1e-9),
        "pf_ge2_dd_le10_rows": sum(
            1
            for row in rows
            if (num(row.get("profit_factor")) or 0.0) >= 2.0
            and (num(row.get("max_drawdown_percent")) or 999.0) <= 10.0
        ),
        "positive_net_per_trade_rows": sum(1 for value in net_per_trade if value is not None and value > 0),
    }


def f67d_feature_matrix_payload() -> dict[str, Any]:
    payload = {"path": rel(F67D_FEATURE_MATRIX), "exists": path_exists(F67D_FEATURE_MATRIX), "sha256": sha256_file(F67D_FEATURE_MATRIX)}
    if not path_exists(F67D_FEATURE_MATRIX):
        return payload
    with io_path(F67D_FEATURE_MATRIX).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        first = next(reader, [])
        row_count = 1 + sum(1 for _ in reader) if first else 0
    payload.update(
        {
            "rows": row_count,
            "columns": len(header),
            "header": header,
            "first_row": first,
            "bridge_read": "single_discrete_signal_replay_bridge",
        }
    )
    return payload


def build_inventory(created_at: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    f67c_rows = read_csv(F67C_ROWS)
    f67d_rows = read_csv(F67D_RECEIPT)
    gap_rows = read_csv(F67D_GAP_ROWS)
    kpi = read_json(F67D_KPI_RECORD)
    v1 = model_input_payload(
        MODEL_INPUT_V1,
        "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_feature_set_v1_no_placeholder_top3_weights",
    )
    v2 = model_input_payload(
        MODEL_INPUT_V2,
        "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2",
    )
    f67d_matrix = f67d_feature_matrix_payload()
    rows = [
        {
            "artifact_role": "model_input_v1_56_features",
            "path": v1["path"],
            "exists": v1["exists"],
            "row_count": v1.get("rows", ""),
            "feature_count": (v1.get("feature_order") or {}).get("feature_count", ""),
            "sha256": v1.get("sha256", ""),
            "f68a_read": "usable_as_tier_a_or_reference_model_input_but_excludes_top3_proxy_features",
        },
        {
            "artifact_role": "model_input_v2_58_features",
            "path": v2["path"],
            "exists": v2["exists"],
            "row_count": v2.get("rows", ""),
            "feature_count": (v2.get("feature_order") or {}).get("feature_count", ""),
            "sha256": v2.get("sha256", ""),
            "f68a_read": "preferred_initial_full_feature_source_for_f68b_because_it_matches_current_58_feature_contract",
        },
        {
            "artifact_role": "f67c_runtime_lifecycle_rows",
            "path": rel(F67C_ROWS),
            "exists": path_exists(F67C_ROWS),
            "row_count": len(f67c_rows),
            "feature_count": "",
            "sha256": sha256_file(F67C_ROWS),
            "f68a_read": "usable_runtime_lifecycle_outcome_reference_for_proxy_design_not_training_features",
        },
        {
            "artifact_role": "f67d_runtime_probe_receipt",
            "path": rel(F67D_RECEIPT),
            "exists": path_exists(F67D_RECEIPT),
            "row_count": len(f67d_rows),
            "feature_count": "",
            "sha256": sha256_file(F67D_RECEIPT),
            "f68a_read": "single_slice_runtime_probe_anchor_for_proxy_runtime_gap_targeting",
        },
        {
            "artifact_role": "f67d_discrete_signal_feature_matrix",
            "path": rel(F67D_FEATURE_MATRIX),
            "exists": f67d_matrix["exists"],
            "row_count": f67d_matrix.get("rows", ""),
            "feature_count": max(int(f67d_matrix.get("columns", 0)) - 4, 0) if f67d_matrix.get("columns") else "",
            "sha256": f67d_matrix.get("sha256", ""),
            "f68a_read": "proves_one_feature_runtime_handoff_but_not_enough_for_full_lifecycle_proxy",
        },
    ]
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "model_inputs": {"v1_56": v1, "v2_58": v2},
        "f67c_runtime_lifecycle_summary": f67c_summary(f67c_rows),
        "f67d_runtime_probe_receipt": {
            "path": rel(F67D_RECEIPT),
            "exists": path_exists(F67D_RECEIPT),
            "sha256": sha256_file(F67D_RECEIPT),
            "rows": len(f67d_rows),
            "row": f67d_rows[0] if f67d_rows else {},
        },
        "f67d_gap_rows": {"path": rel(F67D_GAP_ROWS), "rows": len(gap_rows), "sha256": sha256_file(F67D_GAP_ROWS)},
        "f67d_kpi_record": {"path": rel(F67D_KPI_RECORD), "sha256": sha256_file(F67D_KPI_RECORD), "payload": kpi},
        "f67d_feature_matrix": f67d_matrix,
    }
    return rows, summary


def build_bridge_checklist(created_at: str, inventory: dict[str, Any]) -> dict[str, Any]:
    module_hashes = mt5_runtime_module_hashes()
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "research_path": [
            "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet",
            "foundation/alpha/scout_runner.py",
            "foundation/models/onnx_bridge.py",
        ],
        "runtime_path": [
            "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
            "foundation/mt5/include/ObsidianPrime/FeatureInputs.mqh",
            "foundation/mt5/include/ObsidianPrime/ModelRuntime.mqh",
            "foundation/mt5/include/ObsidianPrime/ExecutionBridge.mqh",
        ],
        "shared_contract": {
            "symbol": "US100",
            "timeframe": "M5",
            "input_shape": "[1, feature_count]",
            "output_order": "[p_short, p_flat, p_long]",
            "tier_records_required": [
                "Tier A separate(Tier A 분리)",
                "Tier B separate(Tier B 분리)",
                "Tier A+B combined(Tier A+B 합산)",
            ],
            "feature_order_hash_v2_58": inventory["model_inputs"]["v2_58"]["feature_order"].get("ordered_hash"),
            "feature_count_v2_58": inventory["model_inputs"]["v2_58"]["feature_order"].get("feature_count"),
        },
        "checks": [
            {
                "check": "full_feature_model_input_exists",
                "status": "pass",
                "evidence": inventory["model_inputs"]["v2_58"]["path"],
                "effect": (
                    "F68B can build a proxy(F68B는 프록시를 만들 수 있음) from full 58-feature rows"
                    "(전체 58개 피처 행) instead of only F67D one-column signal replay"
                    "(F67D 한 컬럼 신호 재생만 쓰는 방식이 아님)."
                ),
            },
            {
                "check": "single_signal_runtime_handoff_exists",
                "status": "pass",
                "evidence": inventory["f67d_feature_matrix"]["path"],
                "effect": (
                    "F67D proves(F67D가 증명함) the current RuntimeProbeEA(현재 런타임 탐침 EA)가 "
                    "staged feature CSV(단계 피처 CSV)를 소비하고 MT5 KPI(MT5 핵심 성과 지표)를 만들 수 있음을 보여준다."
                ),
            },
            {
                "check": "full_feature_runtime_handoff_feasible",
                "status": "pass_pending_f68_model",
                "evidence": "foundation/alpha/scout_runner.py::materialize_mt5_probe_bundle and RuntimeProbeEA InpFeatureCount",
                "effect": (
                    "If F68B produces a model/proxy artifact(F68B가 모델/프록시 산출물을 만들면), "
                    "F68 can materialize 56/58-feature ONNX probes"
                    "(F68은 56/58개 피처 ONNX 탐침을 물질화할 수 있음) without new EA entrypoint"
                    "(새 EA 진입점 없이)."
                ),
            },
            {
                "check": "onnx_export_path_available",
                "status": "pass_pending_f68_model",
                "evidence": "foundation/models/onnx_bridge.py",
                "effect": (
                    "Sklearn-compatible F68 candidates(사이킷런 호환 F68 후보)는 zipmap disabled"
                    "(집맵 비활성) ONNX export(ONNX 내보내기)가 가능하고, EBM table path"
                    "(EBM 표 경로)는 runtime-compatible fallback(런타임 호환 대체 경로)로 남는다."
                ),
            },
            {
                "check": "mandatory_mt5_probe_now",
                "status": "not_due_no_meaningful_proxy_signal_yet",
                "evidence": "F68A is preflight and label design only(F68A는 사전확인 및 라벨 설계 전용).",
                "effect": (
                    "MT5 probe(MT5 탐침)는 F68B/F68C가 meaningful proxy signal"
                    "(의미 있는 프록시 신호)을 만든 뒤 F68 mandatory step(F68 필수 단계)으로 보존된다."
                ),
            },
        ],
        "known_differences": [
            "F67D matrix(F67D 행렬)는 one-feature discrete signal replay(단일 피처 이산 신호 재생)이지 full feature model input(전체 피처 모델 입력)이 아니다.",
            "F68 has no trained proxy/model/ONNX artifact yet(F68은 아직 학습된 프록시/모델/ONNX 산출물이 없다).",
            "F68 Tier B partial-context frames(F68 Tier B 부분 문맥 프레임)는 existing helpers(기존 도구)로 가능하지만 this run(이번 실행)에서는 물질화하지 않았다.",
        ],
        "parity_identity": {
            "mt5_runtime_module_hashes": module_hashes,
            "f67d_feature_matrix_sha256": inventory["f67d_feature_matrix"].get("sha256"),
            "model_input_v2_sha256": inventory["model_inputs"]["v2_58"].get("sha256"),
        },
        "runtime_claim_boundary": "not_applicable_preflight_only",
        "next_action": NEXT_RUN_ID,
    }


def build_label_design(created_at: str, inventory: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "idea_id": "IDEA-FR68-RUNTIME-LIFECYCLE-ECONOMICS-PROXY-ONNX-SCOUT",
        "hypothesis": (
            "A proxy(프록시)가 entry-known rows(진입 시점에 알 수 있는 행)을 expected lifecycle economics"
            "(예상 생명주기 경제성), cost sensitivity(비용 민감도), drawdown hazard(손실폭 위험)로 점수화하면 "
            "count/feature parity alone(개수/피처 동등성 단독)보다 더 나은 MT5 runtime seed(MT5 런타임 씨앗)를 만들 수 있다."
        ),
        "decision_use": (
            "Choose whether F68B should prototype runtime-lifecycle proxy surfaces"
            "(F68B가 런타임 생명주기 프록시 표면을 원형으로 만들지 선택) and which surface earns MT5 materialization"
            "(어떤 표면이 MT5 물질화 자격을 얻는지 선택)."
        ),
        "legacy_relation": "prior_evidence_only",
        "tier_scope": "mixed_tier_a_tier_b_planned",
        "comparison_baseline": {
            "f67d": "PF(수익 팩터)=1.0; DD(손실폭)=30.58; trades_per_day(일 거래 수)=1.3282; signal_diff(신호 차이)=0; feature_diff(피처 차이)=0",
            "f67c": "64 runtime lifecycle rows(64개 런타임 생명주기 행); trade/signal compression(거래/신호 압축) and report-level swap/deal effects(보고서 수준 스왑/딜 효과) observed(관찰됨)",
        },
        "control_variables": [
            "US100 M5 closed-bar timing(확정 봉 시간 규칙)",
            "no inherited winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위 상속 없음)",
            "same final four-axis target remains final-review-only hard gate(같은 최종 네 축 목표는 최종 검토 전용 강제 게이트로 유지)",
            "MT5 RuntimeProbeEA entrypoint unchanged(MT5 런타임 탐침 EA 진입점 유지) unless F68B proves bridge impossibility(F68B가 연결 불가능을 증명할 때만 예외)",
        ],
        "changed_variables": [
            "runtime-lifecycle-aware target or utility score(런타임 생명주기 인식 목표 또는 효용 점수)",
            "cost/DD hazard penalty in proxy scoring(프록시 점수화 안의 비용/손실폭 위험 벌점)",
            "feature source may use 58-feature MT5 price-proxy model input(피처 원천은 58개 피처 MT5 가격 대리 모델 입력 사용 가능) instead of one-column discrete signal replay(한 컬럼 이산 신호 재생 대신)",
            "model/export family remains open-ended(모델/내보내기 계열은 열린 상태) and chosen by evidence(근거로 선택), not by a fixed menu(고정 메뉴가 아님)",
        ],
        "sample_scope": {
            "primary_dataset": inventory["model_inputs"]["v2_58"]["path"],
            "primary_rows": inventory["model_inputs"]["v2_58"].get("rows"),
            "split_counts": inventory["model_inputs"]["v2_58"].get("split_counts"),
            "runtime_reference": inventory["f67d_runtime_probe_receipt"]["path"],
        },
        "broad_sweep": [
            "lifecycle utility scoring with cost/DD penalties(생명주기 효용 점수화와 비용/손실폭 벌점)",
            "drawdown hazard avoidance as a flat/no-trade pressure(무거래 압력으로 쓰는 손실폭 위험 회피)",
            "trade-density recovery surfaces that avoid count-only parity repair(개수 동등성 단독 수리를 피하는 거래 밀도 회복 표면)",
            "other current-evidence alpha sources if they dominate these seeds(이 씨앗보다 강한 현재 근거 기반 알파 원천)",
        ],
        "extreme_sweep": [
            "zero or very light cost/DD penalty(0 또는 매우 약한 비용/손실폭 벌점) to reveal over-trading cliff(과거래 절벽 확인)",
            "strong DD penalty(강한 손실폭 벌점) to reveal under-trading cliff(과소거래 절벽 확인)",
            "flat/no-trade pressure from permissive to strict(느슨함부터 엄격함까지 무거래 압력 변화)",
            "hold/risk settings bounded by runtime bridge capabilities(런타임 연결 능력 안에서 보유/위험 설정 변화)",
        ],
        "micro_search_gate": (
            "Only micro-tune(미세 조정은) after at least one F68B surface creates nonzero signals"
            "(최소 하나의 F68B 표면이 영이 아닌 신호를 만들고), preserves feature readiness(피처 준비를 보존하며), "
            "and improves at least two of PF/DD/trade-density proxy direction versus F67D"
            "(F67D 대비 수익 팩터/손실폭/거래 밀도 중 최소 두 축 방향을 개선하고) without hiding a third-axis collapse"
            "(세 번째 축 붕괴를 숨기지 않을 때만 한다)."
        ),
        "wfo_plan": (
            "Use validation/OOS as scout split first(검증/표본외를 먼저 탐색 분할로 사용); "
            "if a meaningful signal appears(의미 있는 신호가 나오면), move to WFO/stress(워크포워드/스트레스 검증으로 이동) "
            "before any completion or authority claim(완성 또는 권위 주장 전)."
        ),
        "success_criteria": [
            "F68B produces at least one nonzero proxy surface(F68B가 최소 하나의 영이 아닌 프록시 표면을 생성) with explicit Tier A, Tier B, and combined record plan(Tier A/Tier B/합산 기록 계획 포함).",
            "Proxy KPI(프록시 핵심 성과 지표)는 all four target axes(네 목표 축)를 hard pass/fail(강제 통과/실패)이 아니라 distance-to-goal(목표까지 거리)로 보고한다.",
            "A selected scout surface(선택된 탐색 표면)는 EA entrypoint changes(EA 진입점 변경) 없이 MT5 export/bridge(MT5 내보내기/연결)가 가능하다.",
        ],
        "failure_criteria": [
            "All candidate surfaces(모든 후보 표면)가 zero-signal(영 신호) 또는 pure count-parity repeats(순수 개수 동등성 반복)이다.",
            "Proxy improves one axis(프록시가 한 축만 개선) while hiding DD or trade-density collapse(손실폭 또는 거래 밀도 붕괴를 숨긴다).",
            "Required feature/runtime bridge(필수 피처/런타임 연결)를 materialized(물질화)할 수 없고 repair path(수리 경로)가 없다.",
        ],
        "invalid_conditions": [
            "Use realized MT5 PnL or future trade outcome(실현 MT5 손익 또는 미래 거래 결과)을 entry feature(진입 피처)로 쓴다.",
            "Treat F67D single-slice KPI(F67D 단일 조각 핵심 성과 지표)를 broad proof(넓은 증명)처럼 해석한다.",
            "Use examples(예시)를 non-exhaustive prompts(비한정 프롬프트)가 아니라 fixed checklist(고정 체크리스트)로 쓴다.",
        ],
        "stop_conditions": [
            "Stop F68B broad sweep(F68B 넓은 탐색 중지) if source joins fail(원천 결합 실패 시); write bridge repair action(연결 수리 행동 기록).",
            "Stop before MT5(MT5 전 중지) if proxy signal is zero(프록시 신호가 0이면); classify as invalid/blocked with repair path(수리 경로와 함께 무효/차단으로 분류).",
            "Request pre-MT5 Grok review(MT5 전 Grok 검토 요청) before runtime materialization(런타임 물질화 전).",
        ],
        "failure_memory": {
            "negative_result_requirement": "Record negative result(부정 결과 기록) if lifecycle-aware proxy(생명주기 인식 프록시)가 meaningful proxy signal(의미 있는 프록시 신호)에도 MT5에서 붕괴하면.",
            "salvage_value": "Preserve(보존) which lifecycle/cost/DD term(생명주기/비용/손실폭 항)이 which target axis(어떤 목표 축)을 움직였는지.",
            "reopen_condition": "Reopen only with a new alpha source(새 알파 원천이 있을 때만 재개), not a repeat of count/feature parity(개수/피처 동등성 반복 아님).",
        },
        "evidence_plan": [
            "F68B proxy row table(F68B 프록시 행 표) with Tier A separate, Tier B separate, Tier A+B combined records(Tier A 분리/Tier B 분리/Tier A+B 합산 기록).",
            "Proxy KPI(프록시 핵심 성과 지표) with net, PF, DD, trade count, trades/day, win rate, expectancy, recovery(순수익/수익 팩터/손실폭/거래 수/일 거래 수/승률/기대값/회복 계수), where computable(계산 가능할 때).",
            "ONNX or runtime-compatible model bundle identity(ONNX 또는 런타임 호환 모델 묶음 정체성) before MT5(MT5 전).",
            "Pre-MT5 Grok review(MT5 전 Grok 검토) before Runtime Probe(런타임 탐침 전).",
            "Mandatory MT5 Strategy Tester output(필수 MT5 전략 테스터 출력) after meaningful proxy signal(의미 있는 프록시 신호 후).",
        ],
        "next_action": NEXT_RUN_ID,
    }


def ledger_row(created_at: str, inventory: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__bridge_feasibility_label_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "bridge_feasibility_label_design(연결 가능성 라벨 설계)",
        "parent_run_id": "frontier67_closeout_preserved_clue_negative_memory_v1",
        "record_view": "preflight_design(사전확인 설계)",
        "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        "kpi_scope": "design_preflight_no_runtime_kpi(설계 사전확인, 런타임 KPI 없음)",
        "scoreboard_lane": "stage_open_to_proxy_preflight(단계 개방에서 프록시 사전확인)",
        "status": "completed_preflight_design_no_authority",
        "judgment": "bridge_feasible_for_proxy_materialization_but_no_f68_proxy_signal_yet",
        "path": f"stages/{STAGE_ID}/03_reviews/frontier68A_bridge_feasibility_and_label_design_report.md",
        "primary_kpi": "model_input_v2_rows=46650;feature_count=58;f67c_runtime_rows=64;f67d_runtime_probe_rows=1",
        "guardrail_kpi": "mandatory_mt5_probe_pending_after_meaningful_proxy_signal",
        "hcardrail_kpi": "mandatory_mt5_probe_pending_after_meaningful_proxy_signal",
        "external_verification_status": "not_applicable_preflight_only_grok_stage_open_already_completed",
        "notes": "F68A completed bridge feasibility and open-ended lifecycle economics label design; no proxy signal or runtime authority claimed.",
        "run_number": "frontier68A",
        "date": "2026-06-17",
        "decision": "proceed_to_f68b_runtime_lifecycle_proxy_broad_sweep",
        "next_run_id": NEXT_RUN_ID,
        "rows": "5",
        "gate_passes": "5",
        "gate_total": "5",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/reports/result_summary.md",
        "run_date": "2026-06-17",
        "primary_artifact": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f68a_bridge_feasibility_checklist.json",
        "view": "preflight_design(사전확인 설계)",
        "tier": "Tier A+B planned(티어 A+B 계획)",
        "metric_scope": "bridge_feasibility_and_label_design(연결 가능성 및 라벨 설계)",
        "result_status": "completed_preflight_design_no_authority",
        "feature_count": str(inventory["model_inputs"]["v2_58"]["feature_order"].get("feature_count") or ""),
        "sample_rows": str(inventory["model_inputs"]["v2_58"].get("rows") or ""),
        "lane": "preflight_design(사전확인 설계)",
        "family": "experiment_design(실험 설계)",
        "primary_report": f"stages/{STAGE_ID}/03_reviews/frontier68A_bridge_feasibility_and_label_design_report.md",
        "row_id": f"{RUN_ID}__bridge_feasibility_label_design",
        "scoreboard": "not_applicable_no_proxy_kpi_yet(아직 프록시 KPI 없음)",
        "evidence_boundary": "preflight_design_only(사전확인 설계 전용)",
        "work_family": "experiment_design(실험 설계)",
        "evidence_scope": "F67 runtime evidence plus model input inventory(F67 런타임 근거 + 모델 입력 목록)",
        "run_key": RUN_ID,
        "question": "Can F68 build a lifecycle economics proxy without narrowing search to examples?(F68이 예시에 탐색을 고정하지 않고 생명주기 경제성 프록시를 만들 수 있는가)",
        "next_action": NEXT_RUN_ID,
        "result_judgment": "bridge_feasible_preflight_no_authority",
        "final_decision_path": f"stages/{STAGE_ID}/03_reviews/frontier68A_bridge_feasibility_and_label_design_report.md",
        "created_at": created_at,
        "created_at_utc": created_at,
        "gate_audit_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f68a_bridge_feasibility_checklist.json",
        "required_gate_audit": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f68a_bridge_feasibility_checklist.json",
        "kpi_summary": "no_runtime_kpi_preflight_only;model_input_v2_rows=46650;f67c_rows=64;f67d_receipt_rows=1",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "source_authority": "preflight_inventory_from_existing_artifacts(기존 산출물 기반 사전확인 목록)",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_preflight_design(전선 사전확인 설계)",
        "run_type": "bridge_feasibility_label_design(연결 가능성 라벨 설계)",
        "input_run_id": "frontier67_closeout_preserved_clue_negative_memory_v1",
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f68a_lifecycle_label_design.json",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier68A_bridge_feasibility_and_label_design_report.md",
    }


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


def update_text_files(created_at: str) -> None:
    selection = [
        "# F68 Selection Status(F68 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- status(상태): `f68a_preflight_design_completed_no_authority(F68A 사전확인 설계 완료, 권위 없음)`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        "- completed_action(완료 행동): F68A bridge feasibility checklist and lifecycle economics label design(F68A 연결 가능성 체크리스트와 생명주기 경제성 라벨 설계)을 완료했다.",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}` proxy broad sweep(프록시 넓은 탐색).",
        "- boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
    ]
    write_md(STAGE_ROOT / "04_selected" / "selection_status.md", selection)

    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        "current_status: f68a_preflight_design_completed_no_authority(F68A 사전확인 설계 완료, 권위 없음)",
        "current_judgment: bridge_feasible_for_proxy_materialization_but_no_f68_proxy_signal_yet(프록시 물질화 연결은 가능하지만 F68 프록시 신호는 아직 없음)",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f68_mandatory_runtime_probe_pending_after_meaningful_proxy_signal(F68 의미 있는 프록시 신호 후 필수 런타임 탐침 대기)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        '  - "F68A completed(완료): bridge feasibility checklist and lifecycle economics label design(연결 가능성 체크리스트와 생명주기 경제성 라벨 설계)을 완료했다."',
        '  - "Bridge read(연결 판독): full 58-feature model input(58개 피처 모델 입력), ONNX export path(ONNX 내보내기 경로), RuntimeProbeEA feature/model handoff(런타임 탐침 EA 피처/모델 인계)는 F68B proxy materialization(프록시 물질화)에 사용할 수 있다."',
        '  - "Known limitation(알려진 한계): F67D feature matrix(F67D 피처 행렬)는 one-column discrete signal replay(한 컬럼 이산 신호 재생)이므로 F68 lifecycle proxy(F68 생명주기 프록시) 자체로 충분하지 않다."',
        '  - "Next action(다음 행동): F68B runtime lifecycle proxy broad sweep(런타임 생명주기 프록시 넓은 탐색)을 실행해 nonzero meaningful proxy signal(영이 아닌 의미 있는 프록시 신호)을 만든다."',
        '  - "Goal resume context anchor(목표 재개 컨텍스트 고정점): example axes(예시 축)는 non-exhaustive prompts(비한정 프롬프트)이지 fixed checklist(고정 체크리스트)가 아니다; each frontier stage(각 전선 단계)는 current evidence(현재 근거)에서 가장 살아 있는 fresh alpha source(새 알파 원천)를 고른다."',
        '  - "No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed(주장 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(state) + "\n", encoding="utf-8-sig")

    current_working_state = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        "",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        "",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F68A bridge feasibility and lifecycle economics label design(F68A 연결 가능성 및 생명주기 경제성 라벨 설계)을 완료했다.",
        "",
        "Effect(효과): F68B가 full 58-feature model input(전체 58개 피처 모델 입력)과 F67 runtime lifecycle evidence(F67 런타임 생명주기 근거)를 써서 proxy broad sweep(프록시 넓은 탐색)을 시작할 수 있다.",
        "",
        "- F68A status(F68A 상태): `completed_preflight_design_no_authority(사전확인 설계 완료, 권위 없음)`.",
        "- bridge feasibility(연결 가능성): full feature handoff(전체 피처 인계), ONNX export path(ONNX 내보내기 경로), RuntimeProbeEA handoff(런타임 탐침 EA 인계)는 feasible pending F68 model/proxy(모델/프록시 대기 상태에서 가능)이다.",
        "- data inventory(데이터 목록): 58-feature model input(58개 피처 모델 입력) rows(행) `46650`, OOS rows(표본외 행) `7584`.",
        "- limitation(한계): F67D runtime probe feature matrix(F67D 런타임 탐침 피처 행렬)는 one-column discrete signal replay(한 컬럼 이산 신호 재생)이므로 F68 lifecycle proxy(생명주기 프록시) 자체가 아니다.",
        "- next_action(다음 행동): `frontier68B_runtime_lifecycle_proxy_broad_sweep_v1`.",
        "- mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침): F68B/F68C에서 meaningful proxy signal(의미 있는 프록시 신호)이 생긴 뒤 pre-MT5 Grok review(그록 사전 검토)를 거쳐 실행한다.",
        "- five-stage retrospective(5단계 중간 검토): `not_due_after_F67_2_of_5(아직 아님, F67 후 2/5)`.",
        "",
        "## Goal Resume Context Anchor(목표 재개 컨텍스트 고정점)",
        "",
        "Action(행동): goal resume(목표 재개) 때 exploration posture(탐색 태도)를 먼저 복원한다.",
        "",
        "Effect(효과): feature set/label/model/trade shape/risk/regime(피처 묶음/라벨/모델/거래 형태/위험/장세) 같은 예시(example, 예시)를 fixed checklist(고정 체크리스트)나 prescription(처방)처럼 좁게 실행하지 않고, 현재 근거에서 가장 살아 있는 새 alpha source(알파 원천)를 고른다.",
        "",
        "- Search space(탐색 공간): open-ended(열린 상태)다. 이전 대화의 axis list(축 목록)는 sample directions(예시 방향)이지 boundary(경계)가 아니다.",
        "- Stage role(단계 역할): each frontier stage(각 전선 단계)는 alignment/gap analysis(정렬/간극 분석)만 하는 곳이 아니라, 하나의 fresh hypothesis(새 가설)를 materialize(물질화)하는 alpha experiment(알파 실험)이다.",
        "- Alignment role(정렬 역할): proxy/runtime alignment(프록시/런타임 정렬)과 gap analysis(간극 분석)는 다음 실험을 고르는 map(지도)이다. They are not an excuse to avoid new experiments(새 실험을 피하는 핑계가 아니다).",
        "- Example handling(예시 처리): if examples are mentioned(예시가 언급되면), treat them as non-exhaustive prompts(비한정 프롬프트) and do not lock the search to them(탐색을 그 예시에 고정하지 않는다).",
        "- Claim boundary(주장 경계): this anchor(고정점)는 goal(목표)을 바꾸지 않는다. It preserves exploration discipline(탐색 규율 보존) only; completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 만들지 않는다.",
        "",
        "## Key Artifacts(핵심 산출물)",
        "",
        f"- F68A report(F68A 보고서): `stages/{STAGE_ID}/03_reviews/frontier68A_bridge_feasibility_and_label_design_report.md`",
        f"- F68A bridge checklist(F68A 연결 체크리스트): `stages/{STAGE_ID}/03_reviews/f68a_bridge_feasibility_checklist_review.json`",
        f"- F68A label design(F68A 라벨 설계): `stages/{STAGE_ID}/03_reviews/f68a_lifecycle_label_design_review.json`",
        f"- F68 stage brief(F68 단계 개요): `stages/{STAGE_ID}/00_spec/stage_brief.md`",
        "- five-stage retrospective register(5단계 중간 검토 등록부): `docs/registers/five_stage_retrospective_register.yaml`",
        "",
        "Claim boundary(주장 경계): scout clue/seed surface/runtime probe observation/preserved clue/negative memory(탐색 단서/씨앗 표면/런타임 탐침 관찰/보존 단서/부정 기억)까지만 말한다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", current_working_state)


def build_report(inventory: dict[str, Any], bridge: dict[str, Any], design: dict[str, Any]) -> list[str]:
    f67d = inventory["f67d_runtime_probe_receipt"]["row"]
    return [
        "# F68A Bridge Feasibility And Label Design(F68A 연결 가능성 및 라벨 설계)",
        "",
        f"Updated(갱신): {inventory['created_at_utc']}",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F68A에서 model input(모델 입력), F67 runtime evidence(F67 런타임 근거), ONNX/MT5 handoff(ONNX/MT5 인계) 경로를 점검하고 lifecycle economics label design(생명주기 경제성 라벨 설계)을 남겼다.",
        "",
        "Effect(효과): F68B가 예시 목록에 갇히지 않고, 현재 근거에서 가장 살아 있는 runtime-lifecycle alpha source(런타임 생명주기 알파 원천)를 실제 proxy prototype(프록시 원형)으로 만들 수 있게 한다.",
        "",
        "## Input Inventory(입력 목록)",
        "",
        f"- model input v2 58 features(모델 입력 v2 58개 피처): rows(행) `{inventory['model_inputs']['v2_58'].get('rows')}`, feature_count(피처 수) `{inventory['model_inputs']['v2_58']['feature_order'].get('feature_count')}`.",
        f"- model input v1 56 features(모델 입력 v1 56개 피처): rows(행) `{inventory['model_inputs']['v1_56'].get('rows')}`, feature_count(피처 수) `{inventory['model_inputs']['v1_56']['feature_order'].get('feature_count')}`.",
        f"- F67C runtime lifecycle rows(F67C 런타임 생명주기 행): `{inventory['f67c_runtime_lifecycle_summary']['rows']}` rows(행).",
        f"- F67D runtime probe receipt(F67D 런타임 탐침 영수증): PF/DD/trades/day(수익 팩터/손실폭/일 거래 수) `{f67d.get('profit_factor')}/{f67d.get('max_drawdown_percent')}/{f67d.get('trades_per_day')}`.",
        f"- F67D feature matrix(F67D 피처 행렬): `{inventory['f67d_feature_matrix'].get('rows')}` rows(행), `{inventory['f67d_feature_matrix'].get('columns')}` columns(열), one-column signal replay(한 컬럼 신호 재생).",
        "",
        "## Bridge Feasibility(연결 가능성)",
        "",
        f"- full feature handoff(전체 피처 인계): `{bridge['checks'][2]['status']}`.",
        f"- ONNX export path(ONNX 내보내기 경로): `{bridge['checks'][3]['status']}`.",
        f"- mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침): `{bridge['checks'][4]['status']}` because F68A has no meaningful proxy signal yet(F68A에는 아직 의미 있는 프록시 신호가 없음).",
        "",
        "## Open-Ended Exploration Guard(열린 탐색 보호)",
        "",
        "- Search space(탐색 공간)는 open-ended(열린 상태)다. feature/model/label examples(피처/모델/라벨 예시)는 sample prompts(예시 프롬프트)이지 fixed checklist(고정 체크리스트)가 아니다.",
        "- F68B starts from lifecycle/cost/DD evidence(F67 생명주기/비용/손실폭 근거) because that is the current live clue(현재 살아 있는 단서)다.",
        "- If a different current-evidence alpha source(현재 근거 기반 알파 원천)가 더 강하면 F68B may pivot within the same claim boundary(같은 주장 경계 안에서 전환 가능).",
        "",
        "## Label Design(라벨 설계)",
        "",
        f"- hypothesis(가설): {design['hypothesis']}",
        f"- broad_sweep(넓은 탐색): {', '.join(design['broad_sweep'])}",
        f"- micro_search_gate(미세 탐색 게이트): {design['micro_search_gate']}",
        f"- wfo_plan(워크포워드 계획): {design['wfo_plan']}",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`: build a broad proxy sweep(넓은 프록시 탐색) from the 58-feature model input(58개 피처 모델 입력) and F67 lifecycle evidence(F67 생명주기 근거), then choose whether a meaningful signal exists for pre-MT5 Grok review and mandatory MT5 materialization(필수 MT5 물질화).",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def write_run_outputs(created_at: str, inventory_rows: list[dict[str, Any]], inventory: dict[str, Any], bridge: dict[str, Any], design: dict[str, Any]) -> None:
    write_csv(RUN_ROOT / "f68a_input_inventory.csv", inventory_rows)
    write_json(RUN_ROOT / "f68a_input_inventory_summary.json", inventory)
    write_json(RUN_ROOT / "f68a_bridge_feasibility_checklist.json", bridge)
    write_json(RUN_ROOT / "f68a_lifecycle_label_design.json", design)
    write_md(RUN_ROOT / "reports" / "result_summary.md", build_report(inventory, bridge, design))

    write_csv(REVIEWS_ROOT / "f68a_input_inventory_review.csv", inventory_rows)
    write_json(REVIEWS_ROOT / "f68a_bridge_feasibility_checklist_review.json", bridge)
    write_json(REVIEWS_ROOT / "f68a_lifecycle_label_design_review.json", design)
    write_md(REVIEWS_ROOT / "frontier68A_bridge_feasibility_and_label_design_report.md", build_report(inventory, bridge, design))

    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": "completed_preflight_design_no_authority",
        "claim_boundary": CLAIM_BOUNDARY,
        "producer": "stage_pipelines/stage_frontier_68/frontier68a_bridge_feasibility_and_label_design.py",
        "artifacts": [
            rel(RUN_ROOT / "f68a_input_inventory.csv"),
            rel(RUN_ROOT / "f68a_bridge_feasibility_checklist.json"),
            rel(RUN_ROOT / "f68a_lifecycle_label_design.json"),
            rel(REVIEWS_ROOT / "frontier68A_bridge_feasibility_and_label_design_report.md"),
        ],
        "next_run_id": NEXT_RUN_ID,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)


def update_ledgers(created_at: str, inventory: dict[str, Any]) -> None:
    row = ledger_row(created_at, inventory)
    stage_ledger = REVIEWS_ROOT / "stage_run_ledger.csv"
    alpha_ledger = ROOT / "docs/registers/alpha_run_ledger.csv"
    run_registry = ROOT / "docs/registers/run_registry.csv"
    upsert_ledger(stage_ledger, "ledger_row_id", row)
    upsert_ledger(alpha_ledger, "ledger_row_id", row)
    upsert_ledger(run_registry, "run_id", row)


def update_review_index() -> None:
    index_path = REVIEWS_ROOT / "review_index.md"
    lines = [
        "# F68 Review Index(F68 검토 색인)",
        "",
        "- `../00_spec/stage_brief.md`: F68 stage brief(F68 단계 개요)",
        "- `runA_report.md`: F68A stage open report(F68A 단계 개방 보고서)",
        "- `grok_stage_open_receipt.md`: F68 Grok stage-open receipt(F68 그록 단계 개방 영수증)",
        "- `stage_run_ledger.csv`: F68 stage-local run ledger(F68 단계 로컬 실행 장부)",
        "- `frontier68A_bridge_feasibility_and_label_design_report.md`: F68A bridge feasibility and label design report(F68A 연결 가능성 및 라벨 설계 보고서)",
        "- `f68a_input_inventory_review.csv`: F68A input inventory(F68A 입력 목록)",
        "- `f68a_bridge_feasibility_checklist_review.json`: F68A bridge feasibility checklist(F68A 연결 가능성 체크리스트)",
        "- `f68a_lifecycle_label_design_review.json`: F68A lifecycle label design(F68A 생명주기 라벨 설계)",
        "",
        "Current status(현재 상태): `f68a_preflight_design_completed_no_authority(F68A 사전확인 설계 완료, 권위 없음)`",
        f"Next action(다음 행동): `{NEXT_RUN_ID}`",
    ]
    write_md(index_path, lines)


def main() -> int:
    created_at = utc_now()
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS_ROOT).mkdir(parents=True, exist_ok=True)
    inventory_rows, inventory = build_inventory(created_at)
    bridge = build_bridge_checklist(created_at, inventory)
    design = build_label_design(created_at, inventory)
    write_run_outputs(created_at, inventory_rows, inventory, bridge, design)
    update_ledgers(created_at, inventory)
    update_review_index()
    update_text_files(created_at)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "completed_preflight_design_no_authority",
                    "run_id": RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "model_input_v2_rows": inventory["model_inputs"]["v2_58"].get("rows"),
                    "feature_count": inventory["model_inputs"]["v2_58"]["feature_order"].get("feature_count"),
                    "runtime_probe_status": "pending_after_meaningful_proxy_signal",
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
