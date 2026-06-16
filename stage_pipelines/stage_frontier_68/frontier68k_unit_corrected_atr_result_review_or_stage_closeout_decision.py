from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists


STAGE_ID = "stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout"
RUN_ID = "frontier68K_unit_corrected_atr_result_review_or_stage_closeout_decision_v1"
CLOSEOUT_RUN_ID = "frontier68_closeout_preserved_clue_negative_memory_v1"
PARENT_RUN_ID = "frontier68J_unit_corrected_atr_runtime_repair_probe_v1"
NEXT_STAGE_ID = "stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory"
NEXT_RUN_ID = "frontier69A_stage_open_axis_rotation_hypothesis_design_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
CLOSEOUT_ROOT = STAGE_ROOT / "02_runs" / CLOSEOUT_RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f68k_closeout_preserved_clue_negative_memory"
GROK_PROMPT = GROK_PACKET / "prompts/f68k_closeout_review_prompt.md"
GROK_CLEAN_OUTPUT = GROK_PACKET / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET / "outputs/metadata.json"

F68D_RECEIPT = REVIEWS_ROOT / "frontier68D_runtime_probe_receipt_review.csv"
F68F_RECEIPT = REVIEWS_ROOT / "frontier68F_runtime_probe_receipt_review.csv"
F68H_RECEIPT = REVIEWS_ROOT / "frontier68H_runtime_probe_receipt_review.csv"
F68J_RECEIPT = REVIEWS_ROOT / "frontier68J_runtime_probe_receipt_review.csv"
F68J_COMPARISON = REVIEWS_ROOT / "frontier68J_comparison_vs_f68f_review.csv"
F68J_EFFECTIVE = REVIEWS_ROOT / "frontier68J_effective_atr_sltp_summary_review.csv"
F68J_SIGNATURE = REVIEWS_ROOT / "frontier68J_signature_collapse_review.csv"
F68J_MANIFEST = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "run_manifest.json"

CLAIM_BOUNDARY = (
    "preserved_clue_negative_memory_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
CLOSEOUT_STATUS = "closed_preserved_clue_negative_memory_no_authority"
CLOSEOUT_JUDGMENT = "preserved_clue_negative_memory_no_authority"


def main() -> int:
    created_at = utc_now()
    ensure_dirs()
    payload = build_payload(created_at)
    write_artifacts(payload)
    update_registers(payload)
    update_state_files(payload)
    print(json.dumps(json_ready(compact_status(payload)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, CLOSEOUT_ROOT, REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in fieldnames})


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def num(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fmt(value: Any) -> str:
    number = num(value)
    if number is None:
        return "" if value in (None, "") else str(value)
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.6f}".rstrip("0").rstrip(".")


def build_payload(created_at: str) -> dict[str, Any]:
    required = [
        GROK_PROMPT,
        GROK_CLEAN_OUTPUT,
        GROK_METADATA,
        F68D_RECEIPT,
        F68F_RECEIPT,
        F68H_RECEIPT,
        F68J_RECEIPT,
        F68J_COMPARISON,
        F68J_EFFECTIVE,
        F68J_SIGNATURE,
        F68J_MANIFEST,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F68K closeout evidence missing(F68K 마감 근거 누락): {missing}")

    f68d_rows = read_csv_rows(F68D_RECEIPT)
    f68f_rows = read_csv_rows(F68F_RECEIPT)
    f68h_rows = read_csv_rows(F68H_RECEIPT)
    f68j_rows = read_csv_rows(F68J_RECEIPT)
    comparison_rows = read_csv_rows(F68J_COMPARISON)
    effective_rows = read_csv_rows(F68J_EFFECTIVE)
    signature_rows = read_csv_rows(F68J_SIGNATURE)
    manifest = read_json(F68J_MANIFEST)
    grok_clean = read_text(GROK_CLEAN_OUTPUT)
    grok_metadata = read_json(GROK_METADATA)

    closeout_kpi_rows = build_closeout_kpi_rows(f68d_rows, f68f_rows, f68h_rows, f68j_rows, comparison_rows)
    local_verification = build_local_verification(
        f68j_rows=f68j_rows,
        comparison_rows=comparison_rows,
        effective_rows=effective_rows,
        signature_rows=signature_rows,
        manifest=manifest,
        grok_clean=grok_clean,
        grok_metadata=grok_metadata,
    )
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "closeout_run_id": CLOSEOUT_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": CLOSEOUT_STATUS,
        "judgment": CLOSEOUT_JUDGMENT,
        "closeout_label": "preserved_clue_negative_memory_no_authority(보존 단서 + 부정 기억, 권위 없음)",
        "hypothesis": (
            "runtime_native_lifecycle_cost_dd_proxy_can_reduce_mt5_economics_gap"
            "(런타임 기반 생명주기/비용/손실폭 프록시가 MT5 경제성 간극을 줄일 수 있는가)"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
        "f68d_runtime_rows": f68d_rows,
        "f68f_runtime_rows": f68f_rows,
        "f68h_runtime_rows": f68h_rows,
        "f68j_runtime_rows": f68j_rows,
        "f68j_comparison_vs_f68f": comparison_rows,
        "f68j_effective_atr_sltp": effective_rows,
        "f68j_signature_collapse": signature_rows,
        "closeout_kpi_rows": closeout_kpi_rows,
        "artifact_hashes": artifact_hashes(),
        "grok": {
            "prompt_path": rel(GROK_PROMPT),
            "prompt_hash": grok_metadata.get("prompt_hash", ""),
            "prompt_file_sha256": sha256_file(GROK_PROMPT),
            "clean_output_path": rel(GROK_CLEAN_OUTPUT),
            "clean_output_sha256": sha256_file(GROK_CLEAN_OUTPUT),
            "metadata_path": rel(GROK_METADATA),
            "metadata_sha256": sha256_file(GROK_METADATA),
            "classification": classify_grok(grok_clean),
            "metadata": grok_metadata,
        },
        "local_verification": local_verification,
        "preserved_clues": [
            "F68F ONNX/feature handoff(F68F 온엑스/피처 인계)는 MT5에서 signal/feature parity(신호/피처 동등성) 0/0을 유지했다.",
            "F68J unit-corrected ATR telemetry(F68J 단위 보정 평균진폭 기록)는 세 변형을 실제로 구분했고 F68H 180/260 cap signature(상한 서명)와 맞지 않았다.",
            "F68J wide ATR OOS(F68J 넓은 평균진폭 표본외)는 DD(손실폭)를 F68F OOS 19.57%에서 13.76%로 낮추고 trades/day(일 거래 수)를 6.69로 올렸다.",
        ],
        "negative_memory": [
            "lifecycle/cost/DD proxy plus same F68F ONNX plus risk-only repair(생명주기/비용/손실폭 프록시 + 동일 F68F 온엑스 + 위험 로직만 수리)는 네 축을 동시에 닫지 못했다.",
            "F52-style capped ATR repair(F52식 상한 평균진폭 수리)는 180/260 signature collapse(서명 붕괴)를 만들고 PF/DD(수익 팩터/손실폭)를 크게 악화했다.",
            "SL/TP/ATR width only(손절/익절/평균진폭 폭만 조정)는 PF source(수익 팩터 원천)가 아니었다.",
        ],
        "next_action": (
            "Open F69 with a major-axis rotation(F69를 주요 축 회전으로 연다): feature set(피처 묶음), "
            "label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), "
            "risk logic(위험 로직), or regime/session split(장세/세션 분할)."
        ),
    }


def build_closeout_kpi_rows(
    f68d_rows: Sequence[Mapping[str, str]],
    f68f_rows: Sequence[Mapping[str, str]],
    f68h_rows: Sequence[Mapping[str, str]],
    f68j_rows: Sequence[Mapping[str, str]],
    comparison_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source, source_rows in [
        ("F68D density axis runtime probe(F68D 밀도 축 런타임 탐침)", [row for row in f68d_rows if "density_axis" in row.get("attempt_name", "") and row.get("split") == "oos"]),
        ("F68F near-four-axis runtime repair probe(F68F 네 축 근접 런타임 수리 탐침)", f68f_rows),
        ("F68H capped ATR runtime repair probe(F68H 상한 평균진폭 런타임 수리 탐침)", [row for row in f68h_rows if "f52_atr08" in row.get("attempt_name", "")]),
        ("F68J unit-corrected ATR runtime repair probe(F68J 단위 보정 평균진폭 런타임 수리 탐침)", [row for row in f68j_rows if "atr10_tp16" in row.get("attempt_name", "")]),
    ]:
        for row in source_rows:
            rows.append(kpi_row(source, row, comparison_rows))
    return rows


def kpi_row(source: str, row: Mapping[str, str], comparison_rows: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    period = f"{row.get('test_period_start', '')}..{row.get('test_period_end', '')}"
    attempt = str(row.get("attempt_name", ""))
    variant = attempt.replace("f68j_", "").replace("_validation", "").replace("_oos", "")
    split = str(row.get("split", ""))
    comparison = next(
        (
            item
            for item in comparison_rows
            if item.get("variant_id") == variant and item.get("split") == split
        ),
        {},
    )
    gap = ""
    if comparison:
        gap = (
            f"net_delta_vs_f68f={fmt(comparison.get('net_profit_delta_vs_f68f'))}; "
            f"pf_delta_vs_f68f={fmt(comparison.get('profit_factor_delta_vs_f68f'))}; "
            f"dd_delta_vs_f68f={fmt(comparison.get('drawdown_percent_delta_vs_f68f'))}; "
            f"trades_day_delta_vs_f68f={fmt(comparison.get('trades_per_day_delta_vs_f68f'))}"
        )
    return {
        "source_view": source,
        "attempt_name": attempt,
        "test_period": period,
        "split_view": split,
        "net_profit": fmt(row.get("net_profit")),
        "gross_profit": fmt(row.get("gross_profit")),
        "gross_loss": fmt(row.get("gross_loss")),
        "profit_factor": fmt(row.get("profit_factor")),
        "drawdown_percent": fmt(row.get("max_drawdown_percent")),
        "drawdown_amount": fmt(row.get("max_drawdown_amount")),
        "trade_count": fmt(row.get("trade_count")),
        "trades_per_day": fmt(row.get("trades_per_day")),
        "win_rate_percent": fmt(row.get("win_rate_percent")),
        "average_win": fmt(row.get("average_win")),
        "average_loss": fmt(row.get("average_loss")),
        "payoff_ratio": fmt(row.get("payoff_ratio")),
        "expectancy": fmt(row.get("expectancy")),
        "recovery_factor": fmt(row.get("recovery_factor")),
        "time_under_water": "not_available_from_mt5_receipt(테스터 영수증에 없음)",
        "max_consecutive_loss": "not_available_from_mt5_receipt(테스터 영수증에 없음)",
        "long_trade_count": fmt(row.get("long_trade_count")),
        "short_trade_count": fmt(row.get("short_trade_count")),
        "signal_count_diff": fmt(row.get("signal_count_diff")),
        "feature_ready_diff": fmt(row.get("feature_ready_diff")),
        "proxy_runtime_kpi_gap": gap or "not_applicable_or_recorded_in_stage_gap_tables(해당 없거나 단계 간극 표에 기록)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_local_verification(
    *,
    f68j_rows: Sequence[Mapping[str, str]],
    comparison_rows: Sequence[Mapping[str, str]],
    effective_rows: Sequence[Mapping[str, str]],
    signature_rows: Sequence[Mapping[str, str]],
    manifest: Mapping[str, Any],
    grok_clean: str,
    grok_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    wide_rows = [row for row in f68j_rows if "atr10_tp16" in row.get("attempt_name", "")]
    signal_diff_zero = all(fmt(row.get("signal_count_diff")) == "0" for row in f68j_rows)
    feature_diff_zero = all(fmt(row.get("feature_ready_diff")) == "0" for row in f68j_rows)
    no_signature_collapse = all(
        str(row.get("effective_collapsed_all_variants")).lower() == "false"
        and str(row.get("kpi_collapsed_all_variants")).lower() == "false"
        and fmt(row.get("matches_f68h_cap_signature_rows")) == "0"
        for row in signature_rows
    )
    wide_validation = next((row for row in wide_rows if row.get("split") == "validation"), {})
    wide_oos = next((row for row in wide_rows if row.get("split") == "oos"), {})
    return {
        "grok_transport_success": bool(grok_metadata.get("success") is True and grok_metadata.get("returncode") == 0),
        "grok_direction_accepted": "Close F68 as preserved_clue + negative_memory" in grok_clean,
        "f68j_runtime_receipt_rows": len(f68j_rows),
        "f68j_comparison_rows": len(comparison_rows),
        "f68j_effective_rows": len(effective_rows),
        "f68j_signature_rows": len(signature_rows),
        "same_f68f_source_run": manifest.get("source_run_id") == "frontier68F_near_four_axis_onnx_runtime_repair_probe_v1",
        "same_model_path_repo": (manifest.get("handoff") or {}).get("model_path_repo"),
        "same_feature_csv_repo": (manifest.get("handoff") or {}).get("feature_csv_repo"),
        "signal_count_parity_all_zero": signal_diff_zero,
        "feature_readiness_parity_all_zero": feature_diff_zero,
        "signature_collapse_repaired": no_signature_collapse,
        "wide_validation_identity": {
            "attempt_name": wide_validation.get("attempt_name"),
            "net_profit": wide_validation.get("net_profit"),
            "profit_factor": wide_validation.get("profit_factor"),
            "drawdown_percent": wide_validation.get("max_drawdown_percent"),
            "trades_per_day": wide_validation.get("trades_per_day"),
        },
        "wide_oos_identity": {
            "attempt_name": wide_oos.get("attempt_name"),
            "net_profit": wide_oos.get("net_profit"),
            "profit_factor": wide_oos.get("profit_factor"),
            "drawdown_percent": wide_oos.get("max_drawdown_percent"),
            "trades_per_day": wide_oos.get("trades_per_day"),
        },
        "forbidden_claims": {
            "completion": "not_claimed(주장 없음)",
            "baseline": "not_claimed(주장 없음)",
            "promotion": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "live_readiness": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
        },
        "five_stage_retrospective_due_status": "not_due_after_f68_closeout_3_of_5(아직 아님, F68 마감 후 3/5)",
    }


def classify_grok(clean: str) -> dict[str, list[str]]:
    return {
        "accepted": [
            "F68 closeout as preserved clue + negative memory(F68 보존 단서 + 부정 기억 마감)",
            "Preserve F68F parity and F68J telemetry differentiation(F68F 동등성과 F68J 기록 구분성 보존)",
            "Do not repeat capped ATR or risk-only repair loop(상한 평균진폭 또는 위험 단독 수리 반복 금지)",
            "Next frontier requires major-axis rotation(다음 전선은 주요 축 회전 필요)",
        ],
        "rejected": [
            "Final closeout write without register/hash/KPI local check(등록부/해시/KPI 로컬 확인 없는 마감 작성)",
            "Treating F68 as idea dead or proxy useless(F68을 아이디어 사망이나 프록시 무용으로 처리)",
        ],
        "needs_local_verification": [
            "Artifact hashes and canonical paths(산출물 해시와 정식 경로)",
            "F68J wide validation/OOS same-run identity(F68J 넓은 변형 검증/표본외 동일 실행 정체성)",
            "No overclaim drift in state and ledgers(상태와 장부의 과장 주장 없음)",
            "Five-stage retrospective due status(5단계 중간 검토 도래 상태)",
        ],
        "raw_contains_boundary": "Claim boundary respected" in clean,
    }


def artifact_hashes() -> list[dict[str, str]]:
    paths = [
        GROK_PROMPT,
        GROK_CLEAN_OUTPUT,
        GROK_METADATA,
        F68D_RECEIPT,
        F68F_RECEIPT,
        F68H_RECEIPT,
        F68J_RECEIPT,
        F68J_COMPARISON,
        F68J_EFFECTIVE,
        F68J_SIGNATURE,
        F68J_MANIFEST,
    ]
    return [{"path": rel(path), "sha256": sha256_file(path)} for path in paths]


def write_artifacts(payload: Mapping[str, Any]) -> None:
    write_json(RUN_ROOT / "run_manifest.json", payload)
    write_json(RUN_ROOT / "f68k_closeout_decision.json", payload)
    write_json(CLOSEOUT_ROOT / "run_manifest.json", payload)
    write_json(CLOSEOUT_ROOT / "frontier68_closeout_summary.json", payload)
    write_csv(RUN_ROOT / "f68k_closeout_kpi_table.csv", payload["closeout_kpi_rows"])
    write_csv(REVIEWS_ROOT / "frontier68K_closeout_kpi_table_review.csv", payload["closeout_kpi_rows"])
    write_md(REVIEWS_ROOT / "frontier68K_result_review_or_stage_closeout_decision_report.md", result_review_lines(payload))
    write_md(REVIEWS_ROOT / "stage_closeout_report.md", closeout_report_lines(payload))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit.md", gate_audit_lines(payload))
    write_md(REVIEWS_ROOT / "grok_stage_closeout_receipt.md", grok_receipt_lines(payload))
    write_review_index(payload)


def result_review_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        "# F68K Result Review Or Stage Closeout Decision(F68K 결과 검토 또는 단계 마감 결정)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F68J unit-corrected ATR runtime probe(F68J 단위 보정 평균진폭 런타임 탐침)를 F68F/F68H/F68D와 대조했다.",
        "",
        "Effect(효과): risk-only repair loop(위험 로직 단독 수리 반복)가 네 축을 동시에 맞추지 못했다는 점을 closeout(마감)으로 고정한다.",
        "",
        f"- status(상태): `{payload['status']}`",
        f"- judgment(판정): `{payload['judgment']}`",
        f"- claim boundary(주장 경계): `{payload['claim_boundary']}`",
        "",
        "## Codex Direction(코덱스 방향)",
        "",
        "F68은 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫는다. F68F/F68J의 동등성/기록 단서는 보존하지만, 같은 F68F ONNX(온엑스)에 SL/TP/ATR(손절/익절/평균진폭)만 더 만지는 수리는 반복하지 않는다.",
    ]


def closeout_report_lines(payload: Mapping[str, Any]) -> list[str]:
    lines = [
        "# F68 Stage Closeout Report(F68 단계 마감 보고서)",
        "",
        f"Stage(단계): `{STAGE_ID}`",
        f"Closeout run(마감 실행): `{CLOSEOUT_RUN_ID}`",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "## Hypothesis(가설)",
        "",
        str(payload["hypothesis"]),
        "",
        "## Closeout Label(마감 라벨)",
        "",
        f"`{payload['closeout_label']}`",
        "",
        "## Mandatory KPI(필수 핵심 성과 지표)",
        "",
        "| source/view(원천/보기) | period(기간) | split(분할) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | trades/day(일 거래 수) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복 계수) | long/short(롱/숏) | parity gap(동등성 간극) |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in payload["closeout_kpi_rows"]:
        lines.append(
            "| {source} | `{period}` | `{split}` | `{net}` | `{gp}` | `{gl}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{win}` | `{avgw}` | `{avgl}` | `{payoff}` | `{expectancy}` | `{recovery}` | `{long}/{short}` | `{gap}` |".format(
                source=row["source_view"],
                period=row["test_period"],
                split=row["split_view"],
                net=row["net_profit"],
                gp=row["gross_profit"],
                gl=row["gross_loss"],
                pf=row["profit_factor"],
                dd=row["drawdown_percent"],
                trades=row["trade_count"],
                tpd=row["trades_per_day"],
                win=row["win_rate_percent"],
                avgw=row["average_win"],
                avgl=row["average_loss"],
                payoff=row["payoff_ratio"],
                expectancy=row["expectancy"],
                recovery=row["recovery_factor"],
                long=row["long_trade_count"],
                short=row["short_trade_count"],
                gap=f"signal={row['signal_count_diff']};feature={row['feature_ready_diff']}",
            )
        )
    lines.extend(
        [
            "",
            "- time under water(회복 전 체류 시간): `not_available_from_mt5_receipt(테스터 영수증에 없음)`.",
            "- max consecutive loss(최대 연속 손실): `not_available_from_mt5_receipt(테스터 영수증에 없음)`.",
            "",
            "## Preserved Clues(보존 단서)",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in payload["preserved_clues"])
    lines.extend(["", "## Negative Memory(부정 기억)", ""])
    lines.extend(f"- {item}" for item in payload["negative_memory"])
    lines.extend(
        [
            "",
            "## Proxy/Runtime Gap(프록시/런타임 간극)",
            "",
            "F68 proxy(프록시)는 meaningful signal(의미 있는 신호)을 만들고 ONNX/feature parity(온엑스/피처 동등성)를 MT5로 옮겼지만, runtime economics(런타임 경제성), PF(수익 팩터), validation DD(검증 손실폭)는 동시에 닫히지 않았다.",
            "",
            "## Next Action(다음 행동)",
            "",
            str(payload["next_action"]),
            "",
            f"Next stage(다음 단계): `{NEXT_STAGE_ID}`",
            f"First run(첫 실행): `{NEXT_RUN_ID}`",
            "",
            f"Claim boundary(주장 경계): `{payload['claim_boundary']}`",
        ]
    )
    return lines


def gate_audit_lines(payload: Mapping[str, Any]) -> list[str]:
    lv = payload["local_verification"]
    return [
        "# F68 Required Gate Coverage Audit(F68 필수 게이트 커버리지 감사)",
        "",
        f"- work packet(작업 묶음): `{RUN_ID}` and `{CLOSEOUT_RUN_ID}`.",
        "- primary family(주 작업군): `kpi_evidence(KPI 근거)` with runtime evidence support(런타임 근거 보조).",
        "- Grok closeout review(그록 마감 검토): `completed(완료)`.",
        f"- Grok prompt hash(그록 프롬프트 해시): `{payload['grok']['prompt_hash']}`.",
        f"- Grok prompt file sha256(그록 프롬프트 파일 해시): `{payload['grok']['prompt_file_sha256']}`.",
        f"- Grok output hash(그록 출력 해시): `{payload['grok']['clean_output_sha256']}`.",
        f"- MT5 Runtime Probe(MT5 런타임 탐침): `completed in F68D/F68F/F68H/F68J(F68D/F68F/F68H/F68J에서 완료)`.",
        f"- signal parity(신호 동등성): `{lv['signal_count_parity_all_zero']}`.",
        f"- feature readiness parity(피처 준비 동등성): `{lv['feature_readiness_parity_all_zero']}`.",
        f"- F68J signature collapse repaired(F68J 서명 붕괴 수리): `{lv['signature_collapse_repaired']}`.",
        "- KPI closeout table(핵심 성과 지표 마감 표): `frontier68K_closeout_kpi_table_review.csv`.",
        "- five-stage retrospective(5단계 중간 검토): `not_due_after_f68_closeout_3_of_5(아직 아님, F68 마감 후 3/5)`.",
        "- test gate(테스트 게이트): `partial_pass_push_blocked(부분 통과, 원격 반영 차단)`.",
        "- passed tests(통과 테스트): agent control/state/gate suite(에이전트 제어/상태/게이트 묶음) `35 passed(35개 통과)`.",
        "- failed test(실패 테스트): `tests/test_code_surface_audit.py::CodeSurfaceAuditTests::test_current_repo_code_surface_audit_passes_with_registered_debt`.",
        "- push blocker(원격 반영 차단): existing code-surface blockers(기존 코드 표면 차단 요인); see(참조) `frontier68K_verification_blocker_test_gate.md`.",
        "- forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve all `not_claimed(주장 없음)`.",
        f"- claim boundary(주장 경계): `{payload['claim_boundary']}`.",
    ]


def grok_receipt_lines(payload: Mapping[str, Any]) -> list[str]:
    grok = payload["grok"]
    return [
        "# F68 Grok Stage Closeout Receipt(F68 그록 단계 마감 영수증)",
        "",
        "- trigger_reason(트리거 이유): stage closeout required external second opinion(단계 마감 필수 외부 2차 의견).",
        "- review_size(검토 크기): `medium review(중간 검토)`.",
        f"- prompt_path(프롬프트 경로): `{grok['prompt_path']}`",
        f"- prompt_hash(프롬프트 해시): `{grok['prompt_hash']}`",
        f"- prompt_file_sha256(프롬프트 파일 해시): `{grok['prompt_file_sha256']}`",
        f"- clean_output_path(정리 출력 경로): `{grok['clean_output_path']}`",
        f"- clean_output_sha256(정리 출력 해시): `{grok['clean_output_sha256']}`",
        f"- metadata_path(메타데이터 경로): `{grok['metadata_path']}`",
        "",
        "## Advice Classification(조언 분류)",
        "",
    ] + [
        f"- accepted(수용): {item}" for item in grok["classification"]["accepted"]
    ] + [
        f"- rejected(거절): {item}" for item in grok["classification"]["rejected"]
    ] + [
        f"- needs_local_verification(로컬 검증 필요): {item}" for item in grok["classification"]["needs_local_verification"]
    ] + [
        "",
        "## Local Verification(로컬 검증)",
        "",
        f"- transport success(전송 성공): `{payload['local_verification']['grok_transport_success']}`.",
        f"- same F68F source run(같은 F68F 원천 실행): `{payload['local_verification']['same_f68f_source_run']}`.",
        f"- signal/feature parity(신호/피처 동등성): `{payload['local_verification']['signal_count_parity_all_zero']}/{payload['local_verification']['feature_readiness_parity_all_zero']}`.",
        f"- final Codex direction(최종 코덱스 방향): `{payload['status']}`.",
        f"- claim boundary(주장 경계): `{payload['claim_boundary']}`.",
    ]


def write_review_index(payload: Mapping[str, Any]) -> None:
    index_path = REVIEWS_ROOT / "review_index.md"
    existing = read_text(index_path) if path_exists(index_path) else "# Review Index(검토 색인)\n"
    additions = [
        "- `frontier68K_result_review_or_stage_closeout_decision_report.md`: F68K result review and closeout decision(F68K 결과 검토와 마감 결정)",
        "- `frontier68K_closeout_kpi_table_review.csv`: F68 closeout KPI table(F68 마감 핵심 성과 지표 표)",
        "- `stage_closeout_report.md`: F68 stage closeout report(F68 단계 마감 보고서)",
        "- `required_gate_coverage_audit.md`: F68 required gate coverage audit(F68 필수 게이트 커버리지 감사)",
        "- `grok_stage_closeout_receipt.md`: F68 Grok closeout receipt(F68 그록 마감 영수증)",
        "- `frontier68K_verification_blocker_test_gate.md`: F68K test gate and push blocker(F68K 테스트 게이트 및 원격 반영 차단)",
        f"Next action(다음 행동): `{NEXT_RUN_ID}` in `{NEXT_STAGE_ID}`",
    ]
    lines = existing.rstrip().splitlines()
    for line in additions:
        if line not in lines:
            lines.append(line)
    write_md(index_path, lines)


def update_registers(payload: Mapping[str, Any]) -> None:
    rows = registry_rows(payload)
    for row in rows:
        upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")
        upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
        upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    update_five_stage_register()
    append_once(ROOT / "docs/registers/idea_registry.md", "<!-- frontier68_closeout_preserved_clue_negative_memory_v1 -->", idea_registry_block(payload))
    append_once(ROOT / "docs/registers/negative_result_register.md", "<!-- frontier68_closeout_preserved_clue_negative_memory_v1 -->", negative_result_block(payload))


def registry_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    best_oos = next(
        (row for row in payload["closeout_kpi_rows"] if "F68J" in row["source_view"] and row["split_view"] == "oos"),
        {},
    )
    base = {
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A+B planned(Tier A+B 계획)",
        "kpi_scope": "runtime_probe_closeout_decision(런타임 탐침 마감 결정)",
        "scoreboard_lane": "kpi_evidence(KPI 근거)",
        "status": payload["status"],
        "judgment": payload["judgment"],
        "path": f"stages/{STAGE_ID}/03_reviews/stage_closeout_report.md",
        "primary_kpi": (
            f"best_f68j_oos_net={best_oos.get('net_profit', '')}; "
            f"PF={best_oos.get('profit_factor', '')}; "
            f"DD={best_oos.get('drawdown_percent', '')}; "
            f"trades_day={best_oos.get('trades_per_day', '')}"
        ),
        "guardrail_kpi": "signal_diff=0; feature_diff=0; f68j_signature_collapse=false; validation_pf=0.94; validation_dd=38.55",
        "external_verification_status": "completed_mt5_runtime_probe_and_grok_closeout_review(완료된 MT5 런타임 탐침 및 그록 마감 검토)",
        "notes": "F68 closed as preserved clue + negative memory; next frontier must rotate a major axis.",
        "date": str(payload["created_at_utc"])[:10],
        "claim_boundary": payload["claim_boundary"],
        "report_path": f"stages/{STAGE_ID}/03_reviews/stage_closeout_report.md",
        "gate_audit_path": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit.md",
        "created_at": payload["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "F68D/F68F/F68H/F68J MT5 Strategy Tester runtime probes(F68D/F68F/F68H/F68J MT5 전략 테스터 런타임 탐침)",
        "trade_density_per_feature_day": best_oos.get("trades_per_day", ""),
        "net_profit": best_oos.get("net_profit", ""),
        "profit_factor": best_oos.get("profit_factor", ""),
        "drawdown": best_oos.get("drawdown_percent", ""),
        "recovery_factor": best_oos.get("recovery_factor", ""),
        "trade_count": best_oos.get("trade_count", ""),
        "result_status": payload["judgment"],
        "next_action": NEXT_RUN_ID,
    }
    decision_row = {
        **base,
        "ledger_row_id": f"{RUN_ID}__result_review_closeout_decision",
        "row_id": f"{RUN_ID}__result_review_closeout_decision",
        "run_id": RUN_ID,
        "subrun_id": "result_review_closeout_decision(결과 검토 마감 결정)",
        "run_number": "frontier68K",
        "decision": "close_f68_as_preserved_clue_negative_memory",
        "next_run_id": CLOSEOUT_RUN_ID,
        "run_family": "frontier_closeout_decision(전선 마감 결정)",
        "run_type": "result_review_or_stage_closeout_decision(결과 검토 또는 단계 마감 결정)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f68k_closeout_decision.json",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier68K_result_review_or_stage_closeout_decision_report.md",
    }
    closeout_row = {
        **base,
        "ledger_row_id": f"{CLOSEOUT_RUN_ID}__stage_closeout",
        "row_id": f"{CLOSEOUT_RUN_ID}__stage_closeout",
        "run_id": CLOSEOUT_RUN_ID,
        "subrun_id": "stage_closeout(단계 마감)",
        "run_number": "frontier68_closeout",
        "decision": payload["status"],
        "next_run_id": NEXT_RUN_ID,
        "run_family": "frontier_stage_closeout(전선 단계 마감)",
        "run_type": "stage_closeout(단계 마감)",
        "input_run_id": RUN_ID,
        "output_path": f"stages/{STAGE_ID}/03_reviews/stage_closeout_report.md",
        "result_path": f"stages/{STAGE_ID}/03_reviews/stage_closeout_report.md",
    }
    return [decision_row, closeout_row]


def upsert_ledger(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None:
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise RuntimeError(f"ledger header missing: {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update_five_stage_register() -> None:
    path = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
    lines = [
        "version: five_stage_retrospective_register_v1",
        "source_of_truth: docs/registers/five_stage_retrospective_register.yaml",
        'purpose: "Track five-stage Grok retrospective(5단계 Grok 중간 검토) cadence without relying on Codex memory(코덱스 기억)."',
        "adopted_at_utc: '2026-06-16T12:05:00Z'",
        "adopted_during_stage_id: stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64",
        "cadence:",
        '  primary_trigger: "closing_frontier_number % 5 == 0"',
        '  fallback_trigger: "len(closed_frontier_ids_since_last_retrospective) >= 5"',
        "  next_open_block: true",
        '  scope_rule: "Use latest five canonical frontier closeout stage ids with closeout receipts, not numeric NN-4..NN alone."',
        "required_outputs:",
        "  - five_stage_retrospective_packet",
        "  - bounded_evidence_table",
        "  - grok_receipt",
        "  - codex_local_verification",
        "  - advice_classification",
        "  - compact_retrospective_report",
        "  - next_stage_open_block_check",
        "required_row_fields:",
        "  - stage_id",
        "  - hypothesis",
        "  - proxy_kpi",
        "  - mt5_runtime_probe_kpi",
        "  - proxy_runtime_gap_cause",
        "  - closeout_label",
        "  - preserved_clue",
        "  - negative_memory",
        "  - systemic_repeat",
        "  - next_action",
        "claim_boundary:",
        "  allowed:",
        "    - direction_delta",
        "    - repair_priority_delta",
        "  forbidden:",
        "    - completion",
        "    - baseline",
        "    - promotion",
        "    - runtime_authority",
        "    - live_readiness",
        "    - goal_achieve",
        "",
        "state:",
        "  last_completed_packet_id: null",
        "  last_completed_at_frontier: null",
        "  last_completed_stage_ids: []",
        "  last_completed_at_utc: null",
        "  closed_frontier_ids_since_last_retrospective:",
        "    - stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64",
        "    - stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk",
        "    - stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout",
        "  closeouts_since_last: 3",
        "  next_numeric_trigger_frontier: 70",
        "  current_due_status: not_due",
        '  note: "F66, F67, and F68 closeouts(마감)은 3/5로 계산했다. Next expected numeric trigger(다음 숫자 트리거)는 F70 closeout(마감)이다."',
    ]
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8-sig")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path) if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def idea_registry_block(payload: Mapping[str, Any]) -> str:
    return f"""<!-- frontier68_closeout_preserved_clue_negative_memory_v1 -->
- `IDEA-FR68-LIFECYCLE-ECONOMICS-PROXY-ONNX-SCOUT`: `{CLOSEOUT_RUN_ID}` closes Frontier68(전선68) as preserved clue + negative memory(보존 단서 + 부정 기억). Effect(효과): F68F exact signal/feature parity(F68F 정확한 신호/피처 동등성)와 F68J unit-corrected ATR telemetry differentiation(F68J 단위 보정 평균진폭 기록 구분성)은 보존하지만, same F68F ONNX + risk-only repair loop(동일 F68F 온엑스 + 위험 단독 수리 반복)는 다음 전선으로 상속하지 않습니다. Next(다음): `{NEXT_RUN_ID}` major-axis rotation(주요 축 회전)."""


def negative_result_block(payload: Mapping[str, Any]) -> str:
    return f"""<!-- frontier68_closeout_preserved_clue_negative_memory_v1 -->
## {CLOSEOUT_RUN_ID} Frontier68 Negative Memory(전선68 부정 기억)

- hypothesis(가설): lifecycle/cost/DD-aware proxy(생명주기/비용/손실폭 인식 프록시)가 MT5 runtime economics gap(MT5 런타임 경제성 간극)을 줄일 수 있는지 시험했다.
- failed_boundary(실패 경계): F68J best OOS(F68J 최선 표본외)는 net/PF/DD/trades/day(순수익/수익 팩터/손실폭/일 거래 수) `68.24 / 1.04 / 13.76% / 6.6923`였지만 validation(검증)은 `-141.58 / 0.94 / 38.55% / 5.7132`로 실패했다.
- preserved_clue(보존 단서): F68F exact parity(F68F 정확 동등성), F68J no signature collapse(F68J 서명 붕괴 없음), unit-corrected ATR telemetry(단위 보정 평균진폭 기록).
- do_not_repeat(반복 금지): same F68F ONNX(동일 F68F 온엑스)에 capped ATR(상한 평균진폭) 또는 SL/TP/ATR width only(손절/익절/평균진폭 폭만) 덧대는 repair loop(수리 반복)를 PF source(수익 팩터 원천)처럼 쓰지 않는다.
- reopen_condition(재개 조건): feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), or regime/session split(장세/세션 분할) 중 하나 이상이 실제로 바뀌고, 새 MT5 Runtime Probe(MT5 런타임 탐침)를 포함할 때만 재개한다.
- report(보고서): `stages/{STAGE_ID}/03_reviews/stage_closeout_report.md`."""


def update_state_files(payload: Mapping[str, Any]) -> None:
    state_lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {CLOSEOUT_RUN_ID}",
        f"latest_completed_run_id: {CLOSEOUT_RUN_ID}",
        f"current_status: {payload['status']}",
        f"current_judgment: {payload['judgment']}",
        f"next_stage_id: {NEXT_STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f68_mandatory_runtime_probe_completed_multiple_materializations(F68 필수 런타임 탐침 다중 물질화 완료)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{payload['created_at_utc']}'",
        "notes:",
        '  - "F68 closeout action(마감 행동): F68J unit-corrected ATR result(F68J 단위 보정 평균진폭 결과)를 F68D/F68F/F68H와 함께 검토하고 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았다."',
        '  - "Effect(효과): F68F ONNX parity(F68F 온엑스 동등성)와 F68J telemetry differentiation(F68J 기록 구분성)은 보존하지만, risk-only repair loop(위험 로직 단독 수리 반복)는 다음 전선으로 상속하지 않는다."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}`에서 feature/label/model/trade-shape/risk/regime axis rotation(피처/라벨/모델/거래 형태/위험/장세 축 회전)을 새 가설로 연다."',
        '  - "Five-stage retrospective(5단계 중간 검토): not_due_after_f68_closeout_3_of_5(아직 아님, F68 마감 후 3/5)."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(state_lines) + "\n", encoding="utf-8-sig")
    write_md(
        ROOT / "docs/context/current_working_state.md",
        [
            "# Current Working State(현재 작업 상태)",
            "",
            f"Updated(갱신): {payload['created_at_utc']}",
            "",
            f"Active stage(활성 단계): `{STAGE_ID}`",
            f"Current run(현재 실행): `{CLOSEOUT_RUN_ID}`",
            f"Latest completed run(최근 완료 실행): `{CLOSEOUT_RUN_ID}`",
            f"Next stage(다음 단계): `{NEXT_STAGE_ID}`",
            f"Next run(다음 실행): `{NEXT_RUN_ID}`",
            "",
            "## Current Truth(현재 진실)",
            "",
            "Action(행동): F68을 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았다.",
            "",
            "Effect(효과): F68F signal/feature parity(F68F 신호/피처 동등성)와 F68J unit-corrected ATR telemetry(F68J 단위 보정 평균진폭 기록)는 다음 가설의 참고 단서로 남기고, 같은 ONNX(온엑스)에 위험 로직만 덧대는 반복은 중단한다.",
            "",
            f"- closeout status(마감 상태): `{payload['status']}`.",
            "- runtime authority(런타임 권위): `not_claimed(주장 없음)`.",
            "- operating promotion(운영 승격): `not_claimed(주장 없음)`.",
            "- live readiness(실거래 준비): `not_claimed(주장 없음)`.",
            "- goal achieve(목표 달성): `not_claimed(주장 없음)`.",
            "",
            "## Continuity Anchor(연속성 고정점)",
            "",
            "Next frontier(다음 전선)는 F68F risk-only repair(F68F 위험 단독 수리)를 더 미세조정하지 않는다. 주요 축을 바꿔 feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), regime/session split(장세/세션 분할) 중 최소 하나를 실제로 교체한다.",
            "",
            f"Claim boundary(주장 경계): `{payload['claim_boundary']}`",
        ],
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        [
            "# F68 Selection Status(F68 선택 상태)",
            "",
            f"- stage(단계): `{STAGE_ID}`",
            f"- current_run(현재 실행): `{CLOSEOUT_RUN_ID}`",
            f"- latest_completed_run(최근 완료 실행): `{CLOSEOUT_RUN_ID}`",
            f"- status(상태): `{payload['status']}`",
            "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
            "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
            "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
            "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
            "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
            "- completed_action(완료 행동): F68 stage closeout(F68 단계 마감) as preserved clue + negative memory(보존 단서 + 부정 기억).",
            f"- report(보고서): `stages/{STAGE_ID}/03_reviews/stage_closeout_report.md`",
            f"- next_stage(다음 단계): `{NEXT_STAGE_ID}`",
            f"- next_action(다음 행동): `{NEXT_RUN_ID}` major-axis stage open(주요 축 회전 단계 개방).",
            f"- boundary(경계): `{payload['claim_boundary']}`.",
        ],
    )


def compact_status(payload: Mapping[str, Any]) -> dict[str, Any]:
    best = next((row for row in payload["closeout_kpi_rows"] if "F68J" in row["source_view"] and row["split_view"] == "oos"), {})
    return {
        "status": payload["status"],
        "judgment": payload["judgment"],
        "closeout_run_id": CLOSEOUT_RUN_ID,
        "best_f68j_oos": {
            "net_profit": best.get("net_profit"),
            "profit_factor": best.get("profit_factor"),
            "drawdown_percent": best.get("drawdown_percent"),
            "trades_per_day": best.get("trades_per_day"),
        },
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": payload["claim_boundary"],
    }


if __name__ == "__main__":
    raise SystemExit(main())
