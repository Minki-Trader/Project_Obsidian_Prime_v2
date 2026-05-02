from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean, median
from typing import Any, Callable, Mapping, Sequence

from foundation.control_plane.alpha_run_ledgers import materialize_alpha_ledgers
from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, io_path, json_ready, ledger_pairs, sha256_file_lf_normalized, upsert_csv_rows


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_ID = "run04J_mlp_probability_geometry_probe_v1"
PACKET_ID = "stage13_run04J_mlp_probability_geometry_probe_packet_v1"
SOURCE_RUN_ID = "run04F_mlp_direction_asymmetry_runtime_probe_v1"
EXPLORATION_LABEL = "stage13_MLPDirection__ProbabilityGeometry"
BOUNDARY = "probability_geometry_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = RUN_ROOT / "packet"
REPORT_PATH = STAGE_ROOT / "03_reviews/run04J_mlp_probability_geometry_probe_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage13_mlp_probability_geometry_probe.md"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
COMMON_FILES_ROOT = Path.home() / "AppData" / "Roaming" / "MetaQuotes" / "Terminal" / "Common" / "Files"

PROB_COLUMNS = ("split", "metric", "count", "mean", "std", "min", "p05", "p10", "p25", "p50", "p75", "p90", "p95", "max")
CLASS_COLUMNS = ("split", "top_class", "count", "share")
SIGNAL_COLUMNS = ("split", "decision", "count", "share", "mean_entropy_norm", "mean_margin", "mean_p_short", "mean_p_flat", "mean_p_long")
CLUSTER_COLUMNS = ("split", "scope", "signal_count", "cluster_count", "mean_cluster_len", "median_cluster_len", "max_cluster_len", "singleton_cluster_share", "top5_cluster_share", "active_signal_days", "top5_day_share", "max_month_share", "interpretation")
MONTH_COLUMNS = ("split", "month", "bar_count", "signal_count", "long_count", "short_count", "signal_share", "signal_month_share")
STABILITY_COLUMNS = ("metric", "validation_mean", "oos_mean", "mean_delta_oos_minus_validation", "validation_p50", "oos_p50", "p50_delta_oos_minus_validation", "validation_p90", "oos_p90", "p90_delta_oos_minus_validation", "psi_10bin", "interpretation")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.6g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(json_ready(value))


def source_manifest() -> dict[str, Any]:
    return read_json(SOURCE_ROOT / "run_manifest.json")


def source_threshold() -> dict[str, Any]:
    threshold = read_json(SOURCE_ROOT / "thresholds/threshold_handoff.json")
    return {
        "source_run_id": SOURCE_RUN_ID,
        "threshold_id": threshold.get("threshold_id", "q90_m000"),
        "tier_a_threshold": float(threshold["tier_a_threshold"]),
        "min_margin": float(threshold.get("min_margin", 0.0)),
        "threshold_policy": "RUN04F q90 threshold reused for probability geometry analysis without optimization",
        "boundary": "shape_analysis_only_not_selected_threshold",
    }


def both_telemetry_paths(manifest: Mapping[str, Any]) -> dict[str, Path]:
    paths = {}
    for attempt in manifest["attempts"]:
        if "both_no_fallback" in str(attempt["attempt_name"]):
            paths[str(attempt["split"])] = COMMON_FILES_ROOT / str(attempt["common_telemetry_path"])
    return paths


def read_telemetry(split: str, path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        for raw in reader:
            if len(raw) < len(header):
                raw = raw + [""] * (len(header) - len(raw))
            row = dict(zip(header, raw[: len(header)]))
            if row.get("record_type") != "cycle":
                continue
            ps = [float(row["p_short"]), float(row["p_flat"]), float(row["p_long"])]
            ordered = sorted(ps, reverse=True)
            entropy = -sum(value * math.log(max(value, 1.0e-12)) for value in ps) / math.log(3.0)
            top_class = ("short", "flat", "long")[ps.index(max(ps))]
            rows.append(
                {
                    "split": split,
                    "bar_time": row["bar_time"],
                    "month": row["bar_time"][:7],
                    "day": row["bar_time"][:10],
                    "p_short": ps[0],
                    "p_flat": ps[1],
                    "p_long": ps[2],
                    "entropy_norm": entropy,
                    "margin": ordered[0] - ordered[1],
                    "top_class": top_class,
                    "decision": row["decision"],
                }
            )
    return rows


def probability_rows(rows_by_split: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    out = []
    for split, rows in rows_by_split.items():
        for metric in ("p_short", "p_flat", "p_long", "entropy_norm", "margin"):
            out.append({"split": split, "metric": metric, **stats([float(row[metric]) for row in rows])})
    return out


def top_class_rows(rows_by_split: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    out = []
    for split, rows in rows_by_split.items():
        counts = Counter(str(row["top_class"]) for row in rows)
        total = len(rows)
        for key in ("short", "flat", "long"):
            out.append({"split": split, "top_class": key, "count": counts.get(key, 0), "share": safe_div(counts.get(key, 0), total)})
    return out


def signal_rows(rows_by_split: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    out = []
    for split, rows in rows_by_split.items():
        total = len(rows)
        for decision in ("flat", "long", "short", "signal_total"):
            selected = [row for row in rows if row["decision"] != "flat"] if decision == "signal_total" else [row for row in rows if row["decision"] == decision]
            out.append(
                {
                    "split": split,
                    "decision": decision,
                    "count": len(selected),
                    "share": safe_div(len(selected), total),
                    "mean_entropy_norm": mean_or_none([float(row["entropy_norm"]) for row in selected]),
                    "mean_margin": mean_or_none([float(row["margin"]) for row in selected]),
                    "mean_p_short": mean_or_none([float(row["p_short"]) for row in selected]),
                    "mean_p_flat": mean_or_none([float(row["p_flat"]) for row in selected]),
                    "mean_p_long": mean_or_none([float(row["p_long"]) for row in selected]),
                }
            )
    return out


def cluster_summary_rows(rows_by_split: Mapping[str, Sequence[Mapping[str, Any]]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    summaries = []
    details = []
    scopes: tuple[tuple[str, Callable[[Mapping[str, Any]], bool]], ...] = (
        ("any_q90_signal", lambda row: row["decision"] != "flat"),
        ("long_q90_signal", lambda row: row["decision"] == "long"),
        ("short_q90_signal", lambda row: row["decision"] == "short"),
    )
    for split, rows in rows_by_split.items():
        for scope, predicate in scopes:
            clusters = find_clusters(rows, predicate)
            summaries.append(cluster_summary(split, scope, rows, clusters))
            for index, cluster in enumerate(clusters, start=1):
                details.append({"split": split, "scope": scope, "cluster_index": index, "start": cluster[0]["bar_time"], "end": cluster[-1]["bar_time"], "length": len(cluster), "dominant_decision": Counter(row["decision"] for row in cluster).most_common(1)[0][0]})
    return summaries, details


def monthly_signal_rows(rows_by_split: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    out = []
    for split, rows in rows_by_split.items():
        total_signal = sum(1 for row in rows if row["decision"] != "flat")
        months = sorted(set(str(row["month"]) for row in rows))
        for month in months:
            month_rows = [row for row in rows if row["month"] == month]
            signals = [row for row in month_rows if row["decision"] != "flat"]
            out.append({"split": split, "month": month, "bar_count": len(month_rows), "signal_count": len(signals), "long_count": sum(1 for row in signals if row["decision"] == "long"), "short_count": sum(1 for row in signals if row["decision"] == "short"), "signal_share": safe_div(len(signals), len(month_rows)), "signal_month_share": safe_div(len(signals), total_signal)})
    return out


def stability_rows(rows_by_split: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    validation = rows_by_split["validation_is"]
    oos = rows_by_split["oos"]
    out = []
    for metric in ("p_short", "p_flat", "p_long", "entropy_norm", "margin"):
        left = [float(row[metric]) for row in validation]
        right = [float(row[metric]) for row in oos]
        left_stats = stats(left)
        right_stats = stats(right)
        psi = psi_10bin(left, right)
        mean_delta = right_stats["mean"] - left_stats["mean"]
        out.append({"metric": metric, "validation_mean": left_stats["mean"], "oos_mean": right_stats["mean"], "mean_delta_oos_minus_validation": mean_delta, "validation_p50": left_stats["p50"], "oos_p50": right_stats["p50"], "p50_delta_oos_minus_validation": right_stats["p50"] - left_stats["p50"], "validation_p90": left_stats["p90"], "oos_p90": right_stats["p90"], "p90_delta_oos_minus_validation": right_stats["p90"] - left_stats["p90"], "psi_10bin": psi, "interpretation": stability_interpretation(metric, mean_delta, psi)})
    return out


def find_clusters(rows: Sequence[Mapping[str, Any]], predicate: Callable[[Mapping[str, Any]], bool]) -> list[list[Mapping[str, Any]]]:
    clusters: list[list[Mapping[str, Any]]] = []
    current: list[Mapping[str, Any]] = []
    for row in rows:
        if predicate(row):
            current.append(row)
            continue
        if current:
            clusters.append(current)
            current = []
    if current:
        clusters.append(current)
    return clusters


def cluster_summary(split: str, scope: str, rows: Sequence[Mapping[str, Any]], clusters: Sequence[Sequence[Mapping[str, Any]]]) -> dict[str, Any]:
    lengths = [len(cluster) for cluster in clusters]
    signal_count = sum(lengths)
    days = Counter(row["day"] for row in rows if signal_scope_match(scope, row))
    months = Counter(row["month"] for row in rows if signal_scope_match(scope, row))
    top5_cluster_share = safe_div(sum(sorted(lengths, reverse=True)[:5]), signal_count)
    top5_day_share = safe_div(sum(count for _, count in days.most_common(5)), signal_count)
    max_month_share = safe_div(max(months.values()) if months else 0, signal_count)
    return {
        "split": split,
        "scope": scope,
        "signal_count": signal_count,
        "cluster_count": len(clusters),
        "mean_cluster_len": mean_or_none(lengths),
        "median_cluster_len": median(lengths) if lengths else None,
        "max_cluster_len": max(lengths) if lengths else 0,
        "singleton_cluster_share": safe_div(sum(1 for value in lengths if value == 1), len(lengths)),
        "top5_cluster_share": top5_cluster_share,
        "active_signal_days": len(days),
        "top5_day_share": top5_day_share,
        "max_month_share": max_month_share,
        "interpretation": cluster_interpretation(top5_cluster_share, max_month_share, max(lengths) if lengths else 0),
    }


def signal_scope_match(scope: str, row: Mapping[str, Any]) -> bool:
    if scope == "any_q90_signal":
        return row["decision"] != "flat"
    if scope == "long_q90_signal":
        return row["decision"] == "long"
    if scope == "short_q90_signal":
        return row["decision"] == "short"
    return False


def build_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    rows = [scope_row("Tier B", "tier_b_out_of_scope"), scope_row("Tier A+B", "tier_abb_out_of_scope")]
    signal_by_split = {(row["split"], row["decision"]): row for row in summary["signal_summary"]}
    cluster_by_split = {(row["split"], row["scope"]): row for row in summary["q90_cluster_summary"]}
    prob_by_split = {(row["split"], row["metric"]): row for row in summary["probability_distribution"]}
    for split in ("validation_is", "oos"):
        signal = signal_by_split[(split, "signal_total")]
        entropy = prob_by_split[(split, "entropy_norm")]
        margin = prob_by_split[(split, "margin")]
        cluster = cluster_by_split[(split, "any_q90_signal")]
        rows.append({"ledger_row_id": f"{RUN_ID}__probability_shape_{split}", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": f"probability_shape_{split}", "parent_run_id": SOURCE_RUN_ID, "record_view": f"probability_shape_{split}", "tier_scope": "Tier A", "kpi_scope": "probability_geometry", "scoreboard_lane": "structural_scout", "status": "completed", "judgment": "inconclusive_probability_geometry_probe_completed", "path": rel(RUN_ROOT / "probability_distribution_summary.csv"), "primary_kpi": ledger_pairs((("signals", signal["count"]), ("signal_share", signal["share"]), ("entropy_mean", entropy["mean"]), ("margin_mean", margin["mean"]))), "guardrail_kpi": ledger_pairs((("max_cluster", cluster["max_cluster_len"]), ("top5_cluster_share", cluster["top5_cluster_share"]), ("boundary", "shape_only"))), "external_verification_status": "completed_from_existing_mt5_telemetry", "notes": "RUN04J analyzes RUN04F Tier A both-direction MT5 runtime probabilities."})
    stability = {row["metric"]: row for row in summary["split_stability"]}
    rows.append({"ledger_row_id": f"{RUN_ID}__split_stability", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": "split_stability", "parent_run_id": SOURCE_RUN_ID, "record_view": "split_stability", "tier_scope": "Tier A", "kpi_scope": "probability_split_stability", "scoreboard_lane": "structural_scout", "status": "completed", "judgment": summary["judgment"], "path": rel(RUN_ROOT / "split_stability_summary.csv"), "primary_kpi": ledger_pairs((("p_long_mean_delta", stability["p_long"]["mean_delta_oos_minus_validation"]), ("p_short_mean_delta", stability["p_short"]["mean_delta_oos_minus_validation"]), ("entropy_delta", stability["entropy_norm"]["mean_delta_oos_minus_validation"]))), "guardrail_kpi": ledger_pairs((("margin_delta", stability["margin"]["mean_delta_oos_minus_validation"]), ("boundary", "no_alpha_quality"))), "external_verification_status": "completed_from_existing_mt5_telemetry", "notes": "Validation/OOS probability geometry comparison without new threshold selection."})
    ledger_outputs = materialize_alpha_ledgers(stage_run_ledger_path=STAGE_LEDGER_PATH, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=rows)
    registry_output = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "probability_geometry_probe", "status": "reviewed", "judgment": summary["judgment"], "path": rel(RUN_ROOT), "notes": ledger_pairs((("source_run", SOURCE_RUN_ID), ("threshold_id", summary["threshold"]["threshold_id"]), ("boundary", "probability_geometry_only"), ("recommendation", summary["recommendation"]))) }], key="run_id")
    return {"ledger_outputs": ledger_outputs, "run_registry_output": registry_output}


def scope_row(tier_scope: str, suffix: str) -> dict[str, Any]:
    return {"ledger_row_id": f"{RUN_ID}__{suffix}", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": suffix, "parent_run_id": SOURCE_RUN_ID, "record_view": suffix, "tier_scope": tier_scope, "kpi_scope": "claim_scope_boundary", "scoreboard_lane": "structural_scout", "status": "completed", "judgment": "out_of_scope_by_claim_probability_geometry_probe", "path": rel(RUN_ROOT / "summary.json"), "primary_kpi": ledger_pairs((("source_run", SOURCE_RUN_ID),)), "guardrail_kpi": ledger_pairs((("boundary", "tier_a_probability_geometry_only"),)), "external_verification_status": "out_of_scope_by_claim", "notes": "RUN04J uses Tier A both-direction RUN04F telemetry only."}


def build_summary(created_at: str) -> dict[str, Any]:
    manifest = source_manifest()
    paths = both_telemetry_paths(manifest)
    rows_by_split = {split: read_telemetry(split, path) for split, path in paths.items()}
    probability = probability_rows(rows_by_split)
    top_class = top_class_rows(rows_by_split)
    signals = signal_rows(rows_by_split)
    clusters, cluster_details = cluster_summary_rows(rows_by_split)
    monthly = monthly_signal_rows(rows_by_split)
    stability = stability_rows(rows_by_split)
    threshold = source_threshold()
    judgment, recommendation = judge(probability, signals, clusters, stability)
    summary = {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "exploration_label": EXPLORATION_LABEL,
        "status": "completed",
        "external_verification_status": "completed_from_existing_mt5_telemetry",
        "judgment": judgment,
        "recommendation": recommendation,
        "boundary": BOUNDARY,
        "threshold": threshold,
        "source_telemetry": {split: {"path": path.as_posix(), "sha256": sha256_file_lf_normalized(path), "rows": len(rows_by_split[split])} for split, path in paths.items()},
        "probability_distribution": probability,
        "top_class_distribution": top_class,
        "signal_summary": signals,
        "q90_cluster_summary": clusters,
        "q90_cluster_details": cluster_details,
        "monthly_signal_concentration": monthly,
        "split_stability": stability,
    }
    summary["ledger_outputs"] = build_ledgers(summary)
    write_outputs(summary)
    return summary


def write_outputs(summary: Mapping[str, Any]) -> None:
    write_csv(RUN_ROOT / "probability_distribution_summary.csv", PROB_COLUMNS, summary["probability_distribution"])
    write_csv(RUN_ROOT / "top_class_distribution.csv", CLASS_COLUMNS, summary["top_class_distribution"])
    write_csv(RUN_ROOT / "signal_summary.csv", SIGNAL_COLUMNS, summary["signal_summary"])
    write_csv(RUN_ROOT / "q90_signal_cluster_summary.csv", CLUSTER_COLUMNS, summary["q90_cluster_summary"])
    write_csv(RUN_ROOT / "q90_signal_cluster_details.csv", ("split", "scope", "cluster_index", "start", "end", "length", "dominant_decision"), summary["q90_cluster_details"])
    write_csv(RUN_ROOT / "monthly_signal_concentration.csv", MONTH_COLUMNS, summary["monthly_signal_concentration"])
    write_csv(RUN_ROOT / "split_stability_summary.csv", STABILITY_COLUMNS, summary["split_stability"])
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(RUN_ROOT / "kpi_record.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_json(PACKET_ROOT / "skill_receipts.json", skill_receipts(summary))
    write_json(PACKET_ROOT / "command_result.json", {"run_id": RUN_ID, "summary": summary})
    write_md(PACKET_ROOT / "work_packet.md", work_packet_markdown())
    report = report_markdown(summary)
    write_md(RUN_ROOT / "reports/result_summary.md", report)
    write_md(REPORT_PATH, report)
    write_md(DECISION_PATH, decision_markdown(summary))
    sync_docs(summary)


def run_manifest(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {"run_id": RUN_ID, "packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_number": "run04J", "source_run_id": SOURCE_RUN_ID, "model_family": "sklearn_mlpclassifier_probability_geometry_probe", "exploration_label": EXPLORATION_LABEL, "stage_inheritance": "independent_no_stage10_11_12_run_baseline_seed_or_reference", "boundary": BOUNDARY, "inputs": {"source_run_manifest": rel(SOURCE_ROOT / "run_manifest.json"), "source_telemetry": summary["source_telemetry"]}, "outputs": {"summary": rel(RUN_ROOT / "summary.json"), "probability_distribution": rel(RUN_ROOT / "probability_distribution_summary.csv"), "q90_clusters": rel(RUN_ROOT / "q90_signal_cluster_summary.csv"), "split_stability": rel(RUN_ROOT / "split_stability_summary.csv"), "report": rel(REPORT_PATH)}}


def report_markdown(summary: Mapping[str, Any]) -> str:
    signal = {(row["split"], row["decision"]): row for row in summary["signal_summary"]}
    prob = {(row["split"], row["metric"]): row for row in summary["probability_distribution"]}
    clusters = {(row["split"], row["scope"]): row for row in summary["q90_cluster_summary"]}
    stability = {row["metric"]: row for row in summary["split_stability"]}
    lines = [
        f"# {RUN_ID} 결과 요약(Result Summary, 결과 요약)",
        "",
        "- status(상태): `completed(완료)`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- recommendation(추천): `{summary['recommendation']}`",
        f"- source run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "## 핵심 판독(Core Read, 핵심 판독)",
        "",
        f"- validation(검증) q90 signal(상위 10% 신호): `{signal[('validation_is', 'signal_total')]['count']}` / share(비중) `{signal[('validation_is', 'signal_total')]['share']:.3f}`.",
        f"- OOS(표본외) q90 signal(상위 10% 신호): `{signal[('oos', 'signal_total')]['count']}` / share(비중) `{signal[('oos', 'signal_total')]['share']:.3f}`.",
        f"- entropy mean(평균 엔트로피): validation(검증) `{prob[('validation_is', 'entropy_norm')]['mean']:.3f}`, OOS(표본외) `{prob[('oos', 'entropy_norm')]['mean']:.3f}`.",
        f"- margin mean(평균 마진): validation(검증) `{prob[('validation_is', 'margin')]['mean']:.3f}`, OOS(표본외) `{prob[('oos', 'margin')]['mean']:.3f}`.",
        f"- p_long mean delta(매수 확률 평균 차이, OOS-validation): `{stability['p_long']['mean_delta_oos_minus_validation']:.3f}`.",
        f"- p_short mean delta(매도 확률 평균 차이, OOS-validation): `{stability['p_short']['mean_delta_oos_minus_validation']:.3f}`.",
        "",
        "효과(effect, 효과): 확률 모양은 validation/OOS(검증/표본외) 사이에서 크게 무너지지는 않았지만, entropy(엔트로피)가 높고 margin(마진)이 낮아 q90 signal(상위 10% 신호)이 강한 확신보다는 얇은 tail(꼬리) 신호에 가깝다.",
        "",
        "## q90 Clustering(q90 군집)",
        "",
        "| split(분할) | signals(신호) | clusters(군집) | max cluster(최대 군집) | top5 cluster share(상위5 군집 비중) | max month share(최대 월 비중) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for split in ("validation_is", "oos"):
        row = clusters[(split, "any_q90_signal")]
        lines.append(f"| {split} | {row['signal_count']} | {row['cluster_count']} | {row['max_cluster_len']} | {row['top5_cluster_share']:.3f} | {row['max_month_share']:.3f} |")
    lines.extend(["", "## Split Stability(분할 안정성)", "", "| metric(지표) | validation mean(검증 평균) | OOS mean(표본외 평균) | delta(차이) | PSI(모집단 안정성 지수) |", "|---|---:|---:|---:|---:|"])
    for metric in ("p_short", "p_flat", "p_long", "entropy_norm", "margin"):
        row = stability[metric]
        lines.append(f"| {metric} | {row['validation_mean']:.3f} | {row['oos_mean']:.3f} | {row['mean_delta_oos_minus_validation']:.3f} | {row['psi_10bin']:.3f} |")
    lines.extend(["", "효과(effect, 효과): 이 결과는 probability geometry(확률 기하) 판독일 뿐이고, alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다."])
    return "\n".join(lines)


def decision_markdown(summary: Mapping[str, Any]) -> str:
    return "\n".join(["# 2026-05-02 Stage13 MLP Probability Geometry Probe", "", f"- run(실행): `{RUN_ID}`", f"- source(원천): `{SOURCE_RUN_ID}`", f"- judgment(판정): `{summary['judgment']}`", f"- recommendation(추천): `{summary['recommendation']}`", f"- boundary(경계): `{BOUNDARY}`", "", "효과(effect, 효과): Stage13(13단계)에서 같은 q90 probability geometry(q90 확률 기하)를 계속 깊게 파기보다, hidden activation(은닉층 활성화)이나 feature sensitivity(피처 민감도) 같은 새 내부 주제로 넘어가는 근거를 남긴다."])


def work_packet_markdown() -> str:
    return "\n".join([f"# {PACKET_ID}", "", "- primary_family(주 작업군): `model_validation(모델 검증)`", "- primary_skill(주 스킬): `obsidian-model-validation(모델 검증)`", "- hypothesis(가설): MLP(다층 퍼셉트론)의 q90 signal(상위 10% 신호)은 validation/OOS(검증/표본외)에서 형태가 유지되지만, high entropy(높은 엔트로피)와 low margin(낮은 마진) 때문에 약한 tail signal(꼬리 신호)일 수 있다.", "- evidence_plan(근거 계획): RUN04F(실행 04F) MT5 telemetry(원격측정) 확률, q90 clustering(q90 군집), split stability(분할 안정성).", f"- boundary(경계): `{BOUNDARY}`", "", "효과(effect, 효과): 새 MT5(메타트레이더5) 실행 없이 모델 확률 표면만 재분석한다."])


def skill_receipts(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"packet_id": PACKET_ID, "skill": "obsidian-experiment-design", "status": "completed", "hypothesis": "RUN04F MLP probability surface is stable enough to inspect but may be high-entropy low-margin.", "baseline": "RUN04F Tier A both-direction telemetry under q90 threshold.", "changed_variables": ["analysis only; no model, threshold, or MT5 policy change"], "invalid_conditions": ["missing telemetry", "probability columns malformed", "split mismatch"], "evidence_plan": [rel(RUN_ROOT / "probability_distribution_summary.csv"), rel(RUN_ROOT / "q90_signal_cluster_summary.csv"), rel(RUN_ROOT / "split_stability_summary.csv")]},
        {"packet_id": PACKET_ID, "skill": "obsidian-model-validation", "status": "completed", "model_or_threshold_surface": "RUN04F MLPClassifier and fixed q90 threshold; no selection.", "validation_split": "split_v1 validation/OOS", "overfit_checks": "Validation/OOS probability geometry comparison and q90 concentration check.", "selection_metric_boundary": "No model or threshold selected; shape-only probe.", "allowed_claims": ["probability_geometry_read"], "forbidden_claims": ["alpha_quality", "baseline", "promotion", "runtime_authority"]},
        {"packet_id": PACKET_ID, "skill": "obsidian-data-integrity", "status": "completed", "data_sources_checked": [str(item["path"]) for item in summary["source_telemetry"].values()], "time_axis_boundary": "RUN04F MT5 closed-bar telemetry order; broker timestamp as emitted by runtime.", "split_boundary": "validation_is and oos from RUN04F attempts.", "leakage_checks": "No retraining, no threshold search, no label use in this analysis.", "missing_data_boundary": "Tier B and Tier A+B out_of_scope_by_claim.", "allowed_claims": ["telemetry_shape_analysis"], "forbidden_claims": ["data_quality_certification"]},
        {"packet_id": PACKET_ID, "skill": "obsidian-performance-attribution", "status": "completed", "attribution_layers_checked": ["probability_distribution", "entropy", "margin", "q90_signal_clustering", "validation_oos_stability"], "missing_layers": ["trade PnL attribution repeated here", "regime labels", "WFO"], "allowed_claims": ["probability_shape_attribution"], "forbidden_claims": ["alpha_quality", "promotion", "runtime_authority"]},
        {"packet_id": PACKET_ID, "skill": "obsidian-artifact-lineage", "status": "completed", "source_inputs": [rel(SOURCE_ROOT / "run_manifest.json"), rel(SOURCE_ROOT / "thresholds/threshold_handoff.json")], "produced_artifacts": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "probability_distribution_summary.csv"), rel(REPORT_PATH)], "raw_evidence": [value["path"] for value in summary["source_telemetry"].values()], "machine_readable": [rel(RUN_ROOT / "kpi_record.json"), rel(RUN_ROOT / "split_stability_summary.csv")], "human_readable": [rel(REPORT_PATH), rel(DECISION_PATH)], "hashes_or_missing_reasons": "Telemetry SHA256 recorded in summary.json.", "lineage_boundary": BOUNDARY},
        {"packet_id": PACKET_ID, "skill": "obsidian-result-judgment", "status": "completed", "judgment_boundary": summary["judgment"], "allowed_claims": ["stage13_probability_geometry_probe_completed"], "forbidden_claims": ["alpha_quality", "baseline", "promotion", "runtime_authority"], "evidence_used": [rel(RUN_ROOT / "probability_distribution_summary.csv"), rel(RUN_ROOT / "q90_signal_cluster_summary.csv"), rel(RUN_ROOT / "split_stability_summary.csv")]},
    ]


def sync_docs(summary: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = state.replace("active_run04I_mlp_reversal_policy_runtime_probe", "active_run04J_mlp_probability_geometry_probe")
    block = ("stage13_mlp_probability_geometry_probe:\n" f"  run_id: {RUN_ID}\n" "  status: completed\n" f"  judgment: {summary['judgment']}\n" f"  recommendation: {summary['recommendation']}\n" f"  boundary: {BOUNDARY}\n" f"  source_run_id: {SOURCE_RUN_ID}\n" f"  report_path: {rel(REPORT_PATH)}\n")
    if "stage13_mlp_probability_geometry_probe:" not in state:
        state = state.replace("stage01_raw_m5_inventory:\n", block + "stage01_raw_m5_inventory:\n")
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8")

    current = io_path(CURRENT_STATE_PATH).read_text(encoding="utf-8-sig")
    current = current.replace("current run(현재 실행): `run04I_mlp_reversal_policy_runtime_probe_v1`", f"current run(현재 실행): `{RUN_ID}`")
    latest = f"Stage13(13단계)의 현재 실행(current run, 현재 실행)은 `{RUN_ID}`이고, RUN04F(실행 04F) MT5 telemetry(원격측정)의 probability geometry(확률 기하)를 분석했다.\n\n효과(effect, 효과): entropy(엔트로피), margin(마진), q90 signal clustering(q90 신호 군집), validation/OOS stability(검증/표본외 안정성)를 보고 다음 방향을 `{summary['recommendation']}`로 낮춰 판정했다."
    marker = "## 쉬운 설명(Plain Read, 쉬운 설명)"
    if marker in current and "## Latest Stage 13 Update" in current:
        head = current.split("## Latest Stage 13 Update", 1)[0]
        after = current.split(marker, 1)[1]
        current = head + "## Latest Stage 13 Update(최신 Stage 13 업데이트)\n\n" + latest + "\n" + marker + after
    io_path(CURRENT_STATE_PATH).write_text(current, encoding="utf-8-sig")

    write_md(SELECTION_STATUS_PATH, "\n".join(["# Stage 13 Selection Status", "", "## Current Read(현재 판독)", "", f"- stage(단계): `{STAGE_ID}`", "- status(상태): `reviewed_probability_geometry_probe_completed(확률 기하 탐침 검토 완료)`", "- model family(모델 계열): `MLPClassifier(다층 퍼셉트론 분류기)`", "- exploration depth(탐색 깊이): `probability_geometry_only(확률 기하만)`", f"- current run(현재 실행): `{RUN_ID}`", "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`", f"- judgment(판정): `{summary['judgment']}`", f"- recommendation(추천): `{summary['recommendation']}`"]))
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    if RUN_ID not in review:
        review = review.rstrip() + f"\n- `{RUN_ID}`: `{summary['judgment']}`, recommendation(추천) `{summary['recommendation']}`, report(보고서) `{rel(REPORT_PATH)}`\n"
    io_path(REVIEW_INDEX_PATH).write_text(review, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig")
    if RUN_ID not in changelog:
        changelog += f"\n- 2026-05-02: Added `{RUN_ID}` probability geometry probe(확률 기하 탐침); recommendation(추천) `{summary['recommendation']}`; no alpha quality(알파 품질), baseline(기준선), or promotion(승격) claim.\n"
    io_path(CHANGELOG_PATH).write_text(changelog, encoding="utf-8-sig")


def judge(probability: Sequence[Mapping[str, Any]], signals: Sequence[Mapping[str, Any]], clusters: Sequence[Mapping[str, Any]], stability: Sequence[Mapping[str, Any]]) -> tuple[str, str]:
    by_prob = {(row["split"], row["metric"]): row for row in probability}
    by_signal = {(row["split"], row["decision"]): row for row in signals}
    by_cluster = {(row["split"], row["scope"]): row for row in clusters}
    entropy_high = by_prob[("validation_is", "entropy_norm")]["mean"] > 0.88 and by_prob[("oos", "entropy_norm")]["mean"] > 0.88
    margin_low = by_prob[("validation_is", "margin")]["mean"] < 0.23 and by_prob[("oos", "margin")]["mean"] < 0.23
    stable = abs(by_prob[("validation_is", "p_long")]["mean"] - by_prob[("oos", "p_long")]["mean"]) < 0.03 and abs(by_signal[("validation_is", "signal_total")]["share"] - by_signal[("oos", "signal_total")]["share"]) < 0.03
    concentrated = by_cluster[("validation_is", "any_q90_signal")]["max_month_share"] > 0.45
    if entropy_high and margin_low and stable:
        return "inconclusive_probability_shape_stable_but_low_confidence_tail", "pivot_within_stage13_to_activation_or_feature_sensitivity"
    if concentrated:
        return "inconclusive_probability_shape_concentrated_signal_tail", "one_more_time_concentration_probe_only_if_needed"
    return "inconclusive_probability_geometry_probe_completed", "pivot_within_stage13_to_new_model_characteristic_topic"


def stats(values: Sequence[float]) -> dict[str, Any]:
    ordered = sorted(values)
    mu = mean(ordered)
    variance = sum((value - mu) ** 2 for value in ordered) / len(ordered) if ordered else 0.0
    return {"count": len(ordered), "mean": mu, "std": math.sqrt(variance), "min": ordered[0], "p05": percentile(ordered, 5), "p10": percentile(ordered, 10), "p25": percentile(ordered, 25), "p50": percentile(ordered, 50), "p75": percentile(ordered, 75), "p90": percentile(ordered, 90), "p95": percentile(ordered, 95), "max": ordered[-1]}


def percentile(ordered: Sequence[float], q: float) -> float:
    index = (len(ordered) - 1) * q / 100.0
    low = math.floor(index)
    high = math.ceil(index)
    if low == high:
        return ordered[low]
    return ordered[low] * (high - index) + ordered[high] * (index - low)


def psi_10bin(left: Sequence[float], right: Sequence[float]) -> float:
    eps = 1.0e-6
    total_left = len(left)
    total_right = len(right)
    score = 0.0
    for index in range(10):
        low = index / 10.0
        high = (index + 1) / 10.0
        left_count = sum(1 for value in left if low <= value < high or (index == 9 and value <= high))
        right_count = sum(1 for value in right if low <= value < high or (index == 9 and value <= high))
        left_share = max(left_count / total_left, eps)
        right_share = max(right_count / total_right, eps)
        score += (right_share - left_share) * math.log(right_share / left_share)
    return score


def stability_interpretation(metric: str, delta: float, psi: float) -> str:
    if psi < 0.05 and abs(delta) < 0.03:
        return "stable_shape"
    if psi < 0.10:
        return "mild_shift"
    return "material_shift"


def cluster_interpretation(top5_cluster_share: float | None, max_month_share: float | None, max_cluster_len: int) -> str:
    if (max_month_share or 0.0) > 0.45 or max_cluster_len >= 40:
        return "concentrated_tail"
    if (top5_cluster_share or 0.0) < 0.12:
        return "broadly_distributed"
    return "moderately_clustered"


def mean_or_none(values: Sequence[float]) -> float | None:
    return mean(values) if values else None


def safe_div(numerator: float, denominator: float) -> float | None:
    return numerator / denominator if denominator else None


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage13 MLP probability geometry probe.")
    parser.parse_args(argv)
    summary = build_summary(utc_now())
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
