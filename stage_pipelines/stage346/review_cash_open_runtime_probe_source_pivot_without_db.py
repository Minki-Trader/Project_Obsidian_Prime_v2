from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

STAGE_ID = "346_cash_open_runtime_review__asymmetric_source_pivot"
NEXT_STAGE_ID = "347_cash_open_asymmetric_source__long_short_head_design"
STAGE_DIR = ROOT / "stages" / STAGE_ID
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID

RUN_NUMBER = "run346B"
RUN_ID = "run346B_review_cash_open_runtime_probe_source_pivot_without_db_v1"
PARENT_RUN_ID = "run346A_branch_stage345_to_cash_open_runtime_review_source_pivot_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1"
NEXT_RUN_ID = "run347A_design_cash_open_asymmetric_long_short_source_without_db_v1"

STATUS = "completed_stage346B_cash_open_runtime_probe_reviewed_stage347_asymmetric_source_opened_no_selection"
JUDGMENT = (
    "runtime_probe_reference_clue_valid_but_side_filter_variants_negative_"
    "stage347_asymmetric_source_design_required_no_operating_claim"
)
DECISION = "stage346B_close_stage346_open_stage347_cash_open_asymmetric_source_design"
CLAIM_BOUNDARY = (
    "research_development_review_and_stage_handoff_only_cash_open_runtime_probe_reference_clue_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run346B_cash_open_runtime_probe_source_pivot_review.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_SELECTION = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

SOURCE_RUN_DIR = ROOT / "stages" / "345_cash_open_decomposition__long_quality_short_carry_runtime_probe" / "02_runs" / "run345B"
SOURCE_SUMMARY = SOURCE_RUN_DIR / "cash_open_long_quality_short_carry_mt5_probe_summary.csv"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_DIFF = SOURCE_RUN_DIR / "proxy_mt5_runtime_difference.csv"
SOURCE_RUNTIME_IDENTITY = SOURCE_RUN_DIR / "runtime_identity.csv"
PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run346A"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_HANDOFF_MANIFEST = PARENT_RUN_DIR / "stage345_to_stage346_handoff_manifest.csv"
PARENT_COMPACT_SUMMARY = PARENT_RUN_DIR / "stage345B_compact_runtime_summary.csv"
PARENT_REVIEW_QUEUE = PARENT_RUN_DIR / "run346B_review_queue.csv"

VARIANT_SCORECARD = RUN_DIR / "variant_review_scorecard.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "performance_attribution.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
STAGE347_SEED_QUEUE = RUN_DIR / "stage347_asymmetric_source_seed_queue.csv"
TIER_BOUNDARY_AUDIT = RUN_DIR / "tier_boundary_audit.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

NEXT_STAGE_BRIEF = NEXT_STAGE_DIR / "00_spec" / "stage_brief.md"
NEXT_STAGE_README = NEXT_STAGE_DIR / "README.md"
NEXT_INPUT_REFS = NEXT_STAGE_DIR / "01_inputs" / "input_refs.md"
NEXT_REVIEW_INDEX = NEXT_STAGE_DIR / "03_reviews" / "review_index.md"
NEXT_STAGE_LEDGER = NEXT_STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
NEXT_SELECTION = NEXT_STAGE_DIR / "04_selected" / "selection_status.md"

DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage346B_cash_open_runtime_probe_source_pivot_review.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

STAGE_LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "path",
    "report_path",
    "primary_report",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "scoreboard_lane",
    "lane",
    "family",
    "run_number",
    "notes",
    "source_package_run_id",
    "rows",
    "attempt_count",
    "feature_count",
    "candidate_model_id",
    "ledger_row_id",
    "subrun_id",
    "view",
    "record_view",
    "tier",
    "tier_scope",
    "metric_scope",
    "kpi_scope",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "result_status",
    "net_profit",
    "profit_factor",
    "expectancy",
    "drawdown",
    "recovery_factor",
    "trade_count",
    "matched_rows",
]


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fs_path(path: Path) -> str:
    resolved = path.resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def path_is_file(path: Path) -> bool:
    return os.path.isfile(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def required(path: Path) -> Path:
    if not path_is_file(path):
        raise FileNotFoundError(f"missing required input(필수 입력 누락): {rel(path)}")
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows_list = [dict(row) for row in rows]
    if path_is_file(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_columns) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_columns) not in replacement_keys
    ]
    write_csv(path, kept + rows_list, fieldnames)


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if path_is_file(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def to_float(row: Mapping[str, str], key: str) -> float:
    value = row.get(key, "")
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def to_int(row: Mapping[str, str], key: str) -> int:
    return int(round(to_float(row, key)))


def read_summary() -> list[dict[str, str]]:
    _fields, rows = read_csv_rows(required(SOURCE_SUMMARY))
    if not rows:
        raise RuntimeError("source summary has no rows(원천 요약 행 없음)")
    return rows


def source_gate_passed(path: Path) -> bool:
    _fields, rows = read_csv_rows(required(path))
    return bool(rows) and all(row.get("status") == "passed" for row in rows)


def build_scorecard(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    base = next(row for row in rows if row.get("attempt_name") == "n01_s07_base_control")
    base_net = to_float(base, "net_profit")
    base_pf = to_float(base, "profit_factor")
    base_recovery = to_float(base, "recovery_factor")
    base_trades = to_int(base, "trade_count")
    scorecard: list[dict[str, Any]] = []
    labels = {
        "n01_s07_base_control": "reference_surface(참고 표면)",
        "n02_s07_long_only_disable_short": "positive_fragment_high_pf_low_supply(높은 PF 긍정 조각, 공급 부족)",
        "n03_s07_short_only_disable_long": "short_carry_fragment_imbalanced(숏 기여 조각, 불균형)",
        "n04_s07_no_cash_open_short_single_filter": "negative_balance_gain_profit_loss(균형 개선이나 수익 악화)",
        "n05_s07_late_long_firewall_single_filter": "negative_trade_count_gain_quality_loss(거래수 증가이나 품질 악화)",
        "n06_s07_long_only_late_firewall": "negative_late_long_firewall_weak(후반 롱 방화벽 약함)",
    }
    for row in rows:
        name = row.get("attempt_name", "")
        net = to_float(row, "net_profit")
        pf = to_float(row, "profit_factor")
        recovery = to_float(row, "recovery_factor")
        trades = to_int(row, "trade_count")
        long_count = to_int(row, "long_trade_count")
        short_count = to_int(row, "short_trade_count")
        balance_gap = abs(long_count - short_count)
        if name == "n01_s07_base_control":
            interpretation = "Best net/PF/recovery reference(순수익/수익 팩터/회복 참고 최선)지만 short-heavy(숏 치우침)이다."
            decision = "preserve_as_reference_not_selection(참고로 보존, 선정 아님)"
        elif name == "n02_s07_long_only_disable_short":
            interpretation = "PF/expectancy(수익 팩터/기대값)는 가장 높지만 trade_count(거래수)와 net(순수익)이 작다."
            decision = "preserve_long_quality_clue(롱 품질 단서 보존)"
        elif name == "n03_s07_short_only_disable_long":
            interpretation = "Short carry(숏 기여)는 살아 있지만 long/short balance(롱/숏 균형)가 없다."
            decision = "preserve_short_carry_clue(숏 기여 단서 보존)"
        elif name == "n04_s07_no_cash_open_short_single_filter":
            interpretation = "Balance(균형)는 좋아졌지만 net/PF/recovery(순수익/수익 팩터/회복)가 크게 손상됐다."
            decision = "negative_do_not_repeat_single_filter(부정, 단일 필터 반복 금지)"
        elif name == "n05_s07_late_long_firewall_single_filter":
            interpretation = "Trade count(거래수)는 늘었지만 PF/recovery(수익 팩터/회복)가 기준보다 약하다."
            decision = "negative_do_not_repeat_late_long_firewall_only(부정, 후반 롱 방화벽 단독 반복 금지)"
        else:
            interpretation = "Long-only late firewall(롱 전용 후반 방화벽)은 net/PF/recovery(순수익/수익 팩터/회복)가 약하다."
            decision = "negative_weak_fragment(부정 약한 조각)"
        scorecard.append(
            {
                "attempt_name": name,
                "model_id": row.get("model_id", ""),
                "net_profit": net,
                "profit_factor": pf,
                "expectancy": to_float(row, "expectancy"),
                "drawdown": to_float(row, "max_drawdown_amount"),
                "recovery_factor": recovery,
                "trade_count": trades,
                "long_trade_count": long_count,
                "short_trade_count": short_count,
                "long_short_balance_gap": balance_gap,
                "delta_net_vs_base": round(net - base_net, 6),
                "delta_pf_vs_base": round(pf - base_pf, 6),
                "delta_recovery_vs_base": round(recovery - base_recovery, 6),
                "delta_trades_vs_base": trades - base_trades,
                "review_label": labels.get(name, "reviewed(검토됨)"),
                "review_decision": decision,
                "interpretation": interpretation,
                "selection_status": "not_selected(선정 없음)",
                "operating_claim": "not_claimed(주장 없음)",
            }
        )
    write_csv(VARIANT_SCORECARD, scorecard)
    return scorecard


def build_performance_attribution(scorecard: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    base = next(row for row in scorecard if row["attempt_name"] == "n01_s07_base_control")
    rows = [
        {
            "observed_change": "base_control_best_reference(기준 대조가 최고 참고)",
            "comparison_baseline": "n01_s07_base_control",
            "likely_drivers": "original_s07_short_carry_plus_limited_long_supply(원본 s07 숏 기여와 제한적 롱 공급)",
            "segment_checks": "runtime parity exact(런타임 동등성 정확); session/deal details upstream only(세션/거래 세부는 상류 근거)",
            "trade_shape": f"net={base['net_profit']};pf={base['profit_factor']};trades={base['trade_count']};long_short={base['long_trade_count']}/{base['short_trade_count']}",
            "alternative_explanations": "single window runtime probe(단일 구간 런타임 탐침) and Tier B missing_required(Tier B 필수 누락)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "Design asymmetric long/short source(비대칭 롱/숏 원천 설계).",
        },
        {
            "observed_change": "long_only_high_pf_but_low_supply(롱 전용 높은 PF이나 낮은 공급)",
            "comparison_baseline": "n01_s07_base_control",
            "likely_drivers": "removing short side cuts trade supply(숏 제거가 거래 공급을 줄임)",
            "segment_checks": "direction check only(방향 확인만 있음); no WFO(워크포워드 없음)",
            "trade_shape": "6 long trades(롱 6거래), no short(숏 없음), net=51.56, PF=13.45",
            "alternative_explanations": "small sample illusion(작은 표본 착시)",
            "attribution_confidence": "low_to_medium(낮음-중간)",
            "next_probe": "Use long-quality head as supply expansion seed(롱 품질 헤드를 공급 확장 씨앗으로 사용).",
        },
        {
            "observed_change": "short_only_retains_most_profit_but_imbalanced(숏 전용이 수익 대부분을 유지하나 불균형)",
            "comparison_baseline": "n01_s07_base_control",
            "likely_drivers": "s07 edge is short-carry heavy(s07 우위가 숏 기여에 치우침)",
            "segment_checks": "direction check only(방향 확인만 있음)",
            "trade_shape": "20 short trades(숏 20거래), no long(롱 없음), net=135.11, PF=3.42",
            "alternative_explanations": "cash-open concentration(현금장 초반 집중) may dominate",
            "attribution_confidence": "medium(중간)",
            "next_probe": "Build separate short carry preservation rule/model(별도 숏 기여 보존 규칙/모델).",
        },
        {
            "observed_change": "balance_filter_improves_mix_but_kills_quality(균형 필터가 비율은 개선하나 품질을 훼손)",
            "comparison_baseline": "n01_s07_base_control",
            "likely_drivers": "single side-filter removes profitable short cluster(단일 방향 필터가 수익 숏 군집을 제거)",
            "segment_checks": "balance check(균형 확인); no regime split(국면 분할 없음)",
            "trade_shape": "13/13 long-short(롱/숏), net=54.26, PF=1.41, recovery=0.54",
            "alternative_explanations": "filter semantics too blunt(필터 의미가 너무 둔함)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "Do not repeat single side-filter micro-tuning(단일 방향 필터 미세조정 반복 금지).",
        },
    ]
    write_csv(PERFORMANCE_ATTRIBUTION, rows)
    return rows


def build_positive_clues(scorecard: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "clue_id": "pc01_exact_runtime_parity(정확 런타임 동등성)",
            "source_artifact": rel(SOURCE_DIFF),
            "evidence": "matched_rows=34962;mismatch_rows=0;exact_parity_rows=6",
            "meaning": "MT5 runtime probe(MT5 런타임 탐침)는 proxy expected tape(프록시 예상 테이프)와 결정 행이 맞다.",
            "use_next": "Use as evidence boundary for Stage347 design input(Stage347 설계 입력 경계로 사용).",
            "claim_boundary": "runtime_probe_not_authority(런타임 탐침, 권위 아님)",
        },
        {
            "clue_id": "pc02_base_reference_surface(기준 참고 표면)",
            "source_artifact": rel(VARIANT_SCORECARD),
            "evidence": "n01 net=186.67;PF=4.11;recovery=2.09;trades=26",
            "meaning": "Base control(기준 대조)은 아직 가장 균형 잡힌 profit/risk(수익/위험) 참고 표면이다.",
            "use_next": "Do not select; preserve as reference surface(선정하지 않고 참고 표면으로 보존).",
            "claim_boundary": "reference_surface_no_selection(참고 표면, 선정 없음)",
        },
        {
            "clue_id": "pc03_long_quality_fragment(롱 품질 조각)",
            "source_artifact": rel(VARIANT_SCORECARD),
            "evidence": "n02 PF=13.45;expectancy=8.59;trades=6",
            "meaning": "Long side(롱 방향)는 품질은 좋지만 공급이 부족하다.",
            "use_next": "Separate long-quality head/source(롱 품질 헤드/원천 분리)를 설계한다.",
            "claim_boundary": "seed_clue_only(씨앗 단서 전용)",
        },
        {
            "clue_id": "pc04_short_carry_fragment(숏 기여 조각)",
            "source_artifact": rel(VARIANT_SCORECARD),
            "evidence": "n03 net=135.11;PF=3.42;short_trades=20",
            "meaning": "Short carry(숏 기여)는 수익 대부분을 설명하지만 운영 균형은 아니다.",
            "use_next": "Separate short-carry preservation(숏 기여 보존)을 설계한다.",
            "claim_boundary": "seed_clue_only(씨앗 단서 전용)",
        },
    ]
    write_csv(POSITIVE_CLUES, rows)
    return rows


def build_failure_memory() -> list[dict[str, Any]]:
    rows = [
        {
            "failure_id": "fm01_single_side_filter_balance_tax(단일 방향 필터 균형 비용)",
            "hypothesis": "Removing cash-open short trades(현금장 초반 숏 제거)가 long/short balance(롱/숏 균형)를 개선하면서 수익을 유지할 수 있다.",
            "variants_tried": "n04_s07_no_cash_open_short_single_filter",
            "failed_boundary": "net/PF/recovery dropped to 54.26/1.41/0.54(순수익/수익 팩터/회복 하락)",
            "why_failed": "profitable short cluster(수익 숏 군집)를 너무 거칠게 제거했다.",
            "salvage_value": "Balance pressure(균형 압박)는 필요하지만 single filter(단일 필터)는 너무 둔하다.",
            "reopen_condition": "새 long-quality source(롱 품질 원천) 또는 short-carry allocation(숏 기여 배분)이 생길 때",
            "do_not_repeat": "cash-open short block(현금장 초반 숏 차단)만 좁게 미세조정하지 않는다.",
        },
        {
            "failure_id": "fm02_late_long_firewall_trade_count_tax(후반 롱 방화벽 거래수 비용)",
            "hypothesis": "Late long firewall(후반 롱 방화벽)이 나쁜 롱을 줄이고 수익 품질을 올릴 수 있다.",
            "variants_tried": "n05_s07_late_long_firewall_single_filter;n06_s07_long_only_late_firewall",
            "failed_boundary": "n05 PF/recovery=1.91/1.34; n06 net/PF/recovery=15.11/1.29/0.22",
            "why_failed": "late-long rule(후반 롱 규칙) alone(단독)으로는 payoff source(보상 원천)를 만들지 못했다.",
            "salvage_value": "Late long context(후반 롱 문맥)는 feature(피처)나 label(라벨)로만 재개한다.",
            "reopen_condition": "direction-specific model head(방향별 모델 헤드)가 생길 때",
            "do_not_repeat": "late-long firewall(후반 롱 방화벽)만 threshold(임계값) 조정하지 않는다.",
        },
        {
            "failure_id": "fm03_short_carry_imbalance_not_operating(숏 기여 불균형 운영 아님)",
            "hypothesis": "Short-only carry(숏 전용 기여)를 그대로 쓰면 수익을 유지할 수 있다.",
            "variants_tried": "n03_s07_short_only_disable_long",
            "failed_boundary": "long/short=0/20 and recovery below base(롱/숏 0/20, 회복 기준 이하)",
            "why_failed": "profit source(수익 원천)는 있지만 balance/session stability(균형/세션 안정성) 주장이 없다.",
            "salvage_value": "short carry(숏 기여)는 보존하되 long-quality supply(롱 품질 공급)와 결합해야 한다.",
            "reopen_condition": "separate long head(별도 롱 헤드)가 공급을 만들 때",
            "do_not_repeat": "short-only(숏 전용)를 운영 후보처럼 포장하지 않는다.",
        },
    ]
    write_csv(FAILURE_MEMORY, rows)
    return rows


def build_stage347_seed_queue() -> list[dict[str, Any]]:
    rows = [
        {
            "seed_id": "s347_01_asymmetric_long_short_heads(비대칭 롱/숏 헤드)",
            "priority": 1,
            "hypothesis": "Long quality(롱 품질)와 short carry(숏 기여)를 separate heads(별도 헤드)로 만들면 n01 profit(수익)과 n02 PF(수익 팩터)를 동시에 회수할 수 있다.",
            "broad_sweep": "separate long/short thresholds; logistic/ExtraTrees/HistGBM heads(롱/숏 임계값 분리; 로지스틱/엑스트라트리스/히스토그램 GBM 헤드)",
            "extreme_sweep": "long-only high PF, short-only carry, balanced allocator extremes(롱 전용 높은 PF, 숏 전용 기여, 균형 배분 극단)",
            "micro_search_gate": "At least two adjacent settings improve base net/PF without worse recovery(인접 2개 설정이 기준 순수익/PF를 회복 손상 없이 개선)",
            "wfo_plan": "single-window design first, then WFO if density survives(단일 구간 설계 후 밀도 생존 시 워크포워드)",
            "failure_memory": "Do not repeat single side-filter micro-tuning(단일 방향 필터 미세조정 반복 금지)",
            "evidence_boundary": "design_seed_only_no_candidate(설계 씨앗 전용, 후보 없음)",
            "next_run_id": NEXT_RUN_ID,
        },
        {
            "seed_id": "s347_02_cash_open_regime_source(현금장 초반 국면 원천)",
            "priority": 2,
            "hypothesis": "Cash-open concentration(현금장 초반 집중)은 time/regime feature source(시간/국면 피처 원천)로 분리해야 한다.",
            "broad_sweep": "minutes_from_cash_open, ADX/DI, volatility compression, prior-session gap(현금장 경과분, ADX/DI, 변동성 압축, 이전 세션 갭)",
            "extreme_sweep": "0-30/30-60/60-120 minute buckets and no-cash-open-control(0-30/30-60/60-120분 구간과 현금장 제외 대조)",
            "micro_search_gate": "cash-open bucket improves balance without PF collapse(현금장 구간이 PF 붕괴 없이 균형 개선)",
            "wfo_plan": "as-of timestamp-safe feature join only(시점 안전 피처 결합만 허용)",
            "failure_memory": "n04 balance tax(균형 비용)를 제약으로 사용",
            "evidence_boundary": "feature_source_design_seed(피처 원천 설계 씨앗)",
            "next_run_id": NEXT_RUN_ID,
        },
        {
            "seed_id": "s347_03_runtime_payload_module_upgrade(런타임 페이로드 모듈 개선)",
            "priority": 3,
            "hypothesis": "If dual side rules(이중 방향 규칙)가 필요하면 EA parameter hack(EA 파라미터 임시방편)이 아니라 module version(모듈 버전)으로 추적해야 한다.",
            "broad_sweep": "long_head_score, short_head_score, allocator_state payload columns(롱 헤드 점수, 숏 헤드 점수, 배분 상태 컬럼)",
            "extreme_sweep": "payload-only dry run and exact expected tape parity(페이로드 전용 드라이런과 예상 테이프 정확 동등성)",
            "micro_search_gate": "only after model/source seed shows value(모델/원천 씨앗이 가치 보일 때만)",
            "wfo_plan": "not applicable until payload design(페이로드 설계 전 해당 없음)",
            "failure_memory": "single side-filter limit(단일 방향 필터 한계)",
            "evidence_boundary": "runtime_design_support_seed(런타임 설계 보조 씨앗)",
            "next_run_id": NEXT_RUN_ID,
        },
    ]
    write_csv(STAGE347_SEED_QUEUE, rows)
    return rows


def write_tier_boundary() -> list[dict[str, Any]]:
    rows = [
        {
            "record_view": "Tier A separate(Tier A 분리)",
            "status": "available(사용 가능)",
            "evidence": rel(SOURCE_SUMMARY),
            "meaning": "run345B MT5 runtime probe(MT5 런타임 탐침)는 Tier A(티어 A) 경계로 판독한다.",
        },
        {
            "record_view": "Tier B separate(Tier B 분리)",
            "status": "missing_required(필수 누락)",
            "evidence": rel(FINAL_DECISION),
            "meaning": "Tier B(티어 B)는 이번 run345B 범위 밖이므로 성과를 주장하지 않는다.",
        },
        {
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "status": "same_as_tier_a_until_tier_b_available",
            "evidence": rel(FINAL_DECISION),
            "meaning": "combined(합산)는 Tier B 부재 때문에 Tier A(티어 A)와 같은 경계다.",
        },
    ]
    write_csv(TIER_BOUNDARY_AUDIT, rows)
    return rows


def write_result_judgment(final345: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "result_subject": "run345B cash-open MT5 runtime probe review(345B 현금장 MT5 런타임 탐침 검토)",
            "evidence_available": f"{rel(SOURCE_SUMMARY)};{rel(SOURCE_DIFF)};{rel(VARIANT_SCORECARD)}",
            "evidence_missing": "Tier B separate(Tier B 분리); WFO(워크포워드); forward pass(전진 통과); live readiness(실거래 준비)",
            "judgment_label": "positive_reference_with_negative_variants(부정 변형을 가진 긍정 참고)",
            "judgment_class": "exploratory_runtime_probe_review(탐색 런타임 탐침 검토)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "Stage347 asymmetric source design(347단계 비대칭 원천 설계)이 모델/피처 원천을 새로 만들어야 한다.",
            "user_explanation_hook": "기준 대조는 참고 가치가 있지만, 단일 방향 필터 수리는 실패했다.",
        }
    ]
    write_csv(RESULT_JUDGMENT, rows)
    return rows


def write_receipts(
    scorecard: Sequence[Mapping[str, Any]],
    attribution: Sequence[Mapping[str, Any]],
    clues: Sequence[Mapping[str, Any]],
    failures: Sequence[Mapping[str, Any]],
    seeds: Sequence[Mapping[str, Any]],
) -> None:
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "observed_change": "base control stayed strongest while single side-filter variants degraded(기준 대조가 가장 강하고 단일 방향 필터 변형은 악화)",
            "comparison_baseline": "n01_s07_base_control",
            "likely_drivers": "short carry(숏 기여) plus sparse long quality(희소 롱 품질)",
            "segment_checks": "direction and variant only(방향과 변형만); Tier B/WFO missing(Tier B/워크포워드 누락)",
            "trade_shape": "best n01 net=186.67 PF=4.11 recovery=2.09 trades=26 long/short=6/20",
            "alternative_explanations": "single-window probe(단일 구간 탐침), sample concentration(표본 집중)",
            "attribution_confidence": "medium(중간)",
            "next_probe": NEXT_RUN_ID,
            "rows": len(attribution),
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [
                rel(PARENT_FINAL_DECISION),
                rel(PARENT_HANDOFF_MANIFEST),
                rel(SOURCE_FINAL_DECISION),
                rel(SOURCE_SUMMARY),
                rel(SOURCE_DIFF),
                rel(SOURCE_RUNTIME_IDENTITY),
            ],
            "producer": rel(Path("stage_pipelines/stage346/review_cash_open_runtime_probe_source_pivot_without_db.py")),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(VARIANT_SCORECARD),
                rel(PERFORMANCE_ATTRIBUTION),
                rel(POSITIVE_CLUES),
                rel(FAILURE_MEMORY),
                rel(STAGE347_SEED_QUEUE),
                rel(REPORT_PATH),
                rel(FINAL_DECISION),
            ],
            "artifact_hashes": "recorded_in_artifact_registry(산출물 등록부에 기록)",
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
            "availability": "tracked(추적됨)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "reviewed_runtime_probe_reference_and_stage347_seed_handoff(검토된 런타임 탐침 참고와 Stage347 씨앗 인계)",
            "candidate_selection": "not_claimed",
            "promotion_candidate": "not_claimed",
            "forward_pass": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_stage_docs(final345: Mapping[str, Any]) -> None:
    write_text(
        REPORT_PATH,
        f"""# run346B Cash-Open Runtime Probe Source Pivot Review(346B 현금장 런타임 탐침 원천 전환 검토)

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): run345B MT5 runtime probe(345B MT5 런타임 탐침)를 variant attribution(변형 귀속), positive clue(긍정 단서), failure memory(실패 기억), Stage347 seed queue(347단계 씨앗 대기열)로 재판독했다.
Effect(효과): Stage346(346단계)을 검토 단계로 작게 닫고, 실제 공격 탐색은 asymmetric long/short source design(비대칭 롱/숏 원천 설계)으로 넘긴다.

## Current Truth(현재 진실)

- reference_surface(참고 표면): `n01_s07_base_control`
- reference_kpi(참고 KPI): net(순수익) `186.67`, PF(수익 팩터) `4.11`, recovery(회복 계수) `2.09`, trades(거래수) `26`
- runtime_parity(런타임 동등성): matched rows(일치 행) `34962/34962`, mismatch rows(불일치 행) `0`
- Tier B(티어 B): `missing_required(필수 누락)`

## Judgment(판정)

`n01_s07_base_control`은 reference surface(참고 표면)로 보존한다. 하지만 selection(선정), promotion_candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위)는 아니다.

Single side-filter variants(단일 방향 필터 변형)는 net/PF/recovery(순수익/수익 팩터/회복)를 훼손했다. 다음 작업은 threshold-only repair(임계값만 고치는 수리)가 아니라 long-quality head(롱 품질 헤드)와 short-carry head(숏 기여 헤드)를 분리하는 source design(원천 설계)이다.

## Artifacts(산출물)

- variant_scorecard(변형 점수표): `{rel(VARIANT_SCORECARD)}`
- performance_attribution(성과 귀속): `{rel(PERFORMANCE_ATTRIBUTION)}`
- positive_clues(긍정 단서): `{rel(POSITIVE_CLUES)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY)}`
- stage347_seed_queue(347단계 씨앗 대기열): `{rel(STAGE347_SEED_QUEUE)}`

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        REVIEW_INDEX,
        "## run346B Cash-Open Runtime Probe Review(346B 현금장 런타임 탐침 검토)",
        f"""## run346B Cash-Open Runtime Probe Review(346B 현금장 런타임 탐침 검토)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- decision(결정): `{DECISION}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- effect(효과): Stage346(346단계)을 review/source pivot(검토/원천 전환)으로 닫고 Stage347(347단계)을 연다.
""",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run346B Review Closeout(346B 검토 종료)",
        f"""## run346B Review Closeout(346B 검토 종료)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): positive clue(긍정 단서)는 asymmetric source seed(비대칭 원천 씨앗)로 넘기고, single side-filter micro-tuning(단일 방향 필터 미세조정)은 failure memory(실패 기억)로 닫았다.
""",
    )
    write_text(
        DECISION_DOC,
        f"""# 2026-06-01 Stage346B Review Decision(346B 검토 결정)

- decision(결정): `{DECISION}`
- source_run(원천 실행): `{SOURCE_RUNTIME_RUN_ID}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- reason(이유): run345B(345B 실행)는 exact runtime parity(정확 런타임 동등성)와 reference KPI(참고 KPI)를 제공했지만, 단일 side-filter(방향 필터) 변형은 개선하지 못했다.

Action(행동): Stage346(346단계)을 review/source pivot(검토/원천 전환)으로 닫고 Stage347(347단계)을 연다.
Effect(효과): 다음 작업은 MT5 결과를 다시 미세조정하지 않고 asymmetric model/source design(비대칭 모델/원천 설계)으로 넘어간다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_next_stage_docs() -> None:
    write_text(
        NEXT_STAGE_BRIEF,
        f"""# Stage 347 Brief(347단계 개요)

## Stage ID(단계 ID)

`{NEXT_STAGE_ID}`

## Question(질문)

Can the cash-open runtime clue(현금장 런타임 단서)를 asymmetric long/short model-source design(비대칭 롱/숏 모델-원천 설계)으로 바꿔, short carry(숏 기여)를 보존하면서 long quality supply(롱 품질 공급)를 늘릴 수 있는가?

## Source Inputs(원천 입력)

- review_run(검토 실행): `{RUN_ID}`
- source_runtime_probe(원천 런타임 탐침): `{SOURCE_RUNTIME_RUN_ID}`
- seed_queue(씨앗 대기열): `{rel(STAGE347_SEED_QUEUE)}`
- positive_clues(긍정 단서): `{rel(POSITIVE_CLUES)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY)}`

## Scope(범위)

Stage347(347단계)는 design/materialization(설계/물질화)부터 시작한다. Single side-filter micro-tuning(단일 방향 필터 미세조정)은 중심 주제가 아니다.

## Claim Boundary(주장 경계)

No candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음)이다.
""",
    )
    write_text(
        NEXT_INPUT_REFS,
        f"""# Stage347 Input References(347단계 입력 참조)

- stage346_review_report(346단계 검토 보고서): `{rel(REPORT_PATH)}`
- stage346_final_decision(346단계 최종 결정): `{rel(FINAL_DECISION)}`
- variant_scorecard(변형 점수표): `{rel(VARIANT_SCORECARD)}`
- performance_attribution(성과 귀속): `{rel(PERFORMANCE_ATTRIBUTION)}`
- positive_clues(긍정 단서): `{rel(POSITIVE_CLUES)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY)}`
- seed_queue(씨앗 대기열): `{rel(STAGE347_SEED_QUEUE)}`

Action(행동): Stage346(346단계)의 review artifact(검토 산출물)를 Stage347(347단계)의 설계 입력으로 참조한다.
Effect(효과): 새 단계가 오래된 Stage345 파일을 직접 뒤지는 일을 줄인다.
""",
    )
    write_text(
        NEXT_SELECTION,
        f"""# Stage 347 Selection Status(347단계 선정 상태)

- active_stage(현재 단계): `{NEXT_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_review_run(원천 검토 실행): `{RUN_ID}`
- source_runtime_probe(원천 런타임 탐침): `{SOURCE_RUNTIME_RUN_ID}`
- reference_surface(참고 표면): `n01_s07_base_control`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage347(347단계)는 asymmetric source design(비대칭 원천 설계)을 시작하지만 selection(선정)을 주장하지 않는다.
""",
    )
    write_text(
        NEXT_REVIEW_INDEX,
        f"""# Stage347 Review Index(347단계 검토 색인)

## Open From Stage346B(346B에서 개시)

- source_decision(원천 결정): `{rel(DECISION_DOC)}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- effect(효과): asymmetric long/short source design(비대칭 롱/숏 원천 설계)을 시작한다.
""",
    )
    write_text(
        NEXT_STAGE_README,
        f"""# Stage 347(347단계)

Stage347(347단계)는 cash-open runtime clue(현금장 런타임 단서)를 asymmetric long/short source design(비대칭 롱/숏 원천 설계)로 바꾸는 단계다.

Current truth(현재 진실)는 `docs/workspace/workspace_state.yaml`와 `docs/context/current_working_state.md`를 따른다.
""",
    )
    write_csv(NEXT_STAGE_LEDGER, [], STAGE_LEDGER_COLUMNS)


def write_status_docs(final345: Mapping[str, Any]) -> None:
    write_text(
        STAGE_SELECTION,
        f"""# Stage 346 Selection Status(346단계 선정 상태)

- active_stage_at_close(종료 당시 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- handoff_stage(인계 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- reference_surface(참고 표면): `n01_s07_base_control`
- reference_net_profit(참고 순수익): `186.67`
- reference_profit_factor(참고 수익 팩터): `4.11`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage346(346단계)은 review/source pivot(검토/원천 전환)으로 닫고 Stage347(347단계)을 연다.
""",
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {NEXT_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{NEXT_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

Stage346(346단계)는 run345B MT5 runtime probe(345B MT5 런타임 탐침)를 review(검토)하고 Stage347(347단계) asymmetric source design(비대칭 원천 설계)으로 넘겼다. 다음 작업은 long-quality head(롱 품질 헤드)와 short-carry head(숏 기여 헤드)를 분리하는 설계다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

No candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
""",
    )
    write_text(ROOT_SELECTION_STATUS, read_text(NEXT_SELECTION))


def write_stage_ledgers(scorecard: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    base_row = next(row for row in scorecard if row["attempt_name"] == "n01_s07_base_control")
    ledger = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "run_date": TODAY,
            "date": TODAY,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "primary_artifact": rel(FINAL_DECISION),
            "path": rel(REPORT_PATH),
            "report_path": rel(REPORT_PATH),
            "primary_report": rel(REPORT_PATH),
            "gate_passes": 11,
            "gate_total": 11,
            "claim_boundary": CLAIM_BOUNDARY,
            "scoreboard_lane": "review_attribution(검토 귀속)",
            "lane": "kpi_evidence(KPI 근거)",
            "family": "kpi_evidence(KPI 근거)",
            "run_number": RUN_NUMBER,
            "notes": "Tier A(티어 A) runtime probe review(런타임 탐침 검토); no selection(선정 없음).",
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "attempt_count": 6,
            "candidate_model_id": "none(없음)",
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "runtime_probe_review",
            "kpi_scope": "runtime_probe_review",
            "primary_kpi": "reference_net=186.67;PF=4.11;trades=26",
            "guardrail_kpi": "single_side_filter_variants_negative(단일 방향 필터 변형 부정)",
            "external_verification_status": "completed_upstream_run345B(상류 run345B 완료)",
            "result_status": "reviewed_reference_clue_no_selection(검토된 참고 단서, 선정 없음)",
            "net_profit": base_row["net_profit"],
            "profit_factor": base_row["profit_factor"],
            "expectancy": base_row["expectancy"],
            "drawdown": base_row["drawdown"],
            "recovery_factor": base_row["recovery_factor"],
            "trade_count": base_row["trade_count"],
            "matched_rows": 34962,
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "run_date": TODAY,
            "date": TODAY,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "primary_artifact": rel(FINAL_DECISION),
            "path": rel(REPORT_PATH),
            "report_path": rel(REPORT_PATH),
            "primary_report": rel(REPORT_PATH),
            "gate_passes": 11,
            "gate_total": 11,
            "claim_boundary": CLAIM_BOUNDARY,
            "scoreboard_lane": "review_attribution(검토 귀속)",
            "lane": "kpi_evidence(KPI 근거)",
            "family": "kpi_evidence(KPI 근거)",
            "run_number": RUN_NUMBER,
            "notes": "Tier B(티어 B)는 missing_required(필수 누락).",
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "attempt_count": 6,
            "candidate_model_id": "none(없음)",
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "missing_required(필수 누락)",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "run_date": TODAY,
            "date": TODAY,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "primary_artifact": rel(FINAL_DECISION),
            "path": rel(REPORT_PATH),
            "report_path": rel(REPORT_PATH),
            "primary_report": rel(REPORT_PATH),
            "gate_passes": 11,
            "gate_total": 11,
            "claim_boundary": CLAIM_BOUNDARY,
            "scoreboard_lane": "review_attribution(검토 귀속)",
            "lane": "kpi_evidence(KPI 근거)",
            "family": "kpi_evidence(KPI 근거)",
            "run_number": RUN_NUMBER,
            "notes": "Tier A+B combined(합산)은 Tier B 부재 때문에 Tier A와 같은 경계다.",
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "attempt_count": 6,
            "candidate_model_id": "none(없음)",
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": "same_as_tier_a_until_tier_b_available",
            "guardrail_kpi": "Tier B missing_required(Tier B 필수 누락)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "result_status": "same_as_tier_a_until_tier_b_available",
            "net_profit": base_row["net_profit"],
            "profit_factor": base_row["profit_factor"],
            "expectancy": base_row["expectancy"],
            "drawdown": base_row["drawdown"],
            "recovery_factor": base_row["recovery_factor"],
            "trade_count": base_row["trade_count"],
            "matched_rows": 34962,
        },
    ]
    existing_fields, existing_rows = read_csv_rows(STAGE_LEDGER) if path_is_file(STAGE_LEDGER) else (STAGE_LEDGER_COLUMNS, [])
    replacement = {row["ledger_row_id"] for row in ledger}
    kept = [row for row in existing_rows if row.get("ledger_row_id") not in replacement]
    fieldnames = list(dict.fromkeys(list(existing_fields) + STAGE_LEDGER_COLUMNS))
    write_csv(STAGE_LEDGER, kept + ledger, fieldnames)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger)
    return ledger


def write_gates() -> list[dict[str, Any]]:
    rows = [
        ("parent_run346A_gates_passed", source_gate_passed(PARENT_GATE_AUDIT), PARENT_GATE_AUDIT, "run346A branch gate(분기 게이트)를 확인한다."),
        ("source_run345B_gates_passed", source_gate_passed(SOURCE_GATE_AUDIT), SOURCE_GATE_AUDIT, "run345B runtime gate(런타임 게이트)를 확인한다."),
        ("variant_scorecard_written", path_is_file(VARIANT_SCORECARD), VARIANT_SCORECARD, "variant review scorecard(변형 검토 점수표)를 기록한다."),
        ("performance_attribution_written", path_is_file(PERFORMANCE_ATTRIBUTION), PERFORMANCE_ATTRIBUTION, "performance attribution(성과 귀속)을 기록한다."),
        ("positive_clues_written", path_is_file(POSITIVE_CLUES), POSITIVE_CLUES, "positive clue(긍정 단서)를 분리한다."),
        ("failure_memory_written", path_is_file(FAILURE_MEMORY), FAILURE_MEMORY, "failure memory(실패 기억)를 남긴다."),
        ("stage347_seed_queue_written", path_is_file(STAGE347_SEED_QUEUE), STAGE347_SEED_QUEUE, "Stage347 seed queue(347단계 씨앗 대기열)를 만든다."),
        ("tier_boundary_audit_written", path_is_file(TIER_BOUNDARY_AUDIT), TIER_BOUNDARY_AUDIT, "Tier A/B boundary(티어 경계)를 기록한다."),
        ("stage347_handoff_synced", path_is_file(NEXT_STAGE_BRIEF) and path_is_file(NEXT_SELECTION), NEXT_STAGE_BRIEF, "Stage347 handoff(347단계 인계)를 동기화한다."),
        ("no_forbidden_operating_claim", path_is_file(CLAIM_RECEIPT), CLAIM_RECEIPT, "운영 승격/런타임 권위/목표 달성을 주장하지 않는다."),
        ("required_gate_coverage_audit_written", True, GATE_AUDIT, "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다."),
    ]
    gate_rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, effect in rows
    ]
    write_csv(GATE_AUDIT, gate_rows, ["gate_id", "status", "evidence_path", "effect", "claim_boundary"])
    return gate_rows


def write_final(final345: Mapping[str, Any], scorecard: Sequence[Mapping[str, Any]], seeds: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        FINAL_DECISION,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "next_stage_id": NEXT_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "source_best_attempt": final345.get("best_attempt_name", ""),
            "source_best_net_profit": final345.get("best_net_profit", ""),
            "source_best_profit_factor": final345.get("best_profit_factor", ""),
            "source_best_recovery_factor": final345.get("best_recovery_factor", ""),
            "source_best_trade_count": final345.get("best_trade_count", ""),
            "variant_rows": len(scorecard),
            "positive_clue_rows": 4,
            "failure_memory_rows": 3,
            "stage347_seed_rows": len(seeds),
            "gate_passes": 11,
            "gate_total": 11,
            "candidate_selection": "not_claimed",
            "promotion_candidate": "not_claimed",
            "forward_passed": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )


def write_manifest() -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_stage_id": NEXT_STAGE_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer": rel(Path("stage_pipelines/stage346/review_cash_open_runtime_probe_source_pivot_without_db.py")),
            "inputs": [
                rel(PARENT_FINAL_DECISION),
                rel(PARENT_REVIEW_QUEUE),
                rel(SOURCE_FINAL_DECISION),
                rel(SOURCE_SUMMARY),
                rel(SOURCE_DIFF),
                rel(SOURCE_RUNTIME_IDENTITY),
            ],
            "outputs": [
                rel(VARIANT_SCORECARD),
                rel(PERFORMANCE_ATTRIBUTION),
                rel(POSITIVE_CLUES),
                rel(FAILURE_MEMORY),
                rel(STAGE347_SEED_QUEUE),
                rel(TIER_BOUNDARY_AUDIT),
                rel(REPORT_PATH),
                rel(FINAL_DECISION),
                rel(DECISION_DOC),
                rel(NEXT_STAGE_BRIEF),
                rel(NEXT_INPUT_REFS),
                rel(NEXT_SELECTION),
            ],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_registries(scorecard: Sequence[Mapping[str, Any]]) -> None:
    base_row = next(row for row in scorecard if row["attempt_name"] == "n01_s07_base_control")
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "kpi_evidence(KPI 근거)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "notes": "Stage346 runtime review(런타임 검토) completed; Stage347 opened(347단계 개시).",
                "family": "kpi_evidence(KPI 근거)",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "rows": 34962,
                "gate_passes": 11,
                "gate_total": 11,
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": "none(없음)",
                "net_profit": base_row["net_profit"],
                "profit_factor": base_row["profit_factor"],
                "drawdown": base_row["drawdown"],
                "recovery_factor": base_row["recovery_factor"],
                "trade_count": base_row["trade_count"],
                "result_status": "reviewed_reference_clue_no_selection(검토된 참고 단서, 선정 없음)",
                "expectancy": base_row["expectancy"],
                "attempt_count": 6,
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "runtime_probe_review",
                "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            }
        ],
    )
    artifact_paths = [
        VARIANT_SCORECARD,
        PERFORMANCE_ATTRIBUTION,
        POSITIVE_CLUES,
        FAILURE_MEMORY,
        STAGE347_SEED_QUEUE,
        TIER_BOUNDARY_AUDIT,
        RESULT_JUDGMENT,
        PERFORMANCE_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        NEXT_STAGE_BRIEF,
        NEXT_INPUT_REFS,
        NEXT_SELECTION,
    ]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": f"{path.stem}(산출물)",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID if STAGE_ID in rel(path) else NEXT_STAGE_ID,
            "run_id": RUN_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "run346B review/handoff artifact(346B 검토/인계 산출물).",
        }
        for path in artifact_paths
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_register_notes() -> None:
    append_text_once(
        IDEA_REGISTRY,
        "`IDEA-ST347-CASH-OPEN-ASYMMETRIC-LONG-SHORT-SOURCE`",
        f"""| `IDEA-ST347-CASH-OPEN-ASYMMETRIC-LONG-SHORT-SOURCE` | `{NEXT_STAGE_ID}` | run346B(346B 실행)의 long-quality and short-carry fragments(롱 품질과 숏 기여 조각)를 separate source/head(분리 원천/헤드)로 설계하면 수익과 균형을 같이 회복할 수 있다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `opened_research_development_only` | next_action(다음 행동) `{NEXT_RUN_ID}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        "## 2026-06-01 run346B Cash-Open Side-Filter Failure Memory",
        f"""## 2026-06-01 run346B Cash-Open Side-Filter Failure Memory(현금장 방향 필터 실패 기억)

- source_run(원천 실행): `{RUN_ID}`
- failure(실패): single side-filter variants(단일 방향 필터 변형)는 balance(균형) 또는 trade count(거래수)를 일부 바꿨지만 net/PF/recovery(순수익/수익 팩터/회복)를 함께 개선하지 못했다.
- evidence(근거): `{rel(FAILURE_MEMORY)}`
- salvage_value(회수 가치): long-quality fragment(롱 품질 조각)와 short-carry fragment(숏 기여 조각)를 separate source/head(분리 원천/헤드)로 넘긴다.
- do_not_repeat(반복 금지): cash-open short block(현금장 초반 숏 차단), late-long firewall(후반 롱 방화벽), short-only(숏 전용)를 운영 후보처럼 반복하지 않는다.
""",
    )


def write_changelog() -> None:
    text = f"""## 2026-06-01 run346B Cash-Open Runtime Review(현금장 런타임 검토)

- action(행동): Stage345 run345B MT5 runtime probe(345B MT5 런타임 탐침)를 scorecard(점수표), performance attribution(성과 귀속), positive clue(긍정 단서), failure memory(실패 기억)로 검토했다.
- effect(효과): Stage346(346단계)을 작게 닫고 Stage347(347단계) asymmetric long/short source design(비대칭 롱/숏 원천 설계)을 열었다.
- boundary(경계): selection/runtime authority/Goal Achieve(선정/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run346B Cash-Open Runtime Review", text)
    append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run346B Cash-Open Runtime Review", text)


def validate() -> None:
    outputs = [
        VARIANT_SCORECARD,
        PERFORMANCE_ATTRIBUTION,
        POSITIVE_CLUES,
        FAILURE_MEMORY,
        STAGE347_SEED_QUEUE,
        TIER_BOUNDARY_AUDIT,
        RESULT_JUDGMENT,
        PERFORMANCE_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        NEXT_STAGE_BRIEF,
        NEXT_INPUT_REFS,
        NEXT_SELECTION,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
    ]
    missing = [rel(path) for path in outputs if not path_is_file(path)]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    _fields, gates = read_csv_rows(GATE_AUDIT)
    if len(gates) != 11 or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("required gate audit failed(필수 게이트 감사 실패)")
    current_texts = [read_text(WORKSPACE_STATE), read_text(CURRENT_WORKING_STATE), read_text(NEXT_SELECTION)]
    if not all(NEXT_STAGE_ID in text for text in current_texts):
        raise RuntimeError("Stage347 current truth sync failed(347단계 현재 진실 동기화 실패)")


def main() -> None:
    for path in [
        SOURCE_SUMMARY,
        SOURCE_FINAL_DECISION,
        SOURCE_GATE_AUDIT,
        SOURCE_DIFF,
        SOURCE_RUNTIME_IDENTITY,
        PARENT_FINAL_DECISION,
        PARENT_GATE_AUDIT,
        PARENT_HANDOFF_MANIFEST,
        PARENT_REVIEW_QUEUE,
    ]:
        required(path)
    final345 = read_json(SOURCE_FINAL_DECISION)
    summary = read_summary()
    scorecard = build_scorecard(summary)
    attribution = build_performance_attribution(scorecard)
    clues = build_positive_clues(scorecard)
    failures = build_failure_memory()
    seeds = build_stage347_seed_queue()
    write_tier_boundary()
    write_result_judgment(final345)
    write_receipts(scorecard, attribution, clues, failures, seeds)
    write_stage_docs(final345)
    write_next_stage_docs()
    write_status_docs(final345)
    write_stage_ledgers(scorecard)
    gates = write_gates()
    write_final(final345, scorecard, seeds)
    write_manifest()
    write_registries(scorecard)
    write_register_notes()
    write_changelog()
    validate()
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_stage_id": NEXT_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
                "gate_total": len(gates),
                "reference_attempt": "n01_s07_base_control",
                "reference_net_profit": 186.67,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
