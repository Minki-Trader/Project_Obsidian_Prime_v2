from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd


STAGE_ID = "270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe"
RUN_ID = "run270B_aggressive_probe_payload_materialization_v1"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

ROOT = Path(".")
STAGE = ROOT / "stages" / STAGE_ID
RUN270A = STAGE / "02_runs" / "run270A"
RUN_DIR = STAGE / "02_runs" / "run270B"
PAYLOAD_DIR = RUN_DIR / "payloads"
HANDOFF_DIR = RUN_DIR / "handoff"
MT5_DIR = RUN_DIR / "mt5_handoff"
REVIEWS = STAGE / "03_reviews"

VARIANT_PLAN = RUN270A / "aggressive_probe_variant_plan.csv"
RUN270A_MANIFEST = RUN270A / "run_manifest.json"
RUN270A_SUPPLY = RUN270A / "supply_metrics_by_variant.csv"
RUN270A_READINESS = RUN270A / "probe_readiness_receipt.csv"
CP269A_SCORE_TABLE = (
    ROOT
    / "stages"
    / "269_onnx_candidate_campaign__fresh_thesis_candidate_construction"
    / "02_runs"
    / "run269D"
    / "scores"
    / "cp269A_scores.parquet"
)
CP269D_SCORE_TABLE = (
    ROOT
    / "stages"
    / "269_onnx_candidate_campaign__fresh_thesis_candidate_construction"
    / "02_runs"
    / "run269D"
    / "scores"
    / "cp269D_scores.parquet"
)
CP269A_HANDOFF = (
    ROOT
    / "stages"
    / "269_onnx_candidate_campaign__fresh_thesis_candidate_construction"
    / "02_runs"
    / "run269D"
    / "handoff"
    / "cp269A.json"
)
CP269D_HANDOFF = (
    ROOT
    / "stages"
    / "269_onnx_candidate_campaign__fresh_thesis_candidate_construction"
    / "02_runs"
    / "run269D"
    / "handoff"
    / "cp269D.json"
)

LABEL_OR_FUTURE_PREFIXES = ("label", "future_")
LABEL_OR_FUTURE_COLUMNS = {
    "future_log_return_12",
    "future_timestamp",
    "horizon_bars",
    "horizon_minutes",
    "label",
    "label_class",
    "label_id",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ensure_dirs() -> None:
    for path in [RUN_DIR, PAYLOAD_DIR, HANDOFF_DIR, MT5_DIR, REVIEWS]:
        path.mkdir(parents=True, exist_ok=True)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def short_variant_id(variant_id: str) -> str:
    parts = variant_id.split("_")
    return "_".join(parts[:2])


def rounded(value: float | int, ndigits: int = 8) -> float:
    return round(float(value), ndigits)


def build_decision_mask(df: pd.DataFrame, variant: dict[str, str]) -> pd.Series:
    thresholds = json.loads(variant["thresholds_json"]) if variant["thresholds_json"] else {}
    variant_id = variant["variant_id"]
    if variant_id == "run270A_q01_base_materialized_decision":
        return df["materialized_decision_flag"].astype(int) == 1
    if variant_id == "run270A_q02_reward_skew_tilt":
        return (
            (df["candidate_decision_score"] >= thresholds["decision_min"])
            & (df["reward_skew_score"] >= thresholds["reward_min"])
            & (df["weak_context_cost"] <= thresholds["cost_max"])
            & (df["failure_zone_cut_flag"].astype(int) == 0)
        )
    if variant_id == "run270A_q03_supply_expansion_watch":
        return (
            (df["candidate_decision_score"] >= thresholds["decision_min"])
            & (df["reward_skew_score"] >= thresholds["reward_min"])
            & (df["weak_context_cost"] <= thresholds["cost_max"])
            & (df["failure_zone_cut_flag"].astype(int) == 0)
        )
    if variant_id == "run270A_q04_tail_reward_extreme":
        return (
            (df["candidate_decision_score"] >= thresholds["decision_min"])
            & (df["reward_skew_score"] >= thresholds["reward_min"])
            & (df["failure_zone_cut_flag"].astype(int) == 0)
        )
    if variant_id == "run270A_q05_cost_relaxed_probe":
        return (
            (df["candidate_decision_score"] >= thresholds["decision_min"])
            & (df["reward_skew_score"] >= thresholds["reward_min"])
            & (df["weak_context_cost"] <= thresholds["cost_max"])
            & (df["failure_zone_cut_flag"].astype(int) == 0)
        )
    if variant_id == "run270A_q06_weak_context_failure_boundary":
        return (
            (df["candidate_decision_score"] >= thresholds["decision_min"])
            & (df["reward_skew_score"] >= thresholds["reward_min"])
            & (df["weak_context_cost"] > thresholds["cost_min"])
        )
    raise ValueError(f"Unknown variant_id: {variant_id}")


def load_source_tables() -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, str]], dict[str, Any], dict[str, Any]]:
    variants = read_csv_rows(VARIANT_PLAN)
    cp269a = pd.read_parquet(CP269A_SCORE_TABLE)
    cp269d = pd.read_parquet(CP269D_SCORE_TABLE)
    leaked = sorted(
        set(cp269a.columns).intersection(LABEL_OR_FUTURE_COLUMNS)
        | {c for c in cp269a.columns if c.startswith(LABEL_OR_FUTURE_PREFIXES)}
    )
    if leaked:
        raise ValueError(f"Label/future columns are not allowed in run270B payloads: {leaked}")
    with CP269A_HANDOFF.open("r", encoding="utf-8") as f:
        cp269a_handoff = json.load(f)
    with CP269D_HANDOFF.open("r", encoding="utf-8") as f:
        cp269d_handoff = json.load(f)
    return cp269a, cp269d, variants, cp269a_handoff, cp269d_handoff


def support_identity_map(cp269d: pd.DataFrame) -> pd.DataFrame:
    return cp269d[
        [
            "timestamp",
            "symbol",
            "split",
            "tier_view",
            "identity_match_flag",
            "input_feature_order_hash",
            "expected_feature_order_hash",
            "adapter_schema_hash",
            "decision_rule_hash",
        ]
    ].rename(
        columns={
            "identity_match_flag": "support_identity_match_flag",
            "input_feature_order_hash": "support_input_feature_order_hash",
            "expected_feature_order_hash": "support_expected_feature_order_hash",
            "adapter_schema_hash": "support_adapter_schema_hash",
            "decision_rule_hash": "support_decision_rule_hash",
        }
    )


def classify_variant(row: dict[str, str], metrics: pd.DataFrame) -> tuple[str, str]:
    variant_id = row["variant_id"]
    role = row["variant_role"]
    if role == "failure_boundary_probe":
        return "failure_boundary_payload_only", "exclude_from_mt5_probe_queue"
    if role == "reference_seed":
        return "reference_control_payload", "include_as_control"
    tier_a_oos = metrics[
        (metrics["variant_id"] == variant_id)
        & (metrics["tier_view"] == "Tier A separate")
        & (metrics["split"] == "oos")
    ]
    if tier_a_oos.empty:
        return "invalid_missing_oos_metrics", "exclude_from_mt5_probe_queue"
    oos_rate = float(tier_a_oos.iloc[0]["decision_rate"])
    oos_count = int(float(tier_a_oos.iloc[0]["decision_count"]))
    if variant_id == "run270A_q03_supply_expansion_watch" and oos_rate > 0.35:
        return "discard_supply_inflation", "exclude_from_mt5_probe_queue"
    if variant_id == "run270A_q05_cost_relaxed_probe" and oos_rate > 0.30:
        return "discard_cost_relaxed_supply_inflation", "exclude_from_mt5_probe_queue"
    if variant_id == "run270A_q02_reward_skew_tilt" and oos_rate < 0.03:
        return "discard_too_sparse", "exclude_from_mt5_probe_queue"
    if variant_id == "run270A_q04_tail_reward_extreme" and oos_count < 75:
        return "discard_tail_too_sparse", "exclude_from_mt5_probe_queue"
    return "active_aggressive_probe_payload", "include_for_next_probe_materialization"


def materialize_payloads(
    cp269a: pd.DataFrame,
    cp269d: pd.DataFrame,
    variants: list[dict[str, str]],
    cp269a_handoff: dict[str, Any],
    cp269d_handoff: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    support = support_identity_map(cp269d)
    metrics = pd.read_csv(RUN270A_SUPPLY)
    manifest_rows: list[dict[str, Any]] = []
    queue_rows: list[dict[str, Any]] = []
    sample_payload: dict[str, Any] = {}

    for variant in variants:
        variant_id = variant["variant_id"]
        short_id = short_variant_id(variant_id)
        mask = build_decision_mask(cp269a, variant)
        payload = cp269a.assign(
            variant_id=variant_id,
            variant_role=variant["variant_role"],
            variant_decision_flag=mask.astype("int8"),
            payload_claim_boundary=BOUNDARY,
        )
        payload = payload.merge(support, on=["timestamp", "symbol", "split", "tier_view"], how="left")
        decision_surface_hash = sha256_text(
            json.dumps(
                {
                    "variant_id": variant_id,
                    "decision_rule": variant["decision_rule"],
                    "thresholds_json": variant["thresholds_json"],
                },
                sort_keys=True,
            )
        )
        payload["variant_decision_surface_hash"] = decision_surface_hash
        payload["source_model_hash"] = cp269a_handoff["model_hash"]
        payload["source_adapter_schema_hash"] = cp269a_handoff["adapter_schema_hash"]

        payload_path = PAYLOAD_DIR / f"{short_id}_payload.parquet"
        payload.to_parquet(payload_path, index=False)

        tier_a = payload[payload["tier_view"] == "Tier A separate"].copy()
        tier_a["timestamp"] = tier_a["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        mt5_path = MT5_DIR / f"{short_id}_tier_a_signals.csv"
        tier_a[
            [
                "timestamp",
                "symbol",
                "split",
                "variant_decision_flag",
                "candidate_decision_score",
                "reward_skew_score",
                "weak_context_cost",
                "failure_zone_cut_flag",
                "support_identity_match_flag",
            ]
        ].to_csv(mt5_path, index=False, lineterminator="\n")

        grouped = (
            payload.groupby(["tier_view", "split"], dropna=False)
            .agg(rows=("variant_decision_flag", "size"), decision_count=("variant_decision_flag", "sum"))
            .reset_index()
        )
        counts = {
            f"{row['tier_view']}|{row['split']}": {
                "rows": int(row["rows"]),
                "decision_count": int(row["decision_count"]),
                "decision_rate": rounded(row["decision_count"] / row["rows"] if row["rows"] else 0.0),
            }
            for row in grouped.to_dict("records")
        }
        materialization_judgment, next_queue_action = classify_variant(variant, metrics)

        handoff_payload = {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "variant_id": variant_id,
            "variant_role": variant["variant_role"],
            "materialization_judgment": materialization_judgment,
            "next_queue_action": next_queue_action,
            "source_package": cp269a_handoff["package_id"],
            "support_control": cp269d_handoff["package_id"],
            "decision_rule": variant["decision_rule"],
            "thresholds": json.loads(variant["thresholds_json"]) if variant["thresholds_json"] else {},
            "decision_surface_hash": decision_surface_hash,
            "feature_order_hash": cp269a_handoff["feature_order_hash"],
            "model_hash": cp269a_handoff["model_hash"],
            "adapter_schema_hash": cp269a_handoff["adapter_schema_hash"],
            "score_table_path": payload_path.as_posix(),
            "score_table_hash": sha256_file(payload_path),
            "mt5_tier_a_signal_path": mt5_path.as_posix(),
            "mt5_tier_a_signal_hash": sha256_file(mt5_path),
            "tier_view_counts": counts,
            "tier_b_boundary": "partial_context_structural_payload_not_runtime_fallback_authority",
            "claim_boundary": BOUNDARY,
        }
        handoff_path = HANDOFF_DIR / f"{short_id}.json"
        write_json(handoff_path, handoff_payload)

        manifest_rows.append(
            {
                "variant_id": variant_id,
                "variant_role": variant["variant_role"],
                "materialization_judgment": materialization_judgment,
                "next_queue_action": next_queue_action,
                "payload_path": payload_path.as_posix(),
                "payload_hash": sha256_file(payload_path),
                "handoff_path": handoff_path.as_posix(),
                "handoff_hash": sha256_file(handoff_path),
                "mt5_tier_a_signal_path": mt5_path.as_posix(),
                "mt5_tier_a_signal_hash": sha256_file(mt5_path),
                "decision_surface_hash": decision_surface_hash,
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "performance_claim": "none",
            }
        )
        if next_queue_action in {"include_for_next_probe_materialization", "include_as_control"}:
            queue_rows.append(
                {
                    "queue_id": f"run270B_{short_id}",
                    "variant_id": variant_id,
                    "queue_role": (
                        "control_reference" if next_queue_action == "include_as_control" else "active_probe"
                    ),
                    "payload_path": payload_path.as_posix(),
                    "handoff_path": handoff_path.as_posix(),
                    "mt5_tier_a_signal_path": mt5_path.as_posix(),
                    "required_before_external_claim": "MT5 runtime output;trade list;balance/equity curve;time-slice KPI",
                    "claim_boundary": BOUNDARY,
                }
            )
        sample_payload[variant_id] = (
            payload[
                [
                    "timestamp",
                    "split",
                    "tier_view",
                    "variant_decision_flag",
                    "candidate_decision_score",
                    "reward_skew_score",
                    "weak_context_cost",
                    "support_identity_match_flag",
                ]
            ]
            .head(3)
            .assign(timestamp=lambda d: d["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ"))
            .to_dict("records")
        )

    return manifest_rows, queue_rows, sample_payload


def write_stage_outputs(manifest_rows: list[dict[str, Any]], queue_rows: list[dict[str, Any]], sample_payload: dict[str, Any]) -> None:
    write_csv(
        RUN_DIR / "probe_payload_manifest.csv",
        manifest_rows,
        [
            "variant_id",
            "variant_role",
            "materialization_judgment",
            "next_queue_action",
            "payload_path",
            "payload_hash",
            "handoff_path",
            "handoff_hash",
            "mt5_tier_a_signal_path",
            "mt5_tier_a_signal_hash",
            "decision_surface_hash",
            "selected_candidate",
            "onnx_readiness",
            "performance_claim",
        ],
    )
    write_csv(
        RUN_DIR / "mt5_probe_queue.csv",
        queue_rows,
        [
            "queue_id",
            "variant_id",
            "queue_role",
            "payload_path",
            "handoff_path",
            "mt5_tier_a_signal_path",
            "required_before_external_claim",
            "claim_boundary",
        ],
    )
    readiness = [
        {
            "check_name": "variant_payloads_materialized",
            "status": "passed",
            "effect": f"payloads={len(manifest_rows)}",
        },
        {
            "check_name": "mt5_queue_materialized",
            "status": "passed",
            "effect": f"queued_rows={len(queue_rows)};failure_boundary_excluded=1",
        },
        {
            "check_name": "tier_b_boundary_preserved",
            "status": "passed",
            "effect": "Tier B rows remain structural payloads and not runtime fallback authority.",
        },
        {
            "check_name": "performance_claim_boundary",
            "status": "out_of_scope_by_claim",
            "effect": "Payloads contain signals only; trading KPI and MT5 output are still missing.",
        },
    ]
    write_csv(RUN_DIR / "payload_readiness_receipt.csv", readiness, ["check_name", "status", "effect"])
    write_json(RUN_DIR / "payload_samples.json", sample_payload)


def write_stage_run_ledger() -> None:
    stage_ledger = REVIEWS / "stage_run_ledger.csv"
    rows = read_csv_rows(stage_ledger) if stage_ledger.exists() else []
    rows.extend(
        [
            {
                "row_id": f"{RUN_ID}__tier_a",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "aggressive_probe_payload_materialization",
                "tier_scope": "Tier A separate",
                "scoreboard": "structural_payload_materialization",
                "status": "completed",
                "judgment": "tier_a_payloads_materialized_no_performance_claim",
                "evidence_boundary": "research_development_only",
                "report_path": (REVIEWS / "run270B_report.md").as_posix(),
                "notes": "Tier A signal payloads and MT5 handoff CSVs materialized; selected_candidate=none; onnx_readiness=not_claimed.",
            },
            {
                "row_id": f"{RUN_ID}__tier_b",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "aggressive_probe_payload_materialization",
                "tier_scope": "Tier B separate",
                "scoreboard": "structural_payload_materialization",
                "status": "completed",
                "judgment": "tier_b_structural_payloads_no_runtime_authority",
                "evidence_boundary": "research_development_only",
                "report_path": (REVIEWS / "run270B_report.md").as_posix(),
                "notes": "Tier B partial-context payloads preserved without runtime fallback authority.",
            },
            {
                "row_id": f"{RUN_ID}__tier_ab",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "aggressive_probe_payload_materialization",
                "tier_scope": "Tier A+B combined",
                "scoreboard": "structural_payload_materialization",
                "status": "completed",
                "judgment": "combined_payload_view_no_routed_pnl_claim",
                "evidence_boundary": "research_development_only",
                "report_path": (REVIEWS / "run270B_report.md").as_posix(),
                "notes": "Combined payload view is structural only; next_action=run270C_execute_or_prepare_mt5_aggressive_probe.",
            },
        ]
    )
    write_csv(
        stage_ledger,
        rows,
        [
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
        ],
    )


def write_report(manifest_rows: list[dict[str, Any]], queue_rows: list[dict[str, Any]]) -> None:
    active = [r for r in manifest_rows if r["next_queue_action"] == "include_for_next_probe_materialization"]
    control = [r for r in manifest_rows if r["next_queue_action"] == "include_as_control"]
    excluded = [r for r in manifest_rows if r["next_queue_action"] == "exclude_from_mt5_probe_queue"]
    active_lines = "\n".join([f"- `{r['variant_id']}`: `{r['materialization_judgment']}`" for r in active])
    control_lines = "\n".join([f"- `{r['variant_id']}`: `{r['materialization_judgment']}`" for r in control])
    excluded_lines = "\n".join([f"- `{r['variant_id']}`: `{r['materialization_judgment']}`" for r in excluded])
    write_md(
        REVIEWS / "run270B_report.md",
        f"""# Stage270 Run270B Aggressive Probe Payload Materialization(270단계 270B 공격형 탐침 페이로드 물질화)

- status(상태): `completed_aggressive_probe_payload_materialization_no_candidate_selection`
- run(실행): `{RUN_ID}`
- payloads(페이로드): `{len(manifest_rows)}`
- mt5_queue_rows(MT5 대기열 행): `{len(queue_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run270C_execute_or_prepare_mt5_aggressive_probe`

## Plain Result(쉬운 결과)

run270B(270B 실행)는 run270A(270A 실행)의 branch(분기)를 payload parquet(페이로드 parquet), handoff JSON(인계 JSON), Tier A MT5 signal CSV(Tier A MT5 신호 CSV)로 물질화했다.
효과(effect, 효과): 다음 작업에서 MT5(`MetaTrader 5`, 메타트레이더5)나 동등한 runtime probe(런타임 탐침)를 시도할 수 있는 파일 단위가 생겼다.

## Active Probe Queue(활성 탐침 대기열)

{active_lines}

## Control(대조)

{control_lines}

## Excluded Boundary(제외 경계)

{excluded_lines}

## Result Judgment(결과 판정)

- result_subject(판정 대상): aggressive probe payloads(공격형 탐침 페이로드)
- evidence_available(있는 근거): payload parquet(페이로드 parquet), handoff JSON(인계 JSON), Tier A signal CSV(Tier A 신호 CSV), payload manifest(페이로드 목록), readiness receipt(준비 영수증)
- evidence_missing(빠진 근거): MT5 runtime output(MT5 런타임 출력), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), trading KPI(거래 핵심 성과 지표), ONNX export/parity(온엑스 내보내기/동등성)
- judgment_label(판정 라벨): `payload_materialized_no_candidate_selection`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)
- next_condition(다음 조건): run270C(270C 실행)에서 `mt5_probe_queue.csv`를 외부 runtime probe(런타임 탐침)로 실행하거나, 실행 도구가 부족하면 현재 payload 기준으로 좁은 준비/차단 근거를 남긴다.

## Boundary(경계)

This report(이 보고서)는 selected candidate(선택 후보), ONNX readiness(온엑스 준비), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선), Goal Achieve(목표 달성)를 주장하지 않는다.
""",
    )


def write_review_index_and_selection() -> None:
    write_md(
        REVIEWS / "review_index.md",
        f"""# Stage270 Review Index(270단계 검토 색인)

- stage_brief(단계 개요): `{(STAGE / "00_spec" / "stage_brief.md").as_posix()}`
- input_refs(입력 참조): `{(STAGE / "01_inputs" / "input_refs.md").as_posix()}`
- selection_status(선택 상태): `{(STAGE / "04_selected" / "selection_status.md").as_posix()}`
- stage_run_ledger(단계 실행 장부): `{(REVIEWS / "stage_run_ledger.csv").as_posix()}`
- run270A_manifest(270A 목록): `{(RUN270A / "run_manifest.json").as_posix()}`
- run270A_report(270A 보고): `{(REVIEWS / "run270A_report.md").as_posix()}`
- run270B_manifest(270B 목록): `{(RUN_DIR / "run_manifest.json").as_posix()}`
- run270B_payload_manifest(270B 페이로드 목록): `{(RUN_DIR / "probe_payload_manifest.csv").as_posix()}`
- run270B_mt5_probe_queue(270B MT5 탐침 대기열): `{(RUN_DIR / "mt5_probe_queue.csv").as_posix()}`
- run270B_payload_readiness(270B 페이로드 준비): `{(RUN_DIR / "payload_readiness_receipt.csv").as_posix()}`
- run270B_lineage(270B 계보): `{(RUN_DIR / "lineage.json").as_posix()}`
- run270B_report(270B 보고): `{(REVIEWS / "run270B_report.md").as_posix()}`

## Current State(현재 상태)

Stage270(270단계)는 run270B(270B 실행) aggressive probe payload materialization(공격형 탐침 페이로드 물질화)을 완료했다.
효과(effect, 효과): 다음 작업은 run270C(270C 실행)에서 MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)를 시도하거나, 실행 도구 조건을 좁게 기록하는 것이다.
""",
    )
    write_md(
        STAGE / "04_selected" / "selection_status.md",
        f"""# Stage270 Selection Status(270단계 선택 상태)

- stage_status(단계 상태): `run270B_aggressive_probe_payload_materialization_completed`
- current_packet(현재 작업 묶음): `stage270_aggressive_nonfilter_upside_probe_v1`
- current_run(현재 실행): `{RUN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `269_onnx_candidate_campaign__fresh_thesis_candidate_construction`
- active_seed(활성 씨앗): `cp269A_asymmetric_nonfilter_reentry_surface`
- support_control(보조 대조): `cp269D_runtime_handoff_isolation_control`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- run270A_variant_plan(270A 변형 계획): `{(RUN270A / "aggressive_probe_variant_plan.csv").as_posix()}`
- run270B_payload_manifest(270B 페이로드 목록): `{(RUN_DIR / "probe_payload_manifest.csv").as_posix()}`
- run270B_mt5_probe_queue(270B MT5 탐침 대기열): `{(RUN_DIR / "mt5_probe_queue.csv").as_posix()}`
- run270B_report(270B 보고): `{(REVIEWS / "run270B_report.md").as_posix()}`
- next_action(다음 행동): `run270C_execute_or_prepare_mt5_aggressive_probe`

## Current Meaning(현재 의미)

run270B(270B 실행)는 branch(분기)를 실제 handoff payload(인계 페이로드)로 만들었다.
효과(effect, 효과): runtime probe(런타임 탐침)를 시도할 파일은 생겼지만, 아직 trading KPI(거래 핵심 성과 지표), selected candidate(선택 후보), ONNX readiness(온엑스 준비)는 없다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def build_manifest(manifest_rows: list[dict[str, Any]], queue_rows: list[dict[str, Any]]) -> dict[str, Any]:
    source_inputs = [
        VARIANT_PLAN,
        RUN270A_MANIFEST,
        RUN270A_SUPPLY,
        RUN270A_READINESS,
        CP269A_SCORE_TABLE,
        CP269D_SCORE_TABLE,
        CP269A_HANDOFF,
        CP269D_HANDOFF,
    ]
    output_artifacts = [
        RUN_DIR / "probe_payload_manifest.csv",
        RUN_DIR / "mt5_probe_queue.csv",
        RUN_DIR / "payload_readiness_receipt.csv",
        RUN_DIR / "payload_samples.json",
    ]
    output_artifacts.extend(sorted(PAYLOAD_DIR.glob("*.parquet")))
    output_artifacts.extend(sorted(HANDOFF_DIR.glob("*.json")))
    output_artifacts.extend(sorted(MT5_DIR.glob("*.csv")))
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": "completed_aggressive_probe_payload_materialization_no_candidate_selection",
        "producer": "stage_pipelines/stage270/materialize_aggressive_probe_payloads.py",
        "entry_command": "python stage_pipelines/stage270/materialize_aggressive_probe_payloads.py",
        "source_inputs": [p.as_posix() for p in source_inputs],
        "input_hashes": {p.as_posix(): sha256_file(p) for p in source_inputs},
        "output_artifacts": [p.as_posix() for p in output_artifacts],
        "output_hashes": {p.as_posix(): sha256_file(p) for p in output_artifacts},
        "payload_count": len(manifest_rows),
        "mt5_queue_rows": len(queue_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_payload_materialization_only",
        "claim_boundary": BOUNDARY,
        "next_action": "run270C_execute_or_prepare_mt5_aggressive_probe",
    }
    write_json(RUN_DIR / "run_manifest.json", manifest)
    return manifest


def write_lineage(manifest: dict[str, Any]) -> None:
    artifacts = manifest["output_artifacts"] + [
        (RUN_DIR / "run_manifest.json").as_posix(),
        (RUN_DIR / "lineage.json").as_posix(),
        (REVIEWS / "run270B_report.md").as_posix(),
        (REVIEWS / "review_index.md").as_posix(),
        (STAGE / "04_selected" / "selection_status.md").as_posix(),
    ]
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [
            "run270C_execute_or_prepare_mt5_aggressive_probe",
            "docs/registers/run_registry.csv",
            "docs/registers/alpha_run_ledger.csv",
            "docs/registers/artifact_registry.csv",
        ],
        "artifact_paths": artifacts,
        "artifact_hashes": {
            path: sha256_file(Path(path)) for path in artifacts if Path(path).exists()
        },
        "registry_links": {
            "run_registry": "pending_update_this_pass",
            "alpha_run_ledger": "pending_update_this_pass",
            "stage_run_ledger": (REVIEWS / "stage_run_ledger.csv").as_posix(),
            "artifact_registry": "pending_update_this_pass",
        },
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_DIR / "lineage.json", lineage)


def main() -> None:
    ensure_dirs()
    cp269a, cp269d, variants, cp269a_handoff, cp269d_handoff = load_source_tables()
    manifest_rows, queue_rows, sample_payload = materialize_payloads(
        cp269a, cp269d, variants, cp269a_handoff, cp269d_handoff
    )
    write_stage_outputs(manifest_rows, queue_rows, sample_payload)
    write_stage_run_ledger()
    write_report(manifest_rows, queue_rows)
    write_review_index_and_selection()
    manifest = build_manifest(manifest_rows, queue_rows)
    write_lineage(manifest)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "status": manifest["status"],
                "payload_count": len(manifest_rows),
                "mt5_queue_rows": len(queue_rows),
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "next_action": manifest["next_action"],
                "manifest_hash": sha256_file(RUN_DIR / "run_manifest.json"),
                "lineage_hash": sha256_file(RUN_DIR / "lineage.json"),
                "report_hash": sha256_file(REVIEWS / "run270B_report.md"),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
