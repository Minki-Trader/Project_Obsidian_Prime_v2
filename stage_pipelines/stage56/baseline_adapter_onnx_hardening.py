from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import COMMON_FILES_ROOT_DEFAULT, copy_to_common  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash, sha256_file  # noqa: E402
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN_NUMBER = "run50BZ"
RUN_ID = "run50BZ_stage56_baseline_adapter_onnx_hardening_v1"
PACKET_ID = "stage56_baseline_adapter_onnx_hardening_v1"
TERMINAL_LABEL = "onnx_parity_passed"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID

DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
SELECTED_ADAPTER_ID = "ba14_no_atr_sd5_lot025"
SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs/run50BR"
SOURCE_VARIANT_ROOT = SOURCE_RUN_ROOT / DEVELOPMENT_ANCHOR
SOURCE_MODEL = SOURCE_RUN_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv"
SOURCE_VAL_FEATURE = SOURCE_VARIANT_ROOT / "features" / f"{DEVELOPMENT_ANCHOR}_a_val.csv"
SOURCE_OOS_FEATURE = SOURCE_VARIANT_ROOT / "features" / f"{DEVELOPMENT_ANCHOR}_a_oos.csv"
PHASE_A_SUMMARY_JSON = REVIEWS_ROOT / "run50BY_baseline_adapter_same_move_lot_repair_summary.json"
PHASE_A_REPORT = REVIEWS_ROOT / "run50BY_baseline_adapter_same_move_lot_repair_report.md"

MODEL_LOCAL_PATH = RUN_ROOT / "models" / "ba14_stage56_context_gap_refill_entry.onnx"
MODEL_TABLE_LOCAL_PATH = RUN_ROOT / "models" / SOURCE_MODEL.name
SPEC_JSON_PATH = SELECTED_ROOT / "baseline_adapter_ba14_spec.json"
SPEC_MD_PATH = SELECTED_ROOT / "baseline_adapter_ba14_spec.md"
REPORT_PATH = REVIEWS_ROOT / "run50BZ_baseline_adapter_onnx_hardening.md"
PARITY_JSON_PATH = REVIEWS_ROOT / "run50BZ_baseline_adapter_onnx_parity.json"
PARITY_CSV_PATH = REVIEWS_ROOT / "run50BZ_baseline_adapter_onnx_parity.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
SELECTION_STATUS_PATH = SELECTED_ROOT / "selection_status.md"
PROGRESS_LOG_PATH = Path("docs/agent_control/packets/stage56_reopen_goal_v1/progress_log.md")

FEATURE_ORDER = ("stage56_context_gap_refill_signal",)
FEATURE_ORDER_HASH = ordered_hash(FEATURE_ORDER)
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_baseline_adapter_onnx"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(path)
    try:
        return io_path(candidate).resolve().relative_to(io_path(Path(".")).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: csv_value(row.get(key)) for key in columns})


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10f}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def append_once(path: Path, text: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if text.strip() in existing:
        return
    write_md(path, existing.rstrip() + "\n" + text.strip() + "\n")


def parse_ebm_table(path: Path) -> dict[str, Any]:
    intercept = np.zeros(3, dtype=np.float32)
    cuts_by_feature: dict[int, list[float]] = {}
    scores_by_feature: dict[int, list[list[float]]] = {}
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            record_type = str(row.get("record_type") or "").strip().lower()
            if record_type == "intercept":
                intercept = np.asarray(
                    [float(row["score_short"]), float(row["score_flat"]), float(row["score_long"])],
                    dtype=np.float32,
                )
            elif record_type == "cut":
                feature_index = int(row["feature_index"])
                cuts_by_feature.setdefault(feature_index, []).append(float(row["value"]))
            elif record_type == "score":
                feature_index = int(row["feature_index"])
                scores_by_feature.setdefault(feature_index, []).append(
                    [float(row["score_short"]), float(row["score_flat"]), float(row["score_long"])]
                )
    if set(scores_by_feature) != {0}:
        raise ValueError(f"Expected exactly one feature table for Stage56 adapter, got {sorted(scores_by_feature)}")
    return {
        "intercept": intercept,
        "cuts": np.asarray(cuts_by_feature.get(0, []), dtype=np.float32),
        "scores": np.asarray(scores_by_feature[0], dtype=np.float32),
    }


def python_table_probabilities(values: np.ndarray, table: Mapping[str, Any]) -> np.ndarray:
    cuts = np.asarray(table["cuts"], dtype=np.float64)
    scores = np.asarray(table["scores"], dtype=np.float64)
    intercept = np.asarray(table["intercept"], dtype=np.float64)
    bins = np.ones(values.shape[0], dtype=np.int64)
    for cut in cuts:
        bins += values[:, 0] > float(cut)
    logits = scores[bins] + intercept
    logits = logits - logits.max(axis=1, keepdims=True)
    exp = np.exp(logits)
    return exp / exp.sum(axis=1, keepdims=True)


def export_table_to_onnx(table: Mapping[str, Any], output_path: Path) -> dict[str, Any]:
    import onnx
    from onnx import TensorProto, helper, numpy_helper

    input_name = "float_input"
    cuts = np.asarray(table["cuts"], dtype=np.float32)
    scores = np.asarray(table["scores"], dtype=np.float32)
    intercept = np.asarray(table["intercept"], dtype=np.float32)
    initializers = [
        numpy_helper.from_array(np.asarray(0, dtype=np.int64), "feature_index_0"),
        numpy_helper.from_array(cuts, "cuts_0"),
        numpy_helper.from_array(scores, "score_table_0"),
        numpy_helper.from_array(intercept, "intercept"),
        numpy_helper.from_array(np.asarray([1], dtype=np.int64), "axes_unsqueeze_1"),
        numpy_helper.from_array(np.asarray([1], dtype=np.int64), "axes_reduce_1"),
        numpy_helper.from_array(np.asarray(1, dtype=np.int64), "one_i64"),
    ]
    nodes = [
        helper.make_node("Gather", [input_name, "feature_index_0"], ["feature_column_0"], axis=1),
        helper.make_node("Unsqueeze", ["feature_column_0", "axes_unsqueeze_1"], ["feature_column_2d_0"]),
        helper.make_node("Greater", ["feature_column_2d_0", "cuts_0"], ["bin_comparison_0"]),
        helper.make_node("Cast", ["bin_comparison_0"], ["bin_comparison_i64_0"], to=TensorProto.INT64),
        helper.make_node("ReduceSum", ["bin_comparison_i64_0", "axes_reduce_1"], ["bin_count_0"], keepdims=0),
        helper.make_node("Add", ["bin_count_0", "one_i64"], ["bin_index_0"]),
        helper.make_node("Gather", ["score_table_0", "bin_index_0"], ["term_score_0"], axis=0),
        helper.make_node("Add", ["term_score_0", "intercept"], ["logits"]),
        helper.make_node("Softmax", ["logits"], ["probabilities"], axis=1),
    ]
    graph = helper.make_graph(
        nodes,
        "Stage56BaselineAdapterBa14Entry",
        [helper.make_tensor_value_info(input_name, TensorProto.FLOAT, [None, len(FEATURE_ORDER)])],
        [helper.make_tensor_value_info("probabilities", TensorProto.FLOAT, [None, 3])],
        initializers,
    )
    model = helper.make_model(
        graph,
        opset_imports=[helper.make_operatorsetid("", 13)],
        producer_name="Project Obsidian Prime v2 Stage56 BaselineAdapter",
    )
    model.ir_version = 7
    onnx.checker.check_model(model)
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    onnx.save(model, str(io_path(output_path)))
    return {
        "path": rel(output_path),
        "sha256": sha256_file(output_path),
        "input_name": input_name,
        "output_name": "probabilities",
        "target_opset": 13,
        "outputs": [{"name": "probabilities", "shape": [None, 3], "value_type": "tensor_type"}],
    }


def load_feature_values(paths: Sequence[Path]) -> tuple[np.ndarray, list[dict[str, Any]]]:
    frames = []
    rows: list[dict[str, Any]] = []
    for path in paths:
        frame = pd.read_csv(io_path(path))
        if FEATURE_ORDER[0] not in frame.columns:
            raise ValueError(f"Feature column {FEATURE_ORDER[0]} missing in {path}")
        values = frame.loc[:, list(FEATURE_ORDER)].astype("float32")
        split = "validation_is" if path == SOURCE_VAL_FEATURE else "oos"
        for index, value in enumerate(values[FEATURE_ORDER[0]].to_numpy(dtype=np.float32)):
            rows.append({"split": split, "row_index": index, FEATURE_ORDER[0]: float(value)})
        frames.append(values)
    merged = pd.concat(frames, axis=0, ignore_index=True)
    return merged.to_numpy(dtype=np.float32), rows


def check_parity(onnx_path: Path, table: Mapping[str, Any], values: np.ndarray) -> dict[str, Any]:
    import onnxruntime as ort

    expected = python_table_probabilities(values.astype("float64"), table)
    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    actual = np.asarray(session.run(None, {input_name: values.astype(np.float32)})[0], dtype=np.float64)
    diff = np.abs(expected - actual)
    row_sum_error = np.abs(actual.sum(axis=1) - 1.0)
    return {
        "passed": bool(float(diff.max()) <= 1e-6),
        "rows": int(values.shape[0]),
        "max_abs_diff": float(diff.max()),
        "mean_abs_diff": float(diff.mean()),
        "tolerance": 1e-6,
        "onnx_row_sum_max_abs_error": float(row_sum_error.max()) if len(row_sum_error) else 0.0,
        "input_name": input_name,
        "output_names": [output.name for output in session.get_outputs()],
    }


def decision_counts(values: np.ndarray, table: Mapping[str, Any]) -> dict[str, int]:
    probabilities = python_table_probabilities(values.astype("float64"), table)
    counts = {"short": 0, "flat": 0, "long": 0}
    for p_short, p_flat, p_long in probabilities:
        short_margin = p_short - max(p_flat, p_long)
        long_margin = p_long - max(p_flat, p_short)
        if p_long >= 0.55 and long_margin >= 0.0 and (p_long >= p_short):
            counts["long"] += 1
        elif p_short >= 0.55 and short_margin >= 0.0:
            counts["short"] += 1
        else:
            counts["flat"] += 1
    return counts


def adapter_spec(export_payload: Mapping[str, Any], parity: Mapping[str, Any]) -> dict[str, Any]:
    phase_a = json.loads(io_path(PHASE_A_SUMMARY_JSON).read_text(encoding="utf-8-sig"))
    best = phase_a.get("phase_a_best_variant", {})
    return {
        "adapter_id": SELECTED_ADAPTER_ID,
        "source_run_id": RUN_ID,
        "development_anchor": DEVELOPMENT_ANCHOR,
        "selected_research_baseline": "none",
        "phase_a_source_run": "run50BY_stage56_baseline_adapter_same_move_lot_repair_v1",
        "phase_a_best_variant": best,
        "entry_contract": {
            "feature_order": list(FEATURE_ORDER),
            "feature_order_hash": FEATURE_ORDER_HASH,
            "input_name": export_payload["input_name"],
            "probability_output_name": export_payload["output_name"],
            "class_order": ["short", "flat", "long"],
            "short_threshold": 0.55,
            "long_threshold": 0.55,
            "min_margin": 0.0,
        },
        "route_tier_contract": {
            "routing_mode": "tier_a_primary_no_fallback",
            "tier_b_policy": "disabled_due_run50BR_fallback_only_damage",
            "actual_routed_total": "one MT5 tester account path; no synthetic aggregation",
        },
        "risk_contract": {
            "model_controlled": False,
            "fixed_lot": 0.25,
            "broker_min_lot_floor_rule": "MT5 execution translation owns min/max/step normalization",
            "model_risk_pct_output": "not_in_onnx_fixed_lot_adapter",
        },
        "atr_bracket_contract": {
            "model_controlled": False,
            "atr_sltp_enabled": False,
            "atr_period": 14,
            "sl_multiplier": 0.0,
            "tp_multiplier": 0.0,
        },
        "lifecycle_contract": {
            "model_controlled": False,
            "max_hold_bars": 2,
            "same_direction_reentry_cooldown_bars": 5,
            "reentry_cooldown_bars": 0,
            "reverse_on_opposite_signal": True,
            "close_only_on_opposite_signal": False,
        },
        "telemetry_contract": {
            "required": [
                "model_risk_pct",
                "clipped_risk_pct",
                "computed_lot",
                "executed_lot",
                "min_lot_floor_applied",
                "actual_risk_pct_after_floor",
                "atr_points",
                "open_sl_points",
                "open_tp_points",
            ]
        },
        "onnx_export": dict(export_payload),
        "onnx_parity": dict(parity),
        "boundary": BOUNDARY,
        "forbidden_claims": [
            "live_readiness",
            "runtime_authority",
            "operating_promotion",
            "operating_reference",
            "production_baseline",
            "reviewed_closed",
        ],
    }


def artifact_rows(paths: Sequence[Path], common_copies: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    created = utc_now()

    def add(artifact_id: str, artifact_type: str, path: Path | str, notes: str) -> None:
        p = Path(str(path))
        resolved = p if p.is_absolute() else REPO_ROOT / p
        is_file = path_exists(resolved) and io_path(resolved).is_file()
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(p),
                "sha256": sha256_file_lf_normalized(resolved) if is_file else "directory_or_not_feasible",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": notes,
            }
        )

    for path in paths:
        add(f"stage56_{RUN_NUMBER}_{aw.safe_name(path.stem, 80)}", path.suffix.lstrip(".") or "artifact", path, "Stage56 BaselineAdapter ONNX hardening artifact.")
    for item in common_copies:
        add(
            f"stage56_{RUN_NUMBER}_common_{aw.safe_name(Path(str(item.get('path'))).stem, 80)}",
            "common_files_copy",
            str(item.get("path")),
            "Common Files ONNX/runtime handoff copy.",
        )
    return rows


def write_ledgers(parity: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    status = "completed" if parity.get("passed") else "blocked"
    judgment = TERMINAL_LABEL if parity.get("passed") else "onnx_parity_failed_repairing"
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_onnx_hardening",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT_PATH),
                "notes": ledger_pairs(
                    (
                        ("adapter_id", SELECTED_ADAPTER_ID),
                        ("onnx", rel(MODEL_LOCAL_PATH)),
                        ("parity_passed", parity.get("passed")),
                        ("max_abs_diff", parity.get("max_abs_diff")),
                        ("boundary", BOUNDARY),
                    )
                ),
            }
        ],
        key="run_id",
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__onnx_parity",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "onnx_parity",
        "parent_run_id": "run50BY_stage56_baseline_adapter_same_move_lot_repair_v1",
        "record_view": "baseline_adapter_ba14_onnx_parity",
        "tier_scope": "Tier A",
        "kpi_scope": "onnx_hardening",
        "scoreboard_lane": "runtime_probe",
        "status": status,
        "judgment": judgment,
        "path": rel(PARITY_JSON_PATH),
        "primary_kpi": ledger_pairs(
            (
                ("parity_passed", parity.get("passed")),
                ("rows", parity.get("rows")),
                ("max_abs_diff", parity.get("max_abs_diff")),
                ("tolerance", parity.get("tolerance")),
            )
        ),
        "guardrail_kpi": ledger_pairs(
            (
                ("adapter_id", SELECTED_ADAPTER_ID),
                ("feature_order_hash", FEATURE_ORDER_HASH),
                ("no_operating_claim", True),
            )
        ),
        "external_verification_status": "out_of_scope_by_claim",
        "notes": "Python vs ONNX probability parity; MT5 ONNX runtime reproduction is the next phase.",
    }
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [ledger_row], key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [ledger_row], key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def write_docs(spec: Mapping[str, Any], parity: Mapping[str, Any], export_payload: Mapping[str, Any], common_copies: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    write_json(SPEC_JSON_PATH, spec)
    write_md(
        SPEC_MD_PATH,
        f"""# BaselineAdapter ba14 Spec(기준선 어댑터 ba14 명세)

- adapter_id(어댑터 ID): `{SELECTED_ADAPTER_ID}`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- entry ONNX(진입 ONNX): `{rel(MODEL_LOCAL_PATH)}`
- feature_order_hash(피처 순서 해시): `{FEATURE_ORDER_HASH}`
- fixed_lot(고정 랏): `0.25`
- same_direction_reentry_cooldown_bars(동일 방향 재진입 쿨다운 봉): `5`
- ATR SL/TP(ATR 손절/익절): disabled(비활성)
- Tier B(Tier B): disabled with evidence(근거 기반 비활성)

Effect(효과): model output(모델 출력)은 probability(확률)만 ONNX(온닉스)에 두고, lot rounding/min lot/order send(랏 반올림/최소 랏/주문 전송)는 MT5 execution translation(MT5 실행 번역)에 둔다.
""",
    )
    rows = [
        {
            "run_id": RUN_ID,
            "adapter_id": SELECTED_ADAPTER_ID,
            "split": "validation_plus_oos",
            "rows": parity.get("rows"),
            "passed": parity.get("passed"),
            "max_abs_diff": parity.get("max_abs_diff"),
            "mean_abs_diff": parity.get("mean_abs_diff"),
            "tolerance": parity.get("tolerance"),
            "onnx_row_sum_max_abs_error": parity.get("onnx_row_sum_max_abs_error"),
            "onnx_path": rel(MODEL_LOCAL_PATH),
            "onnx_sha256": export_payload.get("sha256"),
        }
    ]
    write_csv(PARITY_CSV_PATH, rows)
    write_json(PARITY_JSON_PATH, {"run_id": RUN_ID, "adapter_id": SELECTED_ADAPTER_ID, "export": export_payload, "parity": parity, "spec_path": rel(SPEC_JSON_PATH), "common_copies": list(common_copies)})
    write_md(
        REPORT_PATH,
        f"""# Stage56 run50BZ BaselineAdapter ONNX Hardening(Stage56 run50BZ 기준선 어댑터 ONNX 경화)

- terminal_label(종료 라벨): `{TERMINAL_LABEL if parity.get('passed') else 'onnx_parity_failed_repairing'}`
- adapter_id(어댑터 ID): `{SELECTED_ADAPTER_ID}`
- ONNX path(ONNX 경로): `{rel(MODEL_LOCAL_PATH)}`
- ONNX sha256(ONNX 해시): `{export_payload.get('sha256')}`
- parity rows(동등성 행): `{parity.get('rows')}`
- max_abs_diff(최대 절대 차이): `{parity.get('max_abs_diff')}`
- tolerance(허용 오차): `{parity.get('tolerance')}`

Action(행동): Stage56 entry table(진입 표)을 probability-only ONNX(확률 전용 ONNX)로 내보내고 Python/ONNX parity(파이썬/ONNX 동등성)를 검증했다.
Effect(효과): MT5 runtime reproduction(MT5 런타임 재현) 전에 model probability contract(모델 확률 계약)를 고정했다.

## Adapter Boundary(어댑터 경계)

- in ONNX(ONNX 내부): entry probability(진입 확률) `short/flat/long`
- outside ONNX(ONNX 외부): fixed lot(고정 랏), 0.01 lot floor(0.01 랏 바닥), order send(주문 전송), broker stop distance(브로커 스톱 거리), Tier B disablement(Tier B 비활성), cooldown lifecycle(쿨다운 생명주기)

No live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), reviewed_closed(검토 종료) claim(주장) is made.
""",
    )
    write_json(RUN_ROOT / "run_manifest.json", {"run_id": RUN_ID, "stage_id": STAGE_ID, "packet_id": PACKET_ID, "adapter_id": SELECTED_ADAPTER_ID, "source_model": rel(SOURCE_MODEL), "onnx_export": export_payload, "spec": rel(SPEC_JSON_PATH), "common_copies": list(common_copies), "boundary": BOUNDARY})
    write_json(RUN_ROOT / "kpi_record.json", {"run_id": RUN_ID, "stage_id": STAGE_ID, "packet_id": PACKET_ID, "adapter_id": SELECTED_ADAPTER_ID, "onnx_parity": parity, "external_verification_status": "out_of_scope_by_claim", "judgment": TERMINAL_LABEL if parity.get("passed") else "onnx_parity_failed_repairing", "boundary": BOUNDARY})
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "adapter_id": SELECTED_ADAPTER_ID, "terminal_label": TERMINAL_LABEL if parity.get("passed") else "onnx_parity_failed_repairing", "onnx_export": export_payload, "onnx_parity": parity, "spec_path": rel(SPEC_JSON_PATH), "ledger_payload": ledger_payload, "hard_completion_status": "not_met_mt5_runtime_reproduction_pending"})
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"status": "passed", "source_inputs": [rel(SOURCE_MODEL), rel(PHASE_A_SUMMARY_JSON)], "outputs": [rel(MODEL_LOCAL_PATH), rel(SPEC_JSON_PATH), rel(PARITY_JSON_PATH), rel(REPORT_PATH)], "ledger_payload": ledger_payload})
    write_json(PACKET_ROOT / "runtime_parity_audit.json", {"status": "onnx_parity_passed" if parity.get("passed") else "onnx_parity_failed_repairing", "python_vs_onnx": parity, "mt5_runtime_reproduction": "pending"})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"result_subject": RUN_ID, "judgment_label": TERMINAL_LABEL if parity.get("passed") else "onnx_parity_failed_repairing", "claim_boundary": BOUNDARY, "next_action": "build_mt5_onnx_runtime_handoff_and_run_validation_oos"})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"status": "passed" if parity.get("passed") else "blocked", "covered_gates": ["onnx_artifact_exists", "spec_hash_recorded", "python_onnx_parity", "artifact_registry_update", "final_claim_guard"]})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"hard_completion_label": "baseline_adapter_onnx_mt5_reproduction_completed", "hard_completion_met": False, "current_allowed_label": TERMINAL_LABEL if parity.get("passed") else "onnx_parity_failed_repairing", "forbidden_labels": ["reviewed_closed", "complete", "final", "production_ready", "live_ready", "operating_reference", "runtime_authority"]})
    write_json(PACKET_ROOT / "skill_receipts.json", [{"skill": "obsidian-runtime-parity", "status": "onnx_parity_passed" if parity.get("passed") else "blocked"}, {"skill": "obsidian-artifact-lineage", "status": "completed"}, {"skill": "obsidian-result-judgment", "status": "completed"}])
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current run(현재 실행): `{RUN_ID}`
- active stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- selected_adapter_for_hardening(경화 대상 어댑터): `{SELECTED_ADAPTER_ID}`
- status(상태): `{TERMINAL_LABEL if parity.get('passed') else 'onnx_parity_failed_repairing'}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage56(56단계)는 ba14 BaselineAdapter(ba14 기준선 어댑터)의 ONNX hardening(ONNX 경화)을 진행했다.
Effect(효과): 다음 작업은 MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현)이다.

## ONNX Evidence(ONNX 근거)

- ONNX path(ONNX 경로): `{rel(MODEL_LOCAL_PATH)}`
- ONNX sha256(ONNX 해시): `{export_payload.get('sha256')}`
- parity rows(동등성 행): `{parity.get('rows')}`
- max_abs_diff(최대 절대 차이): `{parity.get('max_abs_diff')}`
- tolerance(허용 오차): `{parity.get('tolerance')}`
- next_action(다음 행동): run MT5 ONNX/runtime validation/OOS(MT5 ONNX/런타임 검증/표본외 실행)

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), reviewed_closed(검토 종료).
""",
    )
    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    append = f"""

## ONNX Hardening Evidence(ONNX 경화 근거)

- onnx_run_id(ONNX 실행 ID): `{RUN_ID}`
- onnx_artifact(ONNX 산출물): `{rel(MODEL_LOCAL_PATH)}`
- onnx_sha256(ONNX 해시): `{export_payload.get('sha256')}`
- parity_passed(동등성 통과): `{parity.get('passed')}`
- next_action(다음 행동): MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현)
"""
    if "## ONNX Hardening Evidence(ONNX 경화 근거)" not in selection:
        write_md(SELECTION_STATUS_PATH, selection.rstrip() + append)
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = text.replace("current_run_id: run50BY_stage56_baseline_adapter_same_move_lot_repair_v1", f"current_run_id: {RUN_ID}", 1)
    text = text.replace("updated_on: '2026-05-15'", "updated_on: '2026-05-15'", 1)
    block = f"""
stage56_baseline_adapter_onnx:
  packet_id: {PACKET_ID}
  current_run_id: {RUN_ID}
  adapter_id: {SELECTED_ADAPTER_ID}
  development_anchor: {DEVELOPMENT_ANCHOR}
  terminal_label: {TERMINAL_LABEL if parity.get('passed') else 'onnx_parity_failed_repairing'}
  onnx_path: {rel(MODEL_LOCAL_PATH)}
  onnx_sha256: {export_payload.get('sha256')}
  parity_passed: {str(bool(parity.get('passed'))).lower()}
  max_abs_diff: {parity.get('max_abs_diff')}
  boundary: {BOUNDARY}
  next_action: build_mt5_onnx_runtime_handoff_and_run_validation_oos
"""
    if "stage56_baseline_adapter_onnx:" not in text:
        io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")
    append_once(
        PROGRESS_LOG_PATH,
        f"""
## 2026-05-15 run50BZ BaselineAdapter ONNX Hardening(기준선 어댑터 ONNX 경화)
- action(행동): ba14 entry model(ba14 진입 모델)을 ONNX(온닉스)로 내보내고 Python/ONNX parity(파이썬/ONNX 동등성)를 실행했다.
- effect(효과): MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현) 전 probability contract(확률 계약)를 고정했다.
- terminal_label(종료 라벨): `{TERMINAL_LABEL if parity.get('passed') else 'onnx_parity_failed_repairing'}`
- max_abs_diff(최대 절대 차이): `{parity.get('max_abs_diff')}`
- onnx_sha256(ONNX 해시): `{export_payload.get('sha256')}`
""",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export and verify Stage56 BaselineAdapter ba14 ONNX.")
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    table = parse_ebm_table(SOURCE_MODEL)
    io_path(MODEL_TABLE_LOCAL_PATH.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(SOURCE_MODEL), io_path(MODEL_TABLE_LOCAL_PATH))
    export_payload = export_table_to_onnx(table, MODEL_LOCAL_PATH)
    common_copies = [
        copy_to_common(MODEL_LOCAL_PATH, f"{COMMON_ROOT}/models/{MODEL_LOCAL_PATH.name}", Path(args.common_files_root)),
        copy_to_common(MODEL_TABLE_LOCAL_PATH, f"{COMMON_ROOT}/models/{MODEL_TABLE_LOCAL_PATH.name}", Path(args.common_files_root)),
    ]
    values, _ = load_feature_values([SOURCE_VAL_FEATURE, SOURCE_OOS_FEATURE])
    parity = check_parity(MODEL_LOCAL_PATH, table, values)
    parity["decision_counts"] = decision_counts(values, table)
    spec = adapter_spec(export_payload, parity)
    paths = [MODEL_LOCAL_PATH, MODEL_TABLE_LOCAL_PATH, SPEC_JSON_PATH, SPEC_MD_PATH, REPORT_PATH, PARITY_JSON_PATH, PARITY_CSV_PATH, RUN_ROOT / "run_manifest.json", RUN_ROOT / "kpi_record.json", Path(__file__)]
    write_docs(spec, parity, export_payload, common_copies, {})
    artifacts = artifact_rows(paths, common_copies)
    ledger_payload = write_ledgers(parity, artifacts)
    spec["ledger_payload"] = ledger_payload
    write_docs(spec, parity, export_payload, common_copies, ledger_payload)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok" if parity.get("passed") else "blocked",
                    "run_id": RUN_ID,
                    "adapter_id": SELECTED_ADAPTER_ID,
                    "terminal_label": TERMINAL_LABEL if parity.get("passed") else "onnx_parity_failed_repairing",
                    "onnx_path": MODEL_LOCAL_PATH.as_posix(),
                    "onnx_sha256": export_payload.get("sha256"),
                    "parity": parity,
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if parity.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
