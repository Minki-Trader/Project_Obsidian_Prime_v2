from __future__ import annotations

import csv
import json
import math
import sys
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


STAGE_ID = f64b.STAGE_ID
RUN_ID = "frontier64C_handoff_verification_loss_cluster_hazard_v1"
RUN_NUMBER = "frontier64C"
PARENT_RUN_ID = f64b.RUN_ID
NEXT_MT5_RUN_ID = "frontier64D_mt5_runtime_probe_loss_cluster_hazard_v1"
NEXT_REPAIR_RUN_ID = "frontier64D_handoff_adapter_repair_or_block_v1"

STAGE_ROOT = f64b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / "handoff_verification_report.md"
F64B_FINAL = STAGE_ROOT / "02_runs" / f64b.RUN_ID / "final_decision.json"
F64B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f64b.RUN_ID / "candidate_summary.csv"
GROK_PRE_MT5 = Path("docs/agent_control/grok_reviews/2026-06-16_frontier64_pre_mt5_review/small_review/clean_output.md")

CLASS_ORDER = (0, 1, 2)
COMPOSITE_MODEL_ID = "frontier64_composite_hazard_direction_handoff_extratrees_d8_l100_v1"


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    source = load_source()
    base = f64b.build_base()
    models = f64b.train_hazard_models(base)
    original_signal = selected_composed_signal(base, models, source["best"])
    original_metrics = split_metrics(base, original_signal, source["best"])
    composite = train_composite_model(base, original_signal)
    composite_signal = signal_from_composite(composite["probabilities"])
    composite_metrics = split_metrics(base, composite_signal, source["best"])
    parity_rows = parity_summary(base, original_signal, composite_signal)
    pass_flag = handoff_pass(parity_rows, composite_metrics)
    model_artifacts = export_composite_model(base, composite)
    final = {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_MT5_RUN_ID if pass_flag else NEXT_REPAIR_RUN_ID,
        "status": "handoff_verification_passed_runtime_probe_ready_no_authority(인계 검증 통과, 런타임 탐침 준비, 권위 없음)" if pass_flag else "handoff_verification_failed_runtime_probe_blocked_no_authority(인계 검증 실패, 런타임 탐침 차단, 권위 없음)",
        "judgment": "runtime_probe_ready_observation_pending(런타임 탐침 준비, 관찰 대기)" if pass_flag else "blocked_handoff_adapter_mismatch(차단, 인계 어댑터 불일치)",
        "source_best_candidate": source["best"].get("candidate_id"),
        "source_status": source["final"].get("status"),
        "source_judgment": source["final"].get("judgment"),
        "original_metrics": original_metrics,
        "composite_metrics": composite_metrics,
        "parity_rows": parity_rows,
        "handoff_pass": pass_flag,
        "model_artifacts": model_artifacts,
        "classification_rows": composite["classification_rows"],
        "grok_pre_mt5_classification": "needs_local_verification(로컬 검증 필요)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }
    artifacts = write_artifacts(final, original_signal, composite_signal)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(json.dumps(json_ready({"status": final["status"], "judgment": final["judgment"], "handoff_pass": pass_flag, "next_run_id": final["next_run_id"]}), ensure_ascii=False, indent=2))
    return 0 if pass_flag else 1


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_DIR, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_source() -> dict[str, Any]:
    missing = [path.as_posix() for path in (F64B_FINAL, F64B_CANDIDATE_SUMMARY, GROK_PRE_MT5) if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F64C source missing(원천 누락): {missing}")
    with io_path(F64B_FINAL).open("r", encoding="utf-8-sig") as handle:
        final = json.load(handle)
    best = dict(final.get("best_candidate_row") or {})
    if not best:
        raise RuntimeError("F64B best candidate missing(최선 후보 누락)")
    return {"final": final, "best": best}


def selected_composed_signal(base: Mapping[str, Any], models: Mapping[str, Mapping[str, Any]], best: Mapping[str, Any]) -> np.ndarray:
    profile_id = str(best["profile_id"])
    payload = models[profile_id]
    hazard_probability = np.asarray(payload["hazard_probability"], dtype="float64")
    strength = np.asarray(base["entry_strength"], dtype="float64")
    direction = np.asarray(base["direction"], dtype="int8")
    entry_cut = float(best["entry_cut"])
    hazard_ceiling = float(best["hazard_probability_ceiling"])
    base_signal = np.where(strength >= entry_cut, direction, 0).astype("int8")
    return np.where((base_signal != 0) & (hazard_probability <= hazard_ceiling), base_signal, 0).astype("int8")


def split_metrics(base: Mapping[str, Any], signal: np.ndarray, best: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    max_hold = int(best["max_hold_bars"])
    cooldown = int(best["same_direction_cooldown_bars"])
    for split in ("train", "validation", "oos"):
        row = f64b.proxy_metrics(base, signal, split, max_hold, cooldown)
        row["split"] = split
        rows.append(row)
    return rows


def train_composite_model(base: Mapping[str, Any], signal: np.ndarray) -> dict[str, Any]:
    x_raw = np.asarray(base["x_raw"], dtype="float64")
    finite = np.asarray(base["finite"], dtype=bool)
    train_mask = np.asarray(base["train_mask"], dtype=bool)
    labels = np.where(signal < 0, 0, np.where(signal > 0, 2, 1)).astype("int64")
    missing = sorted(set(CLASS_ORDER) - set(int(value) for value in labels[train_mask]))
    if missing:
        raise RuntimeError(f"Composite train labels missing classes(합성 학습 라벨 클래스 누락): {missing}")
    model = ExtraTreesClassifier(
        n_estimators=700,
        max_depth=8,
        min_samples_leaf=100,
        random_state=6413,
        n_jobs=-1,
        class_weight="balanced_subsample",
    )
    model.fit(x_raw[train_mask], labels[train_mask])
    probabilities = np.zeros((len(labels), 3), dtype="float64")
    probabilities[finite] = ordered_sklearn_probabilities(model, x_raw[finite], class_order=CLASS_ORDER)
    return {"model": model, "labels": labels, "probabilities": probabilities, "classification_rows": classification_rows(base, labels, probabilities)}


def signal_from_composite(probabilities: np.ndarray) -> np.ndarray:
    labels = np.asarray(CLASS_ORDER, dtype="int64")[np.asarray(probabilities).argmax(axis=1)]
    return np.where(labels == 0, -1, np.where(labels == 2, 1, 0)).astype("int8")


def classification_rows(base: Mapping[str, Any], labels: np.ndarray, probabilities: np.ndarray) -> list[dict[str, Any]]:
    frame = base["frame"]
    finite = np.asarray(base["finite"], dtype=bool)
    rows = []
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


def parity_summary(base: Mapping[str, Any], original_signal: np.ndarray, composite_signal: np.ndarray) -> list[dict[str, Any]]:
    frame = base["frame"]
    finite = np.asarray(base["finite"], dtype=bool)
    rows = []
    for split in ("train", "validation", "oos"):
        mask = f33b.split_mask(frame, split) & finite
        orig = original_signal[mask]
        comp = composite_signal[mask]
        orig_nonflat = orig != 0
        comp_nonflat = comp != 0
        nonflat_union = orig_nonflat | comp_nonflat
        direction_mismatch = int(((orig != comp) & nonflat_union).sum())
        rows.append(
            {
                "split": split,
                "rows": int(mask.sum()),
                "match_rate": float((orig == comp).mean()) if int(mask.sum()) else 0.0,
                "original_signal_count": int(orig_nonflat.sum()),
                "composite_signal_count": int(comp_nonflat.sum()),
                "signal_count_diff": int(comp_nonflat.sum() - orig_nonflat.sum()),
                "signal_count_diff_ratio": float(abs(int(comp_nonflat.sum() - orig_nonflat.sum())) / max(1, int(orig_nonflat.sum()))),
                "direction_mismatch_count": direction_mismatch,
                "direction_mismatch_ratio": float(direction_mismatch / max(1, int(nonflat_union.sum()))),
                "original_long_count": int((orig > 0).sum()),
                "original_short_count": int((orig < 0).sum()),
                "composite_long_count": int((comp > 0).sum()),
                "composite_short_count": int((comp < 0).sum()),
            }
        )
    return rows


def handoff_pass(parity_rows: list[Mapping[str, Any]], composite_metrics: list[Mapping[str, Any]]) -> bool:
    parity = {row["split"]: row for row in parity_rows}
    metrics = {row["split"]: row for row in composite_metrics}
    for split in ("validation", "oos"):
        row = parity[split]
        met = metrics[split]
        if safe_float(row["match_rate"]) < 0.92:
            return False
        if safe_float(row["signal_count_diff_ratio"]) > 0.10:
            return False
        if safe_float(row["direction_mismatch_ratio"]) > 0.08:
            return False
        if safe_float(met["profit_factor"]) <= 1.0:
            return False
        if not f64b.density_in_band(met["trades_per_day"]):
            return False
        if safe_float(met["dd_risk"]) >= 10.0:
            return False
    return True


def export_composite_model(base: Mapping[str, Any], composite: Mapping[str, Any]) -> dict[str, Any]:
    model = composite["model"]
    model_path = MODEL_DIR / f"{COMPOSITE_MODEL_ID}.joblib"
    onnx_path = MODEL_DIR / f"{COMPOSITE_MODEL_ID}.onnx"
    io_path(model_path.parent).mkdir(parents=True, exist_ok=True)
    joblib.dump(model, io_path(model_path))
    export_meta = export_sklearn_to_onnx_zipmap_disabled(model, onnx_path, feature_count=58, target_opset=12, drop_label_output=False)
    sample = np.asarray(base["x_raw"], dtype="float64")[np.asarray(base["finite"], dtype=bool)][:1024]
    expected = ordered_sklearn_probabilities(model, sample, class_order=CLASS_ORDER)
    parity = f64b.onnx_probability_parity(onnx_path, sample, expected)
    return {
        "model_id": COMPOSITE_MODEL_ID,
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
    }


def write_artifacts(final: Mapping[str, Any], original_signal: np.ndarray, composite_signal: np.ndarray) -> dict[str, Path]:
    artifacts = {
        "final_decision": RUN_ROOT / "handoff_verification.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "parity_summary": RUN_ROOT / "handoff_parity_summary.csv",
        "original_signal": RUN_ROOT / "selected_proxy_signal.npy",
        "composite_signal": RUN_ROOT / "composite_handoff_signal.npy",
        "classification": RUN_ROOT / "composite_classification.csv",
        "original_metrics": RUN_ROOT / "original_proxy_metrics.csv",
        "composite_metrics": RUN_ROOT / "composite_proxy_metrics.csv",
    }
    write_json(artifacts["final_decision"], final)
    write_json(artifacts["run_manifest"], {**final, "artifacts": {key: path.as_posix() for key, path in artifacts.items()}})
    write_csv(artifacts["parity_summary"], list(final["parity_rows"]))
    write_csv(artifacts["classification"], list(final["classification_rows"]))
    write_csv(artifacts["original_metrics"], list(final["original_metrics"]))
    write_csv(artifacts["composite_metrics"], list(final["composite_metrics"]))
    np.save(io_path(artifacts["original_signal"]), original_signal)
    np.save(io_path(artifacts["composite_signal"]), composite_signal)
    return artifacts


def write_report(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> None:
    val = metric_row(final["composite_metrics"], "validation")
    oos = metric_row(final["composite_metrics"], "oos")
    pval = metric_row(final["parity_rows"], "validation")
    poos = metric_row(final["parity_rows"], "oos")
    lines = [
        "# F64C Handoff Verification(F64C 인계 검증)",
        "",
        f"Updated(갱신): {final['created_at_utc']}",
        "",
        f"Status(상태): `{final['status']}`",
        "",
        f"Judgment(판정): `{final['judgment']}`",
        "",
        "## Action And Effect(행동과 효과)",
        "",
        "Action(행동): F64B composed signal(합성 신호)을 3-class runtime handoff ONNX(3분류 런타임 인계 온엑스)로 distill(증류)하고 original signal(원 신호)과 composite signal(합성 온엑스 신호)을 비교했다.",
        "",
        "Effect(효과): 기존 MT5 EA(전문가 자문)가 이해하는 3분류 확률 형태로 F64 proxy(프록시)를 넘길 수 있는지 MT5 실행 전에 확인했다.",
        "",
        "## Result Summary(결과 요약)",
        "",
        f"- handoff_pass(인계 통과): `{final['handoff_pass']}`",
        f"- source_best_candidate(원천 최선 후보): `{final['source_best_candidate']}`",
        f"- validation composite PF/density/DD(검증 합성 수익 팩터/빈도/손실폭): `{fmt(val.get('profit_factor'))}` / `{fmt(val.get('trades_per_day'))}` / `{fmt(val.get('dd_risk'))}%`",
        f"- OOS composite PF/density/DD(표본외 합성 수익 팩터/빈도/손실폭): `{fmt(oos.get('profit_factor'))}` / `{fmt(oos.get('trades_per_day'))}` / `{fmt(oos.get('dd_risk'))}%`",
        f"- validation match/signal_diff/direction_mismatch(검증 일치율/신호 차이/방향 불일치): `{fmt(pval.get('match_rate'))}` / `{pval.get('signal_count_diff')}` / `{fmt(pval.get('direction_mismatch_ratio'))}`",
        f"- OOS match/signal_diff/direction_mismatch(표본외 일치율/신호 차이/방향 불일치): `{fmt(poos.get('match_rate'))}` / `{poos.get('signal_count_diff')}` / `{fmt(poos.get('direction_mismatch_ratio'))}`",
        f"- ONNX parity(온엑스 동등성): `{final['model_artifacts']['onnx_parity'].get('passed')}`, max_abs_diff(최대 절대 차이) `{fmt(final['model_artifacts']['onnx_parity'].get('max_abs_diff'))}`",
        "",
        "## Artifacts(산출물)",
        "",
        f"- final decision(최종 판단): `{artifacts['final_decision'].as_posix()}`",
        f"- parity summary(동등성 요약): `{artifacts['parity_summary'].as_posix()}`",
        f"- composite model(합성 모델): `{final['model_artifacts']['onnx_path']}`",
        "",
        "## Boundary(경계)",
        "",
        "This is local handoff verification(로컬 인계 검증) only. It does not claim runtime authority(런타임 권위), promotion(승격), baseline(기준선), live readiness(실거래 준비), completion(완성), or Goal Achieve(목표 달성).",
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
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(final))
    upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    row = ledger_row(final, artifacts)
    upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(stage_ledger, "ledger_row_id", row)
    append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(final))


def workspace_state(final: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            f"current_stage_id: {STAGE_ID}",
            f"current_run_id: {RUN_ID}",
            f"latest_completed_run_id: {RUN_ID}",
            f"current_status: {final['status']}",
            f"current_judgment: {final['judgment']}",
            "next_stage_id: null",
            f"next_run_id: {final['next_run_id']}",
            "runtime_probe_status: ready_for_mt5_probe" if final["handoff_pass"] else "runtime_probe_status: blocked_handoff_adapter_mismatch",
            "runtime_authority: not_claimed",
            "operating_promotion: not_claimed",
            "live_readiness: not_claimed",
            "goal_achieve: not_claimed",
            f"updated_at_utc: '{final['created_at_utc']}'",
            "notes:",
            f"  - \"F64C handoff verification(인계 검증): pass={final['handoff_pass']}; source_best={final['source_best_candidate']}; next={final['next_run_id']}.\"",
            "  - \"Grok pre-MT5 review(비싼 MT5 전 그록 검토) classified needs_local_verification(로컬 검증 필요); local verification now recorded(기록됨).\"",
            "  - \"No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed(주장 없음).\"",
        ]
    )


def current_working_state(final: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Frontier64(F64, 전선 64단계)는 F64C handoff verification(인계 검증)을 완료했다.

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- judgment(판정): `{final['judgment']}`
- source_best_candidate(원천 최선 후보): `{final['source_best_candidate']}`
- handoff_pass(인계 통과): `{final['handoff_pass']}`
- next_run(다음 실행): `{final['next_run_id']}`

Action(행동): F64B binary hazard plus simple direction(이진 위험 + 단순 방향) 합성 신호를 MT5 EA(전문가 자문)가 읽는 3-class ONNX(3분류 온엑스) 인계 형태로 검증했다.

Effect(효과): MT5 runtime probe(MT5 런타임 탐침)를 실행하기 전에 proxy-runtime gap(프록시-런타임 차이)의 원인이 될 수 있는 handoff mismatch(인계 불일치)를 먼저 측정했다.

Claim boundary(주장 경계): runtime probe observation(런타임 탐침 관찰)도 아직 없다. completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
"""


def selection_status(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> str:
    return f"""# F64 Selection Status(F64 선택 상태)

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- selected_proxy_candidate(선택 프록시 후보): `{final['source_best_candidate']}`
- selected_runtime_handoff_model(선택 런타임 인계 모델): `{final['model_artifacts']['model_id']}`
- handoff_pass(인계 통과): `{final['handoff_pass']}`
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
        "selected_runtime_handoff_model": final["model_artifacts"]["model_id"],
        "handoff_pass": final["handoff_pass"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
        "claim_boundary": final["claim_boundary"],
    }


def review_index(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> str:
    return "\n".join(
        [
            "# F64 Review Index(F64 검토 색인)",
            "",
            "- `runA_report.md`: stage-open report(단계 개방 보고)",
            "- `runB_report.md`: proxy scout report(프록시 탐색 보고)",
            "- `handoff_verification_report.md`: handoff verification(인계 검증)",
            "- `grok_stage_open_receipt.md`: Grok stage-open receipt(그록 단계 개방 영수증)",
            "- `required_gate_coverage_audit.md`: required gate coverage audit(필수 게이트 커버리지 감사)",
            "- `stage_run_ledger.csv`: stage-local run ledger(단계 로컬 실행 장부)",
            "",
        ]
    )


def gate_audit(final: Mapping[str, Any]) -> str:
    runtime_probe_gate = "ready(준비)" if final["handoff_pass"] else "blocked(차단)"
    return f"""# F64 Required Gate Coverage Audit(F64 필수 게이트 커버리지 감사)

- stage_open_grok_review(단계 개방 그록 검토): `accepted(수용)`
- proxy_completed(프록시 완료): `{PARENT_RUN_ID}`
- pre_mt5_grok_review(비싼 MT5 전 그록 검토): `needs_local_verification(로컬 검증 필요)`
- local_handoff_verification(로컬 인계 검증): `{final['judgment']}`
- runtime_probe_gate(런타임 탐침 게이트): `{runtime_probe_gate}`
- final_claim_guard(최종 주장 보호): forbidden claims(금지 주장) 모두 not_claimed(주장 없음).
"""


def run_registry_row(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "handoff_verification(인계 검증)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"handoff_pass={final['handoff_pass']};next={final['next_run_id']};model={final['model_artifacts']['model_id']}",
        "family": "runtime_parity(런타임 동등성)",
        "primary_report": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": final["created_at_utc"][:10],
        "decision": final["judgment"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": "handoff_verification_only_no_runtime_authority(인계 검증 전용, 런타임 권위 없음)",
        "report_path": REPORT_PATH.as_posix(),
        "trained_models": 1,
        "onnx_parity": final["model_artifacts"]["onnx_parity"].get("passed"),
        "best_model_id": final["model_artifacts"]["model_id"],
        "view": "handoff_verification(인계 검증)",
        "tier": "Tier A(티어 A)",
        "metric_scope": "local_handoff_not_mt5(로컬 인계, MT5 아님)",
        "external_verification_status": "pending_mt5_runtime_probe(MT5 런타임 탐침 대기)" if final["handoff_pass"] else "blocked_handoff_mismatch(인계 불일치 차단)",
        "result_judgment": final["judgment"],
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": (STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md").as_posix(),
        "runtime_authority": "not_claimed(주장 없음)",
        "operating_promotion": "not_claimed(주장 없음)",
        "run_family": "frontier_handoff_verification(전선 인계 검증)",
        "run_type": "handoff_verification(인계 검증)",
        "output_path": artifacts["final_decision"].as_posix(),
        "result_path": artifacts["final_decision"].as_posix(),
        "goal_achieve": "not_claimed(주장 없음)",
        "source_authority": "reference_not_inheritance(참조이지 상속 아님)",
    }


def ledger_row(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> dict[str, Any]:
    row = run_registry_row(final, artifacts)
    row.update(
        {
            "ledger_row_id": f"{RUN_ID}__handoff_verification",
            "subrun_id": f"{RUN_ID}__handoff_verification",
            "record_view": "handoff_verification(인계 검증)",
            "tier_scope": "Tier A separate(티어 A 분리)",
            "kpi_scope": "local_handoff_not_runtime(로컬 인계, 런타임 아님)",
            "scoreboard_lane": "handoff_verification(인계 검증)",
            "primary_kpi": f"handoff_pass={final['handoff_pass']};onnx_parity={final['model_artifacts']['onnx_parity'].get('passed')}",
            "guardrail_kpi": "no_runtime_authority_no_promotion_no_completion(런타임 권위/승격/완성 없음)",
            "path": REPORT_PATH.as_posix(),
            "notes": f"next={final['next_run_id']}; source_best={final['source_best_candidate']}",
        }
    )
    return row


def changelog_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {final['created_at_utc'][:10]} Frontier64C Handoff Verification(F64C 인계 검증)\n\n- action(행동): `{RUN_ID}`로 F64B composed signal(합성 신호)을 3-class runtime handoff ONNX(3분류 런타임 인계 온엑스)로 검증했다.\n- effect(효과): handoff_pass(인계 통과) `{final['handoff_pass']}`를 기록하고 next(다음)를 `{final['next_run_id']}`로 설정했다.\n- boundary(경계): MT5 runtime probe(MT5 런타임 탐침)는 아직 pending(대기)이며 runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.\n"


def metric_row(rows: Any, split: str) -> dict[str, Any]:
    for row in rows:
        if row.get("split") == split:
            return dict(row)
    return {}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    pd.DataFrame(json_ready(rows)).to_csv(io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = read_csv_header(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, lineterminator="\n")
        writer.writeheader()


def read_csv_header(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv(path: Path, key: str, row: Mapping[str, Any]) -> None:
    header = read_csv_header(path)
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for existing in csv.DictReader(handle):
            rows.append(dict(existing))
    normalized = {column: f03b.stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: f03b.stringify(item.get(column, "")) for column in header})


def append_once(path: Path, marker: str, line: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    marker_text = f"<!-- {marker} -->"
    if marker_text in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    f03b.write_text_sig(path, text + f"\n{marker_text}\n{line}")


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
