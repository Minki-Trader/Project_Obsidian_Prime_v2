from __future__ import annotations

import hashlib
import json
import math
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage321 import design_post_controller_profit_curve_rebuild as s321  # noqa: E402


STAGE_ID = "322_onnx_candidate_campaign__cp321b_curve_stability_pressure"
RUN_ID = "run322A_design_cp321b_curve_stability_pressure_packet_v1"
RUN_NUMBER = "run322A"
SOURCE_STAGE_ID = "321_onnx_candidate_campaign__post_controller_profit_curve_rebuild"
SOURCE_RUN_ID = "run321C_review_post_controller_profit_curve_mt5_probe_v1"
SOURCE_MATERIALIZATION_RUN_ID = "run321A_design_post_controller_profit_curve_rebuild_packet_v1"
UPDATED_ON = "2026-05-26"
STATUS = "completed_cp321b_curve_stability_pressure_candidates_materialized_no_selection"
JUDGMENT = "cp321b_stability_pressure_candidates_materialized_requires_actual_mt5_no_selection"
NEXT_ACTION = "run322B_execute_cp321b_curve_stability_pressure_mt5_probe"
BOUNDARY = s321.BOUNDARY

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
MODEL_DIR = RUN_ROOT / "models"

SOURCE_STAGE321_ROOT = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_STAGE321_REVIEW = SOURCE_STAGE321_ROOT / "03_reviews" / "run321C_review_stage322_open.md"
SOURCE_SURVIVOR_PACKAGE = SOURCE_STAGE321_ROOT / "04_selected" / "cp321b_survivor_seed_package.md"
SOURCE_STAGE321_SCOREBOARD = SOURCE_STAGE321_ROOT / "02_runs" / "run321C" / "post_controller_profit_curve_review_scoreboard.csv"
SOURCE_STAGE321_SHAPE = SOURCE_STAGE321_ROOT / "02_runs" / "run321C" / "trade_frame_shape_summary.csv"

BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
EXPERIMENT_DESIGN = RUN_ROOT / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_ROOT / "data_integrity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run322A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRODUCER = Path("stage_pipelines/stage322/design_cp321b_curve_stability_pressure.py")
RUNTIME_FEATURE_ORDER = s321.RUNTIME_FEATURE_ORDER
RUNTIME_FEATURE_ORDER_HASH = s321.RUNTIME_FEATURE_ORDER_HASH
MODEL_FEATURE_ORDER_HASH = hashlib.sha256("stage322_cp321b_stability_pressure_v1".encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    rule_name: str
    model_risk_max_pct: float
    fixed_lot: float
    hypothesis: str
    changed_variables: str
    branch_lane: str


def candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec(
            "cp322A_cp321b_exact_replay_control_surface",
            "d_or_b_score60",
            0.026,
            0.42,
            "Exact replay(정확 재생) control(대조) confirms whether cp321B reproduces under a fresh Stage322 handoff(인계).",
            "No decision surface(판단 표면) change; only stage-local identity(단계 정체성) changes.",
            "replay_control",
        ),
        CandidateSpec(
            "cp322B_score65_tight_curve_surface",
            "d_or_b_score65",
            0.024,
            0.38,
            "A tighter threshold(더 높은 임계값) should reduce noisy fills(잡음 체결) while keeping 4-10 trades/day(일 4-10거래).",
            "D/B union(합집합) score rank(점수 순위) threshold(임계값) 0.60 -> 0.65 and lower risk(낮은 위험).",
            "defensive_threshold",
        ),
        CandidateSpec(
            "cp322C_score55_density_upside_surface",
            "d_or_b_score55",
            0.028,
            0.45,
            "A looser threshold(낮은 임계값) tests upside(상방) and failure mode(실패 방식) without repeating cp321C score50 pocket(포켓).",
            "D/B union(합집합) score rank(점수 순위) threshold(임계값) 0.60 -> 0.55 and higher risk(높은 위험).",
            "aggressive_density",
        ),
        CandidateSpec(
            "cp322D_d_b_agree55_consensus_surface",
            "d_b_agree55",
            0.026,
            0.40,
            "D/B agreement(합의) pressure checks whether the curve survives when source agreement(원천 합의) replaces priority routing(우선 라우팅).",
            "Require D and B to agree(동의) at score rank(점수 순위) >= 0.55.",
            "source_consensus",
        ),
        CandidateSpec(
            "cp322E_b_only_score60_dependency_surface",
            "b_only_score60",
            0.025,
            0.40,
            "B-only source swap(B 단독 원천 교체) tests whether cp321B depends too much on the D source(D 원천).",
            "Use only cp319B active signal(B 활성 신호) at score rank(점수 순위) >= 0.60.",
            "source_dependency",
        ),
        CandidateSpec(
            "cp322F_score57_hv90_curve_guard_surface",
            "d_or_b_score57_hv90",
            0.027,
            0.43,
            "A moderate threshold(중간 임계값) plus volatility guard(변동성 방어) tests profit scale(수익 규모) without the cp321C OOS pocket(표본외 포켓).",
            "D/B union(합집합) score rank(점수 순위) >= 0.57 and hv rank(변동성 순위) <= 0.90.",
            "balanced_upside_guard",
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return s321.rel(path)


def write_text(path: Path, text: str) -> None:
    s321.write_text(path, text)


def read_text(path: Path) -> str:
    return s321.read_text(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    s321.write_csv(path, columns, rows)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    s321.safe_upsert(path, columns, rows, key)


def sha256_file(path: Path) -> str:
    return s321.sha256_file(path)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    return s321.replace_line(text, prefix, replacement)


def drop_prefixed_lines(text: str, prefixes: Sequence[str]) -> str:
    return s321.drop_prefixed_lines(text, prefixes)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n" + block.rstrip() + "\n"


def prepend_focus(workspace: str, focus: str, marker: str) -> str:
    return s321.prepend_focus(workspace, focus, marker)


def number(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        if isinstance(value, float) and math.isnan(value):
            return default
        text = str(value).replace(",", "").strip()
        return float(text) if text else default
    except Exception:
        return default


def rule_signal(matrix: pd.DataFrame, rule_name: str) -> pd.Series:
    d = matrix["sig_d"]
    b = matrix["sig_b"]
    if rule_name == "d_or_b_score60":
        signal = np.where(((d != 0) | (b != 0)) & (matrix["score_rank"] >= 0.60), np.where(d != 0, d, b), 0)
    elif rule_name == "d_or_b_score65":
        signal = np.where(((d != 0) | (b != 0)) & (matrix["score_rank"] >= 0.65), np.where(d != 0, d, b), 0)
    elif rule_name == "d_or_b_score55":
        signal = np.where(((d != 0) | (b != 0)) & (matrix["score_rank"] >= 0.55), np.where(d != 0, d, b), 0)
    elif rule_name == "d_b_agree55":
        signal = np.where((d != 0) & (d == b) & (matrix["score_rank"] >= 0.55), d, 0)
    elif rule_name == "b_only_score60":
        signal = np.where((b != 0) & (matrix["score_rank"] >= 0.60), b, 0)
    elif rule_name == "d_or_b_score57_hv90":
        signal = np.where(((d != 0) | (b != 0)) & (matrix["score_rank"] >= 0.57) & (matrix["hv_rank"] <= 0.90), np.where(d != 0, d, b), 0)
    else:
        raise ValueError(f"unknown rule_name: {rule_name}")
    return pd.Series(signal, index=matrix.index).astype("int8")


def gates_for(val: Mapping[str, Any], oos: Mapping[str, Any]) -> dict[str, str]:
    return {
        "minimum_trade_gate": "passed" if number(val["trade_count"]) >= 730 and number(oos["trade_count"]) >= 520 else "failed",
        "density_4_10_trades_day_gate": "passed" if 4 <= number(val["trades_per_day"]) <= 10 and 4 <= number(oos["trades_per_day"]) <= 10 else "failed",
        "positive_pf_gate": "passed" if number(val["net_profit"]) > 0 and number(oos["net_profit"]) > 0 and number(val["profit_factor"]) >= 1.5 and number(oos["profit_factor"]) >= 1.5 else "failed",
        "recovery_shape_precheck": "passed" if number(val["recovery_factor"]) >= 3 and number(oos["recovery_factor"]) >= 3 else "failed",
    }


def materialize(
    spec: CandidateSpec,
    matrix: pd.DataFrame,
    source_payload: pd.DataFrame,
    source_columns: Sequence[str],
    source_manifest: Mapping[str, str],
    trades: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, Any], dict[str, str], dict[str, dict[str, Any]]]:
    signal = rule_signal(matrix, spec.rule_name).to_numpy(dtype="int8")
    branch_id = f"run322A_{spec.package_id.replace('_surface', '')}"
    payload = source_payload.copy()
    payload["stage322_branch_id"] = branch_id
    payload["stage321_seed_package_id"] = "cp321B_d_or_b_score60_scale_curve_surface"
    payload["stage321_source_run_id"] = SOURCE_RUN_ID
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "cp321b_curve_stability_pressure"
    payload["stage322_rule_name"] = spec.rule_name
    payload["stage322_branch_lane"] = spec.branch_lane
    payload["stage322_score_rank"] = matrix["score_rank"].to_numpy()
    payload["stage322_hv_rank"] = matrix["hv_rank"].to_numpy()
    payload["stage322_active_surface_count"] = matrix["active_surface_count"].to_numpy()
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = ["long" if value > 0 else ("short" if value < 0 else "flat") for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = spec.model_risk_max_pct
    payload["payload_claim_boundary"] = BOUNDARY
    risk = {column: source_manifest.get(column, "") for column in source_columns}
    risk.update(
        {
            "model_risk_sizing_enabled": "1",
            "model_risk_min_pct": "0.004",
            "model_risk_max_pct": str(spec.model_risk_max_pct),
            "model_risk_confidence_floor": "0.58",
            "model_risk_confidence_ceiling": "0.99",
            "model_risk_fallback_lot": "0.08",
            "fixed_lot": str(spec.fixed_lot),
            "risk_logic_note": f"Stage322 cp321B stability pressure lane={spec.branch_lane}.",
        }
    )
    replay = s321.estimate(payload, trades)
    identity = {
        "package_id": spec.package_id,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "stage321_seed_package_id": "cp321B_d_or_b_score60_scale_curve_surface",
        "rule_name": spec.rule_name,
        "branch_lane": spec.branch_lane,
        "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
        "runtime_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
        "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
        "risk_logic": risk,
        "claim_boundary": BOUNDARY,
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = RUNTIME_FEATURE_ORDER_HASH
    payload["model_feature_order_hash"] = MODEL_FEATURE_ORDER_HASH
    drop_cols = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    return payload.drop(columns=drop_cols, errors="ignore"), identity | {"direction_surface_hash": surface_hash}, risk, replay


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    source_columns, manifest = s321.load_manifest()
    payloads = s321.load_source_payloads(manifest)
    matrix = s321.build_signal_matrix(payloads)
    trades = s321.load_reference_trades()
    source_payload = payloads[s321.D]
    source_manifest = manifest[s321.D]
    branch_rows: list[dict[str, Any]] = []
    scoreboard: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(candidate_specs(), 1):
        payload, identity, risk, replay = materialize(spec, matrix, source_payload, source_columns, source_manifest, trades)
        branch_id = f"run322A_{spec.package_id.replace('_surface', '')}"
        token = spec.package_id.replace("_surface", "")
        payload_path = PAYLOAD_DIR / f"run322A_{token}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"run322A_{token}_handoff.json"
        model_path = MODEL_DIR / f"run322A_{token}_stability_pressure_surface.json"
        payload.to_parquet(s321.long_path(payload_path), index=False)
        write_text(handoff_path, json.dumps(identity, ensure_ascii=False, indent=2, sort_keys=True))
        write_text(model_path, json.dumps({"identity": identity, "route_signal_column": "route_signal_value", "runtime_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH}, ensure_ascii=False, indent=2, sort_keys=True))
        val = replay["validation"]
        oos = replay["oos"]
        gates = gates_for(val, oos)
        design_gate = "passed" if all(status == "passed" for status in gates.values()) else "failed"
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "rule_name": spec.rule_name,
                "branch_lane": spec.branch_lane,
                "hypothesis": spec.hypothesis,
                "changed_variables": spec.changed_variables,
                "decision_surface": "cp321B D/B source pressure variants with score, consensus, source, and volatility guard changes.",
                "success_criteria": "actual MT5 minimum trades, 4-10 trades/day, net/PF/DD/recovery/expectancy, and zoom curve gates together",
                "failure_criteria": "exact replay drift, density slip, profit scale collapse, OOS pocket, or weak segment concentration",
                "claim_boundary": BOUNDARY,
            }
        )
        row = {
            "package_id": spec.package_id,
            "rule_name": spec.rule_name,
            "branch_lane": spec.branch_lane,
            "validation_estimated_net_profit": val["net_profit"],
            "validation_estimated_trade_count": val["trade_count"],
            "validation_estimated_trades_per_day": val["trades_per_day"],
            "validation_estimated_pf": val["profit_factor"],
            "validation_estimated_recovery": val["recovery_factor"],
            "oos_estimated_net_profit": oos["net_profit"],
            "oos_estimated_trade_count": oos["trade_count"],
            "oos_estimated_trades_per_day": oos["trades_per_day"],
            "oos_estimated_pf": oos["profit_factor"],
            "oos_estimated_recovery": oos["recovery_factor"],
            "combined_estimated_net_profit": val["net_profit"] + oos["net_profit"],
            **gates,
            "design_gate": design_gate,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_started",
        }
        scoreboard.append(row)
        for split_name in ("validation", "oos"):
            split_frame = payload[payload["split"].astype(str).eq(split_name)]
            active_count = int(pd.to_numeric(split_frame["route_signal_value"], errors="coerce").fillna(0).ne(0).sum())
            days = max(1, pd.to_datetime(split_frame["timestamp"]).dt.date.nunique()) if not split_frame.empty else 1
            est = replay[split_name]
            supply_rows.append(
                {
                    "materialized_branch_id": branch_id,
                    "package_id": spec.package_id,
                    "split": split_name,
                    "active_signal_rows": active_count,
                    "approx_signal_rows_per_day": round(active_count / days, 6),
                    "estimated_actual_trade_count": est["trade_count"],
                    "estimated_actual_trades_per_day": est["trades_per_day"],
                    "estimated_actual_net_profit": est["net_profit"],
                    "estimated_actual_pf": est["profit_factor"],
                    "claim_boundary": BOUNDARY,
                }
            )
        manifest_row = {column: source_manifest.get(column, "") for column in source_columns}
        manifest_row.update(
            {
                "queue_id": f"run322A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "cp321b_curve_stability_pressure",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file(handoff_path),
                "model_artifact_path": rel(model_path),
                "model_artifact_hash": sha256_file(model_path),
                "model_feature_order_path": rel(model_path),
                "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
                "direction_surface_hash": identity["direction_surface_hash"],
                "direction_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
                "model_risk_sizing_enabled": "1",
                "model_risk_min_pct": "0.004",
                "model_risk_max_pct": str(spec.model_risk_max_pct),
                "model_risk_confidence_floor": "0.58",
                "model_risk_confidence_ceiling": "0.99",
                "model_risk_fallback_lot": "0.08",
                "fixed_lot": str(spec.fixed_lot),
                "approx_validation_trades_per_day": val["trades_per_day"],
                "approx_oos_trades_per_day": oos["trades_per_day"],
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(manifest_row)
        artifacts.extend([payload_path, handoff_path, model_path])
    scoreboard.sort(key=lambda item: (item["design_gate"] == "passed", number(item["combined_estimated_net_profit"])), reverse=True)
    return branch_rows, scoreboard, supply_rows, manifest_rows, artifacts


def report_markdown(scoreboard: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run322A cp321B Curve Stability Pressure Materialization(322A cp321B 곡선 안정성 압박 물질화)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- candidates(후보): `{len(scoreboard)}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "",
        "Effect(효과): cp321B(321B 씨앗)를 exact replay(정확 재생), defensive threshold(방어 임계값), aggressive density(공격 밀도), source consensus/source swap(원천 합의/교체), volatility guard(변동성 방어)로 압박한다.",
        "",
        "| package(패키지) | lane(레인) | val net est(검증 추정 순익) | val t/day(검증 일거래) | val PF(검증 PF) | OOS net est(표본외 추정 순익) | OOS t/day(표본외 일거래) | OOS PF(표본외 PF) | design gate(설계 관문) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard:
        lines.append(
            "| {pkg} | {lane} | {vn:.2f} | {vtd:.2f} | {vpf:.2f} | {on:.2f} | {otd:.2f} | {opf:.2f} | {gate} |".format(
                pkg=row["package_id"],
                lane=row["branch_lane"],
                vn=number(row["validation_estimated_net_profit"]),
                vtd=number(row["validation_estimated_trades_per_day"]),
                vpf=number(row["validation_estimated_pf"]),
                on=number(row["oos_estimated_net_profit"]),
                otd=number(row["oos_estimated_trades_per_day"]),
                opf=number(row["oos_estimated_pf"]),
                gate=row["design_gate"],
            )
        )
    lines.extend(["", f"- next_action(다음 행동): `{NEXT_ACTION}`", "", f"`{BOUNDARY}`"])
    return "\n".join(lines)


def write_outputs(
    branch_rows: Sequence[Mapping[str, Any]],
    scoreboard: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    artifacts: Sequence[Path],
) -> list[Path]:
    write_csv(BRANCH_QUEUE, list(branch_rows[0].keys()), branch_rows)
    write_csv(MODEL_SCOREBOARD, list(scoreboard[0].keys()), scoreboard)
    write_csv(CANDIDATE_SUPPLY, list(supply_rows[0].keys()), supply_rows)
    write_csv(PAYLOAD_MANIFEST, list(manifest_rows[0].keys()), manifest_rows)
    write_csv(MT5_QUEUE, list(manifest_rows[0].keys()), manifest_rows)
    write_text(
        EXPERIMENT_DESIGN,
        json.dumps(
            {
                "run_id": RUN_ID,
                "hypothesis": "cp321B can become an ONNX-worthy(온엑스 가치 있음) candidate only if exact replay and at least one stability perturbation keep profit, density, and zoom-curve gates together.",
                "decision_use": "Decide whether Stage322 can select a candidate package for Adapter(어댑터) work or must discard cp321B as fragile.",
                "comparison_baseline": "Stage321 cp321B actual MT5 survivor seed and cp321C higher-net but OOS-pocket failure memory.",
                "control_variables": ["US100 M5", "Stage319/Stage321 runtime handoff path", "Tier A primary plus Tier B fallback routed MT5 path", "no ONNX before candidate package gate"],
                "changed_variables": ["score threshold", "D/B agreement", "B-only source swap", "volatility guard", "risk cap by lane"],
                "sample_scope": "validation_is and OOS routed MT5 scope inherited from Stage321.",
                "success_criteria": ["exact replay passes actual MT5 gates", "at least one perturbation passes actual MT5 gates", "4-10 trades/day", "no zoomed curve pocket collapse"],
                "failure_criteria": ["exact replay drifts", "all perturbations fail", "profit scale collapses", "weak segment or OOS pocket appears"],
                "invalid_conditions": ["missing payload lineage", "feature order mismatch", "MT5 KPI missing"],
                "stop_conditions": ["If exact replay fails, do not Adapter(어댑터) cp321B; open a fresh candidate rebuild stage.", "If exact passes but perturbations fail, treat cp321B as fragile and do not start ONNX(온엑스)."],
                "evidence_plan": [rel(MODEL_SCOREBOARD), rel(MT5_QUEUE), rel(CANDIDATE_SUPPLY), "run322B actual MT5 KPI", "run322C review"],
                "claim_boundary": BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )
    write_text(
        DATA_RECEIPT,
        json.dumps(
            {
                "run_id": RUN_ID,
                "source_stage321_review": rel(SOURCE_STAGE321_REVIEW),
                "source_survivor_package": rel(SOURCE_SURVIVOR_PACKAGE),
                "source_stage321_scoreboard": rel(SOURCE_STAGE321_SCOREBOARD),
                "source_stage321_shape": rel(SOURCE_STAGE321_SHAPE),
                "stage319_source_manifest": rel(s321.SOURCE_MANIFEST),
                "feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
                "rows": {"branch_rows": len(branch_rows), "scoreboard_rows": len(scoreboard), "manifest_rows": len(manifest_rows)},
                "claim_boundary": BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )
    write_csv(
        RESULT_JUDGMENT,
        ("run_id", "status", "judgment", "selected_candidate", "adapter_package", "onnx_readiness", "next_action", "claim_boundary"),
        [{"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "next_action": NEXT_ACTION, "claim_boundary": BOUNDARY}],
    )
    write_csv(
        GATE_AUDIT,
        ("gate_name", "status", "evidence_path", "effect"),
        [
            {"gate_name": "fresh_stability_thesis(새 안정성 논제)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "Exact replay(정확 재생)와 perturbation(교란)을 함께 만들어 cp321B fragile/robust(취약/강건)을 분리한다."},
            {"gate_name": "source_lineage(원천 계보)", "status": "passed", "evidence_path": rel(DATA_RECEIPT), "effect": "Stage321(321단계) 생존 씨앗과 Stage319(319단계) payload(페이로드) 원천을 연결한다."},
            {"gate_name": "candidate_materialization(후보 물질화)", "status": "passed", "evidence_path": rel(PAYLOAD_MANIFEST), "effect": "payload(페이로드), handoff(인계), MT5 queue(MT5 대기열)를 만든다."},
            {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "actual MT5(실제 메타트레이더5) 안정성 검토 전에는 Adapter(어댑터)를 시작하지 않는다."},
            {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "선택 후보가 없으므로 ONNX(온엑스)를 시작하지 않는다."},
        ],
    )
    write_text(
        RUN_MANIFEST,
        json.dumps(
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "candidate_rows": len(scoreboard),
                "mt5_queue_rows": len(manifest_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_started",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
                "claim_boundary": BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )
    write_text(
        LINEAGE,
        json.dumps(
            {
                "run_id": RUN_ID,
                "producer": rel(PRODUCER),
                "source_artifacts": [rel(SOURCE_STAGE321_REVIEW), rel(SOURCE_SURVIVOR_PACKAGE), rel(SOURCE_STAGE321_SCOREBOARD), rel(SOURCE_STAGE321_SHAPE), rel(s321.SOURCE_MANIFEST)],
                "output_artifacts": [rel(path) for path in [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, *artifacts]],
                "claim_boundary": BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )
    write_text(REPORT, report_markdown(scoreboard))
    return [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, *artifacts]


def update_docs(scoreboard: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = drop_prefixed_lines(selected, ("- run322A_report(", "- run322A_mt5_queue("))
    selected = selected.rstrip() + f"\n- run322A_report(322A 보고서): `{rel(REPORT)}`\n- run322A_mt5_queue(322A MT5 대기열): `{rel(MT5_QUEUE)}`\n"
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index = drop_prefixed_lines(review_index, ("- run322A_report(", "- run322A_scoreboard(", "- run322A_mt5_queue("))
    review_index = review_index.rstrip() + f"\n- run322A_report(322A 보고서): `{rel(REPORT)}`\n- run322A_scoreboard(322A 점수판): `{rel(MODEL_SCOREBOARD)}`\n- run322A_mt5_queue(322A MT5 대기열): `{rel(MT5_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(current, "run322A_summary", f"- run322A_summary(322A 요약): cp321B(321B 씨앗) stability pressure(안정성 압박) 후보 `{len(scoreboard)}`개를 materialized(물질화)했다. Effect(효과): exact replay(정확 재생)와 perturbation(교란) MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.")
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = prepend_focus(
        workspace,
        f"- >-\n  Stage322(322단계) run322A(322A 실행) cp321B curve stability pressure materialization(cp321B 곡선 안정성 압박 물질화) `{RUN_ID}`. Effect(효과): candidates(후보) `{len(scoreboard)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n",
        RUN_ID,
    )
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run322A cp321B curve stability pressure materialization(322A cp321B 곡선 안정성 압박 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): candidates(후보) `{len(scoreboard)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었다.\n",
    )
    write_text(CHANGELOG, changelog)


def update_registers(paths: Sequence[Path], scoreboard: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    safe_upsert(RUN_REGISTRY, s321.s320.r309.RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "cp321b_curve_stability_pressure_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"candidates={len(scoreboard)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}."}], "run_id")
    safe_upsert(ALPHA_LEDGER, s321.s320.ledger.ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": SOURCE_RUN_ID, "record_view": "cp321b_curve_stability_pressure_materialization", "tier_scope": "Tier A/Tier B paired", "kpi_scope": "design_estimate_actual_replay", "scoreboard_lane": "onnx_candidate_campaign", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "primary_kpi": f"candidates={len(scoreboard)};mt5_queue_rows={len(manifest_rows)}", "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_started", "external_verification_status": "not_started", "notes": f"next_action={NEXT_ACTION}."}], "ledger_row_id")
    safe_upsert(STAGE_LEDGER, s321.s320.r309.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "cp321b_curve_stability_pressure_materialization", "tier_scope": "Tier A/Tier B paired", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "research_development_only_no_onnx", "report_path": rel(REPORT), "notes": f"next_action={NEXT_ACTION}."}], "row_id")
    idea = read_text(IDEA_REGISTER)
    idea = append_once(
        idea,
        RUN_ID,
        f"## {RUN_ID} cp321B curve stability pressure(cp321B 곡선 안정성 압박)\n\n- idea_id(아이디어 ID): `stage322_cp321b_curve_stability_pressure`\n- hypothesis(가설): cp321B(321B 씨앗)는 exact replay(정확 재생)와 threshold/source/risk perturbation(임계값/원천/위험 교란)을 견뎌야 Adapter(어댑터)로 넘길 가치가 있다.\n- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.\n",
    )
    write_text(IDEA_REGISTER, idea)
    rows = []
    created_at = utc_now()
    for path in paths:
        if not s321.s320.r309.path_exists(path):
            continue
        rows.append({"artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}", "artifact_type": "stage322_cp321b_curve_stability_pressure_artifact", "path": rel(path), "sha256": sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": "Stage322 materialization artifact"})
    safe_upsert(ARTIFACT_REGISTRY, s321.s320.r309.ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    branch_rows, scoreboard, supply_rows, manifest_rows, artifacts = build_outputs()
    outputs = write_outputs(branch_rows, scoreboard, supply_rows, manifest_rows, artifacts)
    update_docs(scoreboard, manifest_rows)
    update_registers(outputs, scoreboard, manifest_rows)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "candidate_rows": len(scoreboard),
                "mt5_queue_rows": len(manifest_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_started",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
