from __future__ import annotations

import csv
import json
import math
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import COMMON_FILES_ROOT_DEFAULT, attempt_payload, copy_to_common
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import run267C_p1_axis_selection as p1_selection
from stage_pipelines.stage267 import run267C_p1_soft_axis_followup_materialization as p1_materialization


STAGE_ID = input_probe.STAGE_ID
RUN_ID = "run267D_stage267_adapter_p2_materialization_v1"
RUN_NUMBER = "run267D"
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY
STAGE_ROOT = input_probe.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
DESIGN_ROOT = RUN_ROOT / "adapter_p2_materialization"
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

INPUT_AXIS_SELECTION_PATH = p1_selection.SELECTION_MATRIX_PATH
INPUT_SHORTLIST_PATH = p1_selection.CANDIDATE_SHORTLIST_PATH
INPUT_FEATURE_MANIFEST_PATH = p1_materialization.FEATURE_VARIANT_MANIFEST_PATH
INPUT_P1_KPI_PATH = p1_materialization.P1_ROOT / "p1_soft_axis_kpi_summary.csv"

DESIGN_MATRIX_PATH = DESIGN_ROOT / "design.csv"
RUNTIME_CONTRACT_PATH = DESIGN_ROOT / "contract.csv"
ATTEMPT_MANIFEST_PATH = DESIGN_ROOT / "attempts.csv"
LINEAGE_PATH = DESIGN_ROOT / "lineage.json"
RESULT_PATH = DESIGN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267D_adapter_p2_materialization_report.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267D_adapter_p2_materialization.py")

STATUS = "run267D_adapter_p2_design_materialized_execution_pending"
NEXT_ACTION = "run267D_execute_adapter_prototype_and_p2_replacement_mt5_batch"
PERIOD_LABEL = input_probe.PERIOD_LABEL
COMMON_ROOT = "OPV2/s267d/run267D_adapter_p2"

AXIS_FOCUS = {
    "late21": {
        "role_scope": "adapter_prototype",
        "materialization_intent": "late21 adapter prototype(후반 21시 어댑터 원형)",
        "next_validation": "zoomed equity curve(확대 평가금 곡선); time-slice KPI(시간 구간 핵심 성과 지표); trade quality(거래 품질)",
    },
    "atrcomp": {
        "role_scope": "p2_replacement",
        "materialization_intent": "ATR compression replacement(ATR 압축 대체)",
        "next_validation": "replacement robustness(대체 견고성); signal retention cost(신호 유지 비용); DD watch(손실폭 관찰)",
    },
    "vlowadx": {
        "role_scope": "p2_replacement",
        "materialization_intent": "vol-low ADX replacement(낮은 변동성 ADX 대체)",
        "next_validation": "trade retention(거래 유지); shallow DD repair watch(얕은 손실폭 수리 관찰); feature dependency(피처 의존성)",
    },
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isinf(value):
            return "inf"
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def to_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def to_int(value: Any) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return 0


def copy_local(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"source": rel(source), "path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def selected_axis_rows() -> dict[str, dict[str, str]]:
    rows = {}
    for row in read_csv(INPUT_AXIS_SELECTION_PATH):
        axis = row.get("followup_variant_short", "")
        if axis in AXIS_FOCUS:
            rows[axis] = row
    missing = sorted(set(AXIS_FOCUS) - set(rows))
    if missing:
        raise RuntimeError(f"missing selected axis rows: {missing}")
    return rows


def feature_rows_by_pair() -> dict[tuple[str, str], dict[str, str]]:
    rows = {}
    for row in read_csv(INPUT_FEATURE_MANIFEST_PATH):
        rows[(row["candidate_alias"], row["followup_variant_id"])] = row
    return rows


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def p1_kpi_by_pair() -> dict[tuple[str, str, str], dict[str, str]]:
    rows = {}
    for row in read_csv(INPUT_P1_KPI_PATH):
        record_view = row.get("record_view", "")
        for axis in AXIS_FOCUS:
            marker = f"_{axis}_historical_2024"
            if marker in record_view:
                prefix = record_view.split(marker, 1)[0]
                alias = prefix.removeprefix("mt5_ta_").removeprefix("mt5_rt_")
                rows[(alias, axis, row.get("route_role", ""))] = row
                break
    return rows


def role_rank(row: Mapping[str, str]) -> tuple[int, float]:
    pair_role = row.get("pair_role", "")
    role_order = {
        "primary_adapter_probe_pair": 0,
        "adapter_control_pair": 1,
        "adapter_stress_or_anchor_pair": 2,
        "p2_replacement_pair": 3,
    }
    base = 9
    for key, value in role_order.items():
        if key in pair_role:
            base = value
            break
    return base, -to_float(row.get("p1_net_profit"))


def design_read(row: Mapping[str, Any]) -> str:
    axis = str(row["axis"])
    net = to_float(row.get("p1_net_profit"))
    pf = to_float(row.get("p1_pf"))
    dd = to_float(row.get("p1_dd_percent"))
    trades = to_int(row.get("p1_trade_count"))
    retention = to_float(row.get("signal_retention"))
    if axis == "late21" and net >= 170 and pf >= 1.10 and dd <= 27.0 and trades >= 300:
        return "adapter_probe_ready_not_selection(어댑터 탐침 준비, 선택은 아님)"
    if axis == "atrcomp" and net >= 240 and pf >= 1.14 and retention < 0.85:
        return "p2_net_strong_signal_cost_watch(2차 순수익 강함, 신호 비용 관찰)"
    if axis == "vlowadx" and retention >= 0.94 and dd >= 34.0:
        return "p2_retention_good_dd_watch(2차 유지율 좋음, 손실폭 관찰)"
    return "exploratory_pair_requires_runtime_review(탐색 쌍, 런타임 검토 필요)"


def build_design_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    axes = selected_axis_rows()
    features = feature_rows_by_pair()
    specs = specs_by_alias()
    kpi = p1_kpi_by_pair()
    selected = sorted(
        [row for row in read_csv(INPUT_SHORTLIST_PATH) if row.get("followup_variant_short") in AXIS_FOCUS],
        key=role_rank,
    )
    design_rows: list[dict[str, Any]] = []
    contract_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    lineage: list[dict[str, Any]] = []
    for row_index, row in enumerate(selected, start=1):
        alias = row["candidate_alias"]
        axis = row["followup_variant_short"]
        axis_meta = AXIS_FOCUS[axis]
        variant_id = row["followup_variant_id"]
        feature = features[(alias, variant_id)]
        spec = specs[alias]
        local_root = DESIGN_ROOT / axis_meta["role_scope"] / axis / alias
        copied_feature = copy_local(Path(feature["feature_file"]), local_root / "features" / Path(feature["feature_file"]).name)
        copied_model = copy_local(Path(feature["model_file"]), local_root / "models" / Path(feature["model_file"]).name)
        common_feature_path = f"{COMMON_ROOT}/{axis}/{alias}/features/{Path(copied_feature['path']).name}"
        common_model_path = f"{COMMON_ROOT}/{axis}/{alias}/models/{Path(copied_model['path']).name}"
        common_feature = copy_to_common(Path(copied_feature["path"]), common_feature_path, COMMON_FILES_ROOT_DEFAULT)
        common_model = copy_to_common(Path(copied_model["path"]), common_model_path, COMMON_FILES_ROOT_DEFAULT)
        lineage.extend(
            [
                {
                    "candidate_alias": alias,
                    "axis": axis,
                    "artifact_role": "feature_csv",
                    "source_path": feature["feature_file"],
                    "run267d_path": copied_feature["path"],
                    "common_path": common_feature_path,
                    "source_sha256": feature["feature_sha256"],
                    "run267d_sha256": copied_feature["sha256"],
                    "common_sha256": common_feature["sha256"],
                },
                {
                    "candidate_alias": alias,
                    "axis": axis,
                    "artifact_role": "model_csv",
                    "source_path": feature["model_file"],
                    "run267d_path": copied_model["path"],
                    "common_path": common_model_path,
                    "source_sha256": feature["model_sha256"],
                    "run267d_sha256": copied_model["sha256"],
                    "common_sha256": common_model["sha256"],
                },
            ]
        )
        routed_kpi = kpi.get((alias, axis, "routed_total"), {})
        tier_kpi = kpi.get((alias, axis, "tier_only_total"), {})
        design_row = {
            "candidate_alias": alias,
            "candidate_role": row["candidate_role"],
            "axis": axis,
            "role_scope": axis_meta["role_scope"],
            "pair_role": row["pair_role"],
            "materialization_intent": axis_meta["materialization_intent"],
            "axis_decision": row["axis_decision"],
            "axis_avg_net_delta": axes[axis]["avg_net_profit_delta"],
            "axis_avg_pf_delta": axes[axis]["avg_pf_delta"],
            "axis_avg_trade_delta": axes[axis]["avg_trade_count_delta"],
            "axis_avg_dd_delta": axes[axis]["avg_dd_percent_delta"],
            "p1_net_profit": row["p1_net_profit"],
            "p1_pf": row["p1_pf"],
            "p1_trade_count": row["p1_trade_count"],
            "p1_dd_percent": row["p1_dd_percent"],
            "p1_expectancy": routed_kpi.get("expectancy", ""),
            "p1_recovery_factor": routed_kpi.get("recovery_factor", ""),
            "signal_retention": feature["signal_retention"],
            "blocked_signal_rows": feature["blocked_signal_rows"],
            "kept_signal_rows": feature["kept_signal_rows"],
            "feature_order_hash": feature["feature_order_hash"],
            "run267d_feature_file": copied_feature["path"],
            "run267d_model_file": copied_model["path"],
            "common_feature_path": common_feature_path,
            "common_model_path": common_model_path,
            "design_read": "",
            "next_validation": axis_meta["next_validation"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
        design_row["design_read"] = design_read(design_row)
        design_rows.append(design_row)
        contract_rows.append(
            {
                "candidate_alias": alias,
                "axis": axis,
                "role_scope": axis_meta["role_scope"],
                "shared_contract": "feature_order;thresholds;model_csv;MT5 runtime settings;2024 historical stress window",
                "feature_count": 3,
                "feature_order": feature["feature_order"],
                "feature_order_hash": feature["feature_order_hash"],
                "model_backend": "ebm_table",
                "short_threshold": spec.variant.short_threshold,
                "long_threshold": spec.variant.long_threshold,
                "min_margin": 0.0,
                "max_hold_bars": spec.variant.max_hold_bars,
                "close_on_flat_signal": spec.variant.close_on_flat_signal,
                "reverse_on_opposite_signal": spec.variant.reverse_on_opposite_signal,
                "close_only_on_opposite_signal": spec.variant.close_only_on_opposite_signal,
                "tier_a_p1_net": tier_kpi.get("net_profit", ""),
                "routed_p1_net": routed_kpi.get("net_profit", ""),
                "known_differences": "run267D copies run267C P1 selected feature/model artifacts under adapter lineage; decision logic unchanged until execution.",
                "runtime_claim_boundary": "research_only_runtime_execution_pending",
            }
        )
        for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
            (
                (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{alias}_{axis}", "ta"),
                (input_probe.mt5.TIER_AB, "routed_total", f"mt5_rt_{alias}_{axis}", "rt"),
            ),
            start=1,
        ):
            magic = 26750000 + row_index * 10 + role_index
            payload = attempt_payload(
                run_root=DESIGN_ROOT,
                run_id=RUN_ID,
                stage_number=267,
                exploration_label=f"stage267_AdapterP2__{axis}",
                attempt_name=f"{alias}_{axis}_{attempt_token}_2024",
                tier=tier,
                split=PERIOD_LABEL,
                model_path=common_model_path,
                model_id=f"{RUN_ID}_{alias}_{variant_id}_adapter_p2_2024",
                model_backend="ebm_table",
                feature_path=common_feature_path,
                feature_count=3,
                feature_order_hash=str(feature["feature_order_hash"]),
                short_threshold=spec.variant.short_threshold,
                long_threshold=spec.variant.long_threshold,
                min_margin=0.0,
                invert_signal=False,
                from_date="2024.01.02",
                to_date="2025.01.01",
                primary_active_tier="tier_a",
                attempt_role=attempt_role,
                record_view_prefix=prefix,
                max_hold_bars=spec.variant.max_hold_bars,
                common_root=f"{COMMON_ROOT}/{axis}/{alias}",
                fallback_enabled=False,
                close_on_flat_signal=spec.variant.close_on_flat_signal,
                reverse_on_opposite_signal=spec.variant.reverse_on_opposite_signal,
                close_only_on_opposite_signal=spec.variant.close_only_on_opposite_signal,
                extra_set_values=input_probe.base_extra_set_values(spec, magic),
            )
            payload.update(
                {
                    "candidate_alias": alias,
                    "candidate_role": row["candidate_role"],
                    "axis": axis,
                    "role_scope": axis_meta["role_scope"],
                    "axis_decision": row["axis_decision"],
                    "execution_status": "not_executed",
                }
            )
            attempts.append(payload)
    return design_rows, contract_rows, attempts, lineage


def attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "axis": attempt.get("axis"),
                "role_scope": attempt.get("role_scope"),
                "axis_decision": attempt.get("axis_decision"),
                "attempt_name": attempt.get("attempt_name"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "ini_sha256": attempt.get("ini", {}).get("sha256"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "fallback_enabled": attempt.get("fallback_enabled", False),
                "execution_status": attempt.get("execution_status", "not_executed"),
            }
        )
    return rows


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise ValueError(f"missing replacement text: {old}")
    return text.replace(old, new, 1)


def append_after(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise ValueError(f"missing anchor: {anchor}")
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def update_ledgers(created_at: str, design_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> None:
    stage_row = {
        "row_id": "stage267_run267D_adapter_p2_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "adapter_p2_materialization",
        "tier_scope": "Tier A and Tier A+B historical 2024 adapter/P2 attempts planned",
        "scoreboard": "experiment_materialization",
        "status": STATUS,
        "judgment": "materialized_execution_pending_no_candidate_selection",
        "evidence_boundary": "adapter_p2_design_materialized_no_mt5_kpi_yet_not_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"design_rows={len(design_rows)};attempts={len(attempts)};next_action={NEXT_ACTION}.",
    }
    stage_rows = [row for row in read_csv(STAGE_LEDGER_PATH) if row.get("row_id") != stage_row["row_id"]]
    stage_rows.append(stage_row)
    write_csv(
        STAGE_LEDGER_PATH,
        stage_rows,
        (
            "row_id",
            "stage_id",
            "run_id",
            "view",
            "tier_scope",
            "scoreboard",
            "status",
            "judgment",
            "evidence_boundary",
            "report_path",
            "notes",
        ),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_adapter_p2_materialization",
            "status": STATUS,
            "judgment": "materialized_execution_pending_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"Run267D adapter/P2 design materialized; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__adapter_p2_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "adapter_p2_materialization",
            "parent_run_id": RUN_ID,
            "record_view": "adapter_p2_materialization",
            "tier_scope": "Tier A and Tier A+B historical 2024 adapter/P2 attempts planned",
            "kpi_scope": "materialization_only",
            "scoreboard_lane": "experiment_materialization",
            "status": STATUS,
            "judgment": "materialized_execution_pending_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"design_rows={len(design_rows)};attempts={len(attempts)}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;mt5_execution=pending",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": f"Next action: {NEXT_ACTION}.",
        },
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "subrun_id",
            "parent_run_id",
            "record_view",
            "tier_scope",
            "kpi_scope",
            "scoreboard_lane",
            "status",
            "judgment",
            "path",
            "primary_kpi",
            "guardrail_kpi",
            "external_verification_status",
            "notes",
        ),
    )
    entries = (
        ("stage267_run267D_adapter_p2_materializer", "producer_script", PRODUCER_PATH, "Builds run267D adapter/P2 materialization."),
        ("stage267_run267D_adapter_p2_design_matrix", "design_matrix", DESIGN_MATRIX_PATH, "Adapter prototype and P2 replacement design matrix."),
        ("stage267_run267D_adapter_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract for selected adapter/P2 pairs."),
        ("stage267_run267D_adapter_p2_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "MT5 set/ini attempt manifest for run267D."),
        ("stage267_run267D_adapter_p2_lineage", "artifact_lineage", LINEAGE_PATH, "Feature/model artifact lineage for run267D."),
        ("stage267_run267D_adapter_p2_result", "review_result", RESULT_PATH, "JSON result for run267D materialization."),
        ("stage267_run267D_adapter_p2_report", "review_report", REPORT_PATH, "User-facing run267D materialization report."),
    )
    rows = read_csv(ARTIFACT_REGISTRY_PATH)
    new_rows = []
    for artifact_id, artifact_type, path, notes in entries:
        new_rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    replacement = {row["artifact_id"]: row for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement]
    merged.extend(new_rows)
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_current_truth_docs() -> None:
    report_line_current = "- Stage267(267단계) run267D Adapter/P2 materialization(어댑터/2차 대체 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267D_adapter_p2_materialization_report.md`"
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_once(current, "- current_run(현재 실행): `run267C_stage267_execute_prioritized_ablation_replacement_variants_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_once(current, "- status(상태): `run267C_p1_axis_selection_completed`", f"- status(상태): `{STATUS}`")
    current = append_after(
        current,
        "- Stage267(267단계) run267C P1 axis selection(P1 축 선택): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_axis_selection_report.md`",
        report_line_current,
    )
    current = replace_once(
        current,
        "- next_run(다음 실행): `run267C_stage267_execute_prioritized_ablation_replacement_variants_v1`",
        f"- next_run(다음 실행): `{RUN_ID}`",
    )
    current = replace_once(
        current,
        "- action(행동): run267C(267C 실행) P1 axis selection(P1 축 선택)에서 late21(후반 21시)을 Adapter prototype(어댑터 원형) 축으로, atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)를 P2 replacement(2차 대체) 축으로 분리했다.",
        "- action(행동): run267D(267D 실행)에서 late21(후반 21시) Adapter prototype(어댑터 원형)과 atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX) P2 replacement(2차 대체)를 MT5(MetaTrader 5, 메타트레이더5) 재실행 가능한 설계 묶음으로 물질화했다.",
    )
    current = replace_once(
        current,
        "- effect(효과): 다음 작업은 후보 선택이 아니라 axis family(축 계열)를 Adapter prototype(어댑터 원형)과 P2 replacement(2차 대체)로 물질화하는 것이다.",
        "- effect(효과): 선택 축이 말뿐인 판단이 아니라 feature/model copy(피처/모델 복사), runtime contract(런타임 계약), set/ini(설정/초기화), attempt manifest(시도 목록)로 추적된다.",
    )
    current = replace_once(
        current,
        "- next_action(다음 행동): `run267D_materialize_late21_adapter_prototype_and_p2_replacement_design`. Effect(효과): late21(후반 21시)은 어댑터 원형으로, atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)는 2차 대체 설계로 물질화해 다시 MT5(메타트레이더5) 검증한다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): 새 run267D(267D 실행) set/ini(설정/초기화)를 MT5(MetaTrader 5, 메타트레이더5) Strategy Tester(전략 테스터)에 실행해 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 본다.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_once(selection, "- stage_status(단계 상태): `run267C_p1_axis_selection_completed`", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_once(selection, "- current_run(현재 실행): `run267C_stage267_execute_prioritized_ablation_replacement_variants_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = append_after(
        selection,
        "- run267C_p1_axis_selection(267C P1 축 선택): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_axis_selection_report.md`",
        "- run267D_adapter_p2_materialization(267D 어댑터/2차 대체 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267D_adapter_p2_materialization_report.md`",
    )
    selection = replace_once(selection, "- next_action(다음 행동): `run267D_materialize_late21_adapter_prototype_and_p2_replacement_design`", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_once(
        selection,
        "Run267C(267C 실행)는 P1 axis selection(P1 축 선택)을 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 late21(후반 21시) Adapter prototype(어댑터 원형)과 atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX) P2 replacement(2차 대체)를 물질화하는 작업이다.",
        "Run267D(267D 실행)는 Adapter/P2 materialization(어댑터/2차 대체 물질화)을 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 run267D(267D 실행) attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에 실행해 곡선과 구간 품질을 다시 보는 작업이다.",
    )
    write_md(SELECTION_STATUS_PATH, selection)

    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = replace_once(review, "- status(상태): `run267C_p1_axis_selection_completed`", f"- status(상태): `{STATUS}`")
    review = append_after(
        review,
        "- run267C_p1_axis_selection(267C P1 축 선택): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_axis_selection_report.md`",
        "- run267D_adapter_p2_materialization(267D 어댑터/2차 대체 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267D_adapter_p2_materialization_report.md`",
    )
    review = replace_once(
        review,
        "Run267C(267C 실행)는 P1 axis selection(P1 축 선택)을 완료했다.\nEffect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `run267D_materialize_late21_adapter_prototype_and_p2_replacement_design`로 이어간다.",
        f"Run267D(267D 실행)는 Adapter/P2 materialization(어댑터/2차 대체 물질화)을 완료했다.\nEffect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `{NEXT_ACTION}`로 이어간다.",
    )
    write_md(REVIEW_INDEX_PATH, review)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_once(workspace, "current_run_id: run267C_stage267_execute_prioritized_ablation_replacement_variants_v1", f"current_run_id: {RUN_ID}")
    workspace = replace_once(
        workspace,
        "Stage267(267단계) run267C(267C 실행) P1 axis selection(P1 축 선택) completed(완료). Effect(효과): late21(후반 21시)은 Adapter prototype(어댑터 원형) 축으로, atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)는 P2 replacement(2차 대체) 축으로 나눴지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        "Stage267(267단계) run267D(267D 실행) Adapter/P2 materialization(어댑터/2차 대체 물질화) completed(완료). Effect(효과): late21(후반 21시), atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)가 run267D(267D 실행) feature/model copy(피처/모델 복사), runtime contract(런타임 계약), set/ini(설정/초기화)로 추적되지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    workspace = replace_once(
        workspace,
        "Next action(다음 행동)는 `run267D_materialize_late21_adapter_prototype_and_p2_replacement_design`이다. Effect(효과): late21(후반 21시)은 Adapter prototype(어댑터 원형)으로, atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)는 P2 replacement(2차 대체)로 물질화해 balance/equity curve(잔액/평가금 곡선)와 time-slice KPI(시간 구간 핵심 성과 지표)를 다시 본다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): run267D(267D 실행) MT5(MetaTrader 5, 메타트레이더5) batch(묶음 실행)로 Adapter prototype(어댑터 원형)과 P2 replacement(2차 대체)가 실제 곡선과 거래 품질에서 덜 깨지는지 확인한다.",
    )
    workspace = workspace.replace(
        "active_run267C_p1_axis_selection_completed(267C P1 축 선택 뒤 run267D 물질화 활성)",
        "active_run267D_adapter_p2_materialized_execution_pending(267D 어댑터/2차 대체 물질화 뒤 실행 대기 활성)",
        1,
    )
    workspace = workspace.replace("status: run267C_p1_axis_selection_completed", f"status: {STATUS}", 1)
    workspace = workspace.replace("next_action: run267D_materialize_late21_adapter_prototype_and_p2_replacement_design", f"next_action: {NEXT_ACTION}", 1)
    write_md(WORKSPACE_STATE_PATH, workspace)


def report_markdown(result: Mapping[str, Any], design_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> str:
    adapter_rows = [row for row in design_rows if row["role_scope"] == "adapter_prototype"]
    p2_rows = [row for row in design_rows if row["role_scope"] == "p2_replacement"]
    lines = [
        "# Stage267 Run267D Adapter/P2 Materialization(267단계 267D 어댑터/2차 대체 물질화)",
        "",
        f"- action(행동): late21(후반 21시) Adapter prototype(어댑터 원형)과 atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX) P2 replacement(2차 대체)를 `{len(design_rows)}`개 design row(설계 행)와 `{len(attempts)}`개 MT5 attempt(메타트레이더5 시도)로 물질화했다.",
        "- effect(효과): run267C(267C 실행)의 축 선택을 다음 Strategy Tester(전략 테스터) 실행 가능한 feature/model/set/ini(피처/모델/설정/초기화) 묶음으로 바꿨다.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Experiment Design Receipt(실험 설계 기록)",
        "",
        "- hypothesis(가설): late21(후반 21시)은 Adapter prototype(어댑터 원형)으로 구조화해도 P1 수리 효과를 유지할 수 있고, atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)는 similar replacement(유사 대체) 축으로 약점 설명력을 넓힐 수 있다.",
        "- decision_use(결정 사용처): 다음 MT5(MetaTrader 5, 메타트레이더5) batch(묶음 실행)가 Adapter(어댑터) 개발을 계속할지, P2 replacement(2차 대체)를 살릴지, 또는 실패 기억으로 닫을지 결정한다.",
        f"- comparison_baseline(비교 기준): `{rel(INPUT_AXIS_SELECTION_PATH)}`, `{rel(INPUT_SHORTLIST_PATH)}`, `{rel(INPUT_P1_KPI_PATH)}`.",
        "- control_variables(고정 변수): Stage267(267단계) 5개 후보군, 2024 historical stress(2024 과거 압박), MT5 EA(MetaTrader 5 Expert Advisor, 메타트레이더5 전문가 자문), threshold(임계값), trade management(거래 관리)를 유지한다.",
        "- changed_variables(변경 변수): run267D(267D 실행) 전용 artifact lineage(산출물 계보), runtime contract(런타임 계약), attempt namespace(시도 이름공간)만 바꾼다.",
        "- sample_scope(표본 범위): Tier A(티어 A)와 Tier A+B(티어 A+B) routed historical 2024(라우팅 과거 2024) 재검증 준비.",
        "- success_criteria(성공 기준): 실행 후 balance/equity curve(잔액/평가금 곡선), PF(수익 팩터), DD(drawdown, 손실폭), recovery(회복), expectancy(기대값), trade count(거래 수)가 후보별 역할에 맞게 덜 깨져야 한다.",
        "- failure_criteria(실패 기준): 거래 수 붕괴, 특정 축 과의존, DD 악화, 또는 곡선 구멍이 확대되면 Adapter/P2(어댑터/2차 대체) 이월을 중단한다.",
        "- invalid_conditions(무효 조건): feature order hash(피처 순서 해시), common file copy(공통 파일 복사), set/ini(설정/초기화), MT5 output(MT5 출력) 중 하나라도 불일치하면 실행 해석은 무효다.",
        "- stop_conditions(중단 조건): 한 축/한 월/한 threshold(임계값) 미세조정만 반복되면 repair loop(수리 반복)를 닫고 다른 구조 질문으로 전환한다.",
        "- evidence_plan(근거 계획): run267D attempt(시도), backtest forensics(백테스트 포렌식), KPI(KPI, 핵심 성과 지표), balance/time-slice review(잔액/시간 구간 검토)를 같은 장부에 연결한다.",
        "",
        "## Adapter Prototype(어댑터 원형)",
        "",
        "| candidate(후보) | pair role(쌍 역할) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) | read(판독) |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in adapter_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['pair_role']}` | {csv_value(row['p1_net_profit'])} | {csv_value(row['p1_pf'])} | {csv_value(row['p1_trade_count'])} | {csv_value(row['p1_dd_percent'])} | {row['design_read']} |"
        )
    lines.extend(
        [
            "",
            "## P2 Replacement(2차 대체)",
            "",
            "| candidate(후보) | axis(축) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) | retention(유지율) | read(판독) |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in p2_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['axis']}` | {csv_value(row['p1_net_profit'])} | {csv_value(row['p1_pf'])} | {csv_value(row['p1_trade_count'])} | {csv_value(row['p1_dd_percent'])} | {csv_value(row['signal_retention'])} | {row['design_read']} |"
        )
    lines.extend(
        [
            "",
            "## Runtime Parity Boundary(런타임 동등성 경계)",
            "",
            f"- research_path(연구 경로): `{rel(PRODUCER_PATH)}`.",
            f"- runtime_path(런타임 경로): `{rel(ATTEMPT_MANIFEST_PATH)}`.",
            "- shared_contract(공유 계약): feature order hash(피처 순서 해시), model CSV(모델 표), threshold(임계값), MT5 EA(MetaTrader 5 Expert Advisor, 메타트레이더5 전문가 자문), 2024 date window(2024 날짜 구간).",
            "- known_differences(알려진 차이): run267D(267D 실행)는 run267C(267C 실행) P1 selected artifact(선택 산출물)를 새 lineage(계보) 아래 복사한다. 의사결정 로직은 아직 바꾸지 않는다.",
            "- parity_check(동등성 검사): materialization hash/copy check(물질화 해시/복사 검사) 완료, Strategy Tester output(전략 테스터 출력)은 다음 실행 조건이다.",
            "- runtime_claim_boundary(런타임 주장 경계): `research_only_runtime_execution_pending`.",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- selected_candidate(선택 후보): `none`.",
            "- selected_research_baseline(선택 연구 기준선): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- result_subject(결과 대상): `run267D_adapter_p2_materialization`.",
            "- evidence_available(사용 가능 근거): P1 axis selection(P1 축 선택), P1 KPI(P1 핵심 성과 지표), feature/model hashes(피처/모델 해시), set/ini manifest(설정/초기화 목록).",
            "- evidence_missing(빠진 근거): run267D MT5 execution(267D MT5 실행), zoomed equity curve(확대 평가금 곡선), full time-slice breakdown(전체 시간 구간 분해), Adapter stability review(어댑터 안정성 검토), ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `materialized_execution_pending_no_candidate_selection(물질화 완료, 실행 대기, 후보 선택 없음)`.",
            f"- next_condition(다음 조건): `{NEXT_ACTION}`.",
        ]
    )
    _ = result
    return "\n".join(lines)


def materialize() -> dict[str, Any]:
    created_at = utc_now()
    design_rows, contract_rows, attempts, lineage = build_design_rows()
    result = {
        "status": STATUS,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "design_rows": len(design_rows),
        "adapter_rows": len([row for row in design_rows if row["role_scope"] == "adapter_prototype"]),
        "p2_rows": len([row for row in design_rows if row["role_scope"] == "p2_replacement"]),
        "attempt_count": len(attempts),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
        "outputs": {
            "design_matrix": rel(DESIGN_MATRIX_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(
        DESIGN_MATRIX_PATH,
        design_rows,
        (
            "candidate_alias",
            "candidate_role",
            "axis",
            "role_scope",
            "pair_role",
            "materialization_intent",
            "axis_decision",
            "axis_avg_net_delta",
            "axis_avg_pf_delta",
            "axis_avg_trade_delta",
            "axis_avg_dd_delta",
            "p1_net_profit",
            "p1_pf",
            "p1_trade_count",
            "p1_dd_percent",
            "p1_expectancy",
            "p1_recovery_factor",
            "signal_retention",
            "blocked_signal_rows",
            "kept_signal_rows",
            "feature_order_hash",
            "run267d_feature_file",
            "run267d_model_file",
            "common_feature_path",
            "common_model_path",
            "design_read",
            "next_validation",
            "claim_boundary",
        ),
    )
    write_csv(
        RUNTIME_CONTRACT_PATH,
        contract_rows,
        (
            "candidate_alias",
            "axis",
            "role_scope",
            "shared_contract",
            "feature_count",
            "feature_order",
            "feature_order_hash",
            "model_backend",
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "close_on_flat_signal",
            "reverse_on_opposite_signal",
            "close_only_on_opposite_signal",
            "tier_a_p1_net",
            "routed_p1_net",
            "known_differences",
            "runtime_claim_boundary",
        ),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        attempt_rows(attempts),
        (
            "candidate_alias",
            "candidate_role",
            "axis",
            "role_scope",
            "axis_decision",
            "attempt_name",
            "tier",
            "split",
            "attempt_role",
            "record_view_prefix",
            "set_path",
            "set_sha256",
            "ini_path",
            "ini_sha256",
            "common_telemetry_path",
            "common_summary_path",
            "fallback_enabled",
            "execution_status",
        ),
    )
    write_json(LINEAGE_PATH, {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": created_at, "lineage": lineage})
    write_json(RESULT_PATH, result | {"runtime_contract_rows": len(contract_rows), "lineage_rows": len(lineage)})
    write_md(REPORT_PATH, report_markdown(result, design_rows, attempts))
    update_current_truth_docs()
    update_ledgers(created_at, design_rows, attempts)
    return result


def main() -> int:
    result = materialize()
    print(
        json.dumps(
            {
                "status": result["status"],
                "design_rows": result["design_rows"],
                "adapter_rows": result["adapter_rows"],
                "p2_rows": result["p2_rows"],
                "attempt_count": result["attempt_count"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
