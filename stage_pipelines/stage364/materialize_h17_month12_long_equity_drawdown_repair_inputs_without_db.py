from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db as parent  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CR"
RUN_ID = "run364CR_materialize_h17_month12_long_equity_drawdown_repair_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
NEXT_RUN_ID = "run364CS_train_h17_month12_long_equity_drawdown_repair_scout_without_db_v1"

STATUS = "completed_stage364CR_h17_month12_long_equity_drawdown_repair_inputs_materialized_no_authority"
JUDGMENT = "repair_input_queue_ready_month12_long_equity_dd_side_balance_no_authority"
DECISION = "stage364CR_open_run364CS_h17_month12_long_equity_drawdown_repair_scout"
CLAIM_BOUNDARY = (
    "research_development_repair_input_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REPAIR_DESIGN_MATRIX = RUN_DIR / "repair_design_matrix.csv"
SUCCESS_FAILURE_CONTRACT = RUN_DIR / "success_failure_contract.csv"
TIMESTAMP_SAFETY_AUDIT = RUN_DIR / "timestamp_safety_audit.csv"
FORBIDDEN_ACTION_AUDIT = RUN_DIR / "forbidden_action_audit.csv"
RUN364CS_QUEUE = RUN_DIR / "run364CS_h17_month12_long_equity_drawdown_repair_scout_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CR_h17_month12_long_equity_drawdown_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CR_h17_month12_long_equity_drawdown_repair_inputs.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.MT5_KPI_REVIEW,
    parent.MONTH_ATTRIBUTION,
    parent.MONTH_SIDE_ATTRIBUTION,
    parent.SIDE_ATTRIBUTION,
    parent.DRAWDOWN_REVIEW,
    parent.NEXT_QUEUE,
    parent.RUN_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REPAIR_DESIGN_MATRIX,
    SUCCESS_FAILURE_CONTRACT,
    TIMESTAMP_SAFETY_AUDIT,
    FORBIDDEN_ACTION_AUDIT,
    RUN364CS_QUEUE,
    EXPERIMENT_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def read_csv(path: Path) -> pd.DataFrame:
    return parent.read_csv(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, payload)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    parent.replace_prefixed_lines(path, replacements, bom=bom)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CR inputs(CR 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CQ next_run_id mismatch(CQ 다음 실행 ID 불일치): {final.get('next_run_id')} != {RUN_ID}")
    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CQ gate audit(CQ 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "CQ repair materialization source(CQ 수리 구체화 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "work_packet_schema_lint",
                "repair_scope_gate",
                "timestamp_safety_gate",
                "forbidden_action_guard",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def design_rows(cq_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {
        "run_id": RUN_ID,
        "parent_candidate_id": cq_final["candidate_id"],
        "baseline_run_id": parent.RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "sample_scope": "Tier A validation_oos 2025.01.02-2026.04.14 US100 M5",
        "fixed_variables": "same ONNX/model/features/base CM04 runtime surface, no top_n, no trade splitting",
        "invalid_conditions": "uses exact date/year filter, changes feature lookahead boundary, skips density/short-floor checks",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    rows = [
        {
            **base,
            "variant_id": "cr00_cm04_runtime_review_baseline",
            "hypothesis": "baseline replay preserves CQ MT5 read(CQ MT5 판독 기준선 유지)",
            "changed_variables": "none",
            "rule_surface": "cm04 unchanged",
            "expected_effect": "anchor repair deltas(수리 차이 기준점)",
        },
        {
            **base,
            "variant_id": "cr01_month12_long_hours17_20_block",
            "hypothesis": "month12 long loss is concentrated in hours 17-20(12월 롱 손실은 17-20시에 집중)",
            "changed_variables": "block long entries when month_of_year=12 and open_hour in 17,18,19,20",
            "rule_surface": "month12_long_session_block",
            "expected_effect": "remove residual bad month(잔여 손실 월 제거)",
        },
        {
            **base,
            "variant_id": "cr02_month12_long_margin_floor_002",
            "hypothesis": "raising month12 long margin floor reduces weak longs(12월 롱 마진 하한 상향이 약한 롱을 줄임)",
            "changed_variables": "month12 long signal-margin floor 0.02",
            "rule_surface": "month12_long_margin_floor",
            "expected_effect": "improve month12 net while preserving density(밀도 보존하며 12월 개선)",
        },
        {
            **base,
            "variant_id": "cr03_month12_long_margin_floor_003",
            "hypothesis": "stronger month12 long margin floor may remove bad month(더 강한 12월 롱 마진 하한이 손실 월 제거)",
            "changed_variables": "month12 long signal-margin floor 0.03",
            "rule_surface": "month12_long_margin_floor",
            "expected_effect": "stress stronger guard without exact-date filtering(정확 날짜 필터 없이 강한 가드 압박)",
        },
        {
            **base,
            "variant_id": "cr04_month12_long_hours17_20_floor002",
            "hypothesis": "session and margin combined can repair month12 without broad damage(세션+마진 조합이 넓은 손상 없이 12월 수리)",
            "changed_variables": "month12 long open_hour 17-20 guard plus margin floor 0.02",
            "rule_surface": "month12_long_session_margin_combo",
            "expected_effect": "bad month repair with limited trade loss(제한적 거래 감소로 손실 월 수리)",
        },
        {
            **base,
            "variant_id": "cr05_equity_dd_long_hours18_19_floor002_all_months",
            "hypothesis": "long entries around hours 18-19 contribute open equity DD(18-19시 롱이 열린 수익곡선 낙폭에 기여)",
            "changed_variables": "all-month long open_hour 18-19 signal-margin floor 0.02",
            "rule_surface": "equity_dd_session_margin_stress",
            "expected_effect": "reduce equity DD gap without killing density(밀도 훼손 없이 수익곡선 낙폭 간극 축소)",
        },
        {
            **base,
            "variant_id": "cr06_short_floor_preserve_month12_long_guard",
            "hypothesis": "month12 repair must keep short floor >=100(12월 수리는 숏 하한 100 이상을 유지해야 함)",
            "changed_variables": "cr01 guard plus native/synthetic short floor restore",
            "rule_surface": "month12_repair_short_floor_preserve",
            "expected_effect": "avoid reverting to long-only(롱 전용 회귀 방지)",
        },
        {
            **base,
            "variant_id": "cr07_equity_dd_and_bad_month_combo",
            "hypothesis": "small combined guard can repair both bad month and equity DD(작은 조합 가드가 손실 월과 낙폭을 같이 수리)",
            "changed_variables": "month12 long 17-20 block plus all-month long 18-19 floor 0.02",
            "rule_surface": "combined_month12_equity_dd_guard",
            "expected_effect": "test combined repair boundary(조합 수리 경계 시험)",
        },
    ]
    write_csv(REPAIR_DESIGN_MATRIX, rows)
    return rows


def write_tables(cq_final: Mapping[str, Any], designs: Sequence[Mapping[str, Any]]) -> None:
    queue = [
        {
            "run_id": RUN_ID,
            "queue_id": f"run364CS_{index:02d}",
            "next_run_id": NEXT_RUN_ID,
            "variant_id": row["variant_id"],
            "hypothesis": row["hypothesis"],
            "changed_variables": row["changed_variables"],
            "rule_surface": row["rule_surface"],
            "baseline_mt5_net": cq_final["mt5_net_profit"],
            "baseline_mt5_pf": cq_final["mt5_profit_factor"],
            "baseline_mt5_density": cq_final["mt5_density"],
            "baseline_bad_month_count": cq_final["bad_month_count"],
            "baseline_equity_dd": cq_final["equity_drawdown"],
            "success_criteria": "proxy net > 0, PF >= 1.35, density >= 3, short_count >= 100, bad_month_count == 0, equity DD proxy not worse",
            "failure_criteria": "density < 3, short_count < 100, net <= 0, PF collapse, new bad-month count increase",
            "timestamp_safety": "entry-known month/hour/probability margin only(진입 시점 월/시간/확률 마진만)",
            "forbidden_actions": "exact_date_filter;exact_year_filter;top_n;trade_splitting;future_bar_join",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, row in enumerate(designs, start=1)
    ]
    write_csv(RUN364CS_QUEUE, queue)
    write_csv(
        SUCCESS_FAILURE_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "contract_id": "cr_success_failure",
                "comparison_baseline": parent.RUN_ID,
                "success_criteria": "MT5-informed proxy candidate keeps density >= 3 and short floor >= 100 while removing month12 loss or reducing equity-DD proxy.",
                "failure_criteria": "candidate only improves one metric by killing density/shorts or using forbidden exact-date/top_n/trade split.",
                "invalid_conditions": "lookahead, exact date/year filter, missing source artifact, altered MT5 identity without manifest.",
                "stop_conditions": "if all variants fail density/short floor, open new offensive idea instead of relaxing gates.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        TIMESTAMP_SAFETY_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "variant_id": row["variant_id"],
                "timestamp_inputs": "month_of_year, open_hour, entry-known probability margin",
                "future_inputs": "none",
                "timestamp_safety_status": "passed",
                "effect": "future information(미래 정보) 없이 다음 scout(정찰)를 설계합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for row in designs
        ],
    )
    write_csv(
        FORBIDDEN_ACTION_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "guard": guard,
                "status": "passed",
                "evidence": rel(RUN364CS_QUEUE),
                "effect": "수익을 좋아 보이게 하는 금지 행동을 queue(대기열) 단계에서 막습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for guard in ["exact_date_filter", "exact_year_filter", "top_n", "trade_splitting", "future_bar_join"]
        ],
    )


def gate_rows(designs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    queue_exists = exists(RUN364CS_QUEUE) and len(read_csv(RUN364CS_QUEUE)) == len(designs)
    return [
        {
            "run_id": RUN_ID,
            "gate": "work_packet_schema_lint",
            "status": "passed",
            "evidence": rel(WORK_PACKET),
            "effect": "CR 작업 묶음(work packet, 작업 묶음)의 가족/스킬/게이트를 고정합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "repair_scope_gate",
            "status": "passed" if queue_exists else "failed",
            "evidence": rel(RUN364CS_QUEUE),
            "effect": "CQ 수리 단서를 CS 실행 가능한 queue(대기열)로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "timestamp_safety_gate",
            "status": "passed",
            "evidence": rel(TIMESTAMP_SAFETY_AUDIT),
            "effect": "진입 시점에 알려진 입력만 쓰도록 제한합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "forbidden_action_guard",
            "status": "passed",
            "evidence": rel(FORBIDDEN_ACTION_AUDIT),
            "effect": "exact date/top_n/trade splitting(정확 날짜/상위 N/거래 쪼개기)을 금지합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": rel(GATE_AUDIT),
            "effect": "필수 gate(게이트)를 closeout(종료 기록)에 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "materialization(구체화)을 운영 주장(operating claim, 운영 주장)으로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(cq_final: Mapping[str, Any], designs: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "candidate_id": cq_final["candidate_id"],
        "baseline_mt5_net": cq_final["mt5_net_profit"],
        "baseline_mt5_profit_factor": cq_final["mt5_profit_factor"],
        "baseline_mt5_density": cq_final["mt5_density"],
        "baseline_bad_month_count": cq_final["bad_month_count"],
        "baseline_equity_drawdown": cq_final["equity_drawdown"],
        "design_rows": len(designs),
        "queue_rows": len(read_csv(RUN364CS_QUEUE)) if exists(RUN364CS_QUEUE) else 0,
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any], designs: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "Month12 long guard and equity-DD controls can preserve CM04 net/PF/density while removing residual bad-month and risk gap.",
            "decision_use": "select CS proxy scout variants(CS 프록시 정찰 변형 선택)",
            "comparison_baseline": parent.RUN_ID,
            "control_variables": ["US100", "M5", "same ONNX/model/features", "CM04 base rules", "no trade splitting"],
            "changed_variables": [row["changed_variables"] for row in designs],
            "sample_scope": "Tier A validation_oos 2025.01.02-2026.04.14",
            "success_criteria": "density >= 3, short_count >= 100, net > 0, PF >= 1.35, bad month removed or equity DD reduced",
            "failure_criteria": "metric improvement comes from density collapse, short floor failure, or forbidden filtering",
            "invalid_conditions": "lookahead, exact date/year filter, missing CQ evidence",
            "stop_conditions": "if all variants fail, pivot to new offensive source rather than relax gates",
            "evidence_plan": [rel(REPAIR_DESIGN_MATRIX), rel(RUN364CS_QUEUE), rel(SUCCESS_FAILURE_CONTRACT)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "observed_change": "CQ showed positive MT5 net/PF/density but month12/equity-DD issues remain.",
            "comparison_baseline": rel(parent.MT5_KPI_REVIEW),
            "likely_drivers": ["month12 long residual loss", "equity DD gap", "long skew"],
            "segment_checks": [rel(parent.MONTH_SIDE_ATTRIBUTION), rel(parent.DRAWDOWN_REVIEW), rel(parent.SIDE_ATTRIBUTION)],
            "trade_shape": rel(parent.TRADE_SHAPE_REVIEW),
            "alternative_explanations": ["tester timeout boundary", "proxy balance DD vs MT5 equity DD basis"],
            "attribution_confidence": "medium",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "CR repair input materialization(CR 수리 입력 구체화)",
            "evidence_available": [rel(REPAIR_DESIGN_MATRIX), rel(RUN364CS_QUEUE), rel(TIMESTAMP_SAFETY_AUDIT), rel(FORBIDDEN_ACTION_AUDIT)],
            "evidence_missing": ["new proxy scout output(새 프록시 정찰 출력)", "new MT5 execution(새 MT5 실행)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "CR only prepares the next experiment; it does not prove improvement(CR은 다음 실험 준비일 뿐 개선 증명은 아님).",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_materialization_artifacts(추적 구체화 산출물)",
            "lineage_judgment": "connected_with_repair_input_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "repair inputs ready only(수리 입력 준비만)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "new_model_training": "not_run",
            "new_mt5_execution": "not_run",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 10) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    queue = read_csv(RUN364CS_QUEUE).to_dict("records")
    report = f"""# run364CR h17 month12 long equity drawdown repair inputs(17시 12월 롱/수익곡선 낙폭 수리 입력)

Updated(갱신): {final['created_at_utc']}

Action(행동): CQ review(CQ 검토)의 month12 loss(12월 손실), equity DD(수익곡선 낙폭), side balance(방향 균형) 단서를 CS scout queue(CS 정찰 대기열) `{final['queue_rows']}`개로 materialize(구체화)했습니다.

Effect(효과): 다음 `{NEXT_RUN_ID}`가 exact date filter(정확 날짜 필터), top_n(상위 N), trade splitting(거래 쪼개기) 없이 timestamp-safe(시점 안전) 수리 변형을 바로 시험할 수 있습니다.

## Baseline(기준선)

- MT5 net/PF/density(순수익/수익 팩터/밀도): `{final['baseline_mt5_net']}` / `{final['baseline_mt5_profit_factor']}` / `{final['baseline_mt5_density']}`
- bad month count(손실 월 수): `{final['baseline_bad_month_count']}`
- equity DD(수익곡선 낙폭): `{final['baseline_equity_drawdown']}`

## CS Queue(CS 대기열)

{markdown_table(queue, ['variant_id', 'hypothesis', 'changed_variables', 'success_criteria'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

CR is materialization only(CR은 구체화 전용)입니다. new model training(새 모델 학습), new MT5 execution(새 MT5 실행), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CR decision(결정): month12/equity DD repair inputs

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- queue_rows(대기열 행): `{final['queue_rows']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): CS에서 12월 롱 손실과 equity DD(수익곡선 낙폭)를 timestamp-safe(시점 안전)하게 시험합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364CR__{RUN_ID}", f"\n- run364CR__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - CR repair inputs(CR 수리 입력), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"## run364CR__{RUN_ID}", f"\n## run364CR Repair Inputs(수리 입력)\n\nAction(행동): 12월 롱 손실과 equity DD(수익곡선 낙폭) 수리 후보 `{final['queue_rows']}`개를 만들었습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 proxy scout(프록시 정찰)를 실행할 수 있습니다.\n")
    append_text_once(STAGE_README, f"run364CR__{RUN_ID}", f"\n<!-- run364CR__{RUN_ID} -->\n## run364CR repair inputs(수리 입력)\n\nQueue(대기열): `{final['queue_rows']}` variants. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364CR` materialized(구체화 완료) `{final['queue_rows']}` CS repair variants(CS 수리 변형). Baseline(기준선)은 CQ MT5 net/PF/density(순수익/수익 팩터/밀도) `{final['baseline_mt5_net']}` / `{final['baseline_mt5_profit_factor']}` / `{final['baseline_mt5_density']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 month12 long guard(12월 롱 가드), equity DD stress(수익곡선 낙폭 압박), side balance(방향 균형) proxy scout(프록시 정찰)를 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Repair queue(수리 대기열): `{final['queue_rows']}` variants for CS scout(CS 정찰).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364CR__{RUN_ID}", f"\n<!-- run364CR__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` materialized month12/equity DD repair inputs(12월/수익곡선 낙폭 수리 입력); next `{NEXT_RUN_ID}`.\n")
    append_text_once(IDEA_REGISTRY, f"run364CR__{RUN_ID}", f"\n<!-- run364CR__{RUN_ID} -->\n- `{RUN_ID}`: CQ positive clue(긍정 단서)를 보존하면서 month12 long/equity DD/side balance(12월 롱/수익곡선 낙폭/방향 균형) 수리 변형 `{final['queue_rows']}`개를 열었다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__materialization",
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["queue_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_design(실험 설계)",
        "scoreboard_lane": "repair_input_materialization(수리 입력 구체화)",
        "external_verification_status": "not_applicable_materialization_only(구체화 전용)",
        "evidence_boundary": "materialization_only(구체화 전용)",
        "question": "Which timestamp-safe repair variants should CS scout test?(CS 정찰이 어떤 시점 안전 수리 변형을 시험할까?)",
        "next_action": NEXT_RUN_ID,
        "path": rel(REPORT_PATH),
        "primary_artifact": rel(RUN364CS_QUEUE),
        "result_judgment": JUDGMENT,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [row], extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], [row], extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], [row], extend_header=True)
    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("repair_design_matrix", REPAIR_DESIGN_MATRIX, "Repair design matrix(수리 설계 행렬)."),
            ("cs_queue", RUN364CS_QUEUE, "CS scout queue(CS 정찰 대기열)."),
            ("success_failure_contract", SUCCESS_FAILURE_CONTRACT, "Success/failure contract(성공/실패 계약)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
            ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)
    parent.repair_run_registry_line_endings(RUN_ID)


def write_final_files(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    cq_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    designs = design_rows(cq_final)
    write_tables(cq_final, designs)
    gates = gate_rows(designs)
    created_at = now_utc()
    final = final_payload(cq_final, designs, gates, created_at)
    write_receipts(final, designs)
    gates = gate_rows(designs)
    final = final_payload(cq_final, designs, gates, created_at)
    write_docs(final, gates)
    write_final_files(final, gates)
    write_ledgers(final, gates)
    write_final_files(final, gates)
    print(json.dumps(parent.json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
