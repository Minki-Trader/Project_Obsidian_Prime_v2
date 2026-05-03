from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane.ledger import io_path, json_ready
from foundation.control_plane.mt5_tier_balance_completion import METAEDITOR_PATH_DEFAULT, TERMINAL_PATH_DEFAULT
from stage_pipelines.stage18 import catboost_followup_batch as follow
from stage_pipelines.stage18 import catboost_mt5_characteristic_probe as base


STAGE_ID = base.STAGE_ID
STAGE_NUMBER = base.STAGE_NUMBER
ROOT = base.ROOT
STAGE_ROOT = base.STAGE_ROOT
MODEL_FAMILY = base.MODEL_FAMILY
AGGREGATE_PACKET_ID = "stage18_catboost_compression_mt5_kpi_v1"
AGGREGATE_PACKET_ROOT = ROOT / "docs/agent_control/packets" / AGGREGATE_PACKET_ID


COMPRESSION_TOPICS: tuple[follow.FollowupTopic, ...] = (
    follow.FollowupTopic(
        run_id="run12N_catboost_q85_intersection_compression_probe_v1",
        run_number="run12N",
        packet_id="stage18_run12N_catboost_q85_intersection_mt5_v1",
        exploration_label="stage18_Model__CatBoostQ85IntersectionCompression",
        review_filename="run12N_catboost_q85_intersection_packet.md",
        threshold_quantile=0.85,
        builder="q85_highmargin_lowvol_mid",
        expected_attempts=2,
        expected_kpi_records=6,
        topic_read="q85_high_margin_low_vol_mid_session_intersection",
        question="Does q85 plus high probability margin plus low-volatility or mid-session membership compress drawdown without killing the CatBoost runtime characteristic?",
        boundary="catboost_stage18_compression_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_catboost_compression_mt5_runtime_probe_completed",
        judgment_blocked="blocked_catboost_compression_mt5_runtime_probe_after_attempt",
    ),
    follow.FollowupTopic(
        run_id="run12O_catboost_long_hold6_q85_compression_probe_v1",
        run_number="run12O",
        packet_id="stage18_run12O_catboost_long_hold6_q85_mt5_v1",
        exploration_label="stage18_Model__CatBoostLongHold6Q85Compression",
        review_filename="run12O_catboost_long_hold6_q85_packet.md",
        threshold_quantile=0.85,
        builder="long_hold6_q85",
        expected_attempts=2,
        expected_kpi_records=6,
        topic_read="long_only_hold6_q85_compression",
        question="Does long-only plus hold6 plus q85 make the CatBoost long bias cleaner or just more concentrated?",
        boundary="catboost_stage18_compression_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_catboost_compression_mt5_runtime_probe_completed",
        judgment_blocked="blocked_catboost_compression_mt5_runtime_probe_after_attempt",
    ),
    follow.FollowupTopic(
        run_id="run12P_catboost_plain_same_condition_rematch_probe_v1",
        run_number="run12P",
        packet_id="stage18_run12P_catboost_plain_same_condition_mt5_v1",
        exploration_label="stage18_Model__CatBoostPlainSameConditionRematch",
        review_filename="run12P_catboost_plain_same_condition_packet.md",
        threshold_quantile=0.85,
        builder="q85_highmargin_lowvol_mid",
        expected_attempts=2,
        expected_kpi_records=6,
        topic_read="plain_control_same_condition_rematch",
        question="Does Plain boosting preserve the same compressed q85 high-margin low-volatility or mid-session behavior seen in Ordered boosting?",
        variant_id=follow.PLAIN_CONTROL_VARIANT_ID,
        boundary="catboost_stage18_compression_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_catboost_compression_mt5_runtime_probe_completed",
        judgment_blocked="blocked_catboost_compression_mt5_runtime_probe_after_attempt",
    ),
)


def q85_intersection_builder(
    topic: follow.FollowupTopic,
    context: Mapping[str, Any],
    tier_a_prob: pd.DataFrame,
    tier_b_prob: pd.DataFrame,
) -> tuple[dict[str, dict[str, Any]], list[follow.SegmentAttempt]]:
    feature_matrices: dict[str, dict[str, Any]] = {}
    segments: list[follow.SegmentAttempt] = []
    for split in ("validation", "oos"):
        a_frame, b_frame, a_prob, b_prob = follow.split_frames(context, tier_a_prob, tier_b_prob, split)
        a_threshold = follow.threshold_for(a_prob, 0.85)
        b_threshold = follow.threshold_for(b_prob, 0.85)
        a_score = follow.nonflat_score(a_prob)
        b_score = follow.nonflat_score(b_prob)
        a_pass = a_score.ge(a_threshold)
        b_pass = b_score.ge(b_threshold)
        a_margin_cut = float(a_prob.loc[a_pass, "probability_margin"].astype("float64").quantile(0.70))
        b_margin_cut = float(b_prob.loc[b_pass, "probability_margin"].astype("float64").quantile(0.70))
        vol_cut = float(a_frame["historical_vol_20"].astype("float64").median())
        a_minutes = a_frame["minutes_from_cash_open"].astype("float64")
        b_minutes = b_frame["minutes_from_cash_open"].astype("float64")
        a_context_mask = (
            a_frame["historical_vol_20"].astype("float64").lt(vol_cut)
            | (a_minutes.ge(110.0) & a_minutes.lt(220.0))
        )
        b_context_mask = (
            b_frame["historical_vol_20"].astype("float64").lt(vol_cut)
            | (b_minutes.ge(110.0) & b_minutes.lt(220.0))
        )
        a_mask = (
            a_pass
            & a_prob["probability_margin"].astype("float64").ge(a_margin_cut)
            & a_context_mask
        )
        b_mask = (
            b_pass
            & b_prob["probability_margin"].astype("float64").ge(b_margin_cut)
            & b_context_mask
        )
        follow.export_filtered_pair(
            topic=topic,
            context=context,
            tier_a_prob=tier_a_prob,
            tier_b_prob=tier_b_prob,
            feature_matrices=feature_matrices,
            segments=segments,
            segment_id="q85_high_margin_low_vol_mid",
            segment_label="q85 high margin low-vol or mid-session(q85 높은 여백 저변동성 또는 중반 세션)",
            source_split=split,
            a_mask=a_mask,
            b_mask=b_mask,
            tier_a_threshold=a_threshold,
            tier_b_threshold=b_threshold,
            threshold_quantile=0.85,
            segment_filter=(
                "nonflat>=q85 and margin>=pass_q70 and "
                f"(historical_vol_20<split_median {vol_cut:.10g} or 110<=minutes_from_cash_open<220)"
            ),
        )
    return feature_matrices, segments


def long_hold6_q85_builder(
    topic: follow.FollowupTopic,
    context: Mapping[str, Any],
    tier_a_prob: pd.DataFrame,
    tier_b_prob: pd.DataFrame,
) -> tuple[dict[str, dict[str, Any]], list[follow.SegmentAttempt]]:
    feature_matrices: dict[str, dict[str, Any]] = {}
    segments: list[follow.SegmentAttempt] = []
    for split in ("validation", "oos"):
        a_frame, b_frame, a_prob, b_prob = follow.split_frames(context, tier_a_prob, tier_b_prob, split)
        follow.export_filtered_pair(
            topic=topic,
            context=context,
            tier_a_prob=tier_a_prob,
            tier_b_prob=tier_b_prob,
            feature_matrices=feature_matrices,
            segments=segments,
            segment_id="long_hold6_q85",
            segment_label="long-only hold6 q85(매수 전용 6봉 보유 q85)",
            source_split=split,
            a_mask=pd.Series(True, index=a_frame.index),
            b_mask=pd.Series(True, index=b_frame.index),
            tier_a_threshold=follow.threshold_for(a_prob, 0.85),
            tier_b_threshold=follow.threshold_for(b_prob, 0.85),
            threshold_quantile=0.85,
            max_hold_bars=6,
            direction="long_only",
            segment_filter="full split, long-only, q85 nonflat threshold, max_hold_bars=6",
        )
    return feature_matrices, segments


follow.BUILDERS.update(
    {
        "q85_highmargin_lowvol_mid": q85_intersection_builder,
        "long_hold6_q85": long_hold6_q85_builder,
    }
)


def aggregate_read(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_run = {str(summary["run_number"]): summary for summary in summaries}
    run12n = by_run.get("run12N", {})
    run12o = by_run.get("run12O", {})
    run12p = by_run.get("run12P", {})
    n_oos = (run12n.get("runtime_read", {}).get("best_oos_record") or {}) if isinstance(run12n.get("runtime_read"), Mapping) else {}
    o_oos = (run12o.get("runtime_read", {}).get("best_oos_record") or {}) if isinstance(run12o.get("runtime_read"), Mapping) else {}
    p_oos = (run12p.get("runtime_read", {}).get("best_oos_record") or {}) if isinstance(run12p.get("runtime_read"), Mapping) else {}
    ordered_net = follow.base.safe_float(n_oos.get("net_profit"))
    plain_net = follow.base.safe_float(p_oos.get("net_profit"))
    ordered_dd = follow.base.safe_float(n_oos.get("max_drawdown_percent"))
    plain_dd = follow.base.safe_float(p_oos.get("max_drawdown_percent"))
    completed = [summary for summary in summaries if summary.get("external_verification_status") == "completed"]
    all_completed = len(completed) == len(summaries)
    if all_completed and ordered_net > 0 and ordered_dd < 25.0 and ordered_net >= plain_net:
        recommendation = "stage18_can_take_one_more_attribution_pass_on_ordered_compressed_axis"
    elif all_completed and plain_net > ordered_net:
        recommendation = "ordered_specific_claim_weak_plain_control_matches_or_beats_same_condition"
    else:
        recommendation = "close_or_downgrade_stage18_after_compression_unless_user_requests_more_exploration"
    return {
        "judgment": "inconclusive_catboost_compression_mt5_kpi_completed" if all_completed else "blocked_catboost_compression_mt5_kpi_after_attempt",
        "claim_boundary": "runtime_probe_and_model_characteristic_compression_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        "completed_run_count": len(completed),
        "blocked_runs": [summary.get("run_number") for summary in summaries if summary.get("external_verification_status") != "completed"],
        "total_attempt_count": sum(int(summary.get("attempt_count") or 0) for summary in summaries),
        "total_mt5_kpi_records": sum(int(summary.get("mt5_kpi_record_count") or 0) for summary in summaries),
        "total_normalized_kpi_records": sum(int(summary.get("kpi_management", {}).get("normalized_records") or 0) for summary in summaries),
        "total_trade_attribution_records": sum(int(summary.get("kpi_management", {}).get("trade_attribution_records") or 0) for summary in summaries),
        "ordered_intersection_oos": n_oos,
        "long_hold6_q85_oos": o_oos,
        "plain_same_condition_oos": p_oos,
        "ordered_vs_plain_oos_net_delta": ordered_net - plain_net,
        "ordered_vs_plain_oos_dd_delta": ordered_dd - plain_dd,
        "recommendation": recommendation,
    }


def aggregate_markdown(summaries: Sequence[Mapping[str, Any]], read: Mapping[str, Any]) -> str:
    lines = [
        "# Stage18 CatBoost Compression MT5 KPI Batch(18단계 캣부스트 압축 MT5 KPI 배치)",
        "",
        f"- judgment(판정): `{read.get('judgment')}`",
        f"- recommendation(권고): `{read.get('recommendation')}`",
        f"- boundary(경계): `{read.get('claim_boundary')}`",
        f"- attempts(시도): `{read.get('total_attempt_count')}`",
        f"- MT5 KPI records(MT5 KPI 기록): `{read.get('total_mt5_kpi_records')}`",
        "",
        "| run(실행) | topic(주제) | OOS net/PF/trades/DD(표본 밖 순손익/수익 팩터/거래/손실폭) |",
        "|---|---|---:|",
    ]
    for summary in summaries:
        best = summary.get("runtime_read", {}).get("best_oos_record", {})
        lines.append(
            f"| `{summary.get('run_number')}` | `{summary.get('topic_read')}` | `{best.get('net_profit')} / {best.get('profit_factor')} / {best.get('trade_count')} / {best.get('max_drawdown_percent')}` |"
        )
    lines.extend(
        [
            "",
            f"- ordered vs plain OOS net delta(Ordered-Plain 표본 밖 순손익 차이): `{read.get('ordered_vs_plain_oos_net_delta')}`",
            f"- ordered vs plain OOS DD delta(Ordered-Plain 표본 밖 손실폭 차이): `{read.get('ordered_vs_plain_oos_dd_delta')}`",
            "",
            "효과(effect, 효과): 좋은 구간을 압축했을 때 CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) 특성이 위험 감소로 이어지는지, 그리고 Ordered boosting(순서형 부스팅) 고유성이 Plain boosting(Plain 부스팅) 대조군 앞에서도 남는지 확인했다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)


def write_aggregate_packet(summaries: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    read = aggregate_read(summaries)
    io_path(AGGREGATE_PACKET_ROOT).mkdir(parents=True, exist_ok=True)
    base.write_json(
        AGGREGATE_PACKET_ROOT / "aggregate_summary.json",
        {"packet_id": AGGREGATE_PACKET_ID, "created_at_utc": created_at, "run_summaries": list(summaries), "aggregate_read": read},
    )
    base.write_json(
        AGGREGATE_PACKET_ROOT / "artifact_index.json",
        {
            "run_summary_paths": [base.rel(STAGE_ROOT / "02_runs" / str(summary["run_id"]) / "summary.json") for summary in summaries],
            "report_path": base.rel(STAGE_ROOT / "03_reviews/stage18_catboost_compression_mt5_kpi_packet.md"),
            "created_at_utc": created_at,
        },
    )
    all_completed = not read.get("blocked_runs")
    common_payloads = {
        "performance_attribution_audit": {
            "audit_name": "performance_attribution_audit",
            "status": "pass" if all_completed else "blocked",
            "passed": all_completed,
            "observed_change": "Compressed q85/high-margin/low-vol-or-mid-session and long-hold6-q85 probes were compared against a plain same-condition control.",
            "comparison_baseline": "run12D-run12M follow-up segments, especially q85, high-margin, low-vol, mid-session, hold6, and plain control reads.",
            "attribution_confidence": "diagnostic_runtime_probe",
            "aggregate_read": read,
        },
        "result_judgment_audit": {
            "audit_name": "result_judgment_audit",
            "status": "pass" if all_completed else "blocked",
            "passed": all_completed,
            "judgment_label": read["judgment"],
            "claim_boundary": read["claim_boundary"],
        },
        "final_claim_guard": {
            "audit_name": "final_claim_guard",
            "status": "pass" if all_completed else "blocked",
            "passed": all_completed,
            "allowed_claims": [read["judgment"], "runtime_probe", "model_characteristic_compression_read"],
            "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        "required_gate_coverage_audit": {
            "audit_name": "required_gate_coverage_audit",
            "status": "pass" if all_completed else "blocked",
            "passed": all_completed,
            "required_gates": {
                "runtime_evidence_gate": "pass" if all_completed else "blocked",
                "scope_completion_gate": "pass" if len(summaries) == len(COMPRESSION_TOPICS) else "blocked",
                "kpi_contract_audit": "pass" if all_completed else "blocked",
                "performance_attribution_audit": "pass" if all_completed else "blocked",
                "result_judgment_audit": "pass" if all_completed else "blocked",
                "final_claim_guard": "pass" if all_completed else "blocked",
            },
        },
    }
    for name, payload in common_payloads.items():
        base.write_json(AGGREGATE_PACKET_ROOT / f"{name}.json", payload)
    base.write_md(STAGE_ROOT / "03_reviews/stage18_catboost_compression_mt5_kpi_packet.md", aggregate_markdown(summaries, read))
    return read


def sync_stage18_docs(summaries: Sequence[Mapping[str, Any]], aggregate: Mapping[str, Any]) -> None:
    latest = summaries[-1]
    status = "reviewed_run12N_run12P_catboost_compression_mt5_kpi"
    state_path = ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    state = state.replace("current_run_id: run12M_catboost_threshold_surface_probe_v1", f"current_run_id: {latest.get('run_id')}", 1)
    block = f"""stage18_catboost_compression_mt5_kpi:
  stage_id: {STAGE_ID}
  status: {status}
  lane: independent_model_family_topic_pivot_no_promotion
  model_family: {MODEL_FAMILY}
  current_run_id: {latest.get('run_id')}
  run_range: run12N-run12P
  completed_run_count: {aggregate.get('completed_run_count')}
  blocked_runs: {','.join(aggregate.get('blocked_runs') or []) or 'none'}
  mt5_attempt_count: {aggregate.get('total_attempt_count')}
  mt5_kpi_record_count: {aggregate.get('total_mt5_kpi_records')}
  normalized_kpi_record_count: {aggregate.get('total_normalized_kpi_records')}
  trade_attribution_records: {aggregate.get('total_trade_attribution_records')}
  ordered_vs_plain_oos_net_delta: {aggregate.get('ordered_vs_plain_oos_net_delta')}
  ordered_vs_plain_oos_dd_delta: {aggregate.get('ordered_vs_plain_oos_dd_delta')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {aggregate.get('claim_boundary')}
  aggregate_packet_path: {base.rel(STAGE_ROOT / '03_reviews/stage18_catboost_compression_mt5_kpi_packet.md')}
  packet_summary_path: docs/agent_control/packets/{AGGREGATE_PACKET_ID}/aggregate_summary.json
  next_action: {aggregate.get('recommendation')}
"""
    state = base.replace_top_level_yaml_block(state, "stage18_catboost_compression_mt5_kpi:", block)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")

    review_path = STAGE_ROOT / "03_reviews/review_index.md"
    review = io_path(review_path).read_text(encoding="utf-8-sig")
    insert = "\n".join(
        [
            "- compression aggregate packet(압축 종합 묶음): `stages/18_model_family_challenge__catboost_ordered_boosting_scout/03_reviews/stage18_catboost_compression_mt5_kpi_packet.md`",
            *[
                f"- `{summary.get('run_id')}`: `{summary.get('closure_judgment')}`, report(보고서): `stages/18_model_family_challenge__catboost_ordered_boosting_scout/03_reviews/{COMPRESSION_TOPICS[index].review_filename}`"
                for index, summary in enumerate(summaries)
            ],
        ]
    )
    if "stage18_catboost_compression_mt5_kpi_packet.md" not in review:
        review = review.rstrip() + "\n" + insert + "\n"
        io_path(review_path).write_text(review, encoding="utf-8-sig")

    selection_path = STAGE_ROOT / "04_selected/selection_status.md"
    base.write_md(
        selection_path,
        "\n".join(
            [
                "# Stage18 Selection Status(18단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                f"- status(상태): `{status}`",
                f"- current run(현재 실행): `{latest.get('run_id')}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{aggregate.get('judgment')}`",
                f"- recommendation(권고): `{aggregate.get('recommendation')}`",
                f"- boundary(경계): `{aggregate.get('claim_boundary')}`",
                "",
                "효과(effect, 효과): Stage18(18단계)은 압축 실험 run12N-run12P(실행12N-실행12P)까지 MT5(`MetaTrader 5`, 메타트레이더5) KPI(`Key Performance Indicator`, 핵심 성과 지표)로 닫았지만, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            ]
        ),
    )

    current_path = ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    insert_current = "\n".join(
        [
            "## Latest Stage18 RUN12N-RUN12P Update(최신 18단계 실행12N-실행12P 업데이트)",
            "",
            "Stage18(18단계) CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) 압축 실험 3개를 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)까지 연결했다.",
            "",
            f"효과(effect, 효과): `{aggregate.get('judgment')}`로 기록했다. claim boundary(주장 경계)는 runtime_probe(런타임 탐침)와 model characteristic compression read(모델 특성 압축 판독)뿐이다.",
            "",
        ]
    )
    if "## Latest Stage18 RUN12N-RUN12P Update" not in current:
        current = insert_current + current
        io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")

    changelog_path = ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = f"- 2026-05-03: Stage18(18단계) `run12N-run12P` CatBoost(캣부스트) 압축 MT5 KPI 배치를 완료했다. 효과(effect, 효과): q85/high-margin/low-vol-or-mid-session 압축, long-only hold6 q85, Plain control(Plain 대조군) 재대결을 `{aggregate.get('judgment')}`로 판정했다.\n"
    if line not in changelog:
        io_path(changelog_path).write_text(changelog.rstrip() + "\n" + line, encoding="utf-8-sig")


def build_all(args: argparse.Namespace) -> dict[str, Any]:
    created_at = base.utc_now()
    context = base.load_context()
    specs = follow.variant_map()
    summaries = [
        follow.build_topic_run(topic, args, context, specs[topic.variant_id], created_at)
        for topic in COMPRESSION_TOPICS
    ]
    aggregate = write_aggregate_packet(summaries, created_at)
    sync_stage18_docs(summaries, aggregate)
    payload = {"aggregate": aggregate, "summaries": summaries}
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2))
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage18 CatBoost compression MT5 KPI batch.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--materialize-only", action="store_true")
    args = parser.parse_args(argv)
    build_all(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
