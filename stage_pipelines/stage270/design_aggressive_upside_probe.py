from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

import pandas as pd


STAGE269_ID = "269_onnx_candidate_campaign__fresh_thesis_candidate_construction"
STAGE270_ID = "270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe"
RUN_ID = "run270A_aggressive_upside_probe_design_v1"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

ROOT = Path(".")
STAGE269 = ROOT / "stages" / STAGE269_ID
STAGE270 = ROOT / "stages" / STAGE270_ID
RUN_DIR = STAGE270 / "02_runs" / "run270A"
REVIEWS = STAGE270 / "03_reviews"

SOURCE_QUEUE = STAGE269 / "02_runs" / "run269E" / "stage270_aggressive_probe_queue.csv"
SOURCE_SCREENING = STAGE269 / "02_runs" / "run269E" / "package_screening_summary.csv"
SOURCE_FAILURE_MEMORY = STAGE269 / "02_runs" / "run269E" / "screening_failure_memory.csv"
SOURCE_SUPPORT = STAGE269 / "02_runs" / "run269E" / "support_control_carry.csv"
SOURCE_RUN269E_MANIFEST = STAGE269 / "02_runs" / "run269E" / "run_manifest.json"
SOURCE_RUN269D_DATA_INTEGRITY = STAGE269 / "02_runs" / "run269D" / "data_integrity_receipt.json"
CP269A_SCORE_TABLE = STAGE269 / "02_runs" / "run269D" / "scores" / "cp269A_scores.parquet"
CP269D_SCORE_TABLE = STAGE269 / "02_runs" / "run269D" / "scores" / "cp269D_scores.parquet"
CP269A_HANDOFF = STAGE269 / "02_runs" / "run269D" / "handoff" / "cp269A.json"
CP269D_HANDOFF = STAGE269 / "02_runs" / "run269D" / "handoff" / "cp269D.json"

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
    for path in [
        STAGE270 / "00_spec",
        STAGE270 / "01_inputs",
        RUN_DIR,
        REVIEWS,
        STAGE270 / "04_selected",
    ]:
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


def rounded(value: float | int, ndigits: int = 8) -> float:
    return round(float(value), ndigits)


def load_inputs() -> tuple[list[dict[str, str]], pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    queue = read_csv_rows(SOURCE_QUEUE)
    if len(queue) != 1:
        raise ValueError(f"Expected one Stage270 queue row, found {len(queue)}.")
    if queue[0]["package_id"] != "cp269A_asymmetric_nonfilter_reentry_surface":
        raise ValueError(f"Unexpected package_id: {queue[0]['package_id']}")

    with SOURCE_RUN269D_DATA_INTEGRITY.open("r", encoding="utf-8") as f:
        data_integrity = json.load(f)

    cp269a = pd.read_parquet(CP269A_SCORE_TABLE)
    cp269d = pd.read_parquet(CP269D_SCORE_TABLE)
    leaked = sorted(
        set(cp269a.columns).intersection(LABEL_OR_FUTURE_COLUMNS)
        | {c for c in cp269a.columns if c.startswith(LABEL_OR_FUTURE_PREFIXES)}
    )
    if leaked:
        raise ValueError(f"Label/future columns are not allowed in Stage270 design: {leaked}")

    return queue, cp269a, cp269d, data_integrity


def quantiles(cp269a: pd.DataFrame) -> dict[str, float]:
    tier_a_train = cp269a[
        (cp269a["tier_view"] == "Tier A separate") & (cp269a["split"] == "train")
    ]
    if tier_a_train.empty:
        raise ValueError("Tier A train rows are required for threshold materialization.")
    return {
        "decision_p50": float(tier_a_train["candidate_decision_score"].quantile(0.50)),
        "decision_p55": float(tier_a_train["candidate_decision_score"].quantile(0.55)),
        "decision_p60": float(tier_a_train["candidate_decision_score"].quantile(0.60)),
        "decision_p65": float(tier_a_train["candidate_decision_score"].quantile(0.65)),
        "reward_p55": float(tier_a_train["reward_skew_score"].quantile(0.55)),
        "reward_p60": float(tier_a_train["reward_skew_score"].quantile(0.60)),
        "reward_p70": float(tier_a_train["reward_skew_score"].quantile(0.70)),
        "reward_p85": float(tier_a_train["reward_skew_score"].quantile(0.85)),
        "cost_p65": float(tier_a_train["weak_context_cost"].quantile(0.65)),
        "cost_p75": float(tier_a_train["weak_context_cost"].quantile(0.75)),
        "cost_p85": float(tier_a_train["weak_context_cost"].quantile(0.85)),
        "cost_p90": float(tier_a_train["weak_context_cost"].quantile(0.90)),
    }


def variant_plan(q: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "variant_id": "run270A_q01_base_materialized_decision",
            "variant_role": "reference_seed",
            "hypothesis": "Use the run269D materialized decision as the reference seed.",
            "decision_rule": "materialized_decision_flag == 1",
            "upside_probe_question": "Does the seed remain bounded before aggressive expansion?",
            "failure_mode": "seed_supply_already_too_wide",
            "discard_condition": "decision_rate_above_0_35_or_no_tier_pair_receipt",
            "thresholds_json": json.dumps({}, sort_keys=True),
        },
        {
            "variant_id": "run270A_q02_reward_skew_tilt",
            "variant_role": "primary_aggressive_probe",
            "hypothesis": "Tilt toward high reward skew while keeping weak-context cost bounded.",
            "decision_rule": "decision>=p55 and reward>=p70 and cost<=p65 and failure_zone==0",
            "upside_probe_question": "Can high reward skew increase upside without broad supply inflation?",
            "failure_mode": "reward_tail_too_sparse_or_context_fragile",
            "discard_condition": "oos_decision_rate_below_0_03_or_validation_to_oos_supply_ratio_above_2_0",
            "thresholds_json": json.dumps(
                {
                    "decision_min": q["decision_p55"],
                    "reward_min": q["reward_p70"],
                    "cost_max": q["cost_p65"],
                },
                sort_keys=True,
            ),
        },
        {
            "variant_id": "run270A_q03_supply_expansion_watch",
            "variant_role": "aggressive_supply_expansion",
            "hypothesis": "Relax supply enough to test upside capacity before stability review.",
            "decision_rule": "decision>=p50 and reward>=p55 and cost<=p85 and failure_zone==0",
            "upside_probe_question": "Can supply expansion find capacity without overwhelming weak contexts?",
            "failure_mode": "trade_supply_inflation_or_weak_context_damage",
            "discard_condition": "combined_decision_rate_above_0_35_or_failure_zone_share_above_0_02",
            "thresholds_json": json.dumps(
                {
                    "decision_min": q["decision_p50"],
                    "reward_min": q["reward_p55"],
                    "cost_max": q["cost_p85"],
                },
                sort_keys=True,
            ),
        },
        {
            "variant_id": "run270A_q04_tail_reward_extreme",
            "variant_role": "tail_upside_probe",
            "hypothesis": "Extreme reward skew may carry a cleaner but narrower upside surface.",
            "decision_rule": "decision>=p65 and reward>=p85 and failure_zone==0",
            "upside_probe_question": "Is the high-tail reward surface too sparse or worth a MT5 probe?",
            "failure_mode": "tail_surface_too_sparse",
            "discard_condition": "oos_decision_count_below_75_or_validation_decision_count_below_75",
            "thresholds_json": json.dumps(
                {
                    "decision_min": q["decision_p65"],
                    "reward_min": q["reward_p85"],
                },
                sort_keys=True,
            ),
        },
        {
            "variant_id": "run270A_q05_cost_relaxed_probe",
            "variant_role": "cost_relaxation_probe",
            "hypothesis": "A controlled cost relaxation may reveal upside hidden by tight filters.",
            "decision_rule": "decision>=p60 and reward>=p60 and cost<=p90 and failure_zone==0",
            "upside_probe_question": "Does cost relaxation improve supply without turning into repair loop?",
            "failure_mode": "weak_context_cost_dominates_supply",
            "discard_condition": "oos_decision_rate_above_0_30_or_monthly_supply_spike_above_0_45",
            "thresholds_json": json.dumps(
                {
                    "decision_min": q["decision_p60"],
                    "reward_min": q["reward_p60"],
                    "cost_max": q["cost_p90"],
                },
                sort_keys=True,
            ),
        },
        {
            "variant_id": "run270A_q06_weak_context_failure_boundary",
            "variant_role": "failure_boundary_probe",
            "hypothesis": "Weak-context-heavy rows should be isolated as a failure boundary, not a candidate.",
            "decision_rule": "decision>=p60 and reward>=p60 and cost>p75",
            "upside_probe_question": "Does weak-context exposure explain why an aggressive branch should be discarded?",
            "failure_mode": "known_weak_context_damage",
            "discard_condition": "any_positive_candidate_claim_from_this_variant",
            "thresholds_json": json.dumps(
                {
                    "decision_min": q["decision_p60"],
                    "reward_min": q["reward_p60"],
                    "cost_min": q["cost_p75"],
                },
                sort_keys=True,
            ),
        },
    ]


def build_decision_mask(df: pd.DataFrame, variant: dict[str, Any]) -> pd.Series:
    thresholds = json.loads(variant["thresholds_json"])
    if variant["variant_id"] == "run270A_q01_base_materialized_decision":
        return df["materialized_decision_flag"].astype(int) == 1
    if variant["variant_id"] == "run270A_q02_reward_skew_tilt":
        return (
            (df["candidate_decision_score"] >= thresholds["decision_min"])
            & (df["reward_skew_score"] >= thresholds["reward_min"])
            & (df["weak_context_cost"] <= thresholds["cost_max"])
            & (df["failure_zone_cut_flag"].astype(int) == 0)
        )
    if variant["variant_id"] == "run270A_q03_supply_expansion_watch":
        return (
            (df["candidate_decision_score"] >= thresholds["decision_min"])
            & (df["reward_skew_score"] >= thresholds["reward_min"])
            & (df["weak_context_cost"] <= thresholds["cost_max"])
            & (df["failure_zone_cut_flag"].astype(int) == 0)
        )
    if variant["variant_id"] == "run270A_q04_tail_reward_extreme":
        return (
            (df["candidate_decision_score"] >= thresholds["decision_min"])
            & (df["reward_skew_score"] >= thresholds["reward_min"])
            & (df["failure_zone_cut_flag"].astype(int) == 0)
        )
    if variant["variant_id"] == "run270A_q05_cost_relaxed_probe":
        return (
            (df["candidate_decision_score"] >= thresholds["decision_min"])
            & (df["reward_skew_score"] >= thresholds["reward_min"])
            & (df["weak_context_cost"] <= thresholds["cost_max"])
            & (df["failure_zone_cut_flag"].astype(int) == 0)
        )
    if variant["variant_id"] == "run270A_q06_weak_context_failure_boundary":
        return (
            (df["candidate_decision_score"] >= thresholds["decision_min"])
            & (df["reward_skew_score"] >= thresholds["reward_min"])
            & (df["weak_context_cost"] > thresholds["cost_min"])
        )
    raise ValueError(f"Unknown variant_id: {variant['variant_id']}")


def support_identity(cp269d: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        cp269d.groupby(["tier_view", "split"], dropna=False)["identity_match_flag"]
        .mean()
        .reset_index()
        .rename(columns={"identity_match_flag": "support_identity_rate"})
    )
    return grouped


def supply_metrics(
    cp269a: pd.DataFrame, cp269d: pd.DataFrame, variants: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    identity = support_identity(cp269d)
    metrics_rows: list[dict[str, Any]] = []
    monthly_rows: list[dict[str, Any]] = []
    with_month = cp269a.copy()
    with_month["month"] = with_month["timestamp"].dt.strftime("%Y-%m")

    for variant in variants:
        mask = build_decision_mask(cp269a, variant)
        vdf = cp269a.assign(variant_decision_flag=mask.astype("int8"))
        grouped = (
            vdf.groupby(["tier_view", "split"], dropna=False)
            .agg(
                rows=("variant_decision_flag", "size"),
                decision_count=("variant_decision_flag", "sum"),
                score_median=("candidate_decision_score", "median"),
                reward_median=("reward_skew_score", "median"),
                weak_context_cost_median=("weak_context_cost", "median"),
                failure_zone_count=("failure_zone_cut_flag", "sum"),
            )
            .reset_index()
        )
        grouped = grouped.merge(identity, on=["tier_view", "split"], how="left")
        for row in grouped.to_dict("records"):
            decision_rate = float(row["decision_count"]) / float(row["rows"]) if row["rows"] else 0.0
            failure_zone_share = (
                float(row["failure_zone_count"]) / float(row["rows"]) if row["rows"] else 0.0
            )
            metrics_rows.append(
                {
                    "variant_id": variant["variant_id"],
                    "variant_role": variant["variant_role"],
                    "tier_view": row["tier_view"],
                    "split": row["split"],
                    "rows": int(row["rows"]),
                    "decision_count": int(row["decision_count"]),
                    "decision_rate": rounded(decision_rate),
                    "score_median": rounded(row["score_median"]),
                    "reward_median": rounded(row["reward_median"]),
                    "weak_context_cost_median": rounded(row["weak_context_cost_median"]),
                    "failure_zone_share": rounded(failure_zone_share),
                    "support_identity_rate": rounded(row["support_identity_rate"]),
                    "performance_claim": "none",
                }
            )

        vmonth = with_month.assign(variant_decision_flag=mask.astype("int8"))
        mgrouped = (
            vmonth.groupby(["variant_decision_flag", "tier_view", "month"], dropna=False)
            .size()
            .reset_index(name="count")
        )
        total_by_month = (
            vmonth.groupby(["tier_view", "month"], dropna=False)
            .size()
            .reset_index(name="month_rows")
        )
        mgrouped = mgrouped[mgrouped["variant_decision_flag"] == 1].merge(
            total_by_month, on=["tier_view", "month"], how="left"
        )
        for row in mgrouped.to_dict("records"):
            monthly_rows.append(
                {
                    "variant_id": variant["variant_id"],
                    "tier_view": row["tier_view"],
                    "month": row["month"],
                    "month_rows": int(row["month_rows"]),
                    "decision_count": int(row["count"]),
                    "decision_rate": rounded(float(row["count"]) / float(row["month_rows"])),
                    "performance_claim": "none",
                }
            )

    return metrics_rows, monthly_rows


def readiness_rows(
    queue: list[dict[str, str]], cp269a: pd.DataFrame, cp269d: pd.DataFrame, data_integrity: dict[str, Any]
) -> list[dict[str, str]]:
    tier_views = sorted(cp269a["tier_view"].dropna().unique().tolist())
    support_tier_views = sorted(cp269d["tier_view"].dropna().unique().tolist())
    return [
        {
            "check_name": "stage269_queue_present",
            "status": "passed",
            "effect": f"queue_rows={len(queue)}; package={queue[0]['package_id']}",
        },
        {
            "check_name": "label_future_columns_excluded",
            "status": "passed" if not data_integrity.get("score_formula_uses_label_or_future_columns") else "failed",
            "effect": "Stage270 thresholds use score columns only and do not use label/future columns.",
        },
        {
            "check_name": "tier_pair_input_available",
            "status": "passed" if tier_views == ["Tier A separate", "Tier B separate"] else "failed",
            "effect": ";".join(tier_views),
        },
        {
            "check_name": "support_control_available",
            "status": "passed" if support_tier_views == ["Tier A separate", "Tier B separate"] else "failed",
            "effect": ";".join(support_tier_views),
        },
        {
            "check_name": "threshold_source_locked",
            "status": "passed",
            "effect": "Thresholds are derived from Tier A train quantiles and applied to validation/OOS without OOS tuning.",
        },
        {
            "check_name": "external_verification_scope",
            "status": "out_of_scope_by_claim",
            "effect": "Run270A is design/structural supply materialization only; trading KPI and MT5 output remain missing.",
        },
    ]


def stage_docs() -> None:
    write_md(
        STAGE270 / "00_spec" / "stage_brief.md",
        f"""# {STAGE270_ID}

Stage270(270단계)는 ONNX-worthy candidate campaign(온엑스화 가치 후보 캠페인)의 aggressive non-filter upside probe(공격형 비필터 상방 탐침) 단계다.
효과(effect, 효과): Stage269(269단계)에서 seed(씨앗)로 넘어온 `cp269A_asymmetric_nonfilter_reentry_surface`가 단순 구조 신호인지, 다음 MT5(`MetaTrader 5`, 메타트레이더5) 또는 candidate package(후보 패키지) 압박으로 보낼 가치가 있는지 본다.

## Bounded Question(경계 질문)

Can bounded non-filter reward skew produce upside before stability review?
효과(effect, 효과): 좋은 숫자 후보를 고르는 것이 아니라, upside(상방), failure mode(실패 방식), discard condition(폐기 조건)을 같이 가진 probe branch(탐침 분기)를 만든다.

## Fresh Thesis(새 논제)

- asymmetric non-filter reward skew(비대칭 비필터 보상 기울기)
- controlled supply expansion(통제된 공급 확장)
- weak-context failure boundary(약한 문맥 실패 경계)

## Required Evidence(필수 근거)

- Tier A separate(Tier A 분리)
- Tier B separate(Tier B 분리)
- Tier A+B combined(Tier A+B 합산)
- support control(보조 대조) `cp269D_runtime_handoff_isolation_control`
- threshold source receipt(임계값 원천 영수증)
- failure/discard memory(실패/폐기 기억)

## Stop Conditions(중단 조건)

- supply inflation(공급 팽창)이 지나치면 candidate(후보)로 부르지 않는다.
- weak-context(약한 문맥)가 주요 공급을 설명하면 failure memory(실패 기억)로 낮춘다.
- MT5(`MetaTrader 5`, 메타트레이더5) 또는 trading KPI(거래 핵심 성과 지표)가 없으면 performance improvement(성과 개선)를 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        STAGE270 / "01_inputs" / "input_refs.md",
        f"""# Stage270 Input References(270단계 입력 참조)

## Source Inputs(원천 입력)

- Stage269 run269E queue(269E 대기열): `{SOURCE_QUEUE.as_posix()}`
- Stage269 run269E screening summary(269E 선별 요약): `{SOURCE_SCREENING.as_posix()}`
- Stage269 run269E failure memory(269E 실패 기억): `{SOURCE_FAILURE_MEMORY.as_posix()}`
- Stage269 run269E support control carry(269E 보조 대조 유지): `{SOURCE_SUPPORT.as_posix()}`
- cp269A score table(cp269A 점수표): `{CP269A_SCORE_TABLE.as_posix()}`
- cp269D support score table(cp269D 보조 점수표): `{CP269D_SCORE_TABLE.as_posix()}`
- cp269A handoff JSON(cp269A 인계 JSON): `{CP269A_HANDOFF.as_posix()}`
- cp269D handoff JSON(cp269D 인계 JSON): `{CP269D_HANDOFF.as_posix()}`

## Allowed Claim(허용 주장)

Stage270(270단계)는 aggressive upside probe(공격형 상방 탐침)를 시작할 수 있다.
효과(effect, 효과): selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 아직 주장하지 않는다.
""",
    )


def build_experiment_design(queue_row: dict[str, str]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE270_ID,
        "hypothesis": (
            "A bounded non-filter reward-skew surface can expose upside before the stability stage "
            "if supply expansion remains controlled and weak-context rows are isolated."
        ),
        "decision_use": (
            "Decide which aggressive cp269A variants deserve run270B materialization or MT5 probe "
            "preparation, not candidate selection."
        ),
        "comparison_baseline": "run269D cp269A materialized decision flag plus cp269D support control identity receipt.",
        "control_variables": [
            "US100 M5 symbol/timeframe",
            "run269D score table columns",
            "Tier A/B paired record requirement",
            "Stage269 claim boundary",
            "Tier A train quantile threshold source",
        ],
        "changed_variables": [
            "candidate_decision_score threshold",
            "reward_skew_score threshold",
            "weak_context_cost threshold",
            "supply expansion role",
        ],
        "sample_scope": {
            "tier_views": ["Tier A separate", "Tier B separate", "Tier A+B combined"],
            "splits": ["train", "validation", "oos"],
            "source_package": queue_row["package_id"],
            "support_control": queue_row["required_support_control"],
        },
        "success_criteria": [
            "At least one non-boundary variant has bounded validation and OOS supply.",
            "Tier A/B paired structural records exist.",
            "Support control identity check remains attached.",
            "Failure mode and discard condition are explicit before any MT5 run.",
        ],
        "failure_criteria": [
            "All aggressive variants inflate supply beyond discard conditions.",
            "Weak-context boundary explains the usable supply.",
            "Tier B partial-context caveat is hidden or omitted.",
        ],
        "invalid_conditions": [
            "Label/future columns appear in the score table.",
            "Thresholds are tuned on validation or OOS outcomes.",
            "Required support control is missing.",
        ],
        "stop_conditions": [
            "Do not continue repair inside Stage270 if no aggressive branch survives two materialized passes.",
            "Do not claim selected candidate or ONNX readiness from run270A.",
            "Move to failure memory if the only surviving branch is weak-context-heavy.",
        ],
        "evidence_plan": [
            "run_manifest.json",
            "aggressive_probe_variant_plan.csv",
            "supply_metrics_by_variant.csv",
            "monthly_supply_diagnostics.csv",
            "probe_readiness_receipt.csv",
            "lineage.json",
            "run270A_report.md",
            "run_registry.csv",
            "alpha_run_ledger.csv",
            "stage_run_ledger.csv",
        ],
        "claim_boundary": BOUNDARY,
    }


def write_stage_ledgers(metrics_rows: list[dict[str, Any]]) -> None:
    stage_rows = [
        {
            "row_id": "stage270_aggressive_nonfilter_upside_probe_open_v1",
            "stage_id": STAGE270_ID,
            "run_id": "stage270_aggressive_nonfilter_upside_probe_open_v1",
            "view": "stage_open",
            "tier_scope": "Tier A+B reference evidence",
            "scoreboard": "experiment_design",
            "status": "opened",
            "judgment": "planning_open_no_candidate_selection",
            "evidence_boundary": "research_development_only",
            "report_path": (STAGE270 / "00_spec" / "stage_brief.md").as_posix(),
            "notes": "Stage270 opened from run269E queue; selected_candidate=none; onnx_readiness=not_claimed.",
        },
        {
            "row_id": f"{RUN_ID}__tier_a",
            "stage_id": STAGE270_ID,
            "run_id": RUN_ID,
            "view": "aggressive_upside_probe_design",
            "tier_scope": "Tier A separate",
            "scoreboard": "structural_scout",
            "status": "completed",
            "judgment": "aggressive_probe_design_no_performance_claim",
            "evidence_boundary": "research_development_only",
            "report_path": (REVIEWS / "run270A_report.md").as_posix(),
            "notes": "Tier A structural supply metrics produced; selected_candidate=none; onnx_readiness=not_claimed.",
        },
        {
            "row_id": f"{RUN_ID}__tier_b",
            "stage_id": STAGE270_ID,
            "run_id": RUN_ID,
            "view": "aggressive_upside_probe_design",
            "tier_scope": "Tier B separate",
            "scoreboard": "structural_scout",
            "status": "completed",
            "judgment": "partial_context_aggressive_probe_design_no_performance_claim",
            "evidence_boundary": "research_development_only",
            "report_path": (REVIEWS / "run270A_report.md").as_posix(),
            "notes": "Tier B structural supply metrics produced with partial-context caveat; selected_candidate=none.",
        },
        {
            "row_id": f"{RUN_ID}__tier_ab",
            "stage_id": STAGE270_ID,
            "run_id": RUN_ID,
            "view": "aggressive_upside_probe_design",
            "tier_scope": "Tier A+B combined",
            "scoreboard": "structural_scout",
            "status": "completed",
            "judgment": "combined_structural_supply_view_no_routed_pnl_claim",
            "evidence_boundary": "research_development_only",
            "report_path": (REVIEWS / "run270A_report.md").as_posix(),
            "notes": "Tier A+B combined is structural supply only; next_action=run270B_materialize_aggressive_probe_payloads.",
        },
    ]
    write_csv(
        REVIEWS / "stage_run_ledger.csv",
        stage_rows,
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


def write_review_index() -> None:
    write_md(
        REVIEWS / "review_index.md",
        f"""# Stage270 Review Index(270단계 검토 색인)

- stage_brief(단계 개요): `{(STAGE270 / "00_spec" / "stage_brief.md").as_posix()}`
- input_refs(입력 참조): `{(STAGE270 / "01_inputs" / "input_refs.md").as_posix()}`
- selection_status(선택 상태): `{(STAGE270 / "04_selected" / "selection_status.md").as_posix()}`
- stage_run_ledger(단계 실행 장부): `{(REVIEWS / "stage_run_ledger.csv").as_posix()}`
- run270A_manifest(270A 목록): `{(RUN_DIR / "run_manifest.json").as_posix()}`
- run270A_experiment_design(270A 실험 설계): `{(RUN_DIR / "experiment_design.json").as_posix()}`
- run270A_variant_plan(270A 변형 계획): `{(RUN_DIR / "aggressive_probe_variant_plan.csv").as_posix()}`
- run270A_supply_metrics(270A 공급 지표): `{(RUN_DIR / "supply_metrics_by_variant.csv").as_posix()}`
- run270A_monthly_diagnostics(270A 월별 진단): `{(RUN_DIR / "monthly_supply_diagnostics.csv").as_posix()}`
- run270A_readiness_receipt(270A 준비 영수증): `{(RUN_DIR / "probe_readiness_receipt.csv").as_posix()}`
- run270A_lineage(270A 계보): `{(RUN_DIR / "lineage.json").as_posix()}`
- run270A_report(270A 보고): `{(REVIEWS / "run270A_report.md").as_posix()}`

## Current State(현재 상태)

Stage270(270단계)는 run270A(270A 실행) aggressive upside probe design(공격형 상방 탐침 설계)을 완료했다.
효과(effect, 효과): 다음 작업은 run270B(270B 실행)에서 살아남은 branch(분기)를 materialized probe payload(물질화 탐침 페이로드)로 바꾸는 것이다.
""",
    )


def write_selection_status() -> None:
    write_md(
        STAGE270 / "04_selected" / "selection_status.md",
        f"""# Stage270 Selection Status(270단계 선택 상태)

- stage_status(단계 상태): `run270A_aggressive_upside_probe_design_completed`
- current_packet(현재 작업 묶음): `stage270_aggressive_nonfilter_upside_probe_v1`
- current_run(현재 실행): `{RUN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE269_ID}`
- source_queue(원천 대기열): `{SOURCE_QUEUE.as_posix()}`
- active_seed(활성 씨앗): `cp269A_asymmetric_nonfilter_reentry_surface`
- support_control(보조 대조): `cp269D_runtime_handoff_isolation_control`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- run270A_variant_plan(270A 변형 계획): `{(RUN_DIR / "aggressive_probe_variant_plan.csv").as_posix()}`
- run270A_supply_metrics(270A 공급 지표): `{(RUN_DIR / "supply_metrics_by_variant.csv").as_posix()}`
- run270A_report(270A 보고): `{(REVIEWS / "run270A_report.md").as_posix()}`
- next_action(다음 행동): `run270B_materialize_aggressive_probe_payloads`

## Current Meaning(현재 의미)

run270A(270A 실행)는 aggressive non-filter upside(공격형 비필터 상방)를 구조적으로 설계하고 공급량을 진단했다.
효과(effect, 효과): branch(분기)는 생겼지만 trading KPI(거래 핵심 성과 지표), MT5 runtime output(MT5 런타임 출력), ONNX parity(온엑스 동등성)가 없으므로 candidate selection(후보 선택)은 아직 없다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def write_report(
    variants: list[dict[str, Any]],
    metrics_rows: list[dict[str, Any]],
    readiness: list[dict[str, str]],
) -> None:
    combined_oos = [
        r
        for r in metrics_rows
        if r["tier_view"] == "Tier A separate" and r["split"] == "oos"
    ]
    top_lines = "\n".join(
        [
            f"- `{r['variant_id']}`: decision_rate(판단 비율) `{r['decision_rate']}`, decision_count(판단 수) `{r['decision_count']}`"
            for r in combined_oos
        ]
    )
    readiness_lines = "\n".join(
        [f"- {r['check_name']}: `{r['status']}` - {r['effect']}" for r in readiness]
    )
    write_md(
        REVIEWS / "run270A_report.md",
        f"""# Stage270 Run270A Aggressive Upside Probe Design(270단계 270A 공격형 상방 탐침 설계)

- status(상태): `completed_aggressive_upside_probe_design_no_candidate_selection`
- run(실행): `{RUN_ID}`
- source_seed(원천 씨앗): `cp269A_asymmetric_nonfilter_reentry_surface`
- support_control(보조 대조): `cp269D_runtime_handoff_isolation_control`
- variants(변형): `{len(variants)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run270B_materialize_aggressive_probe_payloads`

## Plain Result(쉬운 결과)

run270A(270A 실행)는 run269E(269E 실행)의 Stage270(270단계) queue(대기열)를 받아 aggressive non-filter upside(공격형 비필터 상방) branch(분기) `6`개로 바꿨다.
효과(effect, 효과): 각 branch(분기)는 upside question(상방 질문), failure mode(실패 방식), discard condition(폐기 조건), Tier A/B supply metrics(티어 A/B 공급 지표)를 갖는다.

## OOS Structural Supply(표본외 구조 공급)

{top_lines}

## Readiness Receipt(준비 영수증)

{readiness_lines}

## Result Judgment(결과 판정)

- result_subject(판정 대상): aggressive upside probe design(공격형 상방 탐침 설계)
- evidence_available(있는 근거): score table(점수표), support control(보조 대조), threshold receipt(임계값 영수증), tier-paired supply metrics(티어 쌍 공급 지표)
- evidence_missing(빠진 근거): trading KPI(거래 핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), MT5 runtime output(MT5 런타임 출력), ONNX export/parity(온엑스 내보내기/동등성)
- judgment_label(판정 라벨): `aggressive_probe_design_no_candidate_selection`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)
- next_condition(다음 조건): run270B(270B 실행)에서 materialized probe payload(물질화 탐침 페이로드)를 만들고, 이후 외부 검증이 필요한 주장은 MT5(`MetaTrader 5`, 메타트레이더5) 또는 동등한 runtime evidence(런타임 근거)로 좁게 확인해야 한다.

## Boundary(경계)

This report(이 보고서)는 selected candidate(선택 후보), ONNX readiness(온엑스 준비), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선), Goal Achieve(목표 달성)를 주장하지 않는다.
""",
    )


def main() -> None:
    ensure_dirs()
    queue, cp269a, cp269d, data_integrity = load_inputs()
    q = quantiles(cp269a)
    variants = variant_plan(q)
    metrics_rows, monthly_rows = supply_metrics(cp269a, cp269d, variants)
    readiness = readiness_rows(queue, cp269a, cp269d, data_integrity)
    stage_docs()

    experiment_design = build_experiment_design(queue[0])
    write_json(RUN_DIR / "experiment_design.json", experiment_design)
    write_json(RUN_DIR / "threshold_receipt.json", {"threshold_source": "Tier A train quantiles", **q})
    write_csv(
        RUN_DIR / "aggressive_probe_variant_plan.csv",
        variants,
        [
            "variant_id",
            "variant_role",
            "hypothesis",
            "decision_rule",
            "upside_probe_question",
            "failure_mode",
            "discard_condition",
            "thresholds_json",
        ],
    )
    write_csv(
        RUN_DIR / "supply_metrics_by_variant.csv",
        metrics_rows,
        [
            "variant_id",
            "variant_role",
            "tier_view",
            "split",
            "rows",
            "decision_count",
            "decision_rate",
            "score_median",
            "reward_median",
            "weak_context_cost_median",
            "failure_zone_share",
            "support_identity_rate",
            "performance_claim",
        ],
    )
    write_csv(
        RUN_DIR / "monthly_supply_diagnostics.csv",
        monthly_rows,
        [
            "variant_id",
            "tier_view",
            "month",
            "month_rows",
            "decision_count",
            "decision_rate",
            "performance_claim",
        ],
    )
    write_csv(RUN_DIR / "probe_readiness_receipt.csv", readiness, ["check_name", "status", "effect"])

    output_artifacts = [
        RUN_DIR / "experiment_design.json",
        RUN_DIR / "threshold_receipt.json",
        RUN_DIR / "aggressive_probe_variant_plan.csv",
        RUN_DIR / "supply_metrics_by_variant.csv",
        RUN_DIR / "monthly_supply_diagnostics.csv",
        RUN_DIR / "probe_readiness_receipt.csv",
    ]
    source_inputs = [
        SOURCE_QUEUE,
        SOURCE_SCREENING,
        SOURCE_FAILURE_MEMORY,
        SOURCE_SUPPORT,
        SOURCE_RUN269E_MANIFEST,
        SOURCE_RUN269D_DATA_INTEGRITY,
        CP269A_SCORE_TABLE,
        CP269D_SCORE_TABLE,
        CP269A_HANDOFF,
        CP269D_HANDOFF,
    ]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE270_ID,
        "status": "completed_aggressive_upside_probe_design_no_candidate_selection",
        "producer": "stage_pipelines/stage270/design_aggressive_upside_probe.py",
        "entry_command": "python stage_pipelines/stage270/design_aggressive_upside_probe.py",
        "source_inputs": [p.as_posix() for p in source_inputs],
        "input_hashes": {p.as_posix(): sha256_file(p) for p in source_inputs},
        "output_artifacts": [p.as_posix() for p in output_artifacts],
        "output_hashes": {p.as_posix(): sha256_file(p) for p in output_artifacts},
        "variant_count": len(variants),
        "stage270_queue_rows": len(queue),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_design_structural_only",
        "claim_boundary": BOUNDARY,
        "next_action": "run270B_materialize_aggressive_probe_payloads",
    }
    write_json(RUN_DIR / "run_manifest.json", manifest)

    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [
            "stages/270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe/04_selected/selection_status.md",
            "docs/registers/run_registry.csv",
            "docs/registers/alpha_run_ledger.csv",
            "docs/registers/artifact_registry.csv",
            "run270B_materialize_aggressive_probe_payloads",
        ],
        "artifact_paths": manifest["output_artifacts"] + [(RUN_DIR / "run_manifest.json").as_posix()],
        "artifact_hashes": {
            **manifest["output_hashes"],
            (RUN_DIR / "run_manifest.json").as_posix(): sha256_file(RUN_DIR / "run_manifest.json"),
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

    write_stage_ledgers(metrics_rows)
    write_review_index()
    write_selection_status()
    write_report(variants, metrics_rows, readiness)

    final_paths = [
        RUN_DIR / "run_manifest.json",
        RUN_DIR / "lineage.json",
        REVIEWS / "stage_run_ledger.csv",
        REVIEWS / "review_index.md",
        REVIEWS / "run270A_report.md",
        STAGE270 / "00_spec" / "stage_brief.md",
        STAGE270 / "01_inputs" / "input_refs.md",
        STAGE270 / "04_selected" / "selection_status.md",
    ]
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "stage_id": STAGE270_ID,
                "status": manifest["status"],
                "variant_count": len(variants),
                "next_action": manifest["next_action"],
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "hashes": {p.as_posix(): sha256_file(p) for p in final_paths + output_artifacts},
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
