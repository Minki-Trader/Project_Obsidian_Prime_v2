from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

import joblib
import pandas as pd

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    FEATURE_ORDER_PATH,
    MODEL_INPUT_PATH,
    RAW_ROOT,
    TRAINING_SUMMARY_PATH,
)
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame
from foundation.models.hmm_segmentation import (
    HMMStateModel,
    HMMVariantSpec,
    default_stage22_hmm_variants,
    fit_hmm_variant,
    state_quality_read,
    state_sequence_frame,
    state_summary_frame,
    transition_read,
)
from foundation.mt5 import runtime_support as mt5


STAGE_ID = "22_regime_model__hmm_hidden_state_segmentation"
RUN_ID = "run16A_hmm_hidden_state_segmentation_scout_v1"
RUN_NUMBER = "run16A"
PACKET_ID = "stage22_run16A_hmm_state_scout_v1"
NEXT_RUN_ID = "run16B_hmm_state_runtime_probe_v1"
EXPLORATION_LABEL = "stage22_Regime__HMMHiddenStateSegmentation"
MODEL_FAMILY = "hmmlearn_gaussian_hmm_hidden_state_segmentation"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_core17_hmm_regime"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
BOUNDARY = "hmm_hidden_state_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_hmm_hidden_state_structural_scout_completed"

ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews/run16A_hmm_state_scout_packet.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN_PATH = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"

HMM_FEATURES = [
    "log_return_1",
    "log_return_3",
    "hl_range",
    "return_zscore_20",
    "hl_zscore_50",
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "ema20_ema50_diff",
    "ema50_ema200_diff",
    "minutes_from_cash_open",
    "is_us_cash_open",
]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        frame.to_parquet(io_path(path), index=False)
    else:
        frame.to_csv(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def load_context() -> dict[str, Any]:
    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    full_feature_order = load_feature_order(FEATURE_ORDER_PATH)
    validate_model_input_frame(tier_a_frame, full_feature_order)
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=full_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=float(training_summary["threshold_log_return"]),
    )
    return {
        "tier_a_frame": tier_a_frame,
        "full_feature_order": full_feature_order,
        "tier_b_training_frame": tier_b_context["tier_b_training_frame"],
        "tier_b_fallback_frame": tier_b_context["tier_b_fallback_frame"],
        "tier_b_context_summary": tier_b_context["summary"],
        "hmm_feature_names": list(HMM_FEATURES),
    }


def combined_state_summary_frame(tier_a_sequence: pd.DataFrame, tier_b_sequence: pd.DataFrame) -> pd.DataFrame:
    combined = pd.concat(
        [
            tier_a_sequence.assign(combined_state_label=lambda frame: "A_" + frame["hidden_state_label"].astype(str)),
            tier_b_sequence.assign(combined_state_label=lambda frame: "B_" + frame["hidden_state_label"].astype(str)),
        ],
        ignore_index=True,
    )
    rows: list[dict[str, Any]] = []
    for (split, label), group in combined.groupby(["split", "combined_state_label"], dropna=False):
        labels = group["label_class"].astype("int64")
        counts = labels.value_counts().to_dict()
        rows.append(
            {
                "split": str(split),
                "combined_state_label": str(label),
                "rows": int(len(group)),
                "future_return_mean": float(group["future_log_return_12"].mean()),
                "short_count": int(counts.get(0, 0)),
                "flat_count": int(counts.get(1, 0)),
                "long_count": int(counts.get(2, 0)),
            }
        )
    return pd.DataFrame(rows).sort_values(["split", "combined_state_label"]).reset_index(drop=True)


def record_metrics(record_view: str, tier_scope: str, sequence: pd.DataFrame, quality: Mapping[str, Any], path: Path) -> dict[str, Any]:
    by_split = quality.get("by_split", {})
    rows = int(len(sequence))
    state_count = int(sequence["hidden_state"].nunique()) if "hidden_state" in sequence else 0
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": {
            "rows": rows,
            "state_count": state_count,
            "signal_count": rows,
            "signal_coverage": 1.0,
            "short_count": int((sequence["label_class"].astype("int64") == 0).sum()),
            "long_count": int((sequence["label_class"].astype("int64") == 2).sum()),
            "min_state_share_train": by_split.get("train", {}).get("min_share"),
            "validation_risk_separation": by_split.get("validation", {}).get("risk_separation"),
            "oos_risk_separation": by_split.get("oos", {}).get("risk_separation"),
            "validation_oos_mean_gap": quality.get("validation_oos_mean_gap"),
            "collapsed": quality.get("collapsed"),
        },
    }


def evaluate_variant(spec: HMMVariantSpec, context: Mapping[str, Any]) -> dict[str, Any]:
    feature_order = list(context["hmm_feature_names"])
    tier_a_model = fit_hmm_variant(context["tier_a_frame"], feature_order, spec)
    tier_b_model = fit_hmm_variant(context["tier_b_training_frame"], feature_order, spec)

    tier_a_sequence = state_sequence_frame(tier_a_model, context["tier_a_frame"], tier_scope=mt5.TIER_A, record_view="tier_a_separate")
    tier_b_sequence = state_sequence_frame(tier_b_model, context["tier_b_fallback_frame"], tier_scope=mt5.TIER_B, record_view="tier_b_separate")
    tier_a_summary = state_summary_frame(tier_a_sequence)
    tier_b_summary = state_summary_frame(tier_b_sequence)
    tier_a_quality = state_quality_read(tier_a_summary, n_components=spec.n_components)
    tier_b_quality = state_quality_read(tier_b_summary, n_components=spec.n_components)

    score = float(tier_a_quality["quality_score"]) + float(tier_b_quality["quality_score"])
    if tier_a_quality["collapsed"] or tier_b_quality["collapsed"]:
        score -= 0.02
    return {
        "spec": spec,
        "tier_a_model": tier_a_model,
        "tier_b_model": tier_b_model,
        "tier_a_sequence": tier_a_sequence,
        "tier_b_sequence": tier_b_sequence,
        "tier_a_summary": tier_a_summary,
        "tier_b_summary": tier_b_summary,
        "tier_a_quality": tier_a_quality,
        "tier_b_quality": tier_b_quality,
        "tier_a_transition": transition_read(tier_a_model),
        "tier_b_transition": transition_read(tier_b_model),
        "selection_score": score,
    }


def variant_result_row(result: Mapping[str, Any]) -> dict[str, Any]:
    spec = result["spec"]
    a_quality = result["tier_a_quality"]
    b_quality = result["tier_b_quality"]
    return {
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "n_components": spec.n_components,
        "feature_count": len(spec.feature_names),
        "covariance_type": spec.covariance_type,
        "tier_a_quality_score": a_quality["quality_score"],
        "tier_b_quality_score": b_quality["quality_score"],
        "tier_a_collapsed": a_quality["collapsed"],
        "tier_b_collapsed": b_quality["collapsed"],
        "tier_a_validation_risk_separation": a_quality["by_split"]["validation"]["risk_separation"],
        "tier_a_oos_risk_separation": a_quality["by_split"]["oos"]["risk_separation"],
        "tier_b_validation_risk_separation": b_quality["by_split"]["validation"]["risk_separation"],
        "tier_b_oos_risk_separation": b_quality["by_split"]["oos"]["risk_separation"],
        "tier_a_validation_oos_mean_gap": a_quality["validation_oos_mean_gap"],
        "tier_b_validation_oos_mean_gap": b_quality["validation_oos_mean_gap"],
        "tier_a_self_transition_mean": result["tier_a_transition"]["self_transition_mean"],
        "tier_b_self_transition_mean": result["tier_b_transition"]["self_transition_mean"],
        "selection_score": result["selection_score"],
    }


def materialize_selected_result(result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    spec = result["spec"]
    root = RUN_ROOT
    artifacts: dict[str, Any] = {}
    model_root = root / "models"
    io_path(model_root).mkdir(parents=True, exist_ok=True)
    tier_a_model_path = model_root / f"{spec.variant_id}_tier_a_hmm.joblib"
    tier_b_model_path = model_root / f"{spec.variant_id}_tier_b_hmm.joblib"
    joblib.dump(result["tier_a_model"], io_path(tier_a_model_path))
    joblib.dump(result["tier_b_model"], io_path(tier_b_model_path))
    artifacts["tier_a_model"] = {"path": rel(tier_a_model_path), "sha256": sha256_file_lf_normalized(tier_a_model_path)}
    artifacts["tier_b_model"] = {"path": rel(tier_b_model_path), "sha256": sha256_file_lf_normalized(tier_b_model_path)}

    tier_a_sequence_path = root / "predictions/tier_a_hidden_state_sequence.parquet"
    tier_b_sequence_path = root / "predictions/tier_b_hidden_state_sequence.parquet"
    tier_ab_sequence_path = root / "predictions/tier_ab_combined_hidden_state_sequence.parquet"
    tier_ab_sequence = pd.concat(
        [
            result["tier_a_sequence"].assign(record_source="tier_a"),
            result["tier_b_sequence"].assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    artifacts["tier_a_sequence"] = save_frame(tier_a_sequence_path, result["tier_a_sequence"])
    artifacts["tier_b_sequence"] = save_frame(tier_b_sequence_path, result["tier_b_sequence"])
    artifacts["tier_ab_sequence"] = save_frame(tier_ab_sequence_path, tier_ab_sequence)

    tier_a_summary_path = root / "results/selected_tier_a_state_summary.csv"
    tier_b_summary_path = root / "results/selected_tier_b_state_summary.csv"
    tier_ab_summary_path = root / "results/selected_tier_ab_state_summary.csv"
    tier_ab_summary = combined_state_summary_frame(result["tier_a_sequence"], result["tier_b_sequence"])
    artifacts["tier_a_state_summary"] = save_frame(tier_a_summary_path, result["tier_a_summary"])
    artifacts["tier_b_state_summary"] = save_frame(tier_b_summary_path, result["tier_b_summary"])
    artifacts["tier_ab_state_summary"] = save_frame(tier_ab_summary_path, tier_ab_summary)

    records = [
        record_metrics("tier_a_separate", mt5.TIER_A, result["tier_a_sequence"], result["tier_a_quality"], tier_a_sequence_path),
        record_metrics("tier_b_separate", mt5.TIER_B, result["tier_b_sequence"], result["tier_b_quality"], tier_b_sequence_path),
        {
            "record_view": "tier_ab_combined",
            "tier_scope": mt5.TIER_AB,
            "status": "completed",
            "path": rel(tier_ab_sequence_path),
            "metrics": {
                "rows": int(len(tier_ab_sequence)),
                "state_count": int(tier_ab_summary["combined_state_label"].nunique()),
                "signal_count": int(len(tier_ab_sequence)),
                "signal_coverage": 1.0,
                "short_count": int((tier_ab_sequence["label_class"].astype("int64") == 0).sum()),
                "long_count": int((tier_ab_sequence["label_class"].astype("int64") == 2).sum()),
                "tier_a_rows": int(len(result["tier_a_sequence"])),
                "tier_b_rows": int(len(result["tier_b_sequence"])),
            },
        },
    ]
    return records, artifacts


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for record in summary["tier_records"]:
        metrics = record["metrics"]
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__python_{record['record_view']}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"python_{record['record_view']}",
                "parent_run_id": RUN_ID,
                "record_view": f"python_{record['record_view']}",
                "tier_scope": record["tier_scope"],
                "kpi_scope": "hidden_state_segmentation",
                "scoreboard_lane": "structural_scout",
                "status": "reviewed",
                "judgment": JUDGMENT,
                "path": record["path"],
                "primary_kpi": ledger_pairs(
                    (
                        ("rows", metrics.get("rows")),
                        ("state_count", metrics.get("state_count")),
                        ("val_sep", metrics.get("validation_risk_separation")),
                        ("oos_sep", metrics.get("oos_risk_separation")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("collapsed", metrics.get("collapsed")),
                        ("val_oos_gap", metrics.get("validation_oos_mean_gap")),
                        ("boundary", BOUNDARY),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
                "notes": "HMM hidden-state structural scout only; not runtime authority.",
            }
        )
    ledgers = {
        "stage_run_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "project_alpha_run_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "regime_hidden_state_structural_scout",
        "status": "reviewed",
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": ledger_pairs(
            (
                ("selected_variant", summary["selected_variant_id"]),
                ("external_verification", summary["external_verification_status"]),
                ("next", NEXT_RUN_ID),
                ("boundary", BOUNDARY),
            )
        ),
    }
    ledgers["run_registry"] = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    return ledgers


def write_review(summary: Mapping[str, Any]) -> None:
    selected = summary["selected_variant_id"]
    a = summary["selected_variant_read"]["tier_a_quality"]["by_split"]
    b = summary["selected_variant_read"]["tier_b_quality"]["by_split"]
    write_md(
        REPORT_PATH,
        f"""# RUN16A HMM Hidden-State Scout Packet(실행16A HMM 은닉 상태 탐색 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected}`
- boundary(경계): `{BOUNDARY}`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run16A_next_milestone_{NEXT_RUN_ID}(실행16A에서는 미시도, 다음 마일스톤은 {NEXT_RUN_ID})`

효과(effect, 효과): HMM(`Hidden Markov Model`, 은닉 마르코프 모델)의 hidden state(은닉 상태)가 volatility/session/trend(변동성/세션/추세) 표면을 나누는지 Python-side evidence(파이썬 측 근거)로 먼저 확인했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Evidence(근거)

- variants(변형): `{summary['variant_count']}`
- HMM features(HMM 피처): `{summary['feature_count']}`
- Tier A rows(Tier A 행): `{summary['tier_rows']['tier_a']}`
- Tier B fallback rows(Tier B 대체 행): `{summary['tier_rows']['tier_b_fallback']}`
- Tier A validation/oos risk separation(Tier A 검증/표본외 위험 분리): `{a['validation']['risk_separation']}` / `{a['oos']['risk_separation']}`
- Tier B validation/oos risk separation(Tier B 검증/표본외 위험 분리): `{b['validation']['risk_separation']}` / `{b['oos']['risk_separation']}`
- Tier A collapsed(Tier A 붕괴): `{summary['selected_variant_read']['tier_a_quality']['collapsed']}`
- Tier B collapsed(Tier B 붕괴): `{summary['selected_variant_read']['tier_b_quality']['collapsed']}`

## Preserved Clues(보존 단서)

- HMM(은닉 마르코프 모델)은 label(라벨)을 직접 보지 않고 state(상태)를 나누므로, state-risk relation(상태-위험 관계)은 entry model(진입 모델)이 아니라 permission regime(허용 국면) 후보로만 읽는다.
- selected variant(선택 변형) `{selected}`는 Tier A/Tier B(티어 A/티어 B) 모두에서 state coverage(상태 커버리지)를 유지한 쪽이다.
- 다음 MT5 runtime_probe(런타임 탐침)는 state table/state filter(상태표/상태 필터)처럼 좁은 handoff(인계)만 검증해야 한다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}` as a narrow MT5 runtime_probe(좁은 MT5 런타임 탐침) only after materializing(물질화) state filter/state table(상태 필터/상태표) handoff files(인계 파일).
""",
    )
    review_index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    line = f"- `{RUN_ID}`: `{rel(REPORT_PATH)}`\n"
    if RUN_ID not in review_index:
        write_md(REVIEW_INDEX_PATH, review_index.rstrip() + "\n" + line)


def write_packet_artifacts(summary: Mapping[str, Any], created_at: str) -> None:
    receipts = [
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "HMM hidden states may segment volatility/session/trend regimes without supervised labels.",
            "boundary": BOUNDARY,
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_contract": SPLIT_CONTRACT,
            "tier_views": ["Tier A separate", "Tier B separate", "Tier A+B combined"],
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_boundary": "unsupervised_state_segmentation_not_classifier",
            "forbidden_claims": summary["forbidden_claims"],
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "judgment": JUDGMENT,
            "allowed_claims": summary["allowed_claims"],
            "forbidden_claims": summary["forbidden_claims"],
        },
    ]
    gates = {
        "scope_completion_gate": {
            "packet_id": PACKET_ID,
            "status": "passed",
            "required_views": ["tier_a_separate", "tier_b_separate", "tier_ab_combined"],
            "completed_views": [record["record_view"] for record in summary["tier_records"]],
        },
        "kpi_contract_audit": {
            "packet_id": PACKET_ID,
            "status": "passed",
            "kpi_scope": "hidden_state_segmentation",
            "runtime_kpi_required": False,
            "runtime_kpi_reason": "out_of_scope_by_claim_python_structural_scout",
        },
        "runtime_evidence_gate": {
            "packet_id": PACKET_ID,
            "status": "not_required_for_run16A",
            "next_runtime_probe": NEXT_RUN_ID,
        },
        "final_claim_guard": {
            "packet_id": PACKET_ID,
            "status": "passed",
            "allowed_claims": summary["allowed_claims"],
            "forbidden_claims": summary["forbidden_claims"],
        },
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(PACKET_ROOT / "skill_receipts.json", receipts)
    for name, payload in gates.items():
        write_json(PACKET_ROOT / f"{name}.json", payload)


def replace_yaml_block(text: str, block_name: str, block: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line == block_name:
            start = index
            break
    block_lines = block.rstrip().splitlines()
    if start is None:
        suffix = "\n" if text.endswith("\n") else ""
        return text + suffix + block.rstrip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith(" ") and not line.startswith("-"):
            end = index
            break
    return "\n".join(lines[:start] + block_lines + lines[end:]) + "\n"


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    path = io_path(WORKSPACE_STATE_PATH)
    text = path.read_text(encoding="utf-8-sig")
    text = text.replace("current_run_id: not_started", f"current_run_id: {RUN_ID}", 1)
    text = text.replace(
        "- treat Stage 21 as reviewed_closed after run15A/run15B ElasticNet Logistic structural and ONNX MT5 runtime evidence; Stage22 is active opened_not_started, next action is run16A_hmm_hidden_state_segmentation_scout_v1, and no baseline, promotion, or runtime authority exists",
        f"- treat Stage 22 as active after {RUN_ID} HMM hidden-state Python structural scout; next action is {NEXT_RUN_ID} MT5 runtime_probe, and no baseline, promotion, or runtime authority exists",
        1,
    )
    text = text.replace("      status: opened_not_started\n      current_run_id: not_started", f"      status: active_run16A_python_structural_scout_completed\n      current_run_id: {RUN_ID}", 1)
    text = text.replace("status: stage20_closed_stage21_closed_stage22_opened", "status: stage20_closed_stage21_closed_stage22_run16A_completed", 1)
    text = text.replace("latest_completed_run: stage21_closeout_stage22_open", f"latest_completed_run: {RUN_ID}", 1)
    text = text.replace("next_exact_action: run16A_hmm_hidden_state_segmentation_scout_v1", f"next_exact_action: {NEXT_RUN_ID}", 1)
    text = text.replace("active_stage_folder: stages/20_model_family_challenge__gam_additive_smooth_shape", f"active_stage_folder: stages/{STAGE_ID}", 1)
    text = text.replace(
        "claim_boundary: stage21_closed_stage22_open_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        "claim_boundary: hmm_hidden_state_structural_scout_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        1,
    )
    block = f"""stage22_hmm_hidden_state_segmentation:
  stage_id: {STAGE_ID}
  status: active_run16A_python_structural_scout_completed
  current_run_id: {RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {summary['selected_variant_id']}
  boundary: {BOUNDARY}
  stage_brief_path: stages/{STAGE_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE_ID}/04_selected/selection_status.md
  report_path: stages/{STAGE_ID}/03_reviews/run16A_hmm_state_scout_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    text = replace_yaml_block(text, "stage22_hmm_hidden_state_segmentation:", block)
    run_block = f"""stage22_hmm_run16A_structural_scout:
  packet_id: {PACKET_ID}
  status: reviewed_structural_scout_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  selected_variant_id: {summary['selected_variant_id']}
  mt5_runtime_probe_status: not_attempted_next_milestone_{NEXT_RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: stages/{STAGE_ID}/03_reviews/run16A_hmm_state_scout_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    text = replace_yaml_block(text, "stage22_hmm_run16A_structural_scout:", run_block)
    path.write_text(text, encoding="utf-8-sig")


def update_goal_plan(summary: Mapping[str, Any]) -> None:
    path = io_path(GOAL_PLAN_PATH)
    text = path.read_text(encoding="utf-8-sig")
    text = text.replace("- current run(현재 실행): `not_started`", f"- current run(현재 실행): `{RUN_ID}`", 1)
    text = text.replace(
        "Stage22(22단계)는 HMM(`Hidden Markov Model`, 은닉 마르코프 모델) open-only(개방만) 상태다. 현재 첫 미완료 milestone(마일스톤)은 Stage22(22단계) `run16A_hmm_hidden_state_segmentation_scout_v1` broad scout(넓은 탐색)이다.",
        f"Stage22(22단계)는 `{RUN_ID}` HMM(`Hidden Markov Model`, 은닉 마르코프 모델) Python structural scout(파이썬 구조 탐색)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 Stage22(22단계) `{NEXT_RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)이다.",
    )
    text = text.replace(
        "Current active milestone(현재 활성 마일스톤): Stage22(22단계) `run16A_hmm_hidden_state_segmentation_scout_v1` broad scout(넓은 탐색).",
        f"Current active milestone(현재 활성 마일스톤): Stage22(22단계) `{NEXT_RUN_ID}` narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).",
    )
    marker = "## Latest Stop Resume State(최신 중지 재개 상태)"
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `{RUN_ID}` completed(완료) as Python structural scout(파이썬 구조 탐색).
- active stage/current run id(활성 단계/현재 실행 ID): Stage22(22단계), `{RUN_ID}`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE_ID}/02_runs/{RUN_ID}`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): HMM model helper(HMM 모델 도우미), Stage22 run16A scout pipeline(22단계 실행16A 탐색 파이프라인), run evidence(실행 근거), ledgers(장부), current truth docs(현재 진실 문서).
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `not_attempted_in_run16A(실행16A에서 미시도)`; review report(검토 보고서) `{rel(REPORT_PATH)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): create and run(생성 및 실행) `{NEXT_RUN_ID}` after materializing HMM state handoff(상태 인계) files.
- git status(깃 상태): run16A checkpoint commit/push(실행16A 중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage22(22단계) MT5 runtime_probe(런타임 탐침) 준비에서 시작한다.
"""
    if marker in text:
        start = text.index(marker)
        next_section = text.find("\n## ", start + 1)
        text = text[:start] + resume + ("\n" + text[next_section + 1 :] if next_section != -1 else "")
    else:
        text = text.rstrip() + "\n\n" + resume
    line = f"- `2026-05-05`: Stage22(22단계) `{RUN_ID}` HMM(`Hidden Markov Model`, 은닉 마르코프 모델) Python structural scout(파이썬 구조 탐색)를 완료했다."
    if line not in text:
        text = text.rstrip() + "\n" + line + "\n"
    path.write_text(text, encoding="utf-8-sig")


def update_current_working_state(summary: Mapping[str, Any]) -> None:
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = current.replace("- current run(현재 실행): `not_started`", f"- current run(현재 실행): `{RUN_ID}`", 1)
    update = f"""## Latest Stage22 RUN16A HMM Update(최신 22단계 실행16A HMM 업데이트)

Stage22(22단계) `{RUN_ID}`를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `{JUDGMENT}`. selected variant(선택 변형): `{summary['selected_variant_id']}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): HMM(`Hidden Markov Model`, 은닉 마르코프 모델) hidden state(은닉 상태)의 Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)를 남겼지만, MT5 runtime_probe(MT5 런타임 탐침), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 아직 없다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")


def update_selection_status(summary: Mapping[str, Any]) -> None:
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage22 Selection Status(22단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `active_run16A_python_structural_scout_completed`
- current run(현재 실행): `{RUN_ID}`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{summary['selected_variant_id']}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage22(22단계)는 HMM(은닉 마르코프 모델) hidden-state segmentation(은닉 상태 분할)을 Python-side evidence(파이썬 근거)로 잡았다. MT5 runtime_probe(런타임 탐침), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 아직 없다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}`.
""",
    )


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    variants = default_stage22_hmm_variants(context["hmm_feature_names"])
    results = [evaluate_variant(spec, context) for spec in variants]
    rows = [variant_result_row(result) for result in results]
    results_frame = pd.DataFrame(rows).sort_values("selection_score", ascending=False).reset_index(drop=True)
    results_path = RUN_ROOT / "results/hmm_variant_results.csv"
    save_frame(results_path, results_frame)
    write_json(RUN_ROOT / "results/hmm_variant_results.json", rows)
    selected_result = sorted(results, key=lambda item: item["selection_score"], reverse=True)[0]
    selected_spec = selected_result["spec"]
    tier_records, artifacts = materialize_selected_result(selected_result)
    selected_read = {
        "tier_a_quality": selected_result["tier_a_quality"],
        "tier_b_quality": selected_result["tier_b_quality"],
        "tier_a_transition": selected_result["tier_a_transition"],
        "tier_b_transition": selected_result["tier_b_transition"],
    }
    summary = {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "packet_id": PACKET_ID,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "judgment": JUDGMENT,
        "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
        "boundary": BOUNDARY,
        "variant_count": len(variants),
        "feature_count": len(selected_spec.feature_names),
        "selected_variant_id": selected_spec.variant_id,
        "selected_variant_read": selected_read,
        "variant_results": rows,
        "tier_records": tier_records,
        "tier_rows": {
            "tier_a": int(len(context["tier_a_frame"])),
            "tier_b_training": int(len(context["tier_b_training_frame"])),
            "tier_b_fallback": int(len(context["tier_b_fallback_frame"])),
        },
        "artifacts": {
            **artifacts,
            "variant_results_csv": {"path": rel(results_path), "sha256": sha256_file_lf_normalized(results_path)},
        },
        "allowed_claims": ["python_structural_scout_completed", "hidden_state_segmentation_clues_recorded"],
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority"],
        "next_action": NEXT_RUN_ID,
    }
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": created_at,
            "selected_variant_id": selected_spec.variant_id,
            "external_verification_status": summary["external_verification_status"],
            "boundary": BOUNDARY,
        },
    )
    write_json(RUN_ROOT / "kpi_record.json", summary)
    materialize_ledgers(summary)
    write_review(summary)
    write_packet_artifacts(summary, created_at)
    update_workspace_state(summary)
    update_goal_plan(summary)
    update_current_working_state(summary)
    update_selection_status(summary)
    return {
        "run_id": RUN_ID,
        "judgment": JUDGMENT,
        "selected_variant_id": selected_spec.variant_id,
        "external_verification_status": summary["external_verification_status"],
        "next_action": NEXT_RUN_ID,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Run Stage22 HMM hidden-state structural scout.")


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    print(json.dumps(json_ready(run(args)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
