from __future__ import annotations

import ast
import csv
import hashlib
import json
import sys
from collections import defaultdict
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from stage_pipelines.stage293 import design_materialize_profit_scale_density_calibration_rebuild as s293  # noqa: E402


STAGE_ID = "295_onnx_candidate_campaign__split_consistent_outcome_distillation_rebuild"
NEXT_STAGE_ID = "296_onnx_candidate_campaign__density_floor_profit_expansion_rebuild"
RUN_ID = "run295C_review_split_consistent_outcome_distillation_mt5_probe_v1"
RUN_NUMBER = "run295C"
SOURCE_RUN_ID = "run295B_split_consistent_outcome_distillation_mt5_probe_v1"
PARENT_RUN_ID = "run295A_design_split_consistent_outcome_distillation_rebuild_v1"
UPDATED_ON = "2026-05-24"
NEXT_ACTION = "run296A_design_density_floor_profit_expansion_rebuild_packet"
STATUS = "completed_split_consistent_outcome_distillation_review_no_candidate_stage296_opened"
JUDGMENT = "split_consistent_outcome_distillation_runtime_probe_negative_density_profit_curve_gate_failed"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN295A = STAGE_ROOT / "02_runs" / "run295A"
RUN295B = STAGE_ROOT / "02_runs" / "run295B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_MANIFEST = RUN295A / "candidate_payload_manifest.csv"
SOURCE_PROXY_SCOREBOARD = RUN295A / "model_scout_scoreboard.csv"
SOURCE_EXECUTION = RUN295B / "execution_result.json"
SOURCE_KPI = RUN295B / "mt5_kpi_summary.csv"
SOURCE_REPORT = REVIEWS / "run295B_split_consistent_outcome_distillation_mt5_probe_report.md"

SCOREBOARD = RUN_ROOT / "split_consistent_outcome_distillation_review_scoreboard.csv"
CURVE_DIAGNOSTICS = RUN_ROOT / "curve_pocket_proxy_diagnostics.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage296_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run295C_split_consistent_outcome_distillation_review_stage296_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage295_split_consistent_outcome_distillation_review_stage296_open.md"

NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
NEXT_STAGE_INPUT = NEXT_STAGE_ROOT / "01_inputs" / "stage296_seed_queue.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SCOREBOARD_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "validation_net_profit",
    "validation_pf",
    "validation_trade_count",
    "validation_trades_per_day",
    "validation_max_drawdown",
    "validation_drawdown_percent",
    "validation_recovery",
    "validation_expectancy",
    "oos_net_profit",
    "oos_pf",
    "oos_trade_count",
    "oos_trades_per_day",
    "oos_max_drawdown",
    "oos_drawdown_percent",
    "oos_recovery",
    "oos_expectancy",
    "combined_net_profit",
    "density_gate",
    "split_profit_gate",
    "curve_proxy_gate",
    "selected_candidate",
    "review_label",
    "failure_reason",
    "next_role",
    "claim_boundary",
)
CURVE_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "split",
    "net_profit",
    "max_drawdown",
    "drawdown_percent",
    "drawdown_to_net_ratio",
    "curve_proxy_gate",
    "effect",
)
FAILURE_COLUMNS = (
    "failure_id",
    "materialized_branch_id",
    "package_id",
    "failure_class",
    "evidence",
    "salvage_value",
    "reopen_condition",
    "claim_boundary",
)
NEXT_QUEUE_COLUMNS = (
    "seed_id",
    "source_stage_id",
    "source_run_id",
    "seed_role",
    "hypothesis",
    "broad_sweep",
    "aggressive_sweep",
    "defensive_sweep",
    "success_gate",
    "discard_condition",
    "prior_stage_refs",
    "claim_boundary",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open(newline="", encoding="utf-8-sig") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def parse_literal_dict(text: str) -> dict[str, Any]:
    value = ast.literal_eval(text)
    return value if isinstance(value, dict) else {}


def parse_mt5_date(text: str) -> date:
    return date.fromisoformat(text.replace(".", "-"))


def days_from_attempt(attempt: Mapping[str, Any]) -> int:
    tester = attempt.get("ini", {}).get("tester", {}) if isinstance(attempt.get("ini"), Mapping) else {}
    from_date = parse_mt5_date(str(tester["FromDate"]))
    to_date = parse_mt5_date(str(tester["ToDate"]))
    return (to_date - from_date).days + 1


def package_by_materialized_id() -> dict[str, str]:
    return {row["materialized_branch_id"]: row.get("package_id", "") for row in read_csv_rows(SOURCE_MANIFEST)}


def load_runtime_rows() -> list[dict[str, Any]]:
    execution = json.loads(io_path(SOURCE_EXECUTION).read_text(encoding="utf-8-sig"))
    attempts = {row["attempt_name"]: row for row in execution.get("attempts", [])}
    packages = package_by_materialized_id()
    rows: list[dict[str, Any]] = []
    for kpi_row in read_csv_rows(SOURCE_KPI):
        metrics = parse_literal_dict(kpi_row["metrics"])
        report = parse_literal_dict(kpi_row["report"])
        attempt_name = str(report.get("attempt_name", ""))
        attempt = attempts.get(attempt_name, {})
        materialized_id = str(attempt.get("stage295_branch_id") or attempt.get("materialized_branch_id") or attempt_name)
        trade_count = float(metrics.get("trade_count") or 0.0)
        days = days_from_attempt(attempt) if attempt else 0
        rows.append(
            {
                "materialized_branch_id": materialized_id,
                "package_id": str(attempt.get("package_id") or packages.get(materialized_id, "")),
                "attempt_name": attempt_name,
                "route_role": kpi_row.get("route_role", ""),
                "tier_scope": kpi_row.get("tier_scope", ""),
                "split": kpi_row.get("split", ""),
                "net_profit": float(metrics.get("net_profit") or 0.0),
                "pf": float(metrics.get("profit_factor") or 0.0),
                "trade_count": int(trade_count),
                "trades_per_day": trade_count / days if days else 0.0,
                "max_drawdown": float(metrics.get("max_drawdown_amount") or metrics.get("equity_drawdown_maximal_amount") or 0.0),
                "drawdown_percent": float(metrics.get("max_drawdown_percent") or metrics.get("equity_drawdown_maximal_percent") or 0.0),
                "recovery": float(metrics.get("recovery_factor") or 0.0),
                "expectancy": float(metrics.get("expectancy") or 0.0),
                "report_path": str(metrics.get("report_path", "")),
            }
        )
    return rows


def curve_gate(row: Mapping[str, Any]) -> bool:
    net = float(row["net_profit"])
    drawdown = float(row["max_drawdown"])
    drawdown_percent = float(row["drawdown_percent"])
    if net <= 0:
        return False
    return (drawdown / max(abs(net), 1e-9)) <= 0.75 and drawdown_percent <= 10.0


def build_review_rows(runtime_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    routed = [row for row in runtime_rows if row["route_role"] == "actual_routed_total"]
    by_candidate: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in routed:
        by_candidate[str(row["materialized_branch_id"])][str(row["split"])] = row

    scoreboard: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    for materialized_id, split_rows in sorted(by_candidate.items()):
        val = split_rows.get("validation_is")
        oos = split_rows.get("oos")
        if not val or not oos:
            continue
        package_id = str(val.get("package_id") or oos.get("package_id") or materialized_id)
        density_gate = 4.0 <= float(val["trades_per_day"]) <= 10.0 and 4.0 <= float(oos["trades_per_day"]) <= 10.0
        split_profit_gate = (
            float(val["net_profit"]) > 0.0
            and float(oos["net_profit"]) > 0.0
            and float(val["pf"]) > 1.0
            and float(oos["pf"]) > 1.0
            and float(val["recovery"]) > 0.0
            and float(oos["recovery"]) > 0.0
            and float(val["expectancy"]) > 0.0
            and float(oos["expectancy"]) > 0.0
        )
        curve_proxy_gate = curve_gate(val) and curve_gate(oos)
        selected = density_gate and split_profit_gate and curve_proxy_gate
        combined_net = float(val["net_profit"]) + float(oos["net_profit"])
        if selected:
            review_label = "candidate_gate_passed"
            next_role = "adapter_package_candidate"
            failure_reason = ""
        elif split_profit_gate and not density_gate:
            review_label = "profit_positive_density_failed"
            next_role = "salvage_as_profit_clue_not_candidate"
            failure_reason = "validation/OOS profit positive, but trades/day below 4 in both splits."
        elif float(oos["net_profit"]) > 0.0 and float(oos["pf"]) > 1.0 and float(val["net_profit"]) <= 0.0:
            review_label = "oos_positive_validation_negative"
            next_role = "salvage_oos_scale_clue_not_candidate"
            failure_reason = "OOS positive, but validation net profit remains negative."
        else:
            review_label = "failed_density_profit_curve_gate"
            next_role = "failure_memory_only"
            failure_reason = "Does not satisfy split profit, density, and curve proxy gates together."
        scoreboard.append(
            {
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "validation_net_profit": val["net_profit"],
                "validation_pf": val["pf"],
                "validation_trade_count": val["trade_count"],
                "validation_trades_per_day": val["trades_per_day"],
                "validation_max_drawdown": val["max_drawdown"],
                "validation_drawdown_percent": val["drawdown_percent"],
                "validation_recovery": val["recovery"],
                "validation_expectancy": val["expectancy"],
                "oos_net_profit": oos["net_profit"],
                "oos_pf": oos["pf"],
                "oos_trade_count": oos["trade_count"],
                "oos_trades_per_day": oos["trades_per_day"],
                "oos_max_drawdown": oos["max_drawdown"],
                "oos_drawdown_percent": oos["drawdown_percent"],
                "oos_recovery": oos["recovery"],
                "oos_expectancy": oos["expectancy"],
                "combined_net_profit": combined_net,
                "density_gate": "passed" if density_gate else "failed",
                "split_profit_gate": "passed" if split_profit_gate else "failed",
                "curve_proxy_gate": "passed" if curve_proxy_gate else "failed",
                "selected_candidate": package_id if selected else "none",
                "review_label": review_label,
                "failure_reason": failure_reason,
                "next_role": next_role,
                "claim_boundary": BOUNDARY,
            }
        )
        for split_name, row in (("validation_is", val), ("oos", oos)):
            drawdown_ratio = float(row["max_drawdown"]) / max(abs(float(row["net_profit"])), 1e-9) if float(row["net_profit"]) != 0.0 else 999999.0
            curve_rows.append(
                {
                    "materialized_branch_id": materialized_id,
                    "package_id": package_id,
                    "split": split_name,
                    "net_profit": row["net_profit"],
                    "max_drawdown": row["max_drawdown"],
                    "drawdown_percent": row["drawdown_percent"],
                    "drawdown_to_net_ratio": drawdown_ratio,
                    "curve_proxy_gate": "passed" if curve_gate(row) else "failed",
                    "effect": "Uses report-level drawdown proxy only; detailed zoom curve gate remains required before Adapter/ONNX.",
                }
            )
        failure_rows.append(
            {
                "failure_id": f"NEG-ST295-{materialized_id}",
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "failure_class": review_label,
                "evidence": failure_reason or "Candidate passed review gates.",
                "salvage_value": salvage_value(review_label, package_id),
                "reopen_condition": "Reopen only through a fresh density-floor profit expansion thesis that keeps 4-10 trades/day and split-positive net/PF.",
                "claim_boundary": BOUNDARY,
            }
        )
    return scoreboard, curve_rows, failure_rows


def salvage_value(review_label: str, package_id: str) -> str:
    if review_label == "profit_positive_density_failed":
        return f"{package_id} preserves split-positive profit/PF and can seed density expansion, not Adapter."
    if review_label == "oos_positive_validation_negative":
        return f"{package_id} preserves OOS upside clue, but validation damage must be rebuilt from a new surface."
    if review_label == "candidate_gate_passed":
        return "Adapter package gate candidate."
    return "Failure memory only."


def next_stage_rows() -> list[dict[str, Any]]:
    refs = ";".join(
        [
            "stage267_reference_evidence",
            "stage294_oos_positive_validation_negative_flip_probe",
            "stage295_density_collapse_and_low_density_profit_clue",
        ]
    )
    return [
        {
            "seed_id": "stage296_density_floor_profit_expansion_primary",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_primary(새 논제 주축)",
            "hypothesis": "Density-floor profit expansion(거래 밀도 하한 수익 확장)이 cp295D의 split-positive(분할 양수) 단서를 4-10 trades/day(일 4-10거래) 후보로 확장할 수 있다.",
            "broad_sweep": "profit-positive state expansion, per-session density quota, adjacent state re-entry, hold 3-7 bar surfaces(수익 양수 상태 확장/세션별 거래 밀도 할당/인접 상태 재진입/3-7봉 보유 표면)",
            "aggressive_sweep": "controlled expansion to 6, 8, and 10 trades/day using payoff-ranked bands(보상 순위 구간으로 일 6/8/10거래까지 통제 확장)",
            "defensive_sweep": "validation damage veto, rolling drawdown pocket cap, weak-session rejection(검증 손상 거부/롤링 손실 포켓 상한/약한 세션 거부)",
            "success_gate": "validation and OOS both net-positive, PF>1, recovery/expectancy positive, 4-10 trades/day, no deep zoomed curve pocket(검증과 표본외 양수, PF>1, 회복/기대값 양수, 일 4-10거래, 깊은 확대 곡선 패임 없음)",
            "discard_condition": "density returns only by validation loss or drawdown pocket concentration(거래 밀도가 검증 손실이나 손실 포켓 집중으로만 돌아옴)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage296_validation_damage_countermodel",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_defensive(새 논제 방어축)",
            "hypothesis": "Validation-damage countermodel(검증 손상 반대 모델)이 cp295B/cp295E의 OOS upside(표본외 상방)를 보존하면서 validation loss(검증 손실)를 제거할 수 있다.",
            "broad_sweep": "train-only damage labels, session/month counterfeatures, density floor constrained acceptance(학습 전용 손상 라벨/세션·월 반대 피처/밀도 하한 제약 수락)",
            "aggressive_sweep": "only re-expand OOS-positive bands after validation damage clears(검증 손상 제거 후에만 표본외 양수 구간 재확장)",
            "defensive_sweep": "hard reject bands with negative validation expectancy or DD/net ratio above 0.75(검증 기대값 음수 또는 DD/net 0.75 초과 구간 강한 거부)",
            "success_gate": "OOS upside stays positive while validation net/PF flips positive above 4 trades/day(표본외 상방을 보존하면서 검증 순수익/PF가 일 4거래 이상에서 양수 전환)",
            "discard_condition": "countermodel becomes thin trade-count repair below 4 trades/day(반대 모델이 일 4거래 미만 얇은 수리로 변함)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage296_aggressive_payoff_tail_capture",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_aggressive(새 논제 공격축)",
            "hypothesis": "Aggressive payoff-tail capture(공격형 보상 꼬리 포착)가 순수익 규모를 키우면서 10 trades/day(일 10거래) 상한 안에 머물 수 있다.",
            "broad_sweep": "payoff-ranked entry widening, asymmetric hold, opposite-signal exit, cost-aware tail filter(보상 순위 진입 확장/비대칭 보유/반대 신호 청산/비용 인식 꼬리 필터)",
            "aggressive_sweep": "expand high payoff tails first, then fill density with neutral-risk bands(고보상 꼬리를 먼저 확장한 뒤 중립 위험 구간으로 밀도 채움)",
            "defensive_sweep": "month/session concentration cap and zoom curve pocket audit(月/세션 집중 상한과 확대 곡선 포켓 감사)",
            "success_gate": "higher net profit and PF without losing split stability or 4-10 trades/day density(분할 안정성과 일 4-10거래를 잃지 않고 순수익과 PF 개선)",
            "discard_condition": "net profit comes from one pocket, one month, or excessive drawdown(순수익이 한 포켓/한 달/과도한 손실폭에서만 나옴)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
    ]


def result_rows(scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = [
        {
            "result_subject": "Stage295 split-consistent outcome distillation MT5 review(295단계 분할 일관 결과 증류 MT5 검토)",
            "evidence_available": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)};source_kpi={rel(SOURCE_KPI)}",
            "evidence_missing": "Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성), MT5 runtime reproduction(MT5 런타임 재현)",
            "judgment_label": "negative",
            "judgment_class": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage295는 OOS 단서와 저밀도 수익 단서를 남겼지만, 목표인 일 4-10거래와 split-positive 수익/곡선 조건을 동시에 만족하지 못했다.",
        }
    ]
    gates = [
        {
            "gate_name": "mt5_runtime_probe(MT5 런타임 탐침)",
            "status": "passed",
            "evidence_path": rel(SOURCE_KPI),
            "effect": "36개 MT5 실행 결과로 후보를 판정했다.",
        },
        {
            "gate_name": "minimum_trade_and_density(최소 거래수와 밀도)",
            "status": "failed",
            "evidence_path": rel(SCOREBOARD),
            "effect": "어떤 후보도 validation/OOS 모두에서 일 4-10거래를 만족하지 못했다.",
        },
        {
            "gate_name": "profit_efficiency_curve(수익/효율/곡선)",
            "status": "failed",
            "evidence_path": rel(SCOREBOARD),
            "effect": "split-positive 수익, PF, 회복, 기대값, drawdown proxy(손실폭 대리 지표)를 함께 통과한 후보가 없다.",
        },
        {
            "gate_name": "adapter_package(어댑터 패키지)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "후보 게이트 실패 때문에 Adapter(어댑터)를 만들지 않는다.",
        },
        {
            "gate_name": "onnx_readiness(ONNX 준비)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "Adapter(어댑터)와 parity(동등성) 전에는 ONNX(온엑스)를 시작하지 않는다.",
        },
    ]
    return rows, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run295C Split-Consistent Outcome Distillation Review(295C 분할 일관 결과 증류 검토)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(ONNX 준비): `not_started`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        f"- next_stage(다음 단계): `{NEXT_STAGE_ID}`",
        "",
        "Effect(효과): Stage295(295단계)는 Stage294(294단계)의 OOS-positive/validation-negative(표본외 양수/검증 음수) 단서를 split-consistent outcome distillation(분할 일관 결과 증류)로 시험했지만, 후보 게이트를 넘지 못했다. 수익 단서는 보존하되 Adapter/ONNX(어댑터/온엑스)로 넘기지 않고 Stage296(296단계) 새 논제로 연다.",
        "",
        "| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | val/day(검증 일거래) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | OOS/day(표본외 일거래) | label(라벨) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {pkg} | {vn:.2f} | {vpf:.2f} | {vtd:.2f} | {on:.2f} | {opf:.2f} | {otd:.2f} | {label} |".format(
                pkg=row["package_id"],
                vn=float(row["validation_net_profit"]),
                vpf=float(row["validation_pf"]),
                vtd=float(row["validation_trades_per_day"]),
                on=float(row["oos_net_profit"]),
                opf=float(row["oos_pf"]),
                otd=float(row["oos_trades_per_day"]),
                label=row["review_label"],
            )
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- cp295D(295D 후보)는 validation/OOS(검증/표본외) 모두 순수익과 PF(수익 팩터)가 양수지만 일 거래수가 0.8대라 목표 4-10에 못 미친다.",
            "- cp295B/cp295E(295B/295E 후보)는 OOS(표본외) 순수익 단서를 키웠지만 validation(검증)이 음수이고 일 거래수도 4 미만이다.",
            "- 따라서 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 없다.",
            "",
            "## Stage296 Thesis(296단계 논제)",
            "",
            f"Stage296(296단계)는 seed(씨앗) `{len(queue_rows)}`개로 density-floor profit expansion(거래 밀도 하한 수익 확장)을 연다. 효과는 cp295D의 수익 단서와 cp295B/E의 OOS 규모 단서를 후보로 보존하지 않고, 4-10 trades/day(일 4-10거래)를 먼저 만족하는 새 decision/risk surface(판단/위험 표면)로 재구성하는 것이다.",
            "",
            f"Claim boundary(주장 경계): `{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def decision_markdown() -> str:
    return f"""# Stage295 Decision(295단계 결정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): Stage295(295단계)는 ONNX-worthy candidate(온엑스화 가치 후보)를 만들지 못했다.
- next_stage(다음 단계): `{NEXT_STAGE_ID}`

Effect(효과): 낮은 거래수의 수익 단서와 OOS(표본외) 상방 단서를 그대로 후보로 승격하지 않고, Stage296(296단계)에서 거래 밀도 4-10을 보존하는 새 profit expansion(수익 확장) 질문으로 넘긴다.
"""


def write_stage296_scaffold(queue_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    for subdir in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        io_path(NEXT_STAGE_ROOT / subdir).mkdir(parents=True, exist_ok=True)
    write_csv_rows(NEXT_STAGE_INPUT, NEXT_QUEUE_COLUMNS, queue_rows)
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# Stage296 Brief(296단계 개요)

- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- question(질문): Can density-floor profit expansion(거래 밀도 하한 수익 확장) keep 4-10 trades/day(일 4-10거래) while preserving split-positive profit(분할 양수 수익) and removing curve pockets(곡선 패임)?
- boundary(경계): `{BOUNDARY}`

Effect(효과): Stage295(295단계)의 낮은 거래수 수익 단서와 OOS(표본외) 상방 단서를 후보로 부르지 않고, 새 feature/decision/risk surface(피처/판단/위험 표면) 개발 입력으로만 사용한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage296 Input Refs(296단계 입력 참조)

- source_report(원천 보고): `{rel(REPORT)}`
- source_scoreboard(원천 점수표): `{rel(SCOREBOARD)}`
- source_failure_memory(원천 실패 기억): `{rel(FAILURE_MEMORY)}`
- seed_queue(씨앗 대기열): `{rel(NEXT_STAGE_INPUT)}`

Effect(효과): Stage296(296단계)는 cp295 후보를 보존하지 않고, 밀도·순수익·곡선 조건을 동시에 만족하는 새 후보 생성 질문으로 시작한다.
""",
    )
    write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", "# Stage296 Review Index(296단계 검토 색인)\n")
    write_csv_rows(
        NEXT_STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv",
        s293.STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage296_opened_from_run295C",
                "stage_id": NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "scoreboard": "stage295_review",
                "status": "opened_density_floor_profit_expansion_rebuild",
                "judgment": "opened_from_stage295_runtime_review_no_candidate",
                "evidence_boundary": "planning_from_stage295_evidence",
                "report_path": rel(REPORT),
                "notes": f"seed_rows={len(queue_rows)};next_action={NEXT_ACTION}",
            }
        ],
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage296 Selection Status(296단계 선택 상태)

- stage_status(단계 상태): `opened_density_floor_profit_expansion_rebuild`
- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`
- current_run(현재 실행): `not_started`
- source_stage(원천 단계): `{STAGE_ID}`
- target_candidate(목표 후보): `none`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- seed_queue(씨앗 대기열): `{rel(NEXT_STAGE_INPUT)}`
""",
    )
    return [
        NEXT_STAGE_INPUT,
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        NEXT_STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv",
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
    ]


def write_outputs(
    scoreboard_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    created_at: str,
) -> list[Path]:
    result, gates = result_rows(scoreboard_rows, failure_rows)
    write_csv_rows(SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv_rows(CURVE_DIAGNOSTICS, CURVE_COLUMNS, curve_rows)
    write_csv_rows(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    write_csv_rows(NEXT_STAGE_QUEUE, NEXT_QUEUE_COLUMNS, queue_rows)
    write_csv_rows(RESULT_JUDGMENT, s293.RESULT_COLUMNS, result)
    write_csv_rows(GATE_AUDIT, s293.GATE_COLUMNS, gates)
    stage296_artifacts = write_stage296_scaffold(queue_rows)
    artifacts = [
        SCOREBOARD,
        CURVE_DIAGNOSTICS,
        FAILURE_MEMORY,
        NEXT_STAGE_QUEUE,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_MANIFEST,
        LINEAGE,
        REPORT,
        DECISION,
        *stage296_artifacts,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_started",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "next_stage_id": NEXT_STAGE_ID,
            "artifacts": [rel(path) for path in artifacts if path != RUN_MANIFEST],
            "created_at_utc": created_at,
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "source": {
                "run295A_manifest": rel(SOURCE_MANIFEST),
                "run295A_proxy_scoreboard": rel(SOURCE_PROXY_SCOREBOARD),
                "run295B_execution": rel(SOURCE_EXECUTION),
                "run295B_kpi": rel(SOURCE_KPI),
            },
            "outputs": {
                "scoreboard": rel(SCOREBOARD),
                "curve_diagnostics": rel(CURVE_DIAGNOSTICS),
                "failure_memory": rel(FAILURE_MEMORY),
                "next_stage_queue": rel(NEXT_STAGE_QUEUE),
                "report": rel(REPORT),
            },
            "claim_boundary": BOUNDARY,
            "created_at_utc": created_at,
        },
    )
    write_md(REPORT, report_markdown(scoreboard_rows, failure_rows, queue_rows))
    write_md(DECISION, decision_markdown())
    return artifacts


def update_registers(scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path], created_at: str) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "split_consistent_outcome_distillation_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)};selected_candidate=none;target_stage={NEXT_STAGE_ID};next_action={NEXT_ACTION}",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "split_consistent_outcome_distillation_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "candidate_selection_review",
                "scoreboard_lane": "split_consistent_outcome_distillation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": "selected_candidate=none;density_gate_all_failed",
                "guardrail_kpi": "adapter_package=none;onnx_readiness=not_started;goal_achieve=not_claimed",
                "external_verification_status": "completed_run295B_mt5_probe",
                "notes": f"target_stage={NEXT_STAGE_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        s293.STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "split_consistent_outcome_distillation_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "split_consistent_outcome_distillation_review_scoreboard",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "candidate_gate_review_no_adapter_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"target_stage={NEXT_STAGE_ID};selected_candidate=none.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage295_split_consistent_outcome_distillation_review_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID if STAGE_ID in rel(path) else NEXT_STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run295C split-consistent outcome distillation review and Stage296 handoff",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, s293.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_docs(scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> None:
    write_md(
        SELECTED,
        f"""# Stage295 Selection Status(295단계 선택 상태)

- stage_status(단계 상태): `{STATUS}`
- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `294_onnx_candidate_campaign__mt5_outcome_relabel_directional_flip_rebuild`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- report(보고): `{rel(REPORT)}`
- scoreboard(점수표): `{rel(SCOREBOARD)}`
""",
    )
    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage295 Review Index(295단계 검토 색인)\n"
    review_index = append_once(
        review_index,
        "run295C_report",
        f"- run295C_report(295C 보고): `{rel(REPORT)}`\n- run295C_scoreboard(295C 점수표): `{rel(SCOREBOARD)}`\n- run295C_failure_memory(295C 실패 기억): `{rel(FAILURE_MEMORY)}`",
    )
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `none`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `opened_density_floor_profit_expansion_rebuild`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run295C_summary",
        f"- run295C_summary(295C 요약): Stage295(295단계) MT5 actual routed total(MT5 실제 라우팅 전체) `{len(scoreboard_rows)}`개 후보를 검토했다. Effect(효과): selected_candidate(선택 후보)는 `none`이고, Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않으며 `{NEXT_STAGE_ID}`를 새 density-floor profit expansion(거래 밀도 하한 수익 확장) 논제로 열었다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage295(295단계) run295C(295C 실행) split-consistent outcome distillation review(분할 일관 결과 증류 검토) `{RUN_ID}`. "
        f"Effect(효과): scoreboard(점수표) `{len(scoreboard_rows)}`행과 failure memory(실패 기억) `{len(failure_rows)}`행을 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)는 없으며 `{NEXT_STAGE_ID}`를 열었다.\n"
    )
    workspace = s293.prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run295C Split-consistent outcome distillation review(295C 분할 일관 결과 증류 검토)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): Stage295(295단계)를 선택 후보 없이 닫고 Stage296(296단계) density-floor profit expansion(거래 밀도 하한 수익 확장)을 열었다.\n"
        f"- boundary(경계): Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 `not_started/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST296-DENSITY-FLOOR-PROFIT-EXPANSION",
        f"| `IDEA-ST296-DENSITY-FLOOR-PROFIT-EXPANSION` | `{NEXT_STAGE_ID}` | density-floor profit expansion(거래 밀도 하한 수익 확장) | `Tier A used + Tier B fallback + actual routed total` | `opened_from_stage295_no_candidate` | cp295D 수익 단서와 cp295B/E OOS 상방 단서를 4-10 trades/day(일 4-10거래) 새 표면으로 재구성 |\n",
    )
    write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    negative = append_once(
        negative,
        "NEG-ST295-SPLIT-CONSISTENT-OUTCOME-DISTILLATION",
        f"| `NEG-ST295-SPLIT-CONSISTENT-OUTCOME-DISTILLATION` | `IDEA-ST295-SPLIT-CONSISTENT-OUTCOME-DISTILLATION` | split-consistent outcome distillation(분할 일관 결과 증류)이 ONNX-worthy candidate(온엑스화 가치 후보)로 닫히지 않음 | 모든 actual routed total(실제 라우팅 전체)이 4-10 trades/day(일 4-10거래), split-positive 수익, 곡선 proxy(대리 지표)를 동시에 통과하지 못함 | cp295D는 저밀도 수익 단서, cp295B/E는 OOS 상방 단서로만 보존 | fresh density-floor profit expansion(새 거래 밀도 하한 수익 확장)에서만 재개 |\n",
    )
    write_md(NEGATIVE_REGISTER, negative)


def main() -> None:
    created_at = utc_now()
    runtime_rows = load_runtime_rows()
    scoreboard_rows, curve_rows, failure_rows = build_review_rows(runtime_rows)
    queue_rows = next_stage_rows()
    artifacts = write_outputs(scoreboard_rows, curve_rows, failure_rows, queue_rows, created_at)
    update_registers(scoreboard_rows, failure_rows, artifacts, created_at)
    update_docs(scoreboard_rows, failure_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "scoreboard_rows": len(scoreboard_rows),
                "failure_rows": len(failure_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_started",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
                "next_stage_id": NEXT_STAGE_ID,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
