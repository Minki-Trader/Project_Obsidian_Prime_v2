from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.mt5 import runtime_support as mt5


STAGE_ID = "stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64"
RUN_ID = "frontier66C_proxy_signal_mt5_backfill_v1"
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
REVIEW_ROOT = Path("stages") / STAGE_ID / "03_reviews"
MANIFEST_PATH = RUN_ROOT / "frontier66_proxy_signal_materialization_manifest.csv"
EXPECTED_PATH = RUN_ROOT / "frontier66_proxy_signal_expected_by_split.csv"
ATTEMPTS_PATH = RUN_ROOT / "frontier66_proxy_signal_mt5_attempts.json"
GROK_REVIEW_ROOT = REVIEW_ROOT / "grok_pre_mt5_proxy_signal_backfill_review"
CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)


def main() -> int:
    created_at = utc_now()
    manifest = read_csv_rows(MANIFEST_PATH)
    expected = read_csv_rows(EXPECTED_PATH)
    attempts = json.loads(io_path(ATTEMPTS_PATH).read_text(encoding="utf-8"))

    signal_rows = audit_signal_counts(expected, attempts)
    spot_rows = source_kind_spot_checks(attempts)
    identity_rows = handoff_identity_rows(attempts)
    zero_rows = zero_signal_rows(manifest, attempts)
    gap_rows = gap_taxonomy_rows(manifest, attempts)

    write_csv(RUN_ROOT / "frontier66_pre_mt5_signal_audit.csv", signal_rows)
    write_csv(RUN_ROOT / "frontier66_pre_mt5_source_kind_spot_checks.csv", spot_rows)
    write_csv(RUN_ROOT / "frontier66_pre_mt5_handoff_identity.csv", identity_rows)
    write_csv(RUN_ROOT / "frontier66_pre_mt5_gap_taxonomy.csv", gap_rows)
    write_json(
        RUN_ROOT / "frontier66_pre_mt5_local_audit_result.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": created_at,
            "signal_row_count": len(signal_rows),
            "signal_audit_failures": sum(1 for row in signal_rows if row["audit_status"] != "pass"),
            "source_kind_spot_check_rows": len(spot_rows),
            "source_kind_spot_check_failures": sum(1 for row in spot_rows if row["audit_status"] != "pass"),
            "zero_signal_rows": zero_rows,
            "handoff_identity_rows": len(identity_rows),
            "gap_taxonomy_rows": len(gap_rows),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_report(created_at, manifest, signal_rows, spot_rows, zero_rows, identity_rows, gap_rows)
    write_grok_receipt(created_at, signal_rows, spot_rows, zero_rows)
    print(json.dumps(json_ready({"status": "completed", "signal_rows": len(signal_rows), "spot_rows": len(spot_rows)}), ensure_ascii=False, indent=2))
    return 0


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames or ["empty"])
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value for key, value in row.items()})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        path = Path(text[4:])
    return path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()


def by_attempt(attempts: Sequence[Mapping[str, Any]]) -> dict[tuple[str, str], Mapping[str, Any]]:
    return {(str(item["stage_num"]), str(item["split"])): item for item in attempts}


def audit_signal_counts(expected: Sequence[Mapping[str, str]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    lookup = by_attempt(attempts)
    rows: list[dict[str, Any]] = []
    for exp in expected:
        key = (str(exp["stage_num"]), str(exp["split"]))
        attempt = lookup[key]
        feature_path = Path(attempt["feature_payload"]["path"])
        frame = pd.read_csv(io_path(feature_path))
        feature_cols = feature_columns(frame)
        feature = feature_cols[-1]
        values = pd.to_numeric(frame[feature], errors="coerce")
        actual_rows = int(len(frame))
        actual_signal = int(values.ne(0).sum())
        actual_long = int(values.gt(0).sum())
        actual_short = int(values.lt(0).sum())
        expected_rows = int(exp["rows"])
        expected_signal = int(exp["signal_count"])
        expected_long = int(exp["long_count"])
        expected_short = int(exp["short_count"])
        status = (
            "pass"
            if (actual_rows, actual_signal, actual_long, actual_short)
            == (expected_rows, expected_signal, expected_long, expected_short)
            else "fail"
        )
        rows.append(
            {
                "stage_num": exp["stage_num"],
                "candidate_id": exp["candidate_id"],
                "split": exp["split"],
                "source_kind": attempt.get("source_kind", ""),
                "feature_path": rel(feature_path),
                "expected_rows": expected_rows,
                "actual_rows": actual_rows,
                "expected_signal_count": expected_signal,
                "actual_signal_count": actual_signal,
                "expected_long_count": expected_long,
                "actual_long_count": actual_long,
                "expected_short_count": expected_short,
                "actual_short_count": actual_short,
                "audit_status": status,
            }
        )
    return rows


def source_kind_spot_checks(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    selected: dict[str, Mapping[str, Any]] = {}
    for attempt in attempts:
        selected.setdefault(str(attempt.get("source_kind", "")), attempt)
    rows: list[dict[str, Any]] = []
    for source_kind, attempt in sorted(selected.items()):
        feature_path = Path(attempt["feature_payload"]["path"])
        frame = pd.read_csv(io_path(feature_path))
        feature_cols = feature_columns(frame)
        feature = feature_cols[-1]
        values = pd.to_numeric(frame[feature], errors="coerce")
        time_col = time_column(frame)
        sample = frame.loc[values.ne(0), [time_col, "split", feature]].head(10)
        valid_values = bool(values.dropna().isin([-1.0, 0.0, 1.0]).all())
        expected_split = "validation" if str(attempt["split"]) == "validation_is" else str(attempt["split"])
        valid_split = bool(frame["split"].astype(str).eq(expected_split).all()) if "split" in frame.columns else False
        rows.append(
            {
                "source_kind": source_kind,
                "stage_num": attempt.get("stage_num"),
                "candidate_id": attempt.get("candidate_id"),
                "split": attempt.get("split"),
                "feature_path": rel(feature_path),
                "nonflat_sample_count": int(len(sample)),
                "sample_timestamps": "|".join(sample[time_col].astype(str).tolist()),
                "sample_values": "|".join(sample[feature].astype(str).tolist()),
                "valid_signal_values": valid_values,
                "valid_split_membership": valid_split,
                "audit_status": "pass" if valid_values and valid_split else "fail",
            }
        )
    return rows


def feature_columns(frame: pd.DataFrame) -> list[str]:
    metadata = {"timestamp", "timestamp_utc", "bar_time_server", "split", "time", "datetime", "row_index"}
    cols = [col for col in frame.columns if col not in metadata]
    if not cols:
        raise RuntimeError("feature matrix has no feature column")
    return cols


def time_column(frame: pd.DataFrame) -> str:
    for col in ("timestamp_utc", "timestamp", "bar_time_server", "time", "datetime"):
        if col in frame.columns:
            return col
    raise RuntimeError("feature matrix has no timestamp column")


def zero_signal_rows(manifest: Sequence[Mapping[str, str]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    attempted_stages = {str(item.get("stage_num")) for item in attempts}
    rows = []
    for row in manifest:
        if row.get("status") != "logic_zero_signal_no_mt5_attempt":
            continue
        stage_num = str(row.get("stage_num"))
        rows.append(
            {
                "stage_num": stage_num,
                "stage_id": row.get("stage_id", ""),
                "status": row.get("status", ""),
                "attempt_absent": stage_num not in attempted_stages,
                "audit_status": "pass" if stage_num not in attempted_stages else "fail",
            }
        )
    return rows


def handoff_identity_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        set_path = ROOT / attempt["set"]["path"]
        ini_path = ROOT / attempt["ini"]["path"]
        model_path = RUN_ROOT / "models" / Path(str(attempt["model_payload"]["path"])).name
        feature_path = Path(attempt["feature_payload"]["path"])
        rows.append(
            {
                "stage_num": attempt.get("stage_num"),
                "candidate_id": attempt.get("candidate_id"),
                "split": attempt.get("split"),
                "source_kind": attempt.get("source_kind"),
                "attempt_name": attempt.get("attempt_name"),
                "set_path": rel(set_path),
                "set_sha256": mt5.sha256_file(set_path) if path_exists(set_path) else "",
                "ini_path": rel(ini_path),
                "ini_sha256": mt5.sha256_file(ini_path) if path_exists(ini_path) else "",
                "model_path": rel(model_path),
                "model_sha256": mt5.sha256_file(model_path) if path_exists(model_path) else "",
                "feature_path": rel(feature_path),
                "feature_sha256": attempt["feature_payload"].get("sha256", ""),
                "max_hold_bars": attempt.get("max_hold_bars"),
                "extra_set_values": attempt.get("extra_set_values", {}),
                "fixed_point_sltp_notes": attempt.get("fixed_point_sltp_notes", ""),
            }
        )
    return rows


def gap_taxonomy_rows(manifest: Sequence[Mapping[str, str]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_stage: dict[str, Mapping[str, Any]] = {}
    for attempt in attempts:
        by_stage.setdefault(str(attempt.get("stage_num")), attempt)
    rows = []
    for row in manifest:
        stage_num = str(row.get("stage_num"))
        attempt = by_stage.get(stage_num, {})
        source_kind = str(attempt.get("source_kind") or row.get("source_kind") or "")
        if row.get("status") == "logic_zero_signal_no_mt5_attempt":
            expected_gap = "stage_logic_zero(단계 로직상 신호 0)"
        elif source_kind in {"stage18_lifecycle_trade_log_replay", "entry_trade_log_replay"}:
            expected_gap = "entry_preserved_exit_risk_representation_gap(진입 보존, 청산/위험 표현 간극)"
        elif "score" in source_kind or "probability" in source_kind or "joblib" in source_kind:
            expected_gap = "signal_handoff_and_exit_risk_representation_gap(신호 인계 및 청산/위험 표현 간극)"
        else:
            expected_gap = "signal_handoff_execution_economics_gap(신호 인계/실행/경제성 간극)"
        rows.append(
            {
                "stage_num": stage_num,
                "candidate_id": row.get("candidate_id", ""),
                "status": row.get("status", ""),
                "source_kind": source_kind,
                "expected_gap_taxonomy": expected_gap,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_report(
    created_at: str,
    manifest: Sequence[Mapping[str, str]],
    signal_rows: Sequence[Mapping[str, Any]],
    spot_rows: Sequence[Mapping[str, Any]],
    zero_rows: Sequence[Mapping[str, Any]],
    identity_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
) -> None:
    signal_failures = [row for row in signal_rows if row["audit_status"] != "pass"]
    spot_failures = [row for row in spot_rows if row["audit_status"] != "pass"]
    zero_failures = [row for row in zero_rows if row["audit_status"] != "pass"]
    materialized = sum(1 for row in manifest if row.get("status") == "proxy_signal_materialized_pending_mt5")
    zero = sum(1 for row in manifest if row.get("status") == "logic_zero_signal_no_mt5_attempt")
    lines = [
        "# Frontier66D Pre-MT5 Local Verification(F66D MT5 전 로컬 검증)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "Action(행동): F11,F15,F18-F49 proxy signal materialization(프록시 신호 물질화)을 MT5 execution(메타트레이더5 실행) 전 로컬로 검증했습니다.",
        "",
        "Effect(효과): runtime probe(런타임 탐침)를 실행하기 전 signal count(신호 수), source-kind spot check(원천 종류 표본 확인), zero-signal exclusion(신호 0 제외), handoff identity(인계 정체성), gap taxonomy(간극 분류)를 고정합니다.",
        "",
        f"- materialized_stages(물질화 단계): `{materialized}`",
        f"- logic_zero_stages(로직상 신호 0 단계): `{zero}`",
        f"- signal_audit_rows(신호 감사 행): `{len(signal_rows)}` failures(실패): `{len(signal_failures)}`",
        f"- source_kind_spot_checks(원천 종류 표본 확인): `{len(spot_rows)}` failures(실패): `{len(spot_failures)}`",
        f"- zero_exclusion_rows(신호 0 제외 행): `{len(zero_rows)}` failures(실패): `{len(zero_failures)}`",
        f"- handoff_identity_rows(인계 정체성 행): `{len(identity_rows)}`",
        f"- gap_taxonomy_rows(간극 분류 행): `{len(gap_rows)}`",
        "",
        "Claim boundary(주장 경계): runtime_probe_observation(런타임 탐침 관찰) only(한정). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음).",
        "",
        "## Grok Local Verification Mapping(Grok 로컬 검증 대응)",
        "",
        "- per-stage signal ledger(단계별 신호 장부): `frontier66_pre_mt5_signal_audit.csv`",
        "- source-kind spot checks(원천 종류 표본 확인): `frontier66_pre_mt5_source_kind_spot_checks.csv`",
        "- F26/F34 exclusion proof(F26/F34 제외 증명): `frontier66_pre_mt5_local_audit_result.json` and zero rows below",
        "- handoff identity bundle(인계 정체성 묶음): `frontier66_pre_mt5_handoff_identity.csv`",
        "- F18 narrow check(F18 좁은 확인): `frontier66_pre_mt5_signal_audit.csv` entry signal counts only; exit parity(청산 동등성) not claimed(주장 없음)",
        "- pre-declared gap taxonomy(사전 선언 간극 분류): `frontier66_pre_mt5_gap_taxonomy.csv`",
        "",
        "## Zero Signal Exclusion(신호 0 제외)",
        "",
        "| stage | attempt_absent | status |",
        "|---:|---|---|",
    ]
    for row in zero_rows:
        lines.append(f"| F{int(row['stage_num']):02d} | `{row['attempt_absent']}` | `{row['audit_status']}` |")
    lines.append("")
    io_path(REVIEW_ROOT / "frontier66D_pre_mt5_local_verification_report.md").write_text("\n".join(lines), encoding="utf-8-sig")


def write_grok_receipt(created_at: str, signal_rows: Sequence[Mapping[str, Any]], spot_rows: Sequence[Mapping[str, Any]], zero_rows: Sequence[Mapping[str, Any]]) -> None:
    clean_output = GROK_REVIEW_ROOT / "clean_output.md"
    metadata = GROK_REVIEW_ROOT / "metadata.json"
    signal_pass = all(row["audit_status"] == "pass" for row in signal_rows)
    spot_pass = all(row["audit_status"] == "pass" for row in spot_rows)
    zero_pass = all(row["audit_status"] == "pass" for row in zero_rows)
    lines = [
        "# Grok Pre-MT5 Proxy Signal Backfill Receipt(Grok MT5 전 프록시 신호 소급 영수증)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "- trigger_reason(트리거 이유): goal rule(목표 규칙) requires Grok review(Grok 검토) before expensive MT5(비싼 MT5 전).",
        "- review_size(검토 크기): small review(소규모 검토)",
        "- direction_before_grok(Grok 전 방향): materialize missing runtime probe stages(누락 런타임 탐침 단계)를 proxy signal(프록시 신호)로 MT5 실행한다.",
        f"- bounded_evidence(제한 근거): F11,F15,F18-F49 materialization summary(물질화 요약), known representation gaps(표현 간극), claim boundary(주장 경계).",
        f"- prompt_identity(프롬프트 정체성): `stages/{STAGE_ID}/03_reviews/grok_pre_mt5_proxy_signal_backfill_prompt.md`",
        f"- grok_output_identity(Grok 출력 정체성): `{clean_output.as_posix()}`",
        "- advice_classification(조언 분류): needs_local_verification(로컬 검증 필요), directionally acceptable(방향상 수용 가능).",
        f"- local_verification(로컬 검증): signal_pass={signal_pass}; spot_pass={spot_pass}; zero_pass={zero_pass}",
        "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음).",
        "- final_codex_direction(최종 Codex 방향): proceed to MT5 runtime probe(메타트레이더5 런타임 탐침 진행) as observation only(관찰 한정), then gap attribution(간극 귀속).",
        f"- metadata(메타데이터): `{metadata.as_posix()}`",
        "",
    ]
    io_path(REVIEW_ROOT / "grok_pre_mt5_proxy_signal_backfill_receipt.md").write_text("\n".join(lines), encoding="utf-8-sig")


if __name__ == "__main__":
    raise SystemExit(main())
