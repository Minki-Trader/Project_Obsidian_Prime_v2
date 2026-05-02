from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from foundation.control_plane.ledger import io_path
from foundation.control_plane.mt5_tier_balance_completion import ROOT
from stage_pipelines.stage13.mlp_internal_behavior_probes import rel


STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_ID = "run04N_mlp_feature_group_interaction_profit_probe_v1"
PACKET_ID = "stage13_run04N_mlp_feature_group_interaction_profit_probe_packet_v1"
SOURCE_RUN_ID = "run04F_mlp_direction_asymmetry_runtime_probe_v1"
SOURCE_LEARNING_RUN_ID = "run04M_mlp_learning_behavior_runtime_probe_v1"
BOUNDARY = "feature_group_interaction_profit_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews/run04N_mlp_feature_group_interaction_profit_probe_packet.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    evidence = [rel(RUN_ROOT / name) for name in ("python_variant_probability_summary.csv", "mt5_runtime_probability_summary.csv", "mt5_python_parity_summary.csv", "mt5_trade_profit_summary.csv", "feature_group_interaction_summary.csv")]
    status = "completed" if payload["external_verification_status"] == "completed" else "blocked"
    return [
        {"packet_id": PACKET_ID, "skill": "obsidian-experiment-design", "status": status, "hypothesis": "Volatility/range features may act as an MLP context gate rather than a standalone signal source.", "decision_use": "Stage13 model learning behavior characterization with profit propagation diagnostics only.", "comparison_baseline": "RUN04F original Tier A q90 trading surface.", "control_variables": ["same model", "same q90 threshold", "same split dates", "same MT5 tester settings", "same immediate-reversal trading policy"], "changed_variables": ["feature group median ablations", "volatility-only restore surface"], "sample_scope": "Tier A validation_is/OOS US100 M5 Strategy Tester runs", "success_criteria": "MT5/Python probability parity passes and trade reports exist for all variants.", "failure_criteria": "missing telemetry, missing reports, row mismatch, or MT5 execution failure", "invalid_conditions": ["feature order mismatch", "threshold optimization", "using profit as selection"], "stop_conditions": ["do not promote", "do not tune threshold on profit"], "evidence_plan": evidence},
        {"packet_id": PACKET_ID, "skill": "obsidian-data-integrity", "status": status, "data_source": "RUN04F Tier A feature matrices transformed by validation median references.", "time_axis": "existing split row order and MT5 bar-close timestamp contract preserved.", "sample_scope": "validation_is rows 9844 and OOS rows 7584 where source feature matrices are available.", "missing_or_duplicate_check": "row counts checked by Python/MT5 parity.", "feature_label_boundary": "no labels used in this run; profit comes from MT5 tester only.", "split_boundary": SPLIT_CONTRACT, "leakage_risk": "post-hoc variant interpretation and profit reading bias", "data_hash_or_identity": "run_manifest records feature matrix hashes.", "integrity_judgment": "usable_with_boundary"},
        {"packet_id": PACKET_ID, "skill": "obsidian-runtime-parity", "status": status, "research_path": "stage_pipelines/stage13/mlp_feature_group_interaction_profit_probe.py", "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5", "shared_contract": "same ONNX model, transformed MT5 feature CSVs, q90 threshold, feature order hash, split dates.", "known_differences": "Python compares probability shape; MT5 also executes trades for diagnostic profit.", "parity_check": rel(RUN_ROOT / "mt5_python_parity_summary.csv"), "parity_identity": "run_manifest records set/ini/report/telemetry identities.", "runtime_claim_boundary": "runtime_probe"},
        {"packet_id": PACKET_ID, "skill": "obsidian-backtest-forensics", "status": status, "tester_identity": "MT5 Strategy Tester US100 M5, deposit 500, leverage 1:100, model 4, same generated set/ini family.", "ea_identity": "ObsidianPrimeV2_RuntimeProbeEA with fixed q90 threshold and max_hold_bars 9.", "report_identity": rel(RUN_ROOT / "mt5/reports"), "trade_evidence": rel(RUN_ROOT / "mt5_trade_profit_summary.csv"), "cost_assumptions": "Tester spread/commission/slippage inherited from terminal/report; no cost tuning.", "forensic_checks": ["report parsed", "trade count recorded", "drawdown recorded", "telemetry/action rows recorded"], "backtest_judgment": "usable_with_boundary"},
        {"packet_id": PACKET_ID, "skill": "obsidian-performance-attribution", "status": status, "observed_change": "profit, drawdown, trade count, and probability shape under feature group perturbations.", "comparison_baseline": "original RUN04F Tier A q90 trading surface.", "likely_drivers": ["volatility/range group removal", "double group removal non-additivity", "trade count shifts"], "segment_checks": ["validation/OOS", "variant", "MT5 trade summary", "telemetry actions"], "trade_shape": rel(RUN_ROOT / "mt5_trade_profit_summary.csv"), "alternative_explanations": ["threshold fixed at old q90", "profit sample noise", "feature median ablation may create unrealistic input states"], "attribution_confidence": "low_to_medium_diagnostic", "next_probe": payload["recommendation"]},
        {"packet_id": PACKET_ID, "skill": "obsidian-artifact-lineage", "status": status, "source_inputs": [rel(SOURCE_ROOT / "run_manifest.json"), rel(SOURCE_ROOT / "thresholds/threshold_handoff.json")], "producer": "stage_pipelines/stage13/mlp_feature_group_interaction_profit_probe.py", "consumer": "Stage13 review, ledgers, run registry.", "artifact_paths": evidence, "artifact_hashes": "manifest records source and generated hashes", "registry_links": [rel(STAGE_LEDGER_PATH), rel(PROJECT_LEDGER_PATH), rel(RUN_REGISTRY_PATH)], "availability": "generated", "lineage_judgment": "connected_with_boundary"},
        {"packet_id": PACKET_ID, "skill": "obsidian-result-judgment", "status": status, "result_subject": RUN_ID, "evidence_available": evidence, "evidence_missing": ["WFO", "threshold retest", "runtime authority packet"], "judgment_label": payload["judgment"], "claim_boundary": BOUNDARY, "next_condition": payload["recommendation"], "user_explanation_hook": "This shows how MLP feature-group perturbations propagate into MT5 profit diagnostics, not whether there is a tradable edge."},
    ]


def report(payload: Mapping[str, Any]) -> str:
    oos_trades = [row for row in payload["trade_rows"] if row["split"] == "oos"]
    top_profit = max(oos_trades, key=lambda row: as_float(row.get("net_profit")) or -1.0e18, default={})
    worst_profit = min(oos_trades, key=lambda row: as_float(row.get("net_profit")) or 1.0e18, default={})
    oos_l1 = sorted((row for row in payload["python_probability_rows"] if row["split"] == "oos"), key=lambda row: as_float(row.get("mean_l1_prob_delta")) or 0.0, reverse=True)
    top_shape = oos_l1[0] if oos_l1 else {}
    parity_pass = sum(1 for row in payload["parity_rows"] if row["parity_status"] == "pass")
    parity_partial = sum(1 for row in payload["parity_rows"] if row["parity_status"] == "partial_trade_stopout")
    lines = [
        f"# {RUN_ID} 결과 요약(Result Summary, 결과 요약)",
        "",
        f"- status(상태): `{payload['external_verification_status']}`",
        f"- judgment(판정): `{payload['judgment']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        f"- MT5/Python parity(MT5/파이썬 동등성): `{parity_pass}` pass(통과), `{parity_partial}` partial trade stopout(부분 거래 손상), total(전체) `{len(payload['parity_rows'])}`.",
        "",
        "## Core Read(핵심 판독)",
        "",
        f"- OOS(표본외) probability shape(확률 모양) 최대 변화: `{top_shape.get('variant')}` / L1 delta(L1 변화) `{fmt(top_shape.get('mean_l1_prob_delta'))}`.",
        f"- OOS(표본외) net profit(순수익) 최고 변형: `{top_profit.get('variant')}` / net(순수익) `{fmt(top_profit.get('net_profit'))}` / trades(거래 수) `{fmt(top_profit.get('trade_count'))}`.",
        f"- OOS(표본외) net profit(순수익) 최저 변형: `{worst_profit.get('variant')}` / net(순수익) `{fmt(worst_profit.get('net_profit'))}` / DD(손실) `{fmt(worst_profit.get('max_drawdown'))}`.",
        "",
        "효과(effect, 효과): 이 결과는 feature group interaction(피처 그룹 상호작용)이 MT5(메타트레이더5) 거래 진단값으로 어떻게 번지는지 보여준다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격)은 만들지 않는다.",
        "",
        "## OOS Profit(표본외 수익)",
        "",
        "| variant(변형) | net(순수익) | delta(원본 대비) | PF(수익 팩터) | DD(손실) | trades(거래) | win%(승률) | avg hold bars(평균 보유 봉) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in sorted(oos_trades, key=lambda item: as_float(item.get("net_profit")) or -1.0e18, reverse=True):
        lines.append(f"| {row['variant']} | {fmt(row['net_profit'])} | {fmt(row['profit_delta_vs_original'])} | {fmt(row['profit_factor'])} | {fmt(row['max_drawdown'])} | {fmt(row['trade_count'])} | {fmt(row['win_rate_percent'])} | {fmt(row['avg_hold_bars'])} |")
    lines.extend(["", "## Interaction Residual(상호작용 잔차)", "", "| partner(상대 그룹) | split(분할) | L1 residual(L1 잔차) | net residual(수익 잔차) | interpretation(해석) |", "|---|---|---:|---:|---|"])
    for row in payload["interaction_rows"]:
        lines.append(f"| {row['partner_group']} | {row['split']} | {fmt(row['l1_residual'])} | {fmt(row['net_profit_residual'])} | {row['interpretation']} |")
    return "\n".join(lines)


def decision(payload: Mapping[str, Any]) -> str:
    return "\n".join([
        "# 2026-05-02 Stage13 MLP Feature Group Interaction Profit Probe",
        "",
        f"- run(실행): `{RUN_ID}`",
        f"- source run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- judgment(판정): `{payload['judgment']}`",
        f"- recommendation(추천): `{payload['recommendation']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "효과(effect, 효과): volatility/range(변동성/범위) 중심의 feature group interaction(피처 그룹 상호작용)을 MT5(메타트레이더5) profit diagnostic(수익 진단)까지 연결했다.",
    ])


def work_packet(payload: Mapping[str, Any]) -> str:
    return "\n".join([
        f"# {PACKET_ID}",
        "",
        "- hypothesis(가설): volatility/range(변동성/범위)는 MLP(다층 퍼셉트론)의 독립 신호라기보다 다른 피처 그룹을 읽는 context gate(문맥 관문)일 수 있다.",
        "- changed_variables(변경값): feature matrix(피처 행렬)의 그룹별 median ablation(중앙값 제거)과 volatility-only restore(변동성만 복원)만 바꾼다.",
        "- controls(고정값): RUN04F(실행 04F) 모델, q90 threshold(q90 기준값), MT5(메타트레이더5) tester settings(테스터 설정), max_hold_bars(최대 보유 봉) 9.",
        "- profit boundary(수익 경계): profit(수익)은 propagation diagnostic(전파 진단값)이며 edge(거래 우위) 판정이 아니다.",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        f"- judgment(판정): `{payload['judgment']}`",
    ])


def sync_docs(payload: Mapping[str, Any]) -> None:
    sync_workspace_state(payload)
    sync_current_state()
    write_md(SELECTION_STATUS_PATH, "\n".join([
        "# Stage 13 Selection Status",
        "",
        "## Current Read(현재 판독)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        "- status(상태): `reviewed_feature_group_interaction_profit_probe_completed(피처 그룹 상호작용 수익 탐침 완료)`",
        f"- current run(현재 실행): `{RUN_ID}`",
        "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
        f"- judgment(판정): `{payload['judgment']}`",
    ]))
    upsert_line_by_token(REVIEW_INDEX_PATH, RUN_ID, f"- `{RUN_ID}`: `{payload['judgment']}`, report(보고서) `{rel(REPORT_PATH)}`")
    append_once(CHANGELOG_PATH, RUN_ID, f"\n- 2026-05-02: Added `{RUN_ID}` feature group interaction profit probe(피처 그룹 상호작용 수익 탐침); profit(수익)은 diagnostic(진단값)이며 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위) claim(주장) 없음.\n")


def sync_workspace_state(payload: Mapping[str, Any]) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    lines = []
    top_current_seen = False
    for line in text.splitlines():
        if line.startswith("current_run_id:"):
            if not top_current_seen:
                lines.append(f"current_run_id: {RUN_ID}")
                top_current_seen = True
            continue
        lines.append(line)
    text = "\n".join(lines)
    if not top_current_seen:
        text = text.replace(f"active_stage: {STAGE_ID}", f"active_stage: {STAGE_ID}\ncurrent_run_id: {RUN_ID}", 1)
    text = text.replace("stage13_active_run04M_mlp_learning_behavior_runtime_probe", "stage13_active_run04N_mlp_feature_group_interaction_profit_probe")
    text = text.replace("active_run04M_mlp_learning_behavior_runtime_probe", "active_run04N_mlp_feature_group_interaction_profit_probe")
    block = (
        "stage13_mlp_feature_group_interaction_profit_probe:\n"
        f"  run_id: {RUN_ID}\n"
        "  status: completed\n"
        f"  judgment: {payload['judgment']}\n"
        f"  recommendation: {payload['recommendation']}\n"
        f"  boundary: {BOUNDARY}\n"
        f"  source_run_id: {SOURCE_RUN_ID}\n"
        f"  report_path: {rel(REPORT_PATH)}\n"
    )
    text = replace_or_insert_block(text, "stage13_mlp_feature_group_interaction_profit_probe", block)
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8")


def sync_current_state() -> None:
    text = io_path(CURRENT_STATE_PATH).read_text(encoding="utf-8-sig")
    lines = [f"- current run(현재 실행): `{RUN_ID}`" if "current run(" in line else line for line in text.splitlines()]
    text = "\n".join(lines)
    latest = (
        f"Stage13(13단계)의 현재 실행(current run, 현재 실행)은 `{RUN_ID}`이고, feature group interaction(피처 그룹 상호작용)을 MT5(메타트레이더5) profit diagnostic(수익 진단)까지 연결했다.\n\n"
        "효과(effect, 효과): 수익(profit, 수익)은 edge search(거래 우위 탐색)가 아니라 MLP(다층 퍼셉트론) learning behavior(학습 행동)가 거래 모양으로 번지는지 보는 보조 진단값으로 유지된다."
    )
    if "## Latest Stage 13 Update" in text and "## 쉬운 설명" in text:
        start = text.find("## Latest Stage 13 Update")
        end = text.find("## 쉬운 설명", start)
        text = text[:start] + "## Latest Stage 13 Update(최신 Stage 13 업데이트)\n\n" + latest + "\n" + text[end:]
    io_path(CURRENT_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_or_insert_block(text: str, key: str, block: str) -> str:
    lines = text.splitlines()
    start = next((index for index, line in enumerate(lines) if line == f"{key}:"), None)
    if start is None:
        insert = next((index for index, line in enumerate(lines) if line == "stage01_raw_m5_inventory:"), len(lines))
        return "\n".join(lines[:insert] + block.rstrip().splitlines() + lines[insert:])
    end = start + 1
    while end < len(lines) and (lines[end].startswith("  ") or not lines[end].strip()):
        end += 1
    return "\n".join(lines[:start] + block.rstrip().splitlines() + lines[end:])


def upsert_line_by_token(path: Path, token: str, line: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if io_path(path).exists() else ""
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if token in existing:
            lines[index] = line.rstrip()
            io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")
            return
    io_path(path).write_text(text.rstrip() + "\n" + line.rstrip() + "\n", encoding="utf-8-sig")


def append_once(path: Path, token: str, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig")
    if token not in text:
        io_path(path).write_text(text.rstrip() + "\n" + addition, encoding="utf-8-sig")


def as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fmt(value: Any) -> str:
    number = as_float(value)
    if number is None:
        return ""
    return f"{number:.4f}".rstrip("0").rstrip(".")
