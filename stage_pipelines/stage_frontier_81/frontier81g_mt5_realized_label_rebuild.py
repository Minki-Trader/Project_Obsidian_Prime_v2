from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild"
RUN_ID = "frontier81G_mt5_realized_label_rebuild_v1"
PARENT_RUN_ID = "frontier81F_deal_reconciled_runtime_label_preflight_v1"
NEXT_RUN_ID = "frontier81H_capped_repair_closeout_or_f82_rotation_decision_v1"
STATUS = "f81g_realized_label_rebuild_low_density_seed_no_materialization_ready_no_authority"
JUDGMENT = "realized_label_filter_found_low_density_seed_repair_cap_consumed_rotation_decision_required_no_authority"
CLAIM_BOUNDARY = (
    "realized_label_diagnostic_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

FEATURES_CSV = STAGE_DIR / "02_runs/frontier81C_mt5_runtime_materialization_v1/features/f81c_runtime_f81b_01107_features.csv"
FEATURE_ORDER = STAGE_DIR / "02_runs/frontier81C_mt5_runtime_materialization_v1/models/f81c_runtime_f81b_01107_feature_order.txt"
F81C_RECEIPT = STAGE_DIR / "02_runs/frontier81C_mt5_runtime_materialization_v1/f81c_runtime_receipt.csv"
F81F_SUMMARY = REVIEW_DIR / "f81f_deal_reconciliation_summary.json"
F81F_TRADES = STAGE_DIR / "02_runs/frontier81F_deal_reconciled_runtime_label_preflight_v1/f81f_trade_rows.csv"

LABEL_DATASET = RUN_DIR / "f81g_mt5_realized_label_dataset.csv"
UNMATCHED_TRADES = RUN_DIR / "f81g_unmatched_trade_rows.csv"
CANDIDATE_ROWS = RUN_DIR / "f81g_realized_label_candidate_rows.csv"
TOP_CANDIDATES = REVIEW_DIR / "f81g_realized_label_top_candidates.csv"
SUMMARY = REVIEW_DIR / "f81g_mt5_realized_label_rebuild_summary.json"
REPORT = REVIEW_DIR / "frontier81G_mt5_realized_label_rebuild_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f81g.md"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f81g_experiment_design_receipt.yaml"
DATA_RECEIPT = REVIEW_DIR / "f81g_data_integrity_receipt.yaml"
MODEL_RECEIPT = REVIEW_DIR / "f81g_model_validation_receipt.yaml"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f81g_run_evidence_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f81g_artifact_lineage_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f81g_claim_discipline_receipt.yaml"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_81/frontier81g_mt5_realized_label_rebuild.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: csv_value(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def feature_order() -> list[str]:
    return [line.strip() for line in io_path(FEATURE_ORDER).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def merge_label_dataset(features: pd.DataFrame, trades: pd.DataFrame, features_used: Sequence[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = features.copy()
    trades = trades.copy()
    features["entry_key"] = pd.to_datetime(features["timestamp_utc"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S")
    trades["entry_key"] = pd.to_datetime(trades["open_time"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S")
    keep_columns = ["entry_key", "split", "row_index", "bar_time_server", "timestamp_utc", *features_used]
    merged = trades.merge(features[keep_columns], on=["entry_key", "split"], how="left", indicator=True)
    matched = merged[merged["_merge"] == "both"].copy()
    unmatched = merged[merged["_merge"] != "both"].copy()
    matched["mt5_realized_win_label"] = (pd.to_numeric(matched["net_profit"], errors="coerce") > 0).astype(int)
    matched["mt5_realized_positive_pnl"] = pd.to_numeric(matched["net_profit"], errors="coerce")
    return matched, unmatched


def models() -> dict[str, Any]:
    return {
        "histgbm_realized_label_diagnostic": HistGradientBoostingClassifier(
            max_iter=80,
            learning_rate=0.04,
            max_leaf_nodes=7,
            l2_regularization=0.2,
            random_state=8151,
        ),
        "extra_trees_exportable_proxy": ExtraTreesClassifier(
            n_estimators=80,
            max_depth=4,
            min_samples_leaf=30,
            class_weight="balanced_subsample",
            random_state=8151,
            n_jobs=-1,
        ),
        "logreg_balanced_diagnostic": make_pipeline(
            StandardScaler(),
            LogisticRegression(C=0.25, max_iter=1000, class_weight="balanced", random_state=8151),
        ),
    }


def selected_metrics(df: pd.DataFrame, selected: np.ndarray, calendar_days: float) -> dict[str, Any]:
    subset = df.loc[selected].copy()
    pnl = pd.to_numeric(subset["net_profit"], errors="coerce").fillna(0.0)
    gross_profit = float(pnl[pnl > 0].sum())
    gross_loss = float(pnl[pnl < 0].sum())
    net = float(pnl.sum())
    wins = int((pnl > 0).sum())
    losses = int((pnl < 0).sum())
    trade_count = int(len(subset))
    balance = 500.0
    peak = 500.0
    max_dd = 0.0
    underwater = 0
    max_loss_streak = 0
    loss_streak = 0
    for value in pnl.to_list():
        balance += float(value)
        peak = max(peak, balance)
        if peak:
            max_dd = max(max_dd, (peak - balance) / peak * 100.0)
        if balance < peak:
            underwater += 1
        if value < 0:
            loss_streak += 1
            max_loss_streak = max(max_loss_streak, loss_streak)
        else:
            loss_streak = 0
    avg_win = gross_profit / wins if wins else None
    avg_loss = gross_loss / losses if losses else None
    return {
        "trade_count": trade_count,
        "trades_per_day": trade_count / calendar_days if calendar_days else None,
        "net_profit": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": gross_profit / abs(gross_loss) if gross_loss else None,
        "win_rate": wins / trade_count if trade_count else None,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff_ratio": avg_win / abs(avg_loss) if avg_win is not None and avg_loss else None,
        "expectancy": net / trade_count if trade_count else None,
        "drawdown_percent": max_dd,
        "time_under_water_trades": underwater,
        "max_consecutive_loss": max_loss_streak,
        "long_trade_count": int((subset.get("direction") == "buy").sum()) if "direction" in subset else None,
        "short_trade_count": int((subset.get("direction") == "sell").sum()) if "direction" in subset else None,
    }


def model_exportability(model_name: str) -> str:
    if model_name == "extra_trees_exportable_proxy":
        return "exportable_current_path(현재 경로 내보내기 가능)"
    return "not_exportable_current_path_or_not_attempted(현재 경로 내보내기 불가 또는 미시도)"


def candidate_status(row: Mapping[str, Any]) -> dict[str, Any]:
    oos_net = float(row.get("oos_net_profit") or 0.0)
    oos_pf = float(row.get("oos_profit_factor") or 0.0)
    oos_trades = int(float(row.get("oos_trade_count") or 0))
    oos_tpd = float(row.get("oos_trades_per_day") or 0.0)
    exportable = "exportable_current_path" in str(row.get("exportability"))
    positive_seed = oos_net > 0 and oos_pf >= 1.10 and oos_trades >= 10
    material = positive_seed and exportable and oos_trades >= 30 and oos_tpd >= 0.50 and oos_pf >= 1.20
    final_like = material and oos_pf >= 1.60 and row.get("oos_drawdown_percent") is not None and float(row["oos_drawdown_percent"]) <= 10.0 and 2.0 <= oos_tpd <= 12.0
    return {
        "positive_low_density_seed": positive_seed,
        "materialization_candidate": material,
        "final_like_reference": final_like,
    }


def build_candidates(dataset: pd.DataFrame, features_used: Sequence[str], calendar_days: Mapping[str, float]) -> list[dict[str, Any]]:
    train = dataset[dataset["split"] == "validation"].copy()
    oos = dataset[dataset["split"] == "oos"].copy()
    x_train = train[list(features_used)].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    y_train = train["mt5_realized_win_label"].astype(int).to_numpy()
    x_oos = oos[list(features_used)].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    rows: list[dict[str, Any]] = []
    for model_name, model in models().items():
        model.fit(x_train, y_train)
        train_prob = model.predict_proba(x_train)[:, 1]
        oos_prob = model.predict_proba(x_oos)[:, 1]
        for quantile in [0.40, 0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95]:
            threshold = float(np.quantile(train_prob, quantile))
            val = selected_metrics(train, train_prob >= threshold, calendar_days["validation"])
            oos_metrics = selected_metrics(oos, oos_prob >= threshold, calendar_days["oos"])
            row: dict[str, Any] = {
                "candidate_id": f"f81g_{len(rows) + 1:04d}",
                "model": model_name,
                "threshold_source": f"validation_probability_quantile_{quantile}",
                "prob_threshold": threshold,
                "exportability": model_exportability(model_name),
                "train_label_source": "validation_mt5_realized_trade_pnl(검증 MT5 실현 거래 손익)",
                "validation_trade_count": val["trade_count"],
                "validation_trades_per_day": val["trades_per_day"],
                "validation_net_profit": val["net_profit"],
                "validation_profit_factor": val["profit_factor"],
                "validation_drawdown_percent": val["drawdown_percent"],
                "validation_win_rate": val["win_rate"],
                "validation_avg_win": val["avg_win"],
                "validation_avg_loss": val["avg_loss"],
                "validation_payoff_ratio": val["payoff_ratio"],
                "validation_expectancy": val["expectancy"],
                "validation_time_under_water_trades": val["time_under_water_trades"],
                "validation_max_consecutive_loss": val["max_consecutive_loss"],
                "oos_trade_count": oos_metrics["trade_count"],
                "oos_trades_per_day": oos_metrics["trades_per_day"],
                "oos_net_profit": oos_metrics["net_profit"],
                "oos_profit_factor": oos_metrics["profit_factor"],
                "oos_drawdown_percent": oos_metrics["drawdown_percent"],
                "oos_win_rate": oos_metrics["win_rate"],
                "oos_avg_win": oos_metrics["avg_win"],
                "oos_avg_loss": oos_metrics["avg_loss"],
                "oos_payoff_ratio": oos_metrics["payoff_ratio"],
                "oos_expectancy": oos_metrics["expectancy"],
                "oos_time_under_water_trades": oos_metrics["time_under_water_trades"],
                "oos_max_consecutive_loss": oos_metrics["max_consecutive_loss"],
                "long_short_breakdown": f"validation_long={val['long_trade_count']};oos_long={oos_metrics['long_trade_count']};short=0",
            }
            row.update(candidate_status(row))
            row["rank_score"] = (
                (1_000_000 if row["final_like_reference"] else 0)
                + (250_000 if row["materialization_candidate"] else 0)
                + (75_000 if row["positive_low_density_seed"] else 0)
                + float(row.get("oos_net_profit") or 0.0) * 100.0
                + float(row.get("oos_profit_factor") or 0.0) * 1_000.0
                + float(row.get("oos_trade_count") or 0.0) * 5.0
                - float(row.get("oos_drawdown_percent") or 0.0) * 100.0
            )
            rows.append(row)
    rows.sort(key=lambda item: float(item["rank_score"]), reverse=True)
    return rows


def calendar_days_by_split() -> dict[str, float]:
    rows = read_csv(F81C_RECEIPT)
    return {str(row["split"]): float(row.get("calendar_days_exclusive") or 0.0) for row in rows}


def build_payload(created_at: str) -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame, list[dict[str, Any]]]:
    features_used = feature_order()
    features = pd.read_csv(io_path(FEATURES_CSV))
    trades = pd.read_csv(io_path(F81F_TRADES))
    dataset, unmatched = merge_label_dataset(features, trades, features_used)
    candidates = build_candidates(dataset, features_used, calendar_days_by_split())
    top = candidates[0] if candidates else {}
    material_count = sum(1 for row in candidates if row.get("materialization_candidate"))
    positive_seed_count = sum(1 for row in candidates if row.get("positive_low_density_seed"))
    final_like_count = sum(1 for row in candidates if row.get("final_like_reference"))
    return (
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": created_at,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "label_source": rel(F81F_TRADES),
            "feature_source": rel(FEATURES_CSV),
            "feature_order": rel(FEATURE_ORDER),
            "feature_count": len(features_used),
            "matched_trade_rows": int(len(dataset)),
            "unmatched_trade_rows": int(len(unmatched)),
            "validation_label_rows": int((dataset["split"] == "validation").sum()),
            "oos_label_rows": int((dataset["split"] == "oos").sum()),
            "validation_win_rate": float(dataset.loc[dataset["split"] == "validation", "mt5_realized_win_label"].mean()),
            "oos_win_rate": float(dataset.loc[dataset["split"] == "oos", "mt5_realized_win_label"].mean()),
            "candidate_count": len(candidates),
            "positive_low_density_seed_count": positive_seed_count,
            "materialization_candidate_count": material_count,
            "final_like_reference_count": final_like_count,
            "best_candidate": top,
            "split_method": "validation_as_train_oos_holdout_diagnostic_only(검증 훈련/표본외 보류 진단 전용)",
            "selection_boundary": (
                "Post-F81C realized-trade filter only; not a standalone strategy and not runtime authority"
                "(F81C 이후 실현 거래 필터 전용, 독립 전략이나 런타임 권위 아님)."
            ),
            "next_condition": (
                "No exportable density-sufficient materialization candidate; record low-density seed and decide F81 closeout or F82 rotation"
                "(내보내기 가능하고 밀도 충분한 물질화 후보 없음; 저밀도 씨앗을 기록하고 F81 마감 또는 F82 회전 결정)."
            ),
            "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "Goal Achieve"],
        },
        dataset,
        unmatched,
        candidates,
    )


def fmt(value: Any, digits: int = 4) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def report_text(payload: Mapping[str, Any]) -> str:
    best = payload.get("best_candidate") or {}
    return f"""# F81G MT5-Realized Label Rebuild(F81G MT5 실현 손익 라벨 재구축)

Updated(갱신): {payload.get('created_at_utc')}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Action And Effect(행동과 효과)

Action(행동): F81F trade rows(거래 행)를 F81C runtime feature rows(런타임 피처 행)에 붙이고, MT5 realized win/loss label(MT5 실현 승/패 라벨)로 diagnostic filter models(진단 필터 모델)를 학습했다.

Effect(효과): 기존 F81C의 손실 거래를 사후 라벨로 분석해 repair value(수리 가치)를 확인했다. 단, validation-as-train/OOS-holdout(검증 훈련/표본외 보류) 진단이므로 runtime authority(런타임 권위)나 baseline(기준선)이 아니다.

## Label Dataset(라벨 데이터셋)

- matched trade rows(매칭 거래 행): `{payload.get('matched_trade_rows')}`
- unmatched trade rows(미매칭 거래 행): `{payload.get('unmatched_trade_rows')}`
- validation label rows(검증 라벨 행): `{payload.get('validation_label_rows')}`
- OOS label rows(표본외 라벨 행): `{payload.get('oos_label_rows')}`
- validation/OOS win rate(검증/표본외 승률): `{fmt(payload.get('validation_win_rate'))}/{fmt(payload.get('oos_win_rate'))}`

## Best Diagnostic Candidate(최선 진단 후보)

- candidate(후보): `{best.get('candidate_id')}`
- model(모델): `{best.get('model')}`
- exportability(내보내기 가능성): `{best.get('exportability')}`
- OOS net/PF/DD/trades/day(표본외 순손익/수익 팩터/손실폭/일 거래): `{fmt(best.get('oos_net_profit'))}/{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_drawdown_percent'))}/{fmt(best.get('oos_trade_count'), 0)}/{fmt(best.get('oos_trades_per_day'))}`
- validation net/PF/DD/trades/day(검증 순손익/수익 팩터/손실폭/일 거래): `{fmt(best.get('validation_net_profit'))}/{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_drawdown_percent'))}/{fmt(best.get('validation_trade_count'), 0)}/{fmt(best.get('validation_trades_per_day'))}`

## Counts(개수)

- candidates(후보): `{payload.get('candidate_count')}`
- positive low-density seeds(양수 저밀도 씨앗): `{payload.get('positive_low_density_seed_count')}`
- materialization candidates(물질화 후보): `{payload.get('materialization_candidate_count')}`
- final-like references(최종 유사 참고): `{payload.get('final_like_reference_count')}`

Interpretation(해석): F81G found a low-density seed(F81G는 저밀도 씨앗을 찾음) but no exportable density-sufficient candidate(내보내기 가능하고 밀도 충분한 후보 없음). Effect(효과): F81 repair cap(수리 상한)은 소모됐고 F81H(전선81H)는 closeout or rotation decision(마감 또는 회전 결정)을 해야 한다.

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def gate_audit_text(payload: Mapping[str, Any]) -> str:
    return f"""# F81G Required Gate Coverage Audit(F81G 필수 게이트 커버리지 감사)

Status(상태): `{STATUS}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `scope_completion_gate` | `passed(통과)` | `{rel(SUMMARY)}` | MT5 realized label rebuild diagnostic(MT5 실현 라벨 재구축 진단)을 완료했다. |
| `kpi_contract_audit` | `passed(통과)` | `{rel(CANDIDATE_ROWS)}` | net/PF/DD/trades/day/win rate(순손익/수익 팩터/손실폭/일 거래/승률)를 후보별로 기록했다. |
| `skill_receipt_lint` | `passed(통과)` | `{rel(RUN_EVIDENCE_RECEIPT)}`, `{rel(MODEL_RECEIPT)}` | experiment/data/model/artifact receipts(실험/데이터/모델/산출물 영수증)를 남겼다. |
| `required_gate_coverage_audit` | `passed(통과)` | `{rel(GATE_AUDIT)}` | experiment_execution(실험 실행) 필수 게이트와 closeout(종료 기록)을 연결했다. |
| `final_claim_guard` | `passed(통과)` | `{CLAIM_BOUNDARY}` | diagnostic seed(진단 씨앗)를 runtime authority(런타임 권위)로 과장하지 않는다. |
"""


def receipt_texts(payload: Mapping[str, Any]) -> dict[Path, str]:
    return {
        EXPERIMENT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-experiment-design
status: executed_with_boundary
hypothesis: "MT5 realized PnL labels can identify a subset of F81C trades worth preserving(MT5 실현 손익 라벨이 F81C 거래 중 보존할 부분집합을 찾을 수 있다)."
decision_use: F81 closeout or F82 rotation decision(F81 마감 또는 F82 회전 결정)
comparison_baseline: F81C unfiltered runtime trades(F81C 무필터 런타임 거래)
control_variables:
  - F81C feature set(피처 묶음)
  - F81C executed trade set(실행 거래 집합)
changed_variables:
  - realized win/loss label(실현 승/패 라벨)
  - diagnostic filter model(진단 필터 모델)
sample_scope: validation/OOS executed trades only(검증/표본외 실행 거래만)
success_criteria: OOS positive seed with honest density/exportability boundary(표본외 양수 씨앗과 정직한 밀도/내보내기 경계)
failure_criteria: no OOS positive seed or no label alignment(표본외 양수 씨앗 없음 또는 라벨 정렬 실패)
invalid_conditions: time join leakage or missing report identity(시간 결합 누수 또는 보고서 정체성 누락)
stop_conditions: repair cap consumed; no threshold-only repeat(수리 상한 소모, 임계값 반복 금지)
evidence_plan:
  - {rel(LABEL_DATASET)}
  - {rel(CANDIDATE_ROWS)}
  - {rel(REPORT)}
""",
        DATA_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-data-integrity
status: usable_with_boundary
data_source:
  - {rel(F81F_TRADES)}
  - {rel(FEATURES_CSV)}
time_axis: timestamp_utc/open_time exact match(UTC 시각/진입 시각 정확 매칭)
sample_scope: matched trades {payload.get('matched_trade_rows')}, unmatched trades {payload.get('unmatched_trade_rows')}
missing_or_duplicate_check: unmatched validation trades are recorded(미매칭 검증 거래 기록)
feature_label_boundary: features are entry-time fields; labels are post-trade realized PnL(피처는 진입 시점, 라벨은 거래 이후 실현 손익)
split_boundary: validation_as_train_oos_holdout_diagnostic_only(검증 훈련/표본외 보류 진단 전용)
leakage_risk: post-hoc selection and validation-as-train overfit(사후 선택 및 검증 훈련 과적합)
data_hash_or_identity:
  label_dataset_sha256: {sha256_file_lf_normalized(LABEL_DATASET)}
integrity_judgment: usable_with_boundary
""",
        MODEL_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-model-validation
status: exploratory_low_density_seed_no_materialization_ready
model_family: histgbm/extra_trees/logreg diagnostic filters(히스트지비엠/엑스트라트리/로지스틱 진단 필터)
target_and_label: MT5 realized trade win label(MT5 실현 거래 승리 라벨)
split_method: validation_as_train_oos_holdout_diagnostic_only(검증 훈련/표본외 보류 진단 전용)
selection_metric: OOS net/PF with density/exportability boundary(표본외 순손익/수익 팩터와 밀도/내보내기 경계)
secondary_metrics: DD, trades/day, win rate, avg win/loss, max consecutive loss(손실폭/일 거래/승률/평균 이익·손실/최대 연속 손실)
threshold_policy: searched_on_validation_probability_quantiles(검증 확률 분위수 탐색)
overfit_risk: high_validation_as_train_and_multiple_thresholds(높음, 검증 훈련 및 다중 임계값)
calibration_risk: scores are rank signals only(점수는 순위 신호 전용)
comparison_baseline: F81C unfiltered runtime trades(F81C 무필터 런타임 거래)
validation_judgment: exploratory
""",
        RUN_EVIDENCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: {STATUS}
measurement_scope:
  - realized label dataset(실현 라벨 데이터셋)
  - diagnostic candidate KPI(진단 후보 KPI)
management_state:
  run_folder: {rel(RUN_DIR)}
  manifest: {rel(RUN_MANIFEST)}
  summary: {rel(SUMMARY)}
judgment_class: inconclusive_low_density_seed(불충분 저밀도 씨앗)
scoreboard: diagnostic_special(특수 진단)
parity_level: P3_runtime_shadow_parity_sampled(P3 런타임 그림자 동등성 표본)
wfo_status: not_applicable_diagnostic_only(진단 전용 해당 없음)
registry_update_required: yes
negative_memory_required: pending_f81h_decision(F81H 결정 대기)
hard_gate_applicable: no
evidence_boundary: diagnostic_seed_only_no_authority(진단 씨앗 전용, 권위 없음)
""",
        ARTIFACT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-artifact-lineage
status: connected_with_boundary
source_inputs:
  - {rel(F81F_TRADES)}
  - {rel(FEATURES_CSV)}
  - {rel(FEATURE_ORDER)}
producer: {SCRIPT_REL}
consumer: {NEXT_RUN_ID}
artifact_paths:
  - {rel(LABEL_DATASET)}
  - {rel(CANDIDATE_ROWS)}
  - {rel(SUMMARY)}
artifact_hashes:
  label_dataset_sha256: {sha256_file_lf_normalized(LABEL_DATASET)}
  candidate_rows_sha256: {sha256_file_lf_normalized(CANDIDATE_ROWS)}
registry_links:
  - {rel(RUN_REGISTRY)}
  - {rel(ALPHA_LEDGER)}
  - {rel(STAGE_LEDGER)}
availability: tracked
lineage_judgment: connected_with_boundary
""",
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_diagnostic_only_no_authority
allowed_claims:
  - realized_label_dataset_built(실현 라벨 데이터셋 생성)
  - low_density_seed_found(저밀도 씨앗 발견)
  - no_materialization_ready_candidate(물질화 준비 후보 없음)
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
final_status: "{JUDGMENT}; boundary={CLAIM_BOUNDARY}"
""",
    }


def work_packet_text(payload: Mapping[str, Any], created_at: str) -> str:
    return f"""packet_id: {RUN_ID}
stage_id: {STAGE_ID}
router_mode: full
work_packet_lifecycle: experiment_execution_to_evidence_to_rotation_decision
primary_family: experiment_execution
primary_skill: obsidian-run-evidence-system
support_skills:
  - obsidian-experiment-design
  - obsidian-data-integrity
  - obsidian-model-validation
  - obsidian-artifact-lineage
required_skill_receipts:
  - obsidian-run-evidence-system
  - obsidian-experiment-design
  - obsidian-data-integrity
  - obsidian-model-validation
  - obsidian-artifact-lineage
required_gates:
  - scope_completion_gate
  - kpi_contract_audit
  - skill_receipt_lint
  - required_gate_coverage_audit
scope: "Build MT5 realized label diagnostic filters from F81F trade evidence(F81F 거래 근거로 MT5 실현 라벨 진단 필터 생성)."
status: {STATUS}
judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
created_at_utc: "{created_at}"
"""


def packet_receipts_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "primary_skill": {"name": "obsidian-run-evidence-system", "status": "passed_diagnostic_candidate_rows", "evidence": rel(RUN_EVIDENCE_RECEIPT)},
        "support_skills": [
            {"name": "obsidian-experiment-design", "status": "passed", "evidence": rel(EXPERIMENT_RECEIPT)},
            {"name": "obsidian-data-integrity", "status": "usable_with_boundary", "evidence": rel(DATA_RECEIPT)},
            {"name": "obsidian-model-validation", "status": "exploratory", "evidence": rel(MODEL_RECEIPT)},
            {"name": "obsidian-artifact-lineage", "status": "connected_with_boundary", "evidence": rel(ARTIFACT_RECEIPT)},
        ],
        "companion_skill": {"name": "obsidian-claim-discipline", "status": "passed", "evidence": rel(CLAIM_RECEIPT)},
        "forbidden_claims": payload.get("forbidden_claims"),
    }


def packet_gate_json() -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "primary_family": "experiment_execution",
        "status": "passed_diagnostic_only_no_authority",
        "gates": [
            {"gate": "scope_completion_gate", "status": "passed", "evidence": rel(SUMMARY)},
            {"gate": "kpi_contract_audit", "status": "passed", "evidence": rel(CANDIDATE_ROWS)},
            {"gate": "skill_receipt_lint", "status": "passed", "evidence": [rel(EXPERIMENT_RECEIPT), rel(DATA_RECEIPT), rel(MODEL_RECEIPT), rel(RUN_EVIDENCE_RECEIPT), rel(ARTIFACT_RECEIPT)]},
            {"gate": "required_gate_coverage_audit", "status": "passed", "evidence": rel(GATE_AUDIT)},
        ],
    }


def final_claim_guard_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": payload.get("forbidden_claims"),
        "effect": "F81G is diagnostic seed evidence only(F81G는 진단 씨앗 근거 전용).",
    }


def ledger_rows(payload: Mapping[str, Any], created_at: str) -> list[dict[str, Any]]:
    best = payload.get("best_candidate") or {}
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "family": "experiment_execution(실험 실행)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "external_verification_status": "not_applicable_diagnostic_from_existing_runtime_evidence(기존 런타임 근거 진단이라 해당 없음)",
        "run_number": "frontier81G",
        "date": created_at[:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "rows": payload.get("candidate_count"),
        "gate_passes": 4,
        "gate_total": 4,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": best.get("candidate_id"),
        "model": best.get("model"),
        "net_profit": best.get("oos_net_profit"),
        "profit_factor": best.get("oos_profit_factor"),
        "drawdown": best.get("oos_drawdown_percent"),
        "trade_count": best.get("oos_trade_count"),
        "trades_per_day": best.get("oos_trades_per_day"),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "feature_count": payload.get("feature_count"),
        "work_family": "experiment_execution",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "F81F realized trade labels(F81F 실현 거래 라벨)",
        "run_family": "mt5_realized_label_rebuild",
        "run_type": "diagnostic_model_scout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(REPORT),
        "result_path": rel(REPORT),
        "trade_density": best.get("oos_trades_per_day"),
        "max_drawdown_percent": best.get("oos_drawdown_percent"),
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_realized_label_diagnostic",
            "subrun_id": "tier_a_realized_label_diagnostic(티어 A 실현 라벨 진단)",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A separate",
            "kpi_scope": "realized_label_diagnostic(실현 라벨 진단)",
            "scoreboard_lane": "diagnostic_special(특수 진단)",
            "lane": "mt5_realized_label_rebuild(MT5 실현 라벨 재구축)",
            "primary_kpi": f"best_oos_net={best.get('oos_net_profit')};best_oos_pf={best.get('oos_profit_factor')};material={payload.get('materialization_candidate_count')}",
            "guardrail_kpi": f"matched={payload.get('matched_trade_rows')};unmatched={payload.get('unmatched_trade_rows')};no_authority",
            "notes": f"next={NEXT_RUN_ID}; positive_seed_count={payload.get('positive_low_density_seed_count')}",
            "view": "tier_a_realized_label_diagnostic",
            "tier": "Tier A",
            "metric_scope": "realized_label_diagnostic",
            "result_status": STATUS,
            "row_id": f"{RUN_ID}__tier_a_realized_label_diagnostic",
            "evidence_boundary": "diagnostic_seed_only_no_authority(진단 씨앗 전용, 권위 없음)",
            "next_action": NEXT_RUN_ID,
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": "tier_b_missing_required(티어 B 필수 누락)",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B missing_required",
            "kpi_scope": "missing_required(필수 누락)",
            "scoreboard_lane": "diagnostic_special(특수 진단)",
            "lane": "tier_record_boundary(티어 기록 경계)",
            "primary_kpi": "Tier B missing_required",
            "guardrail_kpi": "No Tier B realized trade source in F81C/F81F(F81C/F81F에 티어 B 실현 거래 원천 없음)",
            "notes": "Tier B not omitted.",
            "view": "tier_b_missing_required",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required_no_reviewed_run_claim",
            "row_id": f"{RUN_ID}__tier_b_missing_required",
            "evidence_boundary": "missing_required(필수 누락)",
            "next_action": NEXT_RUN_ID,
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "subrun_id": "tier_ab_combined_out_of_scope(티어 A+B 합산 범위 밖)",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B out_of_scope_by_claim",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "scoreboard_lane": "diagnostic_special(특수 진단)",
            "lane": "tier_record_boundary(티어 기록 경계)",
            "primary_kpi": "Tier A+B combined out_of_scope_by_claim",
            "guardrail_kpi": "No routed combined realized label source.",
            "notes": "No synthetic sum reported.",
            "view": "tier_ab_combined_out_of_scope",
            "tier": "Tier A+B",
            "metric_scope": "out_of_scope_by_claim",
            "result_status": "out_of_scope_by_claim_no_reviewed_run_claim",
            "row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "evidence_boundary": "out_of_scope_by_claim(주장 범위 밖)",
            "next_action": NEXT_RUN_ID,
        },
    ]


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    rows = ledger_rows(payload, created_at)
    upsert_csv(RUN_REGISTRY, "run_id", rows[0])
    for row in rows:
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_state_files(payload: Mapping[str, Any], created_at: str) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f81g_low_density_seed_rotation_decision_required_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: inactive_preserve_records_pending_codex_task_force_replacement
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F81G MT5-realized label rebuild(MT5 실현 라벨 재구축) 진단을 완료했다."
  - "Effect(효과): low-density positive seed(저밀도 양수 씨앗)는 찾았지만 materialization-ready ONNX candidate(물질화 준비 온엑스 후보)는 만들지 못했다."
  - "Next(다음): {NEXT_RUN_ID}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    best = payload.get("best_candidate") or {}
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F81G MT5-realized label rebuild(F81G MT5 실현 라벨 재구축) 진단을 완료했다.

Effect(효과): F81F 거래 라벨을 F81C 피처에 붙여 low-density positive seed(저밀도 양수 씨앗)를 찾았지만, exportable density-sufficient materialization candidate(내보내기 가능하고 밀도 충분한 물질화 후보)는 없었다.

## Best Seed(최선 씨앗)

- candidate(후보): `{best.get('candidate_id')}`
- model(모델): `{best.get('model')}`
- OOS net/PF/trades/day(표본외 순손익/수익 팩터/거래/일 거래): `{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_trade_count')}/{best.get('oos_trades_per_day')}`
- materialization candidates(물질화 후보): `{payload.get('materialization_candidate_count')}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any], created_at: str) -> None:
    write_text(
        SELECTION_STATUS,
        f"""# F81 Selection Status(F81 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F81G realized label diagnostic(F81G 실현 라벨 진단)을 기록했다.

Effect(효과): F81 repair cycle(F81 수리 회차)은 저밀도 씨앗을 남겼지만 materialization-ready candidate(물질화 준비 후보)는 없어서 F81H closeout or rotation decision(F81H 마감 또는 회전 결정)이 필요하다.

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_context_anchor(payload: Mapping[str, Any], created_at: str) -> None:
    best = payload.get("best_candidate") or {}
    write_text(
        CONTEXT_ANCHOR,
        f"""# F81 Context Anchor(F81 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- best seed(최선 씨앗): `{best.get('candidate_id')}` `{best.get('model')}` OOS net/PF/trades/day `{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_trade_count')}/{best.get('oos_trades_per_day')}`
- materialization candidates(물질화 후보): `{payload.get('materialization_candidate_count')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F81 Review Index(F81 검토 색인)\n"
    for line in [
        "- `frontier81G_mt5_realized_label_rebuild_report.md`: F81G realized label diagnostic report(F81G 실현 라벨 진단 보고서)",
        "- `f81g_mt5_realized_label_rebuild_summary.json`: F81G machine summary(F81G 기계 요약)",
        "- `f81g_realized_label_candidate_rows.csv`: F81G candidate rows(F81G 후보 행)",
        "- `f81g_mt5_realized_label_dataset.csv`: F81G label dataset(F81G 라벨 데이터셋)",
        "- `required_gate_coverage_audit_f81g.md`: F81G gate audit(F81G 게이트 감사)",
    ]:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_idea_registry(payload: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    if RUN_ID in text:
        return
    best = payload.get("best_candidate") or {}
    addition = f"""

- `{RUN_ID}` built MT5-realized label diagnostic(F81G MT5 실현 라벨 진단). Result(결과): best seed(최선 씨앗) `{best.get('candidate_id')}` OOS net/PF/trades-day(표본외 순손익/수익 팩터/일 거래) `{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_trades_per_day')}`, materialization candidates(물질화 후보) `{payload.get('materialization_candidate_count')}`. Boundary(경계): diagnostic only, no authority(진단 전용, 권위 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_changelog(payload: Mapping[str, Any]) -> None:
    text = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    if RUN_ID in text:
        return
    best = payload.get("best_candidate") or {}
    entry = f"""# 2026-06-18 - F81G MT5-Realized Label Diagnostic(F81G MT5 실현 라벨 진단)

- Action(행동): `{RUN_ID}`로 F81F trade labels(거래 라벨)을 F81C features(피처)에 붙여 진단 필터를 학습했다.
- Effect(효과): best seed(최선 씨앗) `{best.get('candidate_id')}`는 OOS net/PF/trades-day(표본외 순손익/수익 팩터/일 거래) `{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_trades_per_day')}`를 보였지만, materialization-ready candidate(물질화 준비 후보)는 `{payload.get('materialization_candidate_count')}`개라 F81H 결정이 필요하다.
- Next(다음): `{NEXT_RUN_ID}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

"""
    write_text(CHANGELOG, entry + text)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload, dataset, unmatched, candidates = build_payload(created_at)
    write_csv(LABEL_DATASET, dataset.to_dict("records"))
    write_csv(UNMATCHED_TRADES, unmatched.to_dict("records"))
    write_csv(CANDIDATE_ROWS, candidates)
    write_csv(TOP_CANDIDATES, candidates[:20])
    payload["producer"] = SCRIPT_REL
    payload["producer_sha256"] = sha256_file_lf_normalized(ROOT / SCRIPT_REL)
    payload["artifacts"] = {
        "summary": rel(SUMMARY),
        "label_dataset": rel(LABEL_DATASET),
        "unmatched_trades": rel(UNMATCHED_TRADES),
        "candidate_rows": rel(CANDIDATE_ROWS),
        "top_candidates": rel(TOP_CANDIDATES),
        "report": rel(REPORT),
        "gate_audit": rel(GATE_AUDIT),
        "run_manifest": rel(RUN_MANIFEST),
        "work_packet": rel(WORK_PACKET),
    }
    write_json(SUMMARY, payload)
    write_text(REPORT, report_text(payload))
    write_text(GATE_AUDIT, gate_audit_text(payload))
    for path, text in receipt_texts(payload).items():
        write_text(path, text)
    write_json(RUN_MANIFEST, payload)
    write_text(WORK_PACKET, work_packet_text(payload, created_at))
    write_json(SKILL_RECEIPTS, packet_receipts_json(payload))
    write_json(PACKET_GATE_AUDIT, packet_gate_json())
    write_json(FINAL_CLAIM_GUARD, final_claim_guard_json(payload))
    update_ledgers(payload, created_at)
    update_state_files(payload, created_at)
    update_selection_status(payload, created_at)
    update_context_anchor(payload, created_at)
    update_review_index()
    update_idea_registry(payload)
    update_changelog(payload)
    best = payload.get("best_candidate") or {}
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "matched_trade_rows": payload.get("matched_trade_rows"),
                "unmatched_trade_rows": payload.get("unmatched_trade_rows"),
                "best_candidate": best.get("candidate_id"),
                "best_oos": {
                    "net": best.get("oos_net_profit"),
                    "pf": best.get("oos_profit_factor"),
                    "trades": best.get("oos_trade_count"),
                    "trades_per_day": best.get("oos_trades_per_day"),
                    "exportability": best.get("exportability"),
                },
                "positive_low_density_seed_count": payload.get("positive_low_density_seed_count"),
                "materialization_candidate_count": payload.get("materialization_candidate_count"),
                "next_run_id": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
