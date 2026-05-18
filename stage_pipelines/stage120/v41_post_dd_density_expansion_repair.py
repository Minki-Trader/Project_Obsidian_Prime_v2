from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage118 import v41_dd_compression_density_repair as s118  # noqa: E402


s100 = s118.s100
s108 = s118.s108

STAGE_ID = "120_adapter_research__v41_post_dd_density_expansion_repair"
RUN_NUMBER = "run120A"
RUN_ID = "run120A_stage120_v41_post_dd_density_expansion_repair_v1"
PACKET_ID = "stage120_v41_post_dd_density_expansion_repair_v1"
PARENT_RUN_ID = "run119A_stage119_v41_dd_compression_followup_review_v1"
SOURCE_STAGE119_ID = "119_adapter_research__v41_dd_compression_followup_review"
SOURCE_STAGE119_CLOSEOUT_COMMIT = "83fb1a83b27a60a7953c88259a2655ceec772c42"
SOURCE_STAGE119_LATEST_COMMIT = "33280e4223984a5d49484a30cee574874e929b16"
SOURCE_STAGE118_CLOSEOUT_COMMIT = "1edf5a69757ae2e58bfcf0e4126b325d291170af"
SOURCE_STAGE118_LATEST_COMMIT = "d643def47022c81f86847fc802973370ccdeb2db"
SOURCE_ADAPTER_ID = "stage118_risk035_dd_guardrail_surface"
NEXT_STAGE_ID = "121_adapter_research__v41_post_dd_density_followup_review"
NEXT_RUN_ID = "run121A_stage121_v41_post_dd_density_followup_review_v1"
NEXT_PACKET_ID = "stage121_v41_post_dd_density_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
COMMON_ROOT = f"OPV2/s120a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage120_post_dd_density_expansion_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage120_post_dd_density_expansion_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage120_post_dd_density_expansion_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage120_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage120_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage120_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage120_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage120_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage120_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

STAGE110_REFERENCE = {
    "oos_net": 644.76,
    "oos_pf": 1.637076853,
    "oos_dd_pct": 18.69,
    "oos_trade_count": 147,
    "oos_early_net": 38.84,
    "oos_early_pf": 1.157011764,
}
LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE118_GUARDRAILS = {
    "s118_v41_h3_cd9_session_margin_risk035_lng52": {
        "profit_factor": 1.82633452,
        "net_profit": 1195.83,
        "max_drawdown_percent": 14.39,
        "trade_count": 174,
    },
    "s118_v41_h3_cd8_session_margin_risk035_lng53": {
        "profit_factor": 1.733354796,
        "net_profit": 1070.61,
        "max_drawdown_percent": 14.75,
        "trade_count": 176,
    },
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s120_v41_h3_cd9_session_margin_risk035_lng51",
        label="stage120_quality_anchor_risk035_long51",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=9,
        short_threshold=0.55,
        long_threshold=0.51,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage120 density expansion: ease long threshold to 0.51 while preserving risk035 DD guardrail.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s120_v41_h3_cd8_session_margin_risk035_lng52",
        label="stage120_density_anchor_risk035_cd8_long52",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.55,
        long_threshold=0.52,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage120 density expansion: combine cooldown 8 with long threshold 0.52 under risk035.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s120_v41_h3_cd7_session_margin_risk035_lng53",
        label="stage120_density_anchor_risk035_cd7_long53",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=7,
        short_threshold=0.55,
        long_threshold=0.53,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage120 density expansion: ease same-direction cooldown to 7 under risk035.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s120_v41_h3_cd7_session_margin_risk035_lng52",
        label="stage120_density_anchor_risk035_cd7_long52",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=7,
        short_threshold=0.55,
        long_threshold=0.52,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage120 density expansion: combine cooldown 7 with long threshold 0.52 under risk035.",
    ),
)

SOURCE_BASELINE_BY_VARIANT = {
    "s120_v41_h3_cd9_session_margin_risk035_lng51": "s118_v41_h3_cd9_session_margin_risk035_lng52",
    "s120_v41_h3_cd8_session_margin_risk035_lng52": "s118_v41_h3_cd8_session_margin_risk035_lng53",
    "s120_v41_h3_cd7_session_margin_risk035_lng53": "s118_v41_h3_cd8_session_margin_risk035_lng53",
    "s120_v41_h3_cd7_session_margin_risk035_lng52": "s118_v41_h3_cd8_session_margin_risk035_lng53",
}

SOURCE_SPECS_BY_VARIANT = {
    variant.adapter_id: {
        "label": "v41_v22_midcov_et40_agree_h2c0_no_b",
        "feature_anchor": "s59ar_v41_sd8_h3_stage59d_adapter",
        "variant_root": s100.SOURCE_VARIANT_ROOT,
        "model": s100.SOURCE_MODEL,
        "validation_ini": s100.SOURCE_VAL_INI,
        "oos_ini": s100.SOURCE_OOS_INI,
    }
    for variant in VARIANTS
}

CONTEXT_GATE_SPECS = {
    variant.adapter_id: {
        "gate_column": f"stage120_gate_session_margin_{variant.adapter_id.split('_risk035_')[-1]}",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": f"Stage120 post-DD density expansion under risk035: {variant.label}.",
    }
    for variant in VARIANTS
}


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return s118.as_float(row, key, default)


def routed_oos(summary_rows: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return s118.routed_oos(summary_rows)


def early_segment(segment_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> Mapping[str, Any]:
    return s118.early_segment(segment_rows, adapter_id)


def stage120_extra_set_values(variant: s100.repair.RepairVariant, magic: int) -> dict[str, Any]:
    return s118.stage118_extra_set_values(variant, magic)


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(VARIANTS, start=1):
        variant_root = RUN_ROOT / variant.adapter_id
        for split in ("validation_is", "oos"):
            date_values = s100.parse_ini(s100.base.engine.source_attempt_ini(split, variant))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (s100.mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                    (s100.mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 12010000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=120,
                        exploration_label="stage120_BaselineAdapter__PostDdDensityExpansionRepair",
                        attempt_name=f"{variant.adapter_id}_{attempt_token}_{split_token}",
                        tier=tier,
                        split=split,
                        model_path=str(inputs["model_exports"][variant.adapter_id]["common_path"]),
                        model_id=f"{RUN_ID}_{variant.adapter_id}_entry_adapter",
                        model_backend="ebm_table",
                        feature_path=str(inputs["feature_exports"][variant.adapter_id][split]["common_path"]),
                        feature_count=2,
                        feature_order_hash=inputs["model_exports"][variant.adapter_id]["feature_order_hash"],
                        short_threshold=variant.short_threshold,
                        long_threshold=variant.long_threshold,
                        min_margin=0.0,
                        invert_signal=False,
                        from_date=str(date_values["FromDate"]),
                        to_date=str(date_values["ToDate"]),
                        primary_active_tier="tier_a",
                        attempt_role=attempt_role,
                        record_view_prefix=prefix,
                        max_hold_bars=variant.max_hold_bars,
                        common_root=f"{COMMON_ROOT}/{variant.adapter_id}",
                        fallback_enabled=False,
                        close_on_flat_signal=variant.close_on_flat_signal,
                        reverse_on_opposite_signal=variant.reverse_on_opposite_signal,
                        close_only_on_opposite_signal=variant.close_only_on_opposite_signal,
                        extra_set_values=stage120_extra_set_values(variant, magic),
                    )
                )
    return attempts


def source_baseline(row: Mapping[str, Any]) -> Mapping[str, Any]:
    return STAGE118_GUARDRAILS.get(SOURCE_BASELINE_BY_VARIANT.get(str(row.get("adapter_id", "")), ""), {})


def best_stage120(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for row in routed_oos(summary_rows):
        early = early_segment(segment_rows, str(row.get("adapter_id", "")))
        trades = as_float(row, "trade_count")
        pf = as_float(row, "profit_factor")
        net = as_float(row, "net_profit")
        dd = as_float(row, "max_drawdown_percent", 99.0)
        source = source_baseline(row)
        trade_gain = trades - float(source.get("trade_count", 0.0) or 0.0)
        candidates.append(
            (
                trade_gain > 0 and pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"] and dd <= 16.0,
                trade_gain > 0 and pf >= LEGACY_34D["profit_factor"] and dd <= STAGE110_REFERENCE["oos_dd_pct"],
                trade_gain,
                -dd,
                pf,
                net,
                as_float(early, "profit_factor"),
                row,
            )
        )
    return max(candidates, key=lambda item: item[:7])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_density_expansion_runtime_repair_in_stage121_due_to_incomplete_runtime"
    best = best_stage120(summary_rows, segment_rows)
    source = source_baseline(best)
    trade_gain = as_float(best, "trade_count") - float(source.get("trade_count", 0.0) or 0.0)
    if (
        trade_gain > 0
        and as_float(best, "profit_factor") >= LEGACY_34D["profit_factor"]
        and as_float(best, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(best, "max_drawdown_percent", 99.0) <= 16.0
    ):
        return "continue_post_dd_density_followup_review_in_stage121_with_density_gain"
    return "continue_post_dd_density_followup_review_in_stage121"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | source(원천) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | trades(거래 수) | trade gain(거래 증가) | early PF(초반 수익 팩터) |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in routed_oos(summary_rows):
        adapter_id = str(row.get("adapter_id", ""))
        source_id = SOURCE_BASELINE_BY_VARIANT.get(adapter_id, "")
        source = source_baseline(row)
        early = early_segment(segment_rows, adapter_id)
        lines.append(
            "| {adapter} | {source} | {pf:.6f} | {net:.2f} | {dd:.2f} | {trades:.0f} | {gain:.0f} | {early_pf:.6f} |".format(
                adapter=adapter_id,
                source=source_id,
                pf=as_float(row, "profit_factor"),
                net=as_float(row, "net_profit"),
                dd=as_float(row, "max_drawdown_percent"),
                trades=as_float(row, "trade_count"),
                gain=as_float(row, "trade_count") - float(source.get("trade_count", 0.0) or 0.0),
                early_pf=as_float(early, "profit_factor"),
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_stage120(summary_rows, segment_rows)
    source = source_baseline(best)
    return f"""# Stage120 Post-DD Density Expansion Repair Report(120단계 손실률 압축 뒤 밀도 확장 수리 보고서)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE119_ID}`
- source_stage119_closeout_commit(원천 119단계 종료 커밋): `{SOURCE_STAGE119_CLOSEOUT_COMMIT}`
- source_stage119_latest_commit(원천 119단계 최신 커밋): `{SOURCE_STAGE119_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage118/119(118/119단계)에서 확인한 risk cap 0.035(위험 상한 3.5%) DD guardrail(손실률 가드레일)을 유지하면서, trade count(거래 수)를 34D target(34D 목표)에 더 가깝게 늘릴 수 있는가?

Effect(효과): Stage120(120단계)은 새 모델 hunting(모델 탐색)이 아니라 threshold/cooldown(임계값/대기시간)만 좁게 풀어 density(밀도) 회복 가능성을 측정한다.

## Result Table(결과 표)

{row_table(summary_rows, segment_rows)}

## Best Read(최선 판독)

- best_variant(최선 변형): `{best.get("adapter_id", "none")}`
- oos_pf(표본외 수익 팩터): `{as_float(best, "profit_factor"):.6f}`
- oos_net(표본외 순손익): `{as_float(best, "net_profit"):.2f}`
- oos_dd_pct(표본외 손실률): `{as_float(best, "max_drawdown_percent"):.2f}`
- trades(거래 수): `{as_float(best, "trade_count"):.0f}`
- trade_gain_vs_source(원천 대비 거래 증가): `{as_float(best, "trade_count") - float(source.get("trade_count", 0.0) or 0.0):.0f}`

## Judgment(판정)

- result_subject(판정 대상): Stage120 post-DD density expansion repair(120단계 손실률 압축 뒤 밀도 확장 수리).
- evidence_available(있는 근거): MT5 runtime reports(MT5 실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리).
- evidence_missing(부족 근거): Stage121(121단계) 후속 검토 전에는 equity-shape audit(자본 곡선 형태 감사)과 density durability(밀도 지속성)가 아직 부족하다.
- judgment_label(판정 라벨): `post_dd_density_expansion_measured_not_final`.
- claim_boundary(주장 경계): `{BOUNDARY}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage120 Decision(120단계 판정)

decision(판정): `{decision}`

Stage120(120단계)은 Stage119(119단계)의 판정대로 DD guardrail(손실률 가드레일)을 유지한 density expansion repair(밀도 확장 수리)를 실제 MT5 runtime(실행환경)에서 측정했다.

Effect(효과): 결과를 Stage121(121단계) follow-up review(후속 검토)로 넘겨, density gain(밀도 증가)이 PF/net/DD(수익 팩터/순손익/손실률)를 망가뜨렸는지 판정한다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- source_stage119_closeout_commit(원천 119단계 종료 커밋): `{SOURCE_STAGE119_CLOSEOUT_COMMIT}`
- source_stage119_latest_commit(원천 119단계 최신 커밋): `{SOURCE_STAGE119_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage120(120단계) 종료는 전체 목표 완료가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상을 노리는 v2-native research(브이투 고유 연구)는 Stage121(121단계)로 이어진다.
"""


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    paths = [
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        RISK_ATR_TELEMETRY_PATH,
        GATE_FEATURE_SUMMARY_PATH,
        TIER_B_DIAGNOSTIC_PATH,
        DECISION_PATH,
        AUDIT_CSV_PATH,
        STAGE_LEDGER_PATH,
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
    ]
    rows = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage120_post_dd_density_expansion_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage120 v2-native post-DD density expansion repair artifact.",
                }
            )
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        raw_path = report.get("path") or html.get("path")
        if raw_path and path_exists(Path(str(raw_path))):
            path = Path(str(raw_path))
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__mt5_report__{path.stem}",
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Actual Stage120 MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    status = "completed" if external == "completed" else "blocked"
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_post_dd_density_expansion_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage119_closeout_commit", SOURCE_STAGE119_CLOSEOUT_COMMIT),
                        ("source_stage119_latest_commit", SOURCE_STAGE119_LATEST_COMMIT),
                        ("source_stage118_latest_commit", SOURCE_STAGE118_LATEST_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = s100.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        list(artifacts),
        key="artifact_id",
    )
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def tier_b_rows() -> list[dict[str, Any]]:
    rows = []
    coverage = s100.base.engine.route_coverage()
    for variant in VARIANTS:
        variant_cov = coverage.get(variant.adapter_id, {})
        for split_name in ("validation", "oos"):
            split_cov = variant_cov.get(split_name, {})
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": variant.adapter_id,
                    "split": split_name,
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_this_post_dd_density_expansion_repair",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage120 isolates Tier A routed post-DD density expansion before Tier B fallback repair.",
                }
            )
    return rows


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    s108.write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "experiment_design", "primary_skill": "obsidian-experiment-design", "support_skills": ["obsidian-performance-attribution", "obsidian-result-judgment", "obsidian-runtime-parity", "obsidian-artifact-lineage"], "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"], "status": status})
    s108.write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "external_verification_status": result.get("external_verification_status"), "completed_attempt_count": result.get("completed_attempt_count"), "expected_attempt_count": result.get("expected_attempt_count"), "gate_feature_summary_path": rel(GATE_FEATURE_SUMMARY_PATH), "claim_boundary": BOUNDARY})
    s108.write_json(PACKET_ROOT / "result_judgment_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "decision": decision, "judgment_label": "post_dd_density_expansion_measured_not_final", "legacy_relation": "lesson_only_target_surface_no_code_copy", "overall_goal_complete": False})
    s108.write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": decision, "source_stage119_closeout_commit": SOURCE_STAGE119_CLOSEOUT_COMMIT, "source_stage119_latest_commit": SOURCE_STAGE119_LATEST_COMMIT, "source_stage118_latest_commit": SOURCE_STAGE118_LATEST_COMMIT, "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "overall_goal_complete": False})


def create_next_stage(decision: str, external: str) -> None:
    s108.write_md(NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md", f"""# {NEXT_STAGE_ID}

Stage121(121단계)은 Stage120(120단계)의 post-DD density expansion repair(손실률 압축 뒤 밀도 확장 수리) 결과를 후속 검토한다.

## Bounded Question(경계 질문)

Stage120(120단계)의 density gain(밀도 증가)이 PF/net/DD(수익 팩터/순손익/손실률)와 segment KPI(구간 핵심 성과 지표)를 보존했는가?

Effect(효과): Stage121(121단계)은 새 실험을 늘리지 않고, Stage120 evidence(근거)를 판독해 다음 bounded repair(경계 수리)를 정한다.

## Boundary(경계)

`{BOUNDARY}`
""")
    s108.write_md(NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md", f"""# Stage121 Input References(121단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_external_verification_status(원천 외부 검증 상태): `{external}`
- stage120_report(120단계 보고서): `{rel(REPORT_PATH)}`
- stage120_summary(120단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""")
    s108.write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"""# Stage121 Review Index(121단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{decision}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`
""")
    s108.write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage121 Selection Status(121단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")


def update_current_truth(decision: str, external: str) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage120(120단계) closed(종료) as `{decision}` and Stage121(121단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): post-DD density expansion(손실률 압축 뒤 밀도 확장) 결과를 후속 검토로 넘긴다.
- >-
  Stage120 result(120단계 결과)는 `{rel(SUMMARY_CSV_PATH)}`와 `{rel(SEGMENT_KPI_PATH)}`에 기록했다. Effect(효과): DD guardrail(손실률 가드레일)을 지키며 density(밀도)를 늘릴 수 있는지 다음 단계에서 판독한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage120_v41_post_dd_density_expansion_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage119_closeout_commit: {SOURCE_STAGE119_CLOSEOUT_COMMIT}
  source_stage119_latest_commit: {SOURCE_STAGE119_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage120_v41_post_dd_density_expansion_repair:"
    if marker in text:
        text = re.sub(r"\nstage120_v41_post_dd_density_expansion_repair:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    s108.write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage120 Selection Status(120단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE119_ID}`
- source_decision(원천 판정): `continue_post_dd_density_expansion_repair_in_stage120`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage120_decision(120단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")
    s108.write_md(REVIEWS_ROOT / "review_index.md", f"""# Stage120 Review Index(120단계 검토 색인)

- status(상태): `closed_{decision}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
""")
    s108.write_md(CURRENT_WORKING_STATE_PATH, f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage121_post_dd_density_followup_review_surface`
- status(상태): `stage120_closed_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage120(120단계) closed(종료) as v2-native v41 post-DD density expansion repair(브이투 고유 브이41 손실률 압축 뒤 밀도 확장 수리). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰고, 다음 연구는 Stage121(121단계) 후속 검토로 이어진다.

## Latest Stage120 Evidence(최신 120단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `{rel(SEGMENT_KPI_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""")
    create_next_stage(decision, external)


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-18 - Stage120 v41 post-DD density expansion repair closeout(120단계 v41 손실률 압축 뒤 밀도 확장 수리 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): risk cap 0.035(위험 상한 3.5%) DD guardrail(손실률 가드레일)을 유지한 채 threshold/cooldown(임계값/대기시간)을 좁게 풀어 density(밀도) 확장 가능성을 측정하고 Stage121(121단계) 후속 검토로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def configure_stage120() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE117_ID": SOURCE_STAGE119_ID,
        "SOURCE_STAGE117_CLOSEOUT_COMMIT": SOURCE_STAGE119_CLOSEOUT_COMMIT,
        "SOURCE_STAGE117_LATEST_COMMIT": SOURCE_STAGE119_LATEST_COMMIT,
        "SOURCE_STAGE116_CLOSEOUT_COMMIT": SOURCE_STAGE118_CLOSEOUT_COMMIT,
        "SOURCE_STAGE116_LATEST_COMMIT": SOURCE_STAGE118_LATEST_COMMIT,
        "SOURCE_ADAPTER_ID": SOURCE_ADAPTER_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "TARGET_SURFACE": TARGET_SURFACE,
        "BOUNDARY": BOUNDARY,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "SELECTED_ROOT": SELECTED_ROOT,
        "PACKET_ROOT": PACKET_ROOT,
        "NEXT_STAGE_ROOT": NEXT_STAGE_ROOT,
        "COMMON_ROOT": COMMON_ROOT,
        "SUMMARY_JSON_PATH": SUMMARY_JSON_PATH,
        "SUMMARY_CSV_PATH": SUMMARY_CSV_PATH,
        "REPORT_PATH": REPORT_PATH,
        "SEGMENT_KPI_PATH": SEGMENT_KPI_PATH,
        "RISK_ATR_TELEMETRY_PATH": RISK_ATR_TELEMETRY_PATH,
        "GATE_FEATURE_SUMMARY_PATH": GATE_FEATURE_SUMMARY_PATH,
        "TIER_B_DIAGNOSTIC_PATH": TIER_B_DIAGNOSTIC_PATH,
        "DECISION_PATH": DECISION_PATH,
        "AUDIT_CSV_PATH": AUDIT_CSV_PATH,
        "STAGE_LEDGER_PATH": STAGE_LEDGER_PATH,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "CONTEXT_GATE_SPECS": CONTEXT_GATE_SPECS,
        "VARIANTS": VARIANTS,
        "SOURCE_BASELINE_BY_VARIANT": SOURCE_BASELINE_BY_VARIANT,
        "STAGE110_REFERENCE": STAGE110_REFERENCE,
        "LEGACY_34D": LEGACY_34D,
    }.items():
        setattr(s118, name, value)
    s118.build_attempts = build_attempts
    s118.best_stage118 = best_stage120
    s118.decide = decide
    s118.row_table = row_table
    s118.report_markdown = report_markdown
    s118.decision_markdown = decision_markdown
    s118.artifact_rows = artifact_rows
    s118.write_ledgers = write_ledgers
    s118.write_packet_files = write_packet_files
    s118.tier_b_rows = tier_b_rows
    s118.update_current_truth = update_current_truth
    s118.append_changelog = append_changelog
    s118.configure_stage118()
    s100.tier_b_rows = tier_b_rows


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage120()
    return s100.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
