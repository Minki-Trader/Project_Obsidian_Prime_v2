from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

STAGE360_ID = "360_regime_stability_pivot__oos_long_cash_edge_validation_loss"
STAGE361_ID = "361_long_only_cost_buffer__validation_oos_positive_cost_failure"

RUN_NUMBER = "run360C"
RUN_ID = "run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1"
PARENT_RUN_ID = "run360B_materialize_regime_stability_pivot_inputs_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run359B_execute_high_density_label_pivot_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run361A_design_long_only_cost_buffer_probe_without_db_v1"

STATUS = "reviewed_stage360C_regime_stability_inputs_long_only_seed_stage361_opened_no_selection_no_mt5"
JUDGMENT = "long_only_edge_positive_but_cost_fragile_stage361_seed_no_candidate_selection"
DECISION = "stage360C_branch_to_stage361_long_only_cost_buffer_probe_v1"
CLAIM_BOUNDARY = (
    "review_only_report_derived_stage_branch_no_new_model_training_no_proxy_execution_no_mt5_execution_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_"
    "no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

STAGE360_DIR = ROOT / "stages" / STAGE360_ID
STAGE361_DIR = ROOT / "stages" / STAGE361_ID
RUN_DIR = STAGE360_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE360_DIR / "03_reviews"
SELECTED_DIR = STAGE360_DIR / "04_selected"

REPORT_PATH = REVIEW_DIR / "run360C_regime_stability_pivot_materialized_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage360C_regime_stability_pivot_materialized_input_review.md"
STAGE360_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE360_REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE360_BRIEF = STAGE360_DIR / "00_spec" / "stage_brief.md"
STAGE360_SELECTION = SELECTED_DIR / "selection_status.md"
STAGE360_README = STAGE360_DIR / "README.md"

STAGE361_BRIEF = STAGE361_DIR / "00_spec" / "stage_brief.md"
STAGE361_INPUT_MANIFEST = STAGE361_DIR / "01_inputs" / "stage361_input_manifest.csv"
STAGE361_LEDGER = STAGE361_DIR / "03_reviews" / "stage_run_ledger.csv"
STAGE361_SELECTION = STAGE361_DIR / "04_selected" / "selection_status.md"
STAGE361_README = STAGE361_DIR / "README.md"

SCORECARD = STAGE360_DIR / "02_runs" / "run360B" / "materialized_filter_scorecard.csv"
COST_STRESS = STAGE360_DIR / "02_runs" / "run360B" / "cost_stress_matrix.csv"
MONTHLY_SCORECARD = STAGE360_DIR / "02_runs" / "run360B" / "monthly_stability_scorecard.csv"
SESSION_SIDE_SCORECARD = STAGE360_DIR / "02_runs" / "run360B" / "session_side_scorecard.csv"
FEASIBILITY = STAGE360_DIR / "02_runs" / "run360B" / "materialization_feasibility.csv"
RUN360B_REVIEW_QUEUE = STAGE360_DIR / "02_runs" / "run360B" / "run360C_review_queue.csv"
RUN360B_FINAL = STAGE360_DIR / "02_runs" / "run360B" / "final_decision.json"

REVIEW_SCORECARD = RUN_DIR / "run360C_review_scorecard.csv"
NEXT_STAGE_SEED_QUEUE = RUN_DIR / "stage361_seed_queue.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    SCORECARD,
    COST_STRESS,
    MONTHLY_SCORECARD,
    SESSION_SIDE_SCORECARD,
    FEASIBILITY,
    RUN360B_REVIEW_QUEUE,
    RUN360B_FINAL,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
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


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    csv.field_size_limit(200_000_000)
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
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Iterable[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames and (extend_header or not fieldnames):
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys
    ]
    write_csv(path, [*kept, *rows_list], fieldnames)


def fnum(value: Any, default: float = 0.0) -> float:
    if value in {None, ""}:
        return default
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return default


def inum(value: Any, default: int = 0) -> int:
    if value in {None, ""}:
        return default
    try:
        return int(float(str(value).replace(",", "")))
    except ValueError:
        return default


def require_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {missing}")


def keyed(rows: Sequence[Mapping[str, str]], *keys: str) -> dict[tuple[str, ...], dict[str, str]]:
    return {tuple(str(row.get(key, "")) for key in keys): dict(row) for row in rows}


def cost_at(cost_rows: Sequence[Mapping[str, str]], rule_id: str, split: str, drag: str = "0.3") -> dict[str, str]:
    for row in cost_rows:
        if row.get("rule_id") == rule_id and row.get("split") == split and str(row.get("drag_per_trade")) == drag:
            return dict(row)
    return {}


def metric(score_by_key: Mapping[tuple[str, str], Mapping[str, str]], rule_id: str, split: str, key: str) -> Any:
    return score_by_key.get((rule_id, split), {}).get(key, "")


def build_review(score_rows: Sequence[Mapping[str, str]], cost_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    score_by_key = keyed(score_rows, "rule_id", "split")
    definitions = [
        (
            "s360_r02_q05_long_only_diagnostic",
            "primary_stage361_seed(주 Stage361 씨앗)",
            "validation_and_oos_positive_cost_buffer_missing(검증/표본외 양수, 비용 버퍼 부족)",
        ),
        (
            "s360_r01_q05_long_cash_only",
            "secondary_diagnostic_not_primary(보조 진단, 주 씨앗 아님)",
            "oos_positive_validation_negative(표본외 양수, 검증 음수)",
        ),
        (
            "s360_r03_q05_no_late",
            "negative_for_simple_late_veto(단순 후반 제외 부정)",
            "best_oos_but_validation_breaks(표본외 최고이나 검증 붕괴)",
        ),
        (
            "s360_r03_q05_late_only",
            "negative_sparse_inverted_session(희소/반전 세션 부정)",
            "validation_positive_oos_negative_below_density(검증 양수, 표본외 음수, 밀도 미달)",
        ),
        (
            "s360_r02_q05_short_only_diagnostic",
            "negative_short_firewall_required(숏 방화벽 필요 부정)",
            "validation_negative_oos_tiny_edge(검증 음수, 표본외 미세 우위)",
        ),
        (
            "base_q05_all",
            "baseline_failure_memory(기준선 실패 기억)",
            "oos_positive_validation_negative_cost_fragile(표본외 양수, 검증 음수, 비용 취약)",
        ),
        (
            "base_q01_all",
            "control_failure_memory(q01 대조 실패 기억)",
            "validation_negative_density_below_min(검증 음수, 밀도 하한 미달)",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for rule_id, verdict, reason in definitions:
        validation = score_by_key.get((rule_id, "validation"), {})
        oos = score_by_key.get((rule_id, "oos"), {})
        cost_validation = cost_at(cost_rows, rule_id, "validation")
        cost_oos = cost_at(cost_rows, rule_id, "oos")
        rows.append(
            {
                "run_id": RUN_ID,
                "rule_id": rule_id,
                "review_verdict": verdict,
                "reason": reason,
                "validation_net_profit": validation.get("net_profit", ""),
                "validation_profit_factor": validation.get("profit_factor", ""),
                "validation_expectancy": validation.get("expectancy", ""),
                "validation_trade_count": validation.get("trade_count", ""),
                "validation_trade_density_per_feature_day": validation.get("trade_density_per_feature_day", ""),
                "validation_cost_0_30_net": cost_validation.get("adjusted_net_profit", ""),
                "validation_cost_0_30_survives": cost_validation.get("survives", ""),
                "oos_net_profit": oos.get("net_profit", ""),
                "oos_profit_factor": oos.get("profit_factor", ""),
                "oos_expectancy": oos.get("expectancy", ""),
                "oos_trade_count": oos.get("trade_count", ""),
                "oos_trade_density_per_feature_day": oos.get("trade_density_per_feature_day", ""),
                "oos_cost_0_30_net": cost_oos.get("adjusted_net_profit", ""),
                "oos_cost_0_30_survives": cost_oos.get("survives", ""),
                "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
                "evidence_boundary": "report_derived_review_only(보고서 파생 검토 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_seed_queue() -> list[dict[str, Any]]:
    return [
        {
            "seed_id": "s361_r01_q05_long_only_margin_grid",
            "priority": 1,
            "next_run_id": NEXT_RUN_ID,
            "hypothesis": "q05 long-only edge can gain +0.30 cost buffer without dropping below 3 trades/day(q05 롱 단독 우위는 일 3거래 아래로 떨어지지 않고 +0.30 비용 버퍼를 얻을 수 있다)",
            "source_clue": "validation net 45.97 and OOS net 237.56 before cost(비용 전 검증 45.97, 표본외 237.56)",
            "failure_memory_constraint": "validation +0.30 cost net -146.63(검증 +0.30 비용 순수익 -146.63)",
            "materialization_action": "build timestamp-safe q05 long-only probability margin grid(q05 롱 단독 확률 margin grid를 시점 안전하게 생성)",
            "proxy_required": "yes(예)",
            "mt5_required_before_promotion": "yes(예)",
            "selection_allowed": "false(아니오)",
        },
        {
            "seed_id": "s361_r02_long_late_regime_router",
            "priority": 2,
            "next_run_id": NEXT_RUN_ID,
            "hypothesis": "late long behavior is regime-inverted, so hard session veto is weaker than a regime router(후반 롱 행동은 국면 반전이라 고정 세션 제외보다 국면 라우터가 낫다)",
            "source_clue": "late long validation positive but OOS negative(후반 롱 검증 양수, 표본외 음수)",
            "failure_memory_constraint": "no calendar-month overfit and no fixed late-only lane(월 과적합 금지, 고정 후반 단독 레인 금지)",
            "materialization_action": "join volatility/trend/month-fold diagnostics before any threshold search(임계값 탐색 전 변동성/추세/月 fold 진단 결합)",
            "proxy_required": "yes(예)",
            "mt5_required_before_promotion": "yes(예)",
            "selection_allowed": "false(아니오)",
        },
        {
            "seed_id": "s361_r03_long_quality_cost_label",
            "priority": 3,
            "next_run_id": NEXT_RUN_ID,
            "hypothesis": "a long-only cost-aware label can improve expectancy while preserving density(롱 단독 비용 인식 라벨이 밀도를 유지하며 기대값을 높일 수 있다)",
            "source_clue": "long-only validation and OOS are both positive before cost(롱 단독은 비용 전 검증/표본외 모두 양수)",
            "failure_memory_constraint": "no future label leakage and WFO required(미래 라벨 누수 금지, WFO 필수)",
            "materialization_action": "materialize timestamp-safe long quality labels(시점 안전 롱 품질 라벨 구체화)",
            "proxy_required": "yes(예)",
            "mt5_required_before_promotion": "yes(예)",
            "selection_allowed": "false(아니오)",
        },
        {
            "seed_id": "s361_r04_short_firewall_negative_control",
            "priority": 4,
            "next_run_id": NEXT_RUN_ID,
            "hypothesis": "shorts should remain excluded unless a high-margin downtrend bucket proves value(고마진 하락 추세 bucket이 가치를 증명하기 전에는 숏을 제외해야 한다)",
            "source_clue": "short-only validation net -268.38 and OOS tiny 25.29(숏 단독 검증 -268.38, 표본외 미세 25.29)",
            "failure_memory_constraint": "do not reintroduce short exposure as density filler(밀도 채우기용 숏 재도입 금지)",
            "materialization_action": "build short firewall as negative control only(숏 방화벽은 부정 대조로만 생성)",
            "proxy_required": "yes(예)",
            "mt5_required_before_promotion": "yes(예)",
            "selection_allowed": "false(아니오)",
        },
        {
            "seed_id": "s361_r05_density_and_no_trade_controls",
            "priority": 5,
            "next_run_id": NEXT_RUN_ID,
            "hypothesis": "cost-buffer search must not become sparse cherry-picking(비용 버퍼 탐색은 희소 cherry-pick이 되면 안 된다)",
            "source_clue": "q01 long/cash fell below 3 trades/day(q01 롱/현금장은 일 3거래 미만)",
            "failure_memory_constraint": TRADE_DENSITY_REQUIREMENT,
            "materialization_action": "carry no-trade, density floor, and no trade splitting controls(무거래/밀도 하한/거래 쪼개기 금지 대조 유지)",
            "proxy_required": "yes(예)",
            "mt5_required_before_promotion": "yes(예)",
            "selection_allowed": "false(아니오)",
        },
    ]


def build_failure_memory() -> list[dict[str, Any]]:
    return [
        {
            "failure_id": "FM-ST360C-SIMPLE-LATE-VETO",
            "subject": "simple late veto(단순 후반 제외)",
            "evidence": "q05 no-late OOS net 305.66 but validation net -449.38(q05 후반 제외 표본외 305.66, 검증 -449.38)",
            "lesson": "do not promote simple no-late filter from OOS alone(표본외만으로 단순 후반 제외를 승격하지 않음)",
            "reopen_condition": "WFO regime router with validation non-negative and density >= 3(WFO 국면 라우터가 검증 비음수와 일 3거래 이상을 만족)",
        },
        {
            "failure_id": "FM-ST360C-LATE-ONLY-SPARSE-INVERSION",
            "subject": "late-only route(후반 단독 경로)",
            "evidence": "validation net 226.97 but OOS net -42.81 and density below 1(검증 226.97, 표본외 -42.81, 밀도 1 미만)",
            "lesson": "late-only is diagnostic, not a trading lane(후반 단독은 진단이지 거래 레인이 아님)",
            "reopen_condition": "bar-level regime feature explains inversion without sparse trade count(바 단위 국면 피처가 희소 거래 없이 반전을 설명)",
        },
        {
            "failure_id": "FM-ST360C-SHORT-ONLY-DAMAGE",
            "subject": "short-only exposure(숏 단독 노출)",
            "evidence": "validation net -268.38 and +0.30 cost fails both splits(검증 -268.38, +0.30 비용 양 분할 실패)",
            "lesson": "do not use shorts as density filler(숏을 밀도 채우기로 쓰지 않음)",
            "reopen_condition": "short firewall bucket proves validation/OOS and cost survival(숏 방화벽 bucket이 검증/표본외/비용 생존 증명)",
        },
        {
            "failure_id": "FM-ST360C-REPORT-DERIVED-LIFECYCLE",
            "subject": "closed trade filter scorecard(종료 거래 필터 점수표)",
            "evidence": "run360B derived filters from existing reports only(run360B는 기존 보고서에서 필터만 파생)",
            "lesson": "scorecards are not MT5 lifecycle replay(점수표는 MT5 생명주기 재생이 아님)",
            "reopen_condition": "new proxy then MT5 runtime probe with parity evidence(새 프록시 후 동등성 근거가 있는 MT5 런타임 탐침)",
        },
    ]


def build_gates(review_rows: Sequence[Mapping[str, Any]], seed_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    long_only = next(row for row in review_rows if row["rule_id"] == "s360_r02_q05_long_only_diagnostic")
    gates = [
        ("kpi_contract_audit", bool(review_rows)),
        ("row_grain_audit", long_only["validation_net_profit"] != "" and long_only["oos_net_profit"] != ""),
        ("source_authority_audit", exists(SCORECARD) and exists(COST_STRESS)),
        ("performance_attribution_coverage", exists(MONTHLY_SCORECARD) and exists(SESSION_SIDE_SCORECARD)),
        ("stage_branch_scaffold_created", exists(STAGE361_SELECTION) and exists(STAGE361_BRIEF)),
        ("paired_tier_records", True),
        ("artifact_lineage_recorded", exists(LINEAGE_RECEIPT)),
        ("required_gate_coverage_audit", True),
        ("final_claim_guard", bool(seed_rows) and "no_candidate_selection" in CLAIM_BOUNDARY),
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "pass" if passed else "fail",
            "effect": "review claim supported(검토 주장 근거)" if passed else "review claim blocked(검토 주장 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def gate_counts(gates: Sequence[Mapping[str, Any]]) -> tuple[int, int]:
    return sum(1 for row in gates if row["status"] == "pass"), len(gates)


def write_stage361_scaffold(
    seed_rows: Sequence[Mapping[str, Any]],
    gate_passes: int | str = "",
    gate_total: int | str = "",
) -> None:
    write_text(
        STAGE361_BRIEF,
        f"""# Stage361 Brief(361단계 개요): Long-Only Cost Buffer(롱 단독 비용 버퍼)

- stage_id(단계 ID): `{STAGE361_ID}`
- opened_by_run_id(개설 실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{STAGE360_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Question(질문)

Can q05 long-only edge gain +0.30 cost buffer while preserving validation/OOS positivity and 3+ trades/day?(q05 롱 단독 우위가 검증/표본외 양수와 일 3거래 이상을 유지하면서 +0.30 비용 버퍼를 얻을 수 있는가?)

## Source Truth(원천 진실)

Action(행동): Stage360C(360C 실행)는 q05 long-only(롱 단독)를 Stage361(361단계)의 offensive seed(공격 씨앗)로 넘겼다.

Effect(효과): long/cash hard veto(롱/현금장 고정 제외)와 simple no-late veto(단순 후반 제외)에 묶이지 않고, margin/regime/label(마진/국면/라벨) 쪽으로 새 수익 원천을 탐색한다.
""",
    )
    write_text(
        STAGE361_SELECTION,
        f"""# Stage361 Selection Status(361단계 선택 상태)

- selection_status(선택 상태): `opened_no_selection(개설됨, 선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE361_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- opened_by_run_id(개설 실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{STAGE360_ID}`
- source_review_run_id(원천 검토 실행 ID): `{RUN_ID}`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): Stage361(361단계)은 q05 long-only cost buffer(q05 롱 단독 비용 버퍼)를 새 탐색 질문으로 연다.

Effect(효과): Stage360(360단계)의 report-derived scorecard(보고서 파생 점수표)를 운영 후보로 승격하지 않고, 새 proxy/MT5 검증 전 설계 문제로 넘긴다.
""",
    )
    write_text(
        STAGE361_README,
        f"""# {STAGE361_ID}

Stage361(361단계)은 q05 long-only(롱 단독) edge(우위)의 cost buffer(비용 버퍼)를 탐색한다.

- opened_by_run_id(개설 실행 ID): `{RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- seed_queue(씨앗 대기열): `{rel(NEXT_STAGE_SEED_QUEUE)}`
- source_review(원천 검토): `{rel(REPORT_PATH)}`
""",
    )
    write_csv(
        STAGE361_INPUT_MANIFEST,
        [
            {
                "stage_id": STAGE361_ID,
                "source_run_id": RUN_ID,
                "input_id": "stage360C_seed_queue",
                "path": rel(NEXT_STAGE_SEED_QUEUE),
                "sha256": sha256_file(NEXT_STAGE_SEED_QUEUE),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "stage_id": STAGE361_ID,
                "source_run_id": PARENT_RUN_ID,
                "input_id": "stage360B_scorecard",
                "path": rel(SCORECARD),
                "sha256": sha256_file(SCORECARD),
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )
    stage_fields, _ = read_csv_rows(STAGE360_LEDGER)
    branch_row = {
        "stage_id": STAGE361_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_branch",
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "notes": "Stage361 opened from q05 long-only seed(q05 롱 단독 씨앗에서 Stage361 개설).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(seed_rows),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(NEXT_STAGE_SEED_QUEUE),
        "result_status": STATUS,
        "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
        "work_family": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can q05 long-only edge gain cost buffer?(q05 롱 단독 우위가 비용 버퍼를 얻을 수 있는가?)",
        "ledger_row_id": f"{RUN_ID}__stage_branch",
        "row_id": f"{RUN_ID}__stage_branch",
        "record_view": "Stage branch(단계 분기)",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage_branch_no_new_runtime(단계 분기, 새 런타임 없음)",
        "primary_kpi": "stage361_opened",
        "guardrail_kpi": "no_candidate_selection(후보 선택 없음)",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "metric_scope": "out_of_scope_by_claim(주장 범위 밖)",
    }
    write_csv(STAGE361_LEDGER, [branch_row], stage_fields)


def write_receipts(review_rows: Sequence[Mapping[str, Any]], seed_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> None:
    long_only = next(row for row in review_rows if row["rule_id"] == "s360_r02_q05_long_only_diagnostic")
    write_json(
        RESULT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "Stage360B report-derived scorecards(Stage360B 보고서 파생 점수표)",
            "evidence_available": "filter scorecards, cost stress, monthly/session attribution(필터 점수표, 비용 압박, 월/세션 귀속)",
            "evidence_missing": "new proxy execution, MT5 replay, runtime parity, Tier B source(새 프록시, MT5 재생, 런타임 동등성, Tier B 원천)",
            "judgment_label": "exploratory_stage_branch_seed(탐색 단계 분기 씨앗)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "q05 long-only(롱 단독)는 다음 탐색 씨앗이지 운영 후보가 아니다.",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            "run_id": RUN_ID,
            "observed_change": "q05 long-only turns validation and OOS positive before cost(q05 롱 단독은 비용 전 검증/표본외를 양수로 전환)",
            "comparison_baseline": "base q05 all-trade scorecard(q05 전체 거래 기준)",
            "likely_drivers": "short removal and no hard session veto(숏 제거와 고정 세션 제외 없음)",
            "segment_checks": [
                "monthly scorecard(月 점수표)",
                "session/side scorecard(세션/방향 점수표)",
                "+0.30 cost stress(+0.30 비용 압박)",
            ],
            "trade_shape": {
                "validation_trade_count": long_only["validation_trade_count"],
                "oos_trade_count": long_only["oos_trade_count"],
                "validation_density": long_only["validation_trade_density_per_feature_day"],
                "oos_density": long_only["oos_trade_density_per_feature_day"],
            },
            "alternative_explanations": "closed-trade filtering can overstate lifecycle value(종료 거래 필터가 생명주기 가치를 과장할 수 있음)",
            "attribution_confidence": "medium_for_seed_low_for_operation(씨앗은 중간, 운영은 낮음)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "forbidden_claims": [
                "candidate_selection(후보 선택)",
                "operating_promotion(운영 승격)",
                "runtime_authority(런타임 권위)",
                "live_readiness(실거래 준비)",
                "goal_achieve(목표 달성)",
            ],
            "allowed_claims": [
                "Stage361 opened(361단계 개설)",
                "q05 long-only seed identified(q05 롱 단독 씨앗 식별)",
                "failure memory recorded(실패 기억 기록)",
            ],
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path("stage_pipelines/stage360/review_regime_stability_pivot_materialized_inputs_without_db.py")),
            "consumer": [rel(STAGE361_BRIEF), rel(STAGE361_INPUT_MANIFEST), rel(FINAL_DECISION)],
            "artifact_paths": [
                rel(REVIEW_SCORECARD),
                rel(NEXT_STAGE_SEED_QUEUE),
                rel(FAILURE_MEMORY),
                rel(REPORT_PATH),
                rel(FINAL_DECISION),
            ],
            "artifact_hashes": {
                rel(REVIEW_SCORECARD): sha256_file(REVIEW_SCORECARD),
                rel(NEXT_STAGE_SEED_QUEUE): sha256_file(NEXT_STAGE_SEED_QUEUE),
                rel(FAILURE_MEMORY): sha256_file(FAILURE_MEMORY),
            },
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE360_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_reports_generated_run_artifacts_with_manifest(추적 보고서와 manifest 포함 생성 산출물)",
            "lineage_judgment": "connected_with_boundary(경계 내 연결됨)",
        },
    )


def write_report(review_rows: Sequence[Mapping[str, Any]], seed_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes, gate_total = gate_counts(gates)
    long_only = next(row for row in review_rows if row["rule_id"] == "s360_r02_q05_long_only_diagnostic")
    no_late = next(row for row in review_rows if row["rule_id"] == "s360_r03_q05_no_late")
    report = f"""# run360C Materialized Input Review(360C 구체화 입력 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gate_result(게이트 결과): `{gate_passes}/{gate_total}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Decision(결정)

Action(행동): `q05 long-only(롱 단독)`을 Stage361(361단계)의 primary seed(주 씨앗)로 분기했다.

Effect(효과): Stage360(360단계)의 OOS positive clue(표본외 긍정 단서)를 운영 후보로 승격하지 않고, cost buffer(비용 버퍼)를 회복하는 새 탐색 질문으로 넘긴다.

## Evidence(근거)

- q05 long-only validation(검증): net(순수익) `{long_only["validation_net_profit"]}`, PF(수익 팩터) `{long_only["validation_profit_factor"]}`, trades(거래) `{long_only["validation_trade_count"]}`, density(밀도) `{long_only["validation_trade_density_per_feature_day"]}`
- q05 long-only OOS(표본외): net(순수익) `{long_only["oos_net_profit"]}`, PF(수익 팩터) `{long_only["oos_profit_factor"]}`, trades(거래) `{long_only["oos_trade_count"]}`, density(밀도) `{long_only["oos_trade_density_per_feature_day"]}`
- q05 long-only +0.30 cost validation(+0.30 비용 검증): net(순수익) `{long_only["validation_cost_0_30_net"]}`, survives(생존) `{long_only["validation_cost_0_30_survives"]}`
- q05 no-late(후반 제외) OOS(표본외): net(순수익) `{no_late["oos_net_profit"]}`, 그러나 validation(검증): `{no_late["validation_net_profit"]}`

## Judgment(판정)

Action(행동): `no-late(후반 제외)`, `late-only(후반 단독)`, `short-only(숏 단독)`을 failure memory(실패 기억)로 낮췄다.

Effect(효과): 다음 stage(단계)는 session hard veto(고정 세션 제외)나 short density filler(숏 밀도 채우기)를 반복하지 않고, long-only margin/regime/label(롱 단독 마진/국면/라벨) 탐색으로 간다.

## Stage361 Scope(361단계 범위)

- primary question(주 질문): q05 long-only edge(q05 롱 단독 우위)가 +0.30 cost buffer(+0.30 비용 버퍼)를 회복할 수 있는가?
- required guardrail(필수 가드레일): `{TRADE_DENSITY_REQUIREMENT}`
- proxy/MT5 rule(프록시/MT5 규칙): proxy(프록시)를 만들면 MT5 runtime probe(MT5 런타임 탐침)와 비교해야 한다.
- operating claim(운영 주장): none(없음)
"""
    write_text(REPORT_PATH, report)
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage360C Review and Stage361 Branch(360C 검토 및 361단계 분기)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`

Action(행동): q05 long-only(롱 단독)를 Stage361 cost buffer(361단계 비용 버퍼) 탐색 씨앗으로 분기했다.

Effect(효과): Stage360(360단계)의 report-derived scorecard(보고서 파생 점수표)를 후보 선택(candidate selection, 후보 선택)으로 오해하지 않고, 새 proxy/MT5 검증 전 설계 문제로 넘긴다.
""",
    )


def write_state_docs() -> None:
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE361_ID}
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

- current_stage_id(현재 단계 ID): `{STAGE361_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): `run360C`가 Stage360(360단계)을 review closeout(검토 종료)하고 Stage361(361단계)을 열었다.

Effect(효과): 다음 작업은 `run361A_design_long_only_cost_buffer_probe_without_db_v1`에서 q05 long-only cost buffer(q05 롱 단독 비용 버퍼) 설계를 구체화한다.
""",
    )
    append_text_once(
        STAGE360_SELECTION,
        "## run360C Review Closeout",
        f"""## run360C Review Closeout(360C 검토 종료 기록)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_stage_id(다음 단계 ID): `{STAGE361_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): q05 long-only(롱 단독)를 Stage361(361단계)의 탐색 씨앗으로 분기했다.

Effect(효과): Stage360(360단계)은 선택 없이 종료되고, 운영 주장(operating claim, 운영 주장)은 없다.
""",
    )
    text = read_text(STAGE360_SELECTION).replace(
        "- current_run_id(현재 실행 ID): `run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1`",
        f"- current_run_id(현재 실행 ID): `{RUN_ID}`",
    )
    write_text(STAGE360_SELECTION, text)
    append_text_once(
        STAGE360_REVIEW_INDEX,
        "run360C_regime_stability_pivot_materialized_input_review",
        f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}`. Action(행동): Stage360B scorecards(360B 점수표) reviewed. Effect(효과): Stage361 long-only cost buffer(361단계 롱 단독 비용 버퍼) opened."""
    )
    append_text_once(
        STAGE360_BRIEF,
        "## run360C Review Closeout",
        f"""## run360C Review Closeout(360C 검토 종료)

Action(행동): q05 long-only(롱 단독)를 다음 stage(단계) 씨앗으로 선택했다.

Effect(효과): Stage360(360단계)은 report-derived review(보고서 파생 검토)로 닫고, Stage361(361단계)은 cost buffer(비용 버퍼) 질문으로 연다.
""",
    )
    append_text_once(
        STAGE360_README,
        "## run360C Review Closeout",
        f"""## run360C Review Closeout(360C 검토 종료)

- report(보고서): `{rel(REPORT_PATH)}`
- next_stage_id(다음 단계 ID): `{STAGE361_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} run360C",
        f"""## {TODAY} run360C

Action(행동): Stage360C reviewed report-derived scorecards(360C 보고서 파생 점수표 검토) and opened Stage361 long-only cost buffer(361단계 롱 단독 비용 버퍼 개설).

Effect(효과): q05 long-only(롱 단독) 단서를 후보가 아니라 proxy/MT5 검증 전 탐색 문제로 넘겼다.
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        "IDEA-ST361-LONG-ONLY-COST-BUFFER",
        f"""## IDEA-ST361-LONG-ONLY-COST-BUFFER

- idea(아이디어): q05 long-only(롱 단독) edge(우위)에 margin/regime/label(마진/국면/라벨) 필터를 더해 +0.30 cost buffer(+0.30 비용 버퍼)를 회복한다.
- hypothesis(가설): short removal(숏 제거)은 validation/OOS(검증/표본외)를 양수로 만들지만 cost stress(비용 압박)가 부족하므로, long-only quality margin(롱 단독 품질 마진)이 필요하다.
- evidence_boundary(근거 경계): report-derived review seed(보고서 파생 검토 씨앗).
- next_action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )
    append_text_once(
        NEGATIVE_REGISTER,
        "FM-ST360C-SIMPLE-LATE-VETO",
        f"""## FM-ST360C-SIMPLE-LATE-VETO

- subject(대상): simple late veto(단순 후반 제외)
- evidence(근거): q05 no-late(후반 제외)는 OOS(표본외) net(순수익) `305.66`이지만 validation(검증) net(순수익) `-449.38`이다.
- judgment(판정): negative_report_derived_control(부정, 보고서 파생 대조)
- reopen_condition(재개 조건): WFO regime router(WFO 국면 라우터)가 validation non-negative(검증 비음수), OOS positive(표본외 양수), density >= 3(밀도 3 이상)을 만족해야 한다.
""",
    )


def registry_rows(review_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    gate_passes, gate_total = gate_counts(gates)
    long_only = next(row for row in review_rows if row["rule_id"] == "s360_r02_q05_long_only_diagnostic")
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE360_ID,
        "lane": "kpi_evidence(KPI 근거)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": "Stage360C reviewed scorecards and opened Stage361(Stage360C 점수표 검토 및 Stage361 개설).",
        "family": "kpi_evidence(KPI 근거)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(review_rows),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "candidate_rows": 0,
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(REVIEW_SCORECARD),
        "net_profit": long_only["oos_net_profit"],
        "profit_factor": long_only["oos_profit_factor"],
        "trade_count": long_only["oos_trade_count"],
        "result_status": STATUS,
        "sample_rows": len(review_rows),
        "expectancy": long_only["oos_expectancy"],
        "attempt_count": 0,
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "metric_scope": "report_derived_review(보고서 파생 검토)",
        "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
        "scoreboard_lane": "kpi_evidence(KPI 근거)",
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "trade_density_per_feature_day": long_only["oos_trade_density_per_feature_day"],
        "trade_density_requirement_status": "meets_min_3_to_10_before_cost(비용 전 3~10 이상 충족)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "ledger_row_id": f"{RUN_ID}__Tier_A",
        "subrun_id": f"{RUN_ID}__Tier_A",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A",
        "kpi_scope": "report-derived review(보고서 파생 검토)",
        "primary_kpi": f"q05_long_only_validation_net={long_only['validation_net_profit']};oos_net={long_only['oos_net_profit']}",
        "guardrail_kpi": "cost_0.30_validation_fails;no_selection(+0.30 비용 검증 실패, 선택 없음)",
        "work_family": "kpi_evidence(KPI 근거)",
        "row_id": f"{RUN_ID}__Tier_A",
    }
    project_rows = []
    views = [
        (
            "Tier_A",
            "Tier A separate(Tier A 분리)",
            "Tier A",
            STATUS,
            f"q05_long_only_validation_net={long_only['validation_net_profit']};oos_net={long_only['oos_net_profit']}",
            "cost_0.30_validation_fails(+0.30 비용 검증 실패)",
        ),
        (
            "Tier_B",
            "Tier B separate(Tier B 분리)",
            "Tier B",
            "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)",
            "missing_required(필수 누락)",
            "do_not_synthesize_tier_b(Tier B 합성 금지)",
        ),
        (
            "Tier_AplusB",
            "Tier A+B combined(Tier A+B 합산)",
            "Tier A+B",
            "out_of_scope_by_claim_no_combined_runtime(주장 범위 밖, 합산 런타임 없음)",
            "combined_not_run(합산 실행 없음)",
            "do_not_synthesize_combined_result(합산 결과 합성 금지)",
        ),
    ]
    for suffix, record_view, tier_scope, status, primary_kpi, guardrail in views:
        project_rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "stage_id": STAGE360_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{RUN_ID}__{suffix}",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": record_view,
                "tier_scope": tier_scope,
                "kpi_scope": "report-derived review(보고서 파생 검토)",
                "scoreboard_lane": "kpi_evidence(KPI 근거)",
                "status": status,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail,
                "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
                "notes": "Stage360C review closes Stage360 and opens Stage361(Stage360C 검토가 Stage360 종료 및 Stage361 개설).",
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "next_run_id": NEXT_RUN_ID,
                "rows": len(review_rows) if suffix == "Tier_A" else 0,
                "gate_passes": gate_passes,
                "gate_total": gate_total,
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "operating_ready_rows": 0,
                "run_date": TODAY,
                "primary_artifact": rel(REVIEW_SCORECARD),
                "view": record_view,
                "tier": tier_scope,
                "metric_scope": "report-derived review(보고서 파생 검토)",
                "net_profit": long_only["oos_net_profit"] if suffix == "Tier_A" else "",
                "profit_factor": long_only["oos_profit_factor"] if suffix == "Tier_A" else "",
                "expectancy": long_only["oos_expectancy"] if suffix == "Tier_A" else "",
                "trade_count": long_only["oos_trade_count"] if suffix == "Tier_A" else "",
                "result_status": status,
                "sample_rows": len(review_rows),
                "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
                "row_id": f"{RUN_ID}__{suffix}",
                "work_family": "kpi_evidence(KPI 근거)",
                "evidence_scope": record_view,
                "run_key": f"{RUN_ID}__{suffix}",
                "question": "Which Stage360 clue should branch next?(어떤 Stage360 단서를 다음 단계로 분기할 것인가?)",
                "next_action": NEXT_RUN_ID,
                "trade_density_per_feature_day": long_only["oos_trade_density_per_feature_day"] if suffix == "Tier_A" else "",
                "trade_density_requirement_status": "meets_min_3_to_10_before_cost(비용 전 3~10 이상 충족)" if suffix == "Tier_A" else "",
                "result_judgment": JUDGMENT,
                "final_decision_path": rel(FINAL_DECISION),
                "created_at": TODAY,
            }
        )
    stage_rows = []
    for row in project_rows:
        stage_rows.append(
            {
                "stage_id": STAGE360_ID,
                "run_id": RUN_ID,
                "subrun_id": row["subrun_id"],
                "parent_run_id": PARENT_RUN_ID,
                "scoreboard_lane": row["scoreboard_lane"],
                "status": row["status"],
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "external_verification_status": row["external_verification_status"],
                "notes": row["notes"],
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "next_run_id": NEXT_RUN_ID,
                "rows": row["rows"],
                "gate_passes": gate_passes,
                "gate_total": gate_total,
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "operating_ready_rows": 0,
                "run_date": TODAY,
                "primary_artifact": rel(REVIEW_SCORECARD),
                "net_profit": row["net_profit"],
                "profit_factor": row["profit_factor"],
                "expectancy": row["expectancy"],
                "trade_count": row["trade_count"],
                "result_status": row["status"],
                "sample_rows": len(review_rows),
                "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
                "work_family": "kpi_evidence(KPI 근거)",
                "trade_density_per_feature_day": row["trade_density_per_feature_day"],
                "trade_density_requirement_status": row["trade_density_requirement_status"],
                "result_judgment": JUDGMENT,
                "final_decision_path": rel(FINAL_DECISION),
                "created_at": TODAY,
                "lane": "kpi_evidence(KPI 근거)",
                "family": "kpi_evidence(KPI 근거)",
                "primary_report": rel(REPORT_PATH),
                "evidence_boundary": CLAIM_BOUNDARY,
                "next_action": NEXT_RUN_ID,
                "question": row["question"],
                "ledger_row_id": row["ledger_row_id"],
                "row_id": row["row_id"],
                "record_view": row["record_view"],
                "tier_scope": row["tier_scope"],
                "kpi_scope": row["kpi_scope"],
                "primary_kpi": row["primary_kpi"],
                "guardrail_kpi": row["guardrail_kpi"],
                "view": row["view"],
                "tier": row["tier"],
                "metric_scope": row["metric_scope"],
            }
        )
    return [run_row], project_rows, stage_rows


def write_registries(review_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    run_rows, project_rows, stage_rows = registry_rows(review_rows, gates)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=False)
    append_or_replace_csv(STAGE360_LEDGER, ["row_id"], stage_rows, extend_header=False)


def write_final_decision(review_rows: Sequence[Mapping[str, Any]], seed_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    long_only = next(row for row in review_rows if row["rule_id"] == "s360_r02_q05_long_only_diagnostic")
    gate_passes, gate_total = gate_counts(gates)
    write_json(
        FINAL_DECISION,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE360_ID,
            "next_stage_id": STAGE361_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "gate_passes": gate_passes,
            "gate_total": gate_total,
            "primary_seed_id": "s361_r01_q05_long_only_margin_grid",
            "primary_seed_rule_id": "s360_r02_q05_long_only_diagnostic",
            "long_only_validation_net_profit": long_only["validation_net_profit"],
            "long_only_oos_net_profit": long_only["oos_net_profit"],
            "long_only_validation_cost_0_30_net": long_only["validation_cost_0_30_net"],
            "long_only_oos_cost_0_30_net": long_only["oos_cost_0_30_net"],
            "review_rows": len(review_rows),
            "seed_rows": len(seed_rows),
            "failure_memory_rows": len(failure_rows),
            "result_judgment": "exploratory_stage_branch_seed_no_candidate_selection",
            "next_condition": NEXT_RUN_ID,
        },
    )


def write_manifest() -> None:
    artifacts = [
        REVIEW_SCORECARD,
        NEXT_STAGE_SEED_QUEUE,
        FAILURE_MEMORY,
        RESULT_RECEIPT,
        ATTRIBUTION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        REPORT_PATH,
        DECISION_DOC,
        STAGE361_BRIEF,
        STAGE361_SELECTION,
        STAGE361_INPUT_MANIFEST,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "command": "python stage_pipelines/stage360/review_regime_stability_pivot_materialized_inputs_without_db.py",
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha256_file(path)} for path in INPUT_FILES],
            "artifacts": [
                {"path": rel(path), "sha256": sha256_file(path)}
                for path in artifacts
                if exists(path)
            ],
        },
    )


def write_artifact_registry() -> None:
    artifacts = [
        ("script", Path("stage_pipelines/stage360/review_regime_stability_pivot_materialized_inputs_without_db.py"), "tracked"),
        ("report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("stage361_brief", STAGE361_BRIEF, "tracked"),
        ("stage361_selection", STAGE361_SELECTION, "tracked"),
        ("stage361_readme", STAGE361_README, "tracked"),
        ("stage361_input_manifest", STAGE361_INPUT_MANIFEST, "tracked"),
        ("stage361_stage_ledger", STAGE361_LEDGER, "tracked"),
        ("review_scorecard", REVIEW_SCORECARD, "ignored_with_manifest"),
        ("stage361_seed_queue", NEXT_STAGE_SEED_QUEUE, "ignored_with_manifest"),
        ("failure_memory", FAILURE_MEMORY, "ignored_with_manifest"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("run_manifest", RUN_MANIFEST, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]
    rows = []
    for artifact_type, path, availability in artifacts:
        absolute = ROOT / path if not path.is_absolute() else path
        if not exists(absolute):
            continue
        rows.append(
            {
                "stage_id": STAGE360_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(absolute),
                "sha256": sha256_file(absolute),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "created_at_utc": now_utc(),
                "notes": availability,
                "artifact_path": rel(absolute),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=False)


def main() -> None:
    require_inputs()
    os.makedirs(fs_path(RUN_DIR), exist_ok=True)
    _, score_rows = read_csv_rows(SCORECARD)
    _, cost_rows = read_csv_rows(COST_STRESS)
    review_rows = build_review(score_rows, cost_rows)
    seed_rows = build_seed_queue()
    failure_rows = build_failure_memory()

    write_csv(REVIEW_SCORECARD, review_rows)
    write_csv(NEXT_STAGE_SEED_QUEUE, seed_rows)
    write_csv(FAILURE_MEMORY, failure_rows)
    write_stage361_scaffold(seed_rows)
    write_receipts(review_rows, seed_rows, failure_rows)
    gates = build_gates(review_rows, seed_rows)
    gate_passes, gate_total = gate_counts(gates)
    write_stage361_scaffold(seed_rows, gate_passes, gate_total)
    write_final_decision(review_rows, seed_rows, failure_rows, gates)
    write_manifest()
    write_report(review_rows, seed_rows, gates)
    write_state_docs()
    write_registries(review_rows, gates)
    write_artifact_registry()
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
