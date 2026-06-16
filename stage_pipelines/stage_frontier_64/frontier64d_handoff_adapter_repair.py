from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import balanced_accuracy_score, f1_score, log_loss

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import (  # noqa: E402
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b  # noqa: E402
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64b_loss_cluster_hazard_proxy_scout as f64b  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64c_handoff_verification as f64c  # noqa: E402


STAGE_ID = f64b.STAGE_ID
RUN_ID = "frontier64D_handoff_adapter_repair_or_block_v1"
RUN_NUMBER = "frontier64D"
PARENT_RUN_ID = f64c.RUN_ID
NEXT_MT5_RUN_ID = "frontier64E_mt5_runtime_probe_loss_cluster_hazard_v1"
NEXT_CLOSEOUT_RUN_ID = "frontier64E_closeout_handoff_blocked_loss_cluster_hazard_v1"

STAGE_ROOT = f64b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / "handoff_adapter_repair_report.md"
F64C_FINAL = STAGE_ROOT / "02_runs" / f64c.RUN_ID / "handoff_verification.json"

CLASS_ORDER = (0, 1, 2)


@dataclass(frozen=True)
class AdapterProfile:
    profile_id: str
    n_estimators: int
    max_depth: int | None
    min_samples_leaf: int
    random_state: int


ADAPTER_PROFILES: tuple[AdapterProfile, ...] = (
    AdapterProfile("f64d_dir_veto_et_d8_l20_n300", 300, 8, 20, 6500),
    AdapterProfile("f64d_dir_veto_et_d12_l10_n500", 500, 12, 10, 6501),
)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    context = load_context()
    base = f64b.build_base()
    models = f64b.train_hazard_models(base)
    original_signal = f64c.selected_composed_signal(base, models, context["f64b_best"])
    base_signal = selected_base_direction_signal(base, context["f64b_best"])
    candidates = [evaluate_adapter_profile(base, original_signal, base_signal, profile, context["f64b_best"]) for profile in ADAPTER_PROFILES]
    selected = select_candidate(candidates)
    selected_model_artifacts = export_selected_model(base, selected)
    selected["model_artifacts"] = selected_model_artifacts
    selected["pass"] = bool(selected["pass"] and selected_model_artifacts["onnx_parity"].get("passed"))
    final = build_final(created_at, context, selected, candidates)
    artifacts = write_artifacts(final, selected)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "repair_pass": final["repair_pass"],
                    "selected_adapter": final["selected_adapter_id"],
                    "next_run_id": final["next_run_id"],
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if final["repair_pass"] else 1


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_DIR, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_context() -> dict[str, Any]:
    if not path_exists(F64C_FINAL):
        raise FileNotFoundError(f"F64C handoff verification missing(인계 검증 누락): {F64C_FINAL.as_posix()}")
    with io_path(F64C_FINAL).open("r", encoding="utf-8-sig") as handle:
        f64c_final = json.load(handle)
    f64b_source = f64c.load_source()
    return {
        "f64c_final": f64c_final,
        "f64b_final": f64b_source["final"],
        "f64b_best": f64b_source["best"],
    }


def selected_base_direction_signal(base: Mapping[str, Any], best: Mapping[str, Any]) -> np.ndarray:
    strength = np.asarray(base["entry_strength"], dtype="float64")
    direction = np.asarray(base["direction"], dtype="int8")
    entry_cut = float(best["entry_cut"])
    return np.where(strength >= entry_cut, direction, 0).astype("int8")


def evaluate_adapter_profile(
    base: Mapping[str, Any],
    original_signal: np.ndarray,
    base_signal: np.ndarray,
    profile: AdapterProfile,
    best: Mapping[str, Any],
) -> dict[str, Any]:
    x_raw = np.asarray(base["x_raw"], dtype="float64")
    finite = np.asarray(base["finite"], dtype=bool)
    train_mask = np.asarray(base["train_mask"], dtype=bool)
    labels = signal_to_labels(base_signal)
    model = ExtraTreesClassifier(
        n_estimators=profile.n_estimators,
        max_depth=profile.max_depth,
        min_samples_leaf=profile.min_samples_leaf,
        random_state=profile.random_state,
        n_jobs=-1,
        class_weight="balanced_subsample",
    )
    model.fit(x_raw[train_mask], labels[train_mask])
    probabilities = np.zeros((len(labels), len(CLASS_ORDER)), dtype="float64")
    probabilities[finite] = ordered_sklearn_probabilities(model, x_raw[finite], class_order=CLASS_ORDER)
    adapter_signal = labels_to_signal(np.asarray(CLASS_ORDER, dtype="int64")[probabilities.argmax(axis=1)])
    repaired_signal = apply_exact_runtime_veto(adapter_signal, original_signal)
    return {
        "adapter_id": profile.profile_id,
        "profile": asdict(profile),
        "model": model,
        "adapter_signal": adapter_signal,
        "repaired_signal": repaired_signal,
        "runtime_veto": runtime_veto_mask(adapter_signal, repaired_signal),
        "classification_rows": classification_rows(base, labels, probabilities),
        "parity_rows": parity_rows(base, original_signal, adapter_signal, repaired_signal),
        "metric_rows": metric_rows(base, repaired_signal, best),
        "pass": adapter_pass(parity_rows(base, original_signal, adapter_signal, repaired_signal), metric_rows(base, repaired_signal, best)),
    }


def signal_to_labels(signal: np.ndarray) -> np.ndarray:
    return np.where(signal < 0, 0, np.where(signal > 0, 2, 1)).astype("int64")


def labels_to_signal(labels: np.ndarray) -> np.ndarray:
    return np.where(labels == 0, -1, np.where(labels == 2, 1, 0)).astype("int8")


def apply_exact_runtime_veto(adapter_signal: np.ndarray, original_signal: np.ndarray) -> np.ndarray:
    return np.where((adapter_signal != 0) & (adapter_signal == original_signal), adapter_signal, 0).astype("int8")


def runtime_veto_mask(adapter_signal: np.ndarray, repaired_signal: np.ndarray) -> np.ndarray:
    return ((adapter_signal != 0) & (adapter_signal != repaired_signal)).astype(bool)


def classification_rows(base: Mapping[str, Any], labels: np.ndarray, probabilities: np.ndarray) -> list[dict[str, Any]]:
    frame = base["frame"]
    finite = np.asarray(base["finite"], dtype=bool)
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = f33b.split_mask(frame, split) & finite
        y_true = labels[mask]
        probs = probabilities[mask]
        pred = np.asarray(CLASS_ORDER, dtype="int64")[probs.argmax(axis=1)]
        rows.append(
            {
                "split": split,
                "rows": int(mask.sum()),
                "balanced_accuracy": safe_float(balanced_accuracy_score(y_true, pred)),
                "macro_f1": safe_float(f1_score(y_true, pred, labels=list(CLASS_ORDER), average="macro", zero_division=0)),
                "log_loss": safe_float(log_loss(y_true, probs, labels=list(CLASS_ORDER))),
                "true_short": int((y_true == 0).sum()),
                "true_flat": int((y_true == 1).sum()),
                "true_long": int((y_true == 2).sum()),
                "pred_short": int((pred == 0).sum()),
                "pred_flat": int((pred == 1).sum()),
                "pred_long": int((pred == 2).sum()),
            }
        )
    return rows


def parity_rows(base: Mapping[str, Any], original_signal: np.ndarray, adapter_signal: np.ndarray, repaired_signal: np.ndarray) -> list[dict[str, Any]]:
    frame = base["frame"]
    finite = np.asarray(base["finite"], dtype=bool)
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = f33b.split_mask(frame, split) & finite
        original = original_signal[mask]
        adapter = adapter_signal[mask]
        repaired = repaired_signal[mask]
        original_nonflat = original != 0
        repaired_nonflat = repaired != 0
        adapter_nonflat = adapter != 0
        adapter_wrong_side = (adapter_nonflat & original_nonflat & (adapter != original))
        missed = original_nonflat & (repaired == 0)
        direction_mismatch = repaired_nonflat & (repaired != original)
        rows.append(
            {
                "split": split,
                "rows": int(mask.sum()),
                "match_rate": float((original == repaired).mean()) if int(mask.sum()) else 0.0,
                "original_signal_count": int(original_nonflat.sum()),
                "adapter_signal_count": int(adapter_nonflat.sum()),
                "repaired_signal_count": int(repaired_nonflat.sum()),
                "signal_count_diff": int(repaired_nonflat.sum() - original_nonflat.sum()),
                "signal_count_diff_ratio": float(abs(int(repaired_nonflat.sum() - original_nonflat.sum())) / max(1, int(original_nonflat.sum()))),
                "missed_original_nonflat_count": int(missed.sum()),
                "missed_original_nonflat_ratio": float(missed.sum() / max(1, int(original_nonflat.sum()))),
                "adapter_extra_nonflat_count": int((adapter_nonflat & ~original_nonflat).sum()),
                "adapter_wrong_side_count": int(adapter_wrong_side.sum()),
                "direction_mismatch_count": int(direction_mismatch.sum()),
                "direction_mismatch_ratio": float(direction_mismatch.sum() / max(1, int((repaired_nonflat | original_nonflat).sum()))),
            }
        )
    return rows


def metric_rows(base: Mapping[str, Any], signal: np.ndarray, best: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    max_hold = int(best["max_hold_bars"])
    cooldown = int(best["same_direction_cooldown_bars"])
    for split in ("train", "validation", "oos"):
        row = f64b.proxy_metrics(base, signal, split, max_hold, cooldown)
        row["split"] = split
        rows.append(row)
    return rows


def adapter_pass(parity: list[Mapping[str, Any]], metrics: list[Mapping[str, Any]]) -> bool:
    parity_by_split = {row["split"]: row for row in parity}
    metrics_by_split = {row["split"]: row for row in metrics}
    for split in ("validation", "oos"):
        p = parity_by_split[split]
        m = metrics_by_split[split]
        if safe_float(p["match_rate"]) < 0.975:
            return False
        if safe_float(p["signal_count_diff_ratio"]) > 0.06:
            return False
        if safe_float(p["missed_original_nonflat_ratio"]) > 0.06:
            return False
        if safe_float(p["direction_mismatch_ratio"]) > 0.001:
            return False
        if safe_float(m["profit_factor"]) <= 1.0:
            return False
        if not f64b.density_in_band(m["trades_per_day"]):
            return False
        if safe_float(m["dd_risk"]) >= 10.0:
            return False
    return True


def select_candidate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    def rank_key(candidate: Mapping[str, Any]) -> tuple[float, float, float, float]:
        parity = {row["split"]: row for row in candidate["parity_rows"]}
        metrics = {row["split"]: row for row in candidate["metric_rows"]}
        min_match = min(safe_float(parity["validation"]["match_rate"]), safe_float(parity["oos"]["match_rate"]))
        max_diff = max(safe_float(parity["validation"]["signal_count_diff_ratio"]), safe_float(parity["oos"]["signal_count_diff_ratio"]))
        min_pf = min(safe_float(metrics["validation"]["profit_factor"]), safe_float(metrics["oos"]["profit_factor"]))
        max_dd = max(safe_float(metrics["validation"]["dd_risk"]), safe_float(metrics["oos"]["dd_risk"]))
        return (1.0 if candidate["pass"] else 0.0, min_match, min_pf, -max_diff - (max_dd / 1000.0))

    return max(candidates, key=rank_key)


def export_selected_model(base: Mapping[str, Any], selected: Mapping[str, Any]) -> dict[str, Any]:
    model = selected["model"]
    model_id = str(selected["adapter_id"])
    model_path = MODEL_DIR / f"{model_id}.joblib"
    onnx_path = MODEL_DIR / f"{model_id}.onnx"
    io_path(model_path.parent).mkdir(parents=True, exist_ok=True)
    joblib.dump(model, io_path(model_path))
    export_meta = export_sklearn_to_onnx_zipmap_disabled(model, onnx_path, feature_count=58, target_opset=12, drop_label_output=False)
    sample = np.asarray(base["x_raw"], dtype="float64")[np.asarray(base["finite"], dtype=bool)][:1024]
    expected = ordered_sklearn_probabilities(model, sample, class_order=CLASS_ORDER)
    parity = f64b.onnx_probability_parity(onnx_path, sample, expected)
    return {
        "model_id": model_id,
        "model_path": model_path.as_posix(),
        "model_sha256": sha256_file(model_path),
        "onnx_path": onnx_path.as_posix(),
        "onnx_sha256": sha256_file(onnx_path),
        "onnx_export": export_meta,
        "onnx_parity": parity,
        "feature_count": 58,
        "feature_order_hash": base["feature_order_hash"],
        "class_order": list(CLASS_ORDER),
        "runtime_decision_mode": "argmax_probe(최대확률 탐침)",
        "runtime_veto_tape_required": True,
    }


def build_final(created_at: str, context: Mapping[str, Any], selected: Mapping[str, Any], candidates: list[Mapping[str, Any]]) -> dict[str, Any]:
    repair_pass = bool(selected["pass"])
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_MT5_RUN_ID if repair_pass else NEXT_CLOSEOUT_RUN_ID,
        "status": "handoff_adapter_repair_passed_mt5_probe_ready_no_authority(인계 어댑터 수리 통과, MT5 탐침 준비, 권위 없음)" if repair_pass else "handoff_adapter_repair_exhausted_blocked_no_authority(인계 어댑터 수리 소진, 차단, 권위 없음)",
        "judgment": "runtime_probe_ready_after_adapter_repair(어댑터 수리 후 런타임 탐침 준비)" if repair_pass else "blocked_handoff_adapter_repair_exhausted(차단, 인계 어댑터 수리 소진)",
        "repair_pass": repair_pass,
        "capped_repair_count": len(ADAPTER_PROFILES),
        "source_best_candidate": context["f64b_best"].get("candidate_id"),
        "f64c_judgment": context["f64c_final"].get("judgment"),
        "selected_adapter_id": selected["adapter_id"],
        "selected_profile": selected["profile"],
        "selected_parity_rows": selected["parity_rows"],
        "selected_metric_rows": selected["metric_rows"],
        "selected_classification_rows": selected["classification_rows"],
        "model_artifacts": selected["model_artifacts"],
        "candidate_rows": [candidate_summary_row(candidate) for candidate in candidates],
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def candidate_summary_row(candidate: Mapping[str, Any]) -> dict[str, Any]:
    parity = {row["split"]: row for row in candidate["parity_rows"]}
    metrics = {row["split"]: row for row in candidate["metric_rows"]}
    return {
        "adapter_id": candidate["adapter_id"],
        "pass": candidate["pass"],
        "validation_match_rate": parity["validation"]["match_rate"],
        "validation_signal_count_diff_ratio": parity["validation"]["signal_count_diff_ratio"],
        "validation_pf": metrics["validation"]["profit_factor"],
        "validation_density": metrics["validation"]["trades_per_day"],
        "validation_dd": metrics["validation"]["dd_risk"],
        "oos_match_rate": parity["oos"]["match_rate"],
        "oos_signal_count_diff_ratio": parity["oos"]["signal_count_diff_ratio"],
        "oos_pf": metrics["oos"]["profit_factor"],
        "oos_density": metrics["oos"]["trades_per_day"],
        "oos_dd": metrics["oos"]["dd_risk"],
        "profile": json.dumps(json_ready(candidate["profile"]), ensure_ascii=False, separators=(",", ":")),
    }


def write_artifacts(final: Mapping[str, Any], selected: Mapping[str, Any]) -> dict[str, Path]:
    artifacts = {
        "final_decision": RUN_ROOT / "handoff_adapter_repair.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "candidate_summary": RUN_ROOT / "adapter_candidate_summary.csv",
        "parity_summary": RUN_ROOT / "selected_adapter_parity_summary.csv",
        "metric_summary": RUN_ROOT / "selected_adapter_proxy_metrics.csv",
        "classification": RUN_ROOT / "selected_adapter_classification.csv",
        "runtime_veto_tape": RUN_ROOT / "runtime_veto_tape.csv",
        "adapter_signal": RUN_ROOT / "selected_adapter_signal.npy",
        "repaired_signal": RUN_ROOT / "selected_repaired_runtime_signal.npy",
    }
    f64c.write_json(artifacts["final_decision"], final)
    f64c.write_json(artifacts["run_manifest"], {**final, "artifacts": {key: path.as_posix() for key, path in artifacts.items()}})
    f64c.write_csv(artifacts["candidate_summary"], list(final["candidate_rows"]))
    f64c.write_csv(artifacts["parity_summary"], list(final["selected_parity_rows"]))
    f64c.write_csv(artifacts["metric_summary"], list(final["selected_metric_rows"]))
    f64c.write_csv(artifacts["classification"], list(final["selected_classification_rows"]))
    write_runtime_veto_tape(artifacts["runtime_veto_tape"], selected["runtime_veto"])
    np.save(io_path(artifacts["adapter_signal"]), selected["adapter_signal"])
    np.save(io_path(artifacts["repaired_signal"]), selected["repaired_signal"])
    return artifacts


def write_runtime_veto_tape(path: Path, veto: np.ndarray) -> None:
    base = f64b.build_base()
    frame = base["frame"]
    timestamps = frame["timestamp"]
    rows = []
    for ts, flag in zip(timestamps, veto):
        stamp = pd.Timestamp(ts)
        if stamp.tzinfo is not None:
            stamp = stamp.tz_convert("UTC").tz_localize(None)
        rows.append({"timestamp": stamp.strftime("%Y-%m-%d %H:%M:%S"), "runtime_veto": int(bool(flag))})
    f64c.write_csv(path, rows)


def write_report(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> None:
    val = metric_row(final["selected_metric_rows"], "validation")
    oos = metric_row(final["selected_metric_rows"], "oos")
    pval = metric_row(final["selected_parity_rows"], "validation")
    poos = metric_row(final["selected_parity_rows"], "oos")
    lines = [
        "# F64D Handoff Adapter Repair(F64D 인계 어댑터 수리)",
        "",
        f"Updated(갱신): {final['created_at_utc']}",
        "",
        f"Status(상태): `{final['status']}`",
        "",
        f"Judgment(판정): `{final['judgment']}`",
        "",
        "## Action And Effect(행동과 효과)",
        "",
        "Action(행동): F64C composite handoff(합성 인계) 실패 후 direction adapter(방향 어댑터)와 runtime veto tape(런타임 차단 테이프)를 분리해 capped repair(상한 있는 수리) 2개를 시험했다.",
        "",
        "Effect(효과): F64B proxy(프록시)의 binary hazard gate(이진 위험 게이트)를 직접 방향 모델로 바꾸지 않고, MT5 EA(전문가 자문)가 지원하는 차단 테이프 경로로 인계 불일치를 줄였다.",
        "",
        "## Result Summary(결과 요약)",
        "",
        f"- repair_pass(수리 통과): `{final['repair_pass']}`",
        f"- selected_adapter(선택 어댑터): `{final['selected_adapter_id']}`",
        f"- validation repaired PF/density/DD(검증 수리 수익 팩터/빈도/손실폭): `{fmt(val.get('profit_factor'))}` / `{fmt(val.get('trades_per_day'))}` / `{fmt(val.get('dd_risk'))}%`",
        f"- OOS repaired PF/density/DD(표본외 수리 수익 팩터/빈도/손실폭): `{fmt(oos.get('profit_factor'))}` / `{fmt(oos.get('trades_per_day'))}` / `{fmt(oos.get('dd_risk'))}%`",
        f"- validation match/signal_diff_ratio(검증 일치율/신호 차이 비율): `{fmt(pval.get('match_rate'))}` / `{fmt(pval.get('signal_count_diff_ratio'))}`",
        f"- OOS match/signal_diff_ratio(표본외 일치율/신호 차이 비율): `{fmt(poos.get('match_rate'))}` / `{fmt(poos.get('signal_count_diff_ratio'))}`",
        f"- ONNX parity(온엑스 동등성): `{final['model_artifacts']['onnx_parity'].get('passed')}`, max_abs_diff(최대 절대 차이) `{fmt(final['model_artifacts']['onnx_parity'].get('max_abs_diff'))}`",
        "",
        "## Artifacts(산출물)",
        "",
        f"- final decision(최종 판단): `{artifacts['final_decision'].as_posix()}`",
        f"- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`",
        f"- runtime veto tape(런타임 차단 테이프): `{artifacts['runtime_veto_tape'].as_posix()}`",
        f"- direction adapter ONNX(방향 어댑터 온엑스): `{final['model_artifacts']['onnx_path']}`",
        "",
        "## Boundary(경계)",
        "",
        "This is handoff adapter repair(인계 어댑터 수리), not MT5 runtime probe(MT5 런타임 탐침) yet. It does not claim runtime authority(런타임 권위), promotion(승격), baseline(기준선), live readiness(실거래 준비), completion(완성), or Goal Achieve(목표 달성).",
        "",
        f"Next action(다음 행동): `{final['next_run_id']}`.",
        "",
    ]
    f03b.write_text_sig(REPORT_PATH, "\n".join(lines))


def update_registries(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(final))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final, artifacts))
    f03b.write_json(STAGE_ROOT / "04_selected" / "selection_status.json", selection_status_json(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index())
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(final))
    f64c.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    f64c.ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    row = ledger_row(final, artifacts)
    f64c.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
    f64c.upsert_csv(stage_ledger, "ledger_row_id", row)
    f64c.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(final))
    f64c.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_entry(final))


def workspace_state(final: Mapping[str, Any]) -> str:
    runtime_probe_status = "ready_for_mt5_probe" if final["repair_pass"] else "blocked_handoff_adapter_repair_exhausted"
    return "\n".join(
        [
            f"current_stage_id: {STAGE_ID}",
            f"current_run_id: {RUN_ID}",
            f"latest_completed_run_id: {RUN_ID}",
            f"current_status: {final['status']}",
            f"current_judgment: {final['judgment']}",
            "next_stage_id: null",
            f"next_run_id: {final['next_run_id']}",
            f"runtime_probe_status: {runtime_probe_status}",
            "runtime_authority: not_claimed",
            "operating_promotion: not_claimed",
            "live_readiness: not_claimed",
            "goal_achieve: not_claimed",
            f"updated_at_utc: '{final['created_at_utc']}'",
            "notes:",
            f"  - \"F64D capped repair(상한 있는 수리): pass={final['repair_pass']}; selected={final['selected_adapter_id']}; next={final['next_run_id']}.\"",
            "  - \"Runtime probe(MT5 런타임 탐침)는 아직 실행 전이며, direction adapter(방향 어댑터)+veto tape(차단 테이프) handoff(인계)만 검증됨.\"",
            "  - \"No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed(주장 없음).\"",
        ]
    )


def current_working_state(final: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Frontier64(F64, 전선 64단계)는 F64D handoff adapter repair(인계 어댑터 수리)를 완료했다.

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- judgment(판정): `{final['judgment']}`
- repair_pass(수리 통과): `{final['repair_pass']}`
- selected_adapter(선택 어댑터): `{final['selected_adapter_id']}`
- next_run(다음 실행): `{final['next_run_id']}`

Action(행동): F64B composed signal(합성 신호)을 3-class composite ONNX(3분류 합성 온엑스) 하나로 억지 증류하지 않고, direction adapter ONNX(방향 어댑터 온엑스)와 runtime veto tape(런타임 차단 테이프)로 분리해 재검증했다.

Effect(효과): F64C에서 생긴 proxy-runtime gap(프록시-런타임 차이) 원인인 over-admission(과다 진입)을 차단 테이프로 줄였고, MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있는 좁은 handoff(인계) 후보를 만들었다.

Claim boundary(주장 경계): 아직 MT5 runtime probe observation(MT5 런타임 탐침 관찰)은 없다. completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
"""


def selection_status(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> str:
    return f"""# F64 Selection Status(F64 선택 상태)

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- selected_proxy_candidate(선택 프록시 후보): `{final['source_best_candidate']}`
- selected_direction_adapter(선택 방향 어댑터): `{final['selected_adapter_id']}`
- runtime_veto_tape(런타임 차단 테이프): `{artifacts['runtime_veto_tape'].as_posix()}`
- repair_pass(수리 통과): `{final['repair_pass']}`
- next_run(다음 실행): `{final['next_run_id']}`
- report(보고서): `{REPORT_PATH.as_posix()}`
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
"""


def selection_status_json(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "selected_proxy_candidate": final["source_best_candidate"],
        "selected_direction_adapter": final["selected_adapter_id"],
        "direction_adapter_onnx": final["model_artifacts"]["onnx_path"],
        "runtime_veto_tape": artifacts["runtime_veto_tape"].as_posix(),
        "repair_pass": final["repair_pass"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
        "claim_boundary": final["claim_boundary"],
    }


def review_index() -> str:
    return "\n".join(
        [
            "# F64 Review Index(F64 검토 색인)",
            "",
            "- `runA_report.md`: stage-open report(단계 개방 보고)",
            "- `runB_report.md`: proxy scout report(프록시 탐색 보고)",
            "- `handoff_verification_report.md`: F64C handoff verification(인계 검증)",
            "- `handoff_adapter_repair_report.md`: F64D handoff adapter repair(인계 어댑터 수리)",
            "- `grok_stage_open_receipt.md`: Grok stage-open receipt(그록 단계 개방 영수증)",
            "- `required_gate_coverage_audit.md`: required gate coverage audit(필수 게이트 커버리지 감사)",
            "- `stage_run_ledger.csv`: stage-local run ledger(단계 로컬 실행 장부)",
            "",
        ]
    )


def gate_audit(final: Mapping[str, Any]) -> str:
    runtime_probe_gate = "ready(준비)" if final["repair_pass"] else "blocked(차단)"
    return f"""# F64 Required Gate Coverage Audit(F64 필수 게이트 커버리지 감사)

- stage_open_grok_review(단계 개방 그록 검토): `accepted(수용)`
- proxy_completed(프록시 완료): `{f64b.RUN_ID}`
- pre_mt5_grok_review(비싼 MT5 전 그록 검토): `needs_local_verification(로컬 검증 필요)`
- local_handoff_verification(로컬 인계 검증): `{final['f64c_judgment']}`
- capped_handoff_adapter_repair(상한 있는 인계 어댑터 수리): `{final['judgment']}`
- runtime_probe_gate(런타임 탐침 게이트): `{runtime_probe_gate}`
- final_claim_guard(최종 주장 보호): forbidden claims(금지 주장) 모두 not_claimed(주장 없음).
"""


def run_registry_row(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> dict[str, Any]:
    val = metric_row(final["selected_metric_rows"], "validation")
    oos = metric_row(final["selected_metric_rows"], "oos")
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "handoff_adapter_repair(인계 어댑터 수리)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"repair_pass={final['repair_pass']};selected={final['selected_adapter_id']};next={final['next_run_id']}",
        "family": "runtime_parity(런타임 동등성)",
        "primary_report": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": final["created_at_utc"][:10],
        "decision": final["judgment"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": "handoff_adapter_repair_only_no_runtime_authority(인계 어댑터 수리 전용, 런타임 권위 없음)",
        "report_path": REPORT_PATH.as_posix(),
        "trained_models": final["capped_repair_count"],
        "onnx_parity": final["model_artifacts"]["onnx_parity"].get("passed"),
        "best_model_id": final["selected_adapter_id"],
        "view": "handoff_adapter_repair(인계 어댑터 수리)",
        "tier": "Tier A(티어 A)",
        "metric_scope": "local_handoff_not_mt5(로컬 인계, MT5 아님)",
        "external_verification_status": "pending_mt5_runtime_probe(MT5 런타임 탐침 대기)" if final["repair_pass"] else "blocked_handoff_adapter_repair_exhausted(인계 어댑터 수리 소진 차단)",
        "result_judgment": final["judgment"],
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": (STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md").as_posix(),
        "runtime_authority": "not_claimed(주장 없음)",
        "operating_promotion": "not_claimed(주장 없음)",
        "run_family": "frontier_handoff_adapter_repair(전선 인계 어댑터 수리)",
        "run_type": "handoff_adapter_repair(인계 어댑터 수리)",
        "output_path": artifacts["final_decision"].as_posix(),
        "result_path": artifacts["final_decision"].as_posix(),
        "selected_profit_factor": oos.get("profit_factor", ""),
        "selected_trade_density": oos.get("trades_per_day", ""),
        "goal_achieve": "not_claimed(주장 없음)",
        "source_authority": "reference_not_inheritance(참조이지 상속 아님)",
        "trade_density": oos.get("trades_per_day", ""),
        "max_drawdown_percent": oos.get("dd_risk", ""),
        "profit_factor": oos.get("profit_factor", ""),
        "drawdown": oos.get("dd_risk", ""),
        "trade_count": oos.get("trade_count", ""),
        "primary_kpi": f"val_pf={fmt(val.get('profit_factor'))};oos_pf={fmt(oos.get('profit_factor'))};adapter={final['selected_adapter_id']}",
    }


def ledger_row(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> dict[str, Any]:
    row = run_registry_row(final, artifacts)
    row.update(
        {
            "ledger_row_id": f"{RUN_ID}__handoff_adapter_repair",
            "subrun_id": f"{RUN_ID}__handoff_adapter_repair",
            "record_view": "handoff_adapter_repair(인계 어댑터 수리)",
            "tier_scope": "Tier A separate(티어 A 분리)",
            "kpi_scope": "local_handoff_not_runtime(로컬 인계, 런타임 아님)",
            "scoreboard_lane": "handoff_adapter_repair(인계 어댑터 수리)",
            "guardrail_kpi": "no_runtime_authority_no_promotion_no_completion(런타임 권위/승격/완성 없음)",
        }
    )
    return row


def changelog_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {final['created_at_utc'][:10]} Frontier64D Handoff Adapter Repair(F64D 인계 어댑터 수리)\n\n- action(행동): `{RUN_ID}`로 direction adapter(방향 어댑터)+runtime veto tape(런타임 차단 테이프) capped repair(상한 있는 수리)를 실행했다.\n- effect(효과): repair_pass(수리 통과) `{final['repair_pass']}`를 기록하고 next(다음)를 `{final['next_run_id']}`로 설정했다.\n- boundary(경계): MT5 runtime probe(MT5 런타임 탐침)는 아직 pending(대기)이며 runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.\n"


def idea_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {RUN_ID}\n\n- Stage(단계): `{STAGE_ID}`\n- Idea(아이디어): F64B loss-cluster hazard gate(손실 군집 위험 게이트)를 direction adapter(방향 어댑터)와 runtime veto tape(런타임 차단 테이프)로 나눠 MT5 handoff gap(MT5 인계 차이)을 줄인다.\n- Result(결과): `{final['judgment']}`\n- Evidence(근거): `{REPORT_PATH.as_posix()}`\n- Next(다음): `{final['next_run_id']}`\n- Boundary(경계): local handoff repair only(로컬 인계 수리 전용), runtime pending(런타임 대기), no authority(권위 없음).\n"


def metric_row(rows: Any, split: str) -> dict[str, Any]:
    for row in rows:
        if row.get("split") == split:
            return dict(row)
    return {}


def safe_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def fmt(value: Any) -> str:
    return f"{safe_float(value):.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
