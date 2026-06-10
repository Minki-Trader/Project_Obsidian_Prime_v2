from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import review_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db as hg  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db as hf  # noqa: E402


TODAY = "2026-06-08"
STAGE_ID = hf.STAGE_ID
STAGE_DIR = hf.STAGE_DIR
REVIEW_DIR = hf.REVIEW_DIR
SPEC_DIR = hf.SPEC_DIR
SELECTED_DIR = hf.SELECTED_DIR

RUN_NUMBER = "run364HH"
RUN_ID = "run364HH_materialize_h17_oos108_pf125_near_miss_profit_pf_lift_runtime_capability_inputs_without_db_v1"
PARENT_RUN_ID = hg.RUN_ID
HF_SOURCE_RUN_ID = hf.RUN_ID
NEXT_RUN_ID = "run364HI_implement_h17_oos108_pf125_probability_bin_veto_runtime_support_without_db_v1"

STATUS = "completed_stage364HH_runtime_capability_inputs_materialized_probability_bin_veto_support_required_no_authority"
JUDGMENT = "materialization_completed_runtime_capability_inputs_probability_bin_veto_support_required_no_authority"
DECISION = "stage364HH_open_run364HI_probability_bin_veto_runtime_support"
CLAIM_BOUNDARY = (
    "research_development_runtime_capability_materialization_only_no_runtime_package_no_new_mt5_execution_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
EA_PATH = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.mq5"
DECISION_SURFACE_MQH = ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime" / "DecisionSurface.mqh"
FEATURE_ORDER_PATH = hf.dt.dp.MODEL_INPUT_FEATURE_ORDER

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUNTIME_CAPABILITY_CONTRACT = RUN_DIR / "runtime_capability_contract.csv"
SOURCE_MODEL_RUNTIME_MANIFEST = RUN_DIR / "source_model_runtime_manifest.csv"
VETO_RULE_MANIFEST = RUN_DIR / "veto_rule_manifest.csv"
PROBABILITY_BIN_EDGES = RUN_DIR / "probability_bin_edges.json"
EXPECTED_TRADE_TAPE = RUN_DIR / "expected_trade_tape.csv"
EXPECTED_ROUTE_SUMMARY = RUN_DIR / "expected_route_summary.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.json"
RUN364HI_QUEUE = RUN_DIR / "hh_hi_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HH_near_miss_profit_pf_lift_runtime_capability_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HH_near_miss_profit_pf_lift_runtime_capability_materialization.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

THIS_FILE = Path(__file__)

INPUT_FILES = [
    hg.FINAL_DECISION,
    hg.GATE_AUDIT,
    hg.RUNTIME_CAPABILITY_GAP,
    hg.RUN364HH_QUEUE,
    hf.FINAL_DECISION,
    hf.GATE_AUDIT,
    hf.TRADE_SURFACE,
    hf.SELECTED_CANDIDATE,
    hf.SELECTED_TRADE_TAPE,
    hf.SELECTED_VETO_GROUPS,
    hf.MODEL_ARTIFACT_MANIFEST,
    hf.ONNX_SMOKE_REPORT,
    hf.DATA_INTEGRITY_AUDIT,
    FEATURE_ORDER_PATH,
    EA_PATH,
    DECISION_SURFACE_MQH,
    THIS_FILE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    RUNTIME_CAPABILITY_CONTRACT,
    SOURCE_MODEL_RUNTIME_MANIFEST,
    VETO_RULE_MANIFEST,
    PROBABILITY_BIN_EDGES,
    EXPECTED_TRADE_TAPE,
    EXPECTED_ROUTE_SUMMARY,
    RUNTIME_PARITY_CONTRACT,
    RUN364HI_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    RUNTIME_PARITY_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    THIS_FILE,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return hf.rel(path)


def exists(path: Path | str) -> bool:
    return hf.exists(path)


def sha(path: Path | str) -> str:
    return hf.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return hf.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    number = as_float(value, default=math.nan)
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def read_json(path: Path) -> dict[str, Any]:
    return hf.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    hf.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    hf.write_text(path, text, bom=bom)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    hf.write_csv(path, rows)


def append_text_once(path: Path, marker: str, text: str) -> None:
    hf.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    hf.append_or_replace_csv(path, key_fields, rows)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HH inputs(HH 입력 누락): " + ", ".join(missing))

    parent = read_json(hg.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HG next_run_id mismatch(HG 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")

    source = read_json(hf.FINAL_DECISION)
    if source.get("run_id") != HF_SOURCE_RUN_ID:
        raise RuntimeError(f"HF source run mismatch(HF 원천 실행 불일치): {source.get('run_id')} != {HF_SOURCE_RUN_ID}")

    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden parent claim(금지된 상위 주장): {key}={parent.get(key)}")
        if source.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden HF claim(금지된 HF 주장): {key}={source.get(key)}")

    for label, gate_path in [("HG", hg.GATE_AUDIT), ("HF", hf.GATE_AUDIT)]:
        gates = read_csv(gate_path)
        if gates.empty or any(gates["status"].astype(str) != "passed"):
            raise RuntimeError(f"{label} gate audit({label} 게이트 감사)가 모두 passed(통과)가 아닙니다.")

    selected_tape = read_csv(hf.SELECTED_TRADE_TAPE)
    selected_groups = read_csv(hf.SELECTED_VETO_GROUPS)
    if selected_tape.empty:
        raise RuntimeError("HF selected trade tape(HF 선택 거래 테이프)가 비어 있습니다.")
    if selected_groups.empty:
        raise RuntimeError("HF selected veto groups(HF 선택 차단 그룹)가 비어 있습니다.")
    return parent, source


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "runtime capability materialization input(런타임 기능 물질화 입력)",
            "effect": "입력 계보를 고정해 다음 HI 구현이 같은 원천을 보게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def selected_surface_row(parent: Mapping[str, Any]) -> dict[str, Any]:
    surface = read_csv(hf.TRADE_SURFACE)
    selected = surface[surface["route_variant_id"].astype(str).eq(str(parent["selected_route_variant_id"]))]
    if selected.empty:
        raise RuntimeError("selected HF route(HF 선택 라우트)를 hf_surface.csv에서 찾지 못했습니다.")
    return dict(selected.iloc[0])


def write_work_packet(parent: Mapping[str, Any], source: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "hf_source_run_id": HF_SOURCE_RUN_ID,
            "primary_family": "runtime_verification(런타임 검증)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "input_lineage_gate",
                "expected_tape_gate",
                "source_model_manifest_gate",
                "veto_rule_manifest_gate",
                "runtime_capability_contract_gate",
                "runtime_parity_boundary_gate",
                "next_action_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "question": "Can HF runtime inputs be materialized before EA support?(EA 지원 전에 HF 런타임 입력을 물질화할 수 있는가?)",
            "action": "Materialize runtime contract, expected tape, source model manifest, and veto manifest(런타임 계약, 예상 테이프, 원천 모델 목록, 차단 목록을 물질화합니다).",
            "effect": "다음 HI 구현이 숫자와 파일 계보를 재해석하지 않고 바로 EA 지원을 추가할 수 있습니다.",
            "parent_summary": {
                "hg_judgment": parent.get("judgment"),
                "hf_judgment": source.get("judgment"),
                "selected_route_variant_id": parent.get("selected_route_variant_id"),
                "selected_veto_key_fields": source.get("selected_veto_key_fields"),
                "selected_oos_net": source.get("selected_oos_net"),
                "selected_oos_profit_factor": source.get("selected_oos_profit_factor"),
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def source_model_runtime_rows(tape: pd.DataFrame, smoke: pd.DataFrame, manifest: pd.DataFrame) -> list[dict[str, Any]]:
    tape = tape.copy()
    rows: list[dict[str, Any]] = []
    used = (
        tape.groupby(["source_run_id", "source_model_id", "route_role"], dropna=False)
        .size()
        .reset_index(name="trade_count")
        .sort_values(["source_run_id", "source_model_id", "route_role"])
    )
    onnx_rows = manifest[manifest["artifact_type"].astype(str).str.contains("onnx", case=False, na=False)]
    joblib_rows = manifest[manifest["artifact_type"].astype(str).str.contains("joblib", case=False, na=False)]
    for raw in used.to_dict("records"):
        model_id = str(raw["source_model_id"])
        source_run_id = str(raw["source_run_id"])
        route_role = str(raw["route_role"])
        runtime_role = "primary_anchor(우선 기준)" if "gz" in route_role.lower() else "fallback_profit(수익 대체)"
        onnx = onnx_rows[onnx_rows["model_id"].astype(str).eq(model_id)]
        joblib = joblib_rows[joblib_rows["model_id"].astype(str).eq(model_id)]
        smoke_row = smoke[smoke["model_id"].astype(str).eq(model_id)]
        onnx_path = str(onnx.iloc[0].get("path", "")) if not onnx.empty else ""
        joblib_path = str(joblib.iloc[0].get("path", "")) if not joblib.empty else ""
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": source_run_id,
                "source_model_id": model_id,
                "route_role": route_role,
                "runtime_role": runtime_role,
                "trade_count_in_expected_tape": int(raw["trade_count"]),
                "onnx_path": onnx_path,
                "onnx_sha256": sha(ROOT / onnx_path) if onnx_path and exists(ROOT / onnx_path) else (onnx.iloc[0].get("sha256", "") if not onnx.empty else ""),
                "joblib_path": joblib_path,
                "joblib_sha256": sha(ROOT / joblib_path) if joblib_path and exists(ROOT / joblib_path) else (joblib.iloc[0].get("sha256", "") if not joblib.empty else ""),
                "feature_order_path": rel(FEATURE_ORDER_PATH),
                "feature_order_sha256": sha(FEATURE_ORDER_PATH),
                "feature_count": 56,
                "onnx_smoke_status": str(smoke_row.iloc[0].get("status", "")) if not smoke_row.empty else "missing(누락)",
                "onnx_smoke_max_abs_diff": str(smoke_row.iloc[0].get("max_abs_diff", "")) if not smoke_row.empty else "",
                "effect": "ONNX(온엑스) 모델 파일과 feature order(피처 순서)를 함께 묶어 MT5 입력 불일치를 줄입니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(SOURCE_MODEL_RUNTIME_MANIFEST, rows)
    return rows


def bin_range(edges: Sequence[float], bin_id: int) -> tuple[str, str, str]:
    if not edges:
        return "", "", "single_bin_or_missing_edges(단일 구간 또는 경계 누락)"
    lower = "-inf" if bin_id <= 0 else str(edges[bin_id])
    upper = "inf" if bin_id + 1 >= len(edges) else str(edges[bin_id + 1])
    if bin_id <= 0:
        lower = str(edges[0])
    return lower, upper, "pd.cut_interval_left_open_right_closed_first_inclusive(pd.cut 구간, 첫 구간만 양끝 포함)"


def write_veto_manifest(groups: pd.DataFrame, surface_row: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    bin_edges = json.loads(str(surface_row.get("bin_edges_json", "{}")) or "{}")
    rows: list[dict[str, Any]] = []
    for index, raw in enumerate(groups.to_dict("records"), start=1):
        key_values = json.loads(str(raw.get("veto_key_values", "{}")) or "{}")
        open_hour = int(as_float(key_values.get("open_hour"), 0))
        pflat_bin = int(as_float(key_values.get("pflat_bin"), -1))
        sl_gap_bin = int(as_float(key_values.get("sl_gap_bin"), -1))
        pflat_lower, pflat_upper, pflat_semantics = bin_range(bin_edges.get("pflat_bin", []), pflat_bin)
        sl_lower, sl_upper, sl_semantics = bin_range(bin_edges.get("sl_gap_bin", []), sl_gap_bin)
        rows.append(
            {
                "run_id": RUN_ID,
                "veto_rule_id": f"hh_veto_rule_{index:02d}",
                "source_veto_policy_id": raw.get("veto_policy_id", ""),
                "source_veto_policy_label": raw.get("veto_policy_label", ""),
                "veto_key_fields": raw.get("veto_key_fields", ""),
                "open_hour": open_hour,
                "pflat_bin": pflat_bin,
                "pflat_lower": pflat_lower,
                "pflat_upper": pflat_upper,
                "pflat_bin_semantics": pflat_semantics,
                "sl_gap_bin": sl_gap_bin,
                "sl_gap_lower": sl_lower,
                "sl_gap_upper": sl_upper,
                "sl_gap_bin_semantics": sl_semantics,
                "runtime_match_expression": f"open_hour=={open_hour} && pflat_bin=={pflat_bin} && sl_gap_bin=={sl_gap_bin}",
                "validation_count": raw.get("validation_count", ""),
                "validation_net": raw.get("validation_net", ""),
                "validation_expectancy": raw.get("validation_expectancy", ""),
                "removed_total_count": raw.get("removed_total_count", ""),
                "removed_oos_count": raw.get("removed_oos_count", ""),
                "removed_oos_net": raw.get("removed_oos_net", ""),
                "veto_min_count": raw.get("veto_min_count", ""),
                "veto_sum_floor": raw.get("veto_sum_floor", ""),
                "effect": "검증 손실 구간을 MT5 EA(메타트레이더5 전문가 자문)가 같은 방식으로 차단할 수 있게 숫자 계약으로 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(VETO_RULE_MANIFEST, rows)
    write_json(
        PROBABILITY_BIN_EDGES,
        {
            "run_id": RUN_ID,
            "source_run_id": HF_SOURCE_RUN_ID,
            "source_route_variant_id": surface_row.get("route_variant_id", ""),
            "bin_edges": bin_edges,
            "bin_semantics": "pd.cut(..., labels=False, include_lowest=True) from validation split only(검증 분할 전용 pd.cut 구간)",
            "effect": "EA 구현이 Python proxy(Python 프록시)의 확률 구간 계산을 재현할 수 있습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return rows, bin_edges


def write_expected_tape(tape: pd.DataFrame) -> list[dict[str, Any]]:
    out = tape.copy()
    out.insert(0, "expected_trade_sequence", range(1, len(out) + 1))
    out.insert(1, "source_trade_tape_run_id", out["run_id"].astype(str))
    out["run_id"] = RUN_ID
    out["expected_tape_role"] = "proxy_expected_trade_tape(프록시 예상 거래 테이프)"
    out["expected_runtime_status"] = "pending_runtime_implementation(런타임 구현 대기)"
    out["claim_boundary"] = CLAIM_BOUNDARY
    rows = out.to_dict("records")
    write_csv(EXPECTED_TRADE_TAPE, rows)
    return rows


def route_summary_rows(tape: pd.DataFrame, parent: Mapping[str, Any]) -> list[dict[str, Any]]:
    frame = tape.copy()
    frame["net_profit"] = pd.to_numeric(frame["net_profit"], errors="coerce").fillna(0.0)
    frame["entry_dt"] = pd.to_datetime(frame["entry_time"], utc=True, errors="coerce")
    rows: list[dict[str, Any]] = []

    def add_row(view_name: str, group: pd.DataFrame, extra: Mapping[str, Any]) -> None:
        profits = group["net_profit"].to_numpy(dtype="float64")
        rows.append(
            {
                "run_id": RUN_ID,
                "view": view_name,
                **extra,
                "trade_count": int(len(group)),
                "net_profit": finite(float(profits.sum()), 4),
                "profit_factor": finite(hf.profit_factor(profits), 10),
                "expectancy": finite(float(profits.mean()) if len(profits) else 0.0, 10),
                "long_trade_count": int(group["direction"].astype(str).eq("long").sum()) if "direction" in group else "",
                "short_trade_count": int(group["direction"].astype(str).eq("short").sum()) if "direction" in group else "",
                "first_entry_time": str(group["entry_time"].min()) if len(group) else "",
                "last_entry_time": str(group["entry_time"].max()) if len(group) else "",
                "effect": "예상 테이프를 분해해 MT5 probe(MT5 탐침)와 비교할 기준을 만듭니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    add_row("all_expected_tape(전체 예상 테이프)", frame, {"split": "combined", "route_role": "all(전체)", "source_model_id": "all(전체)", "direction": "all(전체)"})
    for split, group in frame.groupby("split", sort=True):
        add_row("split_total(분할 전체)", group, {"split": split, "route_role": "all(전체)", "source_model_id": "all(전체)", "direction": "all(전체)"})
    for (split, role, model_id, direction), group in frame.groupby(["split", "route_role", "source_model_id", "direction"], sort=True):
        add_row("split_route_model_direction(분할 라우트 모델 방향)", group, {"split": split, "route_role": role, "source_model_id": model_id, "direction": direction})

    rows.append(
        {
            "run_id": RUN_ID,
            "view": "parent_final_metrics(상위 최종 지표)",
            "split": "oos",
            "route_role": "selected_hf(선택 HF)",
            "source_model_id": parent.get("selected_source_models", ""),
            "direction": "all(전체)",
            "trade_count": parent.get("selected_oos_trade_count", ""),
            "net_profit": parent.get("selected_oos_net", ""),
            "profit_factor": parent.get("selected_oos_profit_factor", ""),
            "expectancy": "",
            "long_trade_count": "",
            "short_trade_count": "",
            "first_entry_time": "",
            "last_entry_time": "",
            "effect": "HG/HF 최종 KPI(핵심 성과 지표)를 요약 기준으로 보존합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    write_csv(EXPECTED_ROUTE_SUMMARY, rows)
    return rows


def capability_contract_rows(parent: Mapping[str, Any], model_rows: Sequence[Mapping[str, Any]], veto_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "capability": "dual_source_onnx_route(이중 원천 ONNX 라우트)",
            "required": "true",
            "current_status": "partially_supported_by_current_ea(현재 EA가 부분 지원)",
            "materialized_artifact": rel(SOURCE_MODEL_RUNTIME_MANIFEST),
            "implementation_requirement": "confirm primary/fallback selection semantics before package(패키지 전에 우선/대체 선택 의미 확인)",
            "evidence": rel(EA_PATH),
            "effect": f"{len(model_rows)}개 원천 모델을 런타임 입력으로 고정했습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "capability": "probability_bin_veto(확률 구간 차단)",
            "required": "true",
            "current_status": "missing_required(필수 누락)",
            "materialized_artifact": rel(VETO_RULE_MANIFEST),
            "implementation_requirement": "add generic open_hour+pflat_bin+sl_gap_bin veto support(일반 진입 시간+평탄확률 구간+숏롱차 구간 차단 지원 추가)",
            "evidence": rel(RUNTIME_CAPABILITY_CONTRACT),
            "effect": f"{len(veto_rows)}개 차단 그룹을 HI 구현 입력으로 고정했습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "capability": "expected_tape_handoff(예상 테이프 인계)",
            "required": "true",
            "current_status": "materialized(물질화됨)",
            "materialized_artifact": rel(EXPECTED_TRADE_TAPE),
            "implementation_requirement": "compare after MT5 probe(MT5 탐침 뒤 비교)",
            "evidence": rel(EXPECTED_ROUTE_SUMMARY),
            "effect": "프록시 예상 결과와 MT5 결과의 diff(차이)를 계산할 기준을 만들었습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "capability": "runtime_parity_contract(런타임 동등성 계약)",
            "required": "true",
            "current_status": "prepared_but_unexecuted(준비됨, 미실행)",
            "materialized_artifact": rel(RUNTIME_PARITY_CONTRACT),
            "implementation_requirement": "execute only after HI EA support(HI EA 지원 뒤 실행)",
            "evidence": rel(RUNTIME_PARITY_CONTRACT),
            "effect": "런타임 실행 전 주장 경계를 명확히 닫았습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "capability": "runtime_package(런타임 패키지)",
            "required": "false_for_HH",
            "current_status": "not_opened(열지 않음)",
            "materialized_artifact": "",
            "implementation_requirement": "blocked until probability-bin veto support is implemented(확률 구간 차단 지원 전까지 차단)",
            "evidence": rel(RUN364HI_QUEUE),
            "effect": "프록시 통과를 운영 패키지로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(RUNTIME_CAPABILITY_CONTRACT, rows)
    return rows


def write_runtime_parity_contract(parent: Mapping[str, Any], source: Mapping[str, Any], model_rows: Sequence[Mapping[str, Any]], veto_rows: Sequence[Mapping[str, Any]], bin_edges: Mapping[str, Any]) -> dict[str, Any]:
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "hf_source_run_id": HF_SOURCE_RUN_ID,
        "expected_trade_tape": rel(EXPECTED_TRADE_TAPE),
        "source_model_runtime_manifest": rel(SOURCE_MODEL_RUNTIME_MANIFEST),
        "veto_rule_manifest": rel(VETO_RULE_MANIFEST),
        "probability_bin_edges": rel(PROBABILITY_BIN_EDGES),
        "target_ea_path": rel(EA_PATH),
        "target_ea_sha256_at_materialization": sha(EA_PATH),
        "decision_surface_module": rel(DECISION_SURFACE_MQH),
        "decision_surface_module_sha256_at_materialization": sha(DECISION_SURFACE_MQH),
        "source_models": list(model_rows),
        "veto_rules": list(veto_rows),
        "bin_edges": bin_edges,
        "expected_model_output": ["p_short", "p_flat", "p_long"],
        "entry_timing": "closed M5 bar to next executable tick assumption(닫힌 M5 봉 뒤 다음 실행 가능 틱 가정)",
        "position_policy": "single_position_router_overlap_skip(단일 포지션 라우터 겹침 건너뛰기)",
        "max_hold_bars": 2,
        "known_gap": "current EA lacks generic probability-bin veto(현재 EA는 일반 확률 구간 차단이 없음)",
        "mt5_execution": "not_run(실행 안 함)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "effect": "HI/이후 MT5 probe(MT5 탐침)가 무엇을 재현해야 하는지 같은 계약으로 고정합니다.",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_metrics": {
            "selected_oos_net": source.get("selected_oos_net"),
            "selected_oos_profit_factor": source.get("selected_oos_profit_factor"),
            "selected_oos_trade_density": source.get("selected_oos_trade_density"),
            "selected_combined_trade_density": source.get("selected_combined_trade_density"),
            "selected_combined_cost09_net": source.get("selected_combined_cost09_net"),
            "hg_judgment": parent.get("judgment"),
        },
    }
    write_json(RUNTIME_PARITY_CONTRACT, payload)
    return payload


def queue_rows(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "hi01_implement_probability_bin_veto_runtime_support(확률 구간 차단 런타임 지원 구현)",
            "source_candidate": source.get("selected_route_variant_id", ""),
            "required_inputs": ";".join([rel(RUNTIME_CAPABILITY_CONTRACT), rel(SOURCE_MODEL_RUNTIME_MANIFEST), rel(VETO_RULE_MANIFEST), rel(EXPECTED_TRADE_TAPE), rel(RUNTIME_PARITY_CONTRACT)]),
            "edit_scope": "foundation/mt5/include/ObsidianPrime and RuntimeProbeEA(ObsidianPrime 포함 모듈과 RuntimeProbeEA)",
            "do_next": "implement generic probability-bin veto, compile, then prepare MT5 probe(일반 확률 구간 차단을 구현하고 컴파일 뒤 MT5 탐침을 준비)",
            "avoid": "do not open runtime package before EA support and compile evidence(EA 지원 및 컴파일 근거 전 런타임 패키지 개방 금지)",
            "effect": "차단 원인을 다음 회차의 구현 범위로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUN364HI_QUEUE, rows)
    return rows


def selected_final(source: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "hf_source_run_id": HF_SOURCE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "runtime_inputs_materialized": True,
        "runtime_capability_gap": True,
        "package_eligible": False,
        "runtime_package": "not_opened",
        "new_model_training": "not_run(실행 안 함)",
        "new_mt5_execution": "not_run(실행 안 함)",
        "selected_route_variant_id": source["selected_route_variant_id"],
        "selected_veto_policy_label": source["selected_veto_policy_label"],
        "selected_veto_key_fields": source["selected_veto_key_fields"],
        "selected_oos_net": source["selected_oos_net"],
        "selected_oos_profit_factor": source["selected_oos_profit_factor"],
        "selected_oos_trade_density": source["selected_oos_trade_density"],
        "selected_oos_cost06_net": source["selected_oos_cost06_net"],
        "selected_combined_trade_density": source["selected_combined_trade_density"],
        "selected_combined_cost09_net": source["selected_combined_cost09_net"],
        "expected_tape_rows": source["selected_trade_tape_rows"],
        "veto_rule_count": source["selected_veto_group_rows"],
        "source_model_count": len(str(source["selected_source_models"]).split("|")),
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def gate_rows(final: Mapping[str, Any], *, final_written: bool) -> list[dict[str, Any]]:
    receipts = [RUN_EVIDENCE_RECEIPT, DATA_RECEIPT, RUNTIME_PARITY_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("scope_completion_gate", exists(RUNTIME_CAPABILITY_CONTRACT) and exists(EXPECTED_TRADE_TAPE) and exists(RUN364HI_QUEUE), RUNTIME_CAPABILITY_CONTRACT, "HH 핵심 산출물을 작성했습니다."),
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "HG/HF/EA 입력 계보를 기록했습니다."),
        ("expected_tape_gate", exists(EXPECTED_TRADE_TAPE) and int(final["expected_tape_rows"]) > 0, EXPECTED_TRADE_TAPE, "프록시 예상 거래 테이프를 물질화했습니다."),
        ("source_model_manifest_gate", exists(SOURCE_MODEL_RUNTIME_MANIFEST) and int(final["source_model_count"]) >= 2, SOURCE_MODEL_RUNTIME_MANIFEST, "우선/대체 ONNX(온엑스) 모델 목록을 물질화했습니다."),
        ("veto_rule_manifest_gate", exists(VETO_RULE_MANIFEST) and int(final["veto_rule_count"]) > 0, VETO_RULE_MANIFEST, "확률 구간 차단 규칙을 물질화했습니다."),
        ("runtime_capability_contract_gate", exists(RUNTIME_CAPABILITY_CONTRACT), RUNTIME_CAPABILITY_CONTRACT, "런타임 기능 계약을 작성했습니다."),
        ("runtime_parity_boundary_gate", exists(RUNTIME_PARITY_CONTRACT), RUNTIME_PARITY_CONTRACT, "MT5 미실행 경계와 동등성 계약을 기록했습니다."),
        ("next_action_gate", exists(RUN364HI_QUEUE), RUN364HI_QUEUE, "HI 구현 대기열을 작성했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RUN_EVIDENCE_RECEIPT, "필수 receipt(영수증)를 작성했습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 gate(게이트) 감사가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", final["runtime_authority"] == "not_claimed" and final["operating_promotion"] == "not_claimed" and final["goal_achieve"] == "not_claimed", CLAIM_RECEIPT, "운영 권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    rows = [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in gates]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_receipts(final: Mapping[str, Any], parity_payload: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **base,
            "runtime_capability_contract": rel(RUNTIME_CAPABILITY_CONTRACT),
            "expected_trade_tape": rel(EXPECTED_TRADE_TAPE),
            "expected_route_summary": rel(EXPECTED_ROUTE_SUMMARY),
            "measurement_boundary": "materialization only(물질화 전용), no MT5 execution(MT5 실행 없음)",
            "effect": "다음 MT5 probe(MT5 탐침)의 비교 기준을 남겼습니다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "source_tape": rel(hf.SELECTED_TRADE_TAPE),
            "source_veto_groups": rel(hf.SELECTED_VETO_GROUPS),
            "timestamp_boundary": "uses existing HF timestamps only(기존 HF 시각만 사용)",
            "lookahead_guard": "no new feature or label computed(새 피처 또는 라벨 계산 없음)",
            "effect": "미래참조 편향을 새로 만들지 않고 입력을 복제/계약화했습니다.",
        },
    )
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            **base,
            "runtime_parity_contract": rel(RUNTIME_PARITY_CONTRACT),
            "target_ea_path": parity_payload.get("target_ea_path"),
            "known_gap": parity_payload.get("known_gap"),
            "mt5_execution": "not_run(실행 안 함)",
            "next_condition": NEXT_RUN_ID,
            "effect": "런타임 동등성은 HI 구현 이후에만 판단하도록 경계를 닫았습니다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()],
            "producer": rel(THIS_FILE),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "effect": "HH 산출물이 어떤 HF/HG/EA 입력에서 나왔는지 추적할 수 있습니다.",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "judgment_label": final["judgment"],
            "evidence_available": [rel(RUNTIME_CAPABILITY_CONTRACT), rel(SOURCE_MODEL_RUNTIME_MANIFEST), rel(VETO_RULE_MANIFEST), rel(EXPECTED_TRADE_TAPE), rel(RUNTIME_PARITY_CONTRACT)],
            "evidence_missing": ["EA implementation evidence(EA 구현 근거)", "MetaEditor compile evidence(메타에디터 컴파일 근거)", "MT5 runtime probe(MT5 런타임 탐침)"],
            "next_condition": NEXT_RUN_ID,
            "effect": "완료 주장을 입력 물질화로만 제한했습니다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_package": "not_opened(열지 않음)",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "프록시와 물질화 결과를 운영 가능 주장으로 올리지 않습니다.",
        },
    )


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364HH Runtime Capability Input Materialization(런타임 기능 입력 물질화)

Created(생성): {final['created_at_utc']}

Action(행동): HG review(HG 검토)가 요청한 runtime capability inputs(런타임 기능 입력)을 contract(계약), expected tape(예상 테이프), source model manifest(원천 모델 목록), veto rule manifest(차단 규칙 목록)로 물질화했습니다.

Effect(효과): 다음 `{NEXT_RUN_ID}`에서 EA(전문가 자문)가 어떤 ONNX(온엑스) 모델과 probability-bin veto(확률 구간 차단)를 재현해야 하는지 다시 해석하지 않아도 됩니다.

- judgment(판정): `{final['judgment']}`
- selected_route_variant_id(선택 라우트 변형 ID): `{final['selected_route_variant_id']}`
- selected_veto_policy(선택 차단 정책): `{final['selected_veto_policy_label']}`
- veto_key_fields(차단 키 필드): `{final['selected_veto_key_fields']}`
- OOS net/profit factor/density/cost0.6(표본밖 순수익/수익 팩터/거래 밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`
- expected_tape_rows(예상 테이프 행): `{final['expected_tape_rows']}`
- veto_rule_count(차단 규칙 수): `{final['veto_rule_count']}`
- source_model_count(원천 모델 수): `{final['source_model_count']}`
- runtime_package(런타임 패키지): `{final['runtime_package']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Key Artifacts(핵심 산출물):

- runtime_capability_contract(런타임 기능 계약): `{rel(RUNTIME_CAPABILITY_CONTRACT)}`
- source_model_runtime_manifest(원천 모델 런타임 목록): `{rel(SOURCE_MODEL_RUNTIME_MANIFEST)}`
- veto_rule_manifest(차단 규칙 목록): `{rel(VETO_RULE_MANIFEST)}`
- expected_trade_tape(예상 거래 테이프): `{rel(EXPECTED_TRADE_TAPE)}`
- runtime_parity_contract(런타임 동등성 계약): `{rel(RUNTIME_PARITY_CONTRACT)}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364HH Runtime Capability Input Materialization(런타임 기능 입력 물질화)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): HF/HG 산출물을 EA 구현 전에 필요한 runtime contract(런타임 계약)와 handoff artifacts(인계 산출물)로 나눴습니다.

Effect(효과): HI는 probability-bin veto(확률 구간 차단) 구현, 컴파일, MT5 probe(MT5 탐침) 준비로 바로 좁혀질 수 있습니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364HH__{RUN_ID}", f"\n- run364HH__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - runtime capability input materialization(런타임 기능 입력 물질화), next(다음) `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364HH__{RUN_ID}", f"\n<!-- run364HH__{RUN_ID} -->\n\n## run364HH Runtime Capability Input Materialization(런타임 기능 입력 물질화)\n\nAction(행동): HF/HG의 runtime capability inputs(런타임 기능 입력)를 계약과 목록으로 물질화했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 probability-bin veto(확률 구간 차단) EA 구현을 바로 시작할 수 있습니다.\n")
    append_text_once(STAGE_README, f"run364HH__{RUN_ID}", f"\n<!-- run364HH__{RUN_ID} -->\n## run364HH runtime capability input materialization(런타임 기능 입력 물질화)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364HH` materialized(물질화 완료) HF/HG runtime capability inputs(런타임 기능 입력). HF OOS net/profit factor/density/cost0.6(HF 표본밖 순수익/수익 팩터/거래 밀도/비용0.6)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`입니다.

Runtime truth(런타임 진실): package(패키지)는 not opened(열지 않음)입니다. 이유는 current EA(현재 전문가 자문)가 `open_hour|pflat_bin|sl_gap_bin` probability-bin veto(확률 구간 차단)를 아직 재현한다는 근거가 없기 때문입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 probability-bin veto(확률 구간 차단) 런타임 지원을 구현하고 compile/probe(컴파일/탐침) 준비로 넘어갑니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest materialization(최근 물질화): HH created(생성) runtime capability contract(런타임 기능 계약), expected tape(예상 테이프), source model runtime manifest(원천 모델 런타임 목록), veto rule manifest(차단 규칙 목록).

HF OOS net/profit factor/density/cost0.6(HF 표본밖 순수익/수익 팩터/거래 밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`

Next seed(다음 씨앗): HI probability-bin veto runtime support(HI 확률 구간 차단 런타임 지원).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364HH__{RUN_ID}", f"\n<!-- run364HH__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` materialized runtime capability inputs(런타임 기능 입력 물질화); next(다음) `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HH__{RUN_ID}", f"\n<!-- run364HH__{RUN_ID} -->\n- `{RUN_ID}`: HF probability-bin veto(확률 구간 차단)를 EA 구현 입력으로 물질화했습니다. Effect(효과): HI가 런타임 기능 부족을 구현 범위로 바꿉니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    artifact_count = len([path for path in OUTPUT_FILES if exists(path)])
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "artifact_count": artifact_count,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Can HF runtime inputs be materialized before EA support?(EA 지원 전에 HF 런타임 입력을 물질화할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"expected_tape_rows={final['expected_tape_rows']};veto_rule_count={final['veto_rule_count']};package_eligible={final['package_eligible']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_runtime_input(필수 누락, Tier B 런타임 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_runtime_materialization_only(주장 범위 밖, 런타임 물질화 전용)"),
    ]:
        rows.append(
            {
                **common,
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "view": record_view,
                "tier": tier_scope,
                "kpi_scope": "HH materialization(HH 물질화)",
                "metric_scope": "runtime_input_no_mt5(런타임 입력, MT5 없음)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "source_authority": "proxy_input_materialization_no_mt5(프록시 입력 물질화, MT5 없음)",
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **common,
                "run_family": "runtime_verification(런타임 검증)",
                "run_type": "runtime_capability_input_materialization(런타임 기능 입력 물질화)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(RUNTIME_CAPABILITY_CONTRACT),
                "selected_net_profit": final["selected_oos_net"],
                "selected_profit_factor": final["selected_oos_profit_factor"],
                "selected_trade_density": final["selected_oos_trade_density"],
            }
        ],
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "artifact_path": rel(path),
            "artifact_type": "hh_runtime_capability_materialization(HH 런타임 기능 물질화)",
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "HH 산출물 계보를 register(등록부)에 연결합니다.",
        }
        for path in OUTPUT_FILES
        if exists(path)
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def write_run_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer": rel(THIS_FILE),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "final_decision": rel(FINAL_DECISION),
            "report_path": rel(REPORT_PATH),
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    ensure_dirs()
    parent, source = validate_inputs()
    created_at = now_utc()
    surface_row = selected_surface_row(source)
    tape = read_csv(hf.SELECTED_TRADE_TAPE)
    groups = read_csv(hf.SELECTED_VETO_GROUPS)
    smoke = read_csv(hf.ONNX_SMOKE_REPORT)
    manifest = read_csv(hf.MODEL_ARTIFACT_MANIFEST)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent, source)
    expected_rows = write_expected_tape(tape)
    summary_rows = route_summary_rows(tape, source)
    model_rows = source_model_runtime_rows(tape, smoke, manifest)
    veto_rows, bin_edges = write_veto_manifest(groups, surface_row)
    contract_rows = capability_contract_rows(source, model_rows, veto_rows)
    parity_payload = write_runtime_parity_contract(parent, source, model_rows, veto_rows, bin_edges)
    queue = queue_rows(source)

    preliminary_final = selected_final(source, [], created_at)
    write_receipts(preliminary_final, parity_payload)
    gates = gate_rows(preliminary_final, final_written=False)
    final = selected_final(source, gates, created_at)
    gates = gate_rows(final, final_written=True)
    final = selected_final(source, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_run_manifest(final)
    write_docs(final, gates)
    write_receipts(final, parity_payload)
    gates = gate_rows(final, final_written=True)
    final = selected_final(source, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_run_manifest(final)
    write_ledgers(final, gates)

    failed = [row for row in gates if row["status"] != "passed"]
    if failed:
        raise RuntimeError("HH gates failed(HH 게이트 실패): " + json.dumps(failed, ensure_ascii=False))
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "expected_tape_rows": len(expected_rows),
                "route_summary_rows": len(summary_rows),
                "source_model_rows": len(model_rows),
                "veto_rule_rows": len(veto_rows),
                "capability_contract_rows": len(contract_rows),
                "queue_rows": len(queue),
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": NEXT_RUN_ID,
                "runtime_authority": "not_claimed",
                "operating_promotion": "not_claimed",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
