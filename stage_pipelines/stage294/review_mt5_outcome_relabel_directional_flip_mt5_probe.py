from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage293 import review_profit_scale_density_calibration_mt5_probe as r293  # noqa: E402


STAGE_ID = "294_onnx_candidate_campaign__mt5_outcome_relabel_directional_flip_rebuild"
NEXT_REBUILD_STAGE_ID = "295_onnx_candidate_campaign__split_consistent_outcome_distillation_rebuild"
NEXT_ADAPTER_STAGE_ID = "295_onnx_candidate_campaign__adapter_package_for_stage294_candidate"
RUN_ID = "run294C_review_mt5_outcome_relabel_directional_flip_mt5_probe_v1"
RUN_NUMBER = "run294C"
SOURCE_RUN_ID = "run294B_mt5_outcome_relabel_directional_flip_mt5_probe_v1"
PARENT_RUN_ID = "run294A_design_mt5_outcome_relabel_directional_flip_rebuild_v1"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN294A = STAGE_ROOT / "02_runs" / "run294A"
RUN294B = STAGE_ROOT / "02_runs" / "run294B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_MANIFEST = RUN294A / "candidate_payload_manifest.csv"
SOURCE_KPI = RUN294B / "mt5_kpi_summary.csv"
SOURCE_EXECUTION = RUN294B / "execution_result.json"
PRODUCER = Path("stage_pipelines/stage294/review_mt5_outcome_relabel_directional_flip_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "mt5_outcome_relabel_directional_flip_review_scoreboard.csv"
MONTHLY = RUN_ROOT / "monthly_attribution.csv"
SESSION = RUN_ROOT / "session_attribution.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
LOCAL_POCKETS = RUN_ROOT / "local_curve_pocket_diagnostics.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage295_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run294C_mt5_outcome_relabel_directional_flip_review_stage295_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage294_mt5_outcome_relabel_directional_flip_review_stage295_open.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def patch_review293_constants() -> None:
    replacements: dict[str, Any] = {
        "STAGE_ID": STAGE_ID,
        "NEXT_REBUILD_STAGE_ID": NEXT_REBUILD_STAGE_ID,
        "NEXT_ADAPTER_STAGE_ID": NEXT_ADAPTER_STAGE_ID,
        "RUN_ID": RUN_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "SOURCE_RUN_ID": SOURCE_RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "UPDATED_ON": UPDATED_ON,
        "BOUNDARY": BOUNDARY,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN293A": RUN294A,
        "RUN293B": RUN294B,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS": REVIEWS,
        "SELECTED": SELECTED,
        "REVIEW_INDEX": REVIEW_INDEX,
        "STAGE_LEDGER": STAGE_LEDGER,
        "SOURCE_MANIFEST": SOURCE_MANIFEST,
        "SOURCE_KPI": SOURCE_KPI,
        "SOURCE_EXECUTION": SOURCE_EXECUTION,
        "PRODUCER": PRODUCER,
        "SCOREBOARD": SCOREBOARD,
        "MONTHLY": MONTHLY,
        "SESSION": SESSION,
        "TRADE_QUALITY": TRADE_QUALITY,
        "CURVE": CURVE,
        "LOCAL_POCKETS": LOCAL_POCKETS,
        "FAILURE_MEMORY": FAILURE_MEMORY,
        "NEXT_STAGE_QUEUE": NEXT_STAGE_QUEUE,
        "RESULT_JUDGMENT": RESULT_JUDGMENT,
        "GATE_AUDIT": GATE_AUDIT,
        "RUN_MANIFEST": RUN_MANIFEST,
        "LINEAGE": LINEAGE,
        "REPORT": REPORT,
        "DECISION": DECISION,
        "RUN_REGISTRY": RUN_REGISTRY,
        "ALPHA_LEDGER": ALPHA_LEDGER,
        "ARTIFACT_REGISTRY": ARTIFACT_REGISTRY,
        "IDEA_REGISTER": IDEA_REGISTER,
        "NEGATIVE_REGISTER": NEGATIVE_REGISTER,
        "CURRENT_STATE": CURRENT_STATE,
        "WORKSPACE_STATE": WORKSPACE_STATE,
        "CHANGELOG": CHANGELOG,
    }
    for name, value in replacements.items():
        setattr(r293, name, value)


def stage295_queue_rows(selected: Mapping[str, Any] | None) -> list[dict[str, Any]]:
    refs = ";".join(
        [
            "stage267_reference_evidence",
            "stage293_profit_scale_density_calibration_negative",
            "stage294_outcome_flip_oos_positive_validation_negative",
        ]
    )
    if selected:
        return [
            {
                "seed_id": "stage295_adapter_package_for_stage294_candidate",
                "source_stage_id": STAGE_ID,
                "source_run_id": RUN_ID,
                "seed_role": "adapter_package_build(어댑터 패키지 구성)",
                "hypothesis": f"{selected['package_id']} can be formalized as an Adapter package(어댑터 패키지).",
                "broad_sweep": "feature order, rule/model surface, risk logic, runtime handoff receipts(피처 순서/규칙 또는 모델 표면/위험 로직/런타임 인계 영수증)",
                "aggressive_sweep": "none; adapter packaging only(없음; 어댑터 패키징만)",
                "defensive_sweep": "parity pressure before ONNX export(ONNX 내보내기 전 동등성 압박)",
                "success_gate": "Adapter package complete and reproducible(어댑터 패키지 완료 및 재현 가능)",
                "discard_condition": "handoff cannot be traced(인계 추적 불가)",
                "prior_stage_refs": refs,
                "claim_boundary": BOUNDARY,
            }
        ]
    return [
        {
            "seed_id": "stage295_split_consistent_outcome_distillation",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_primary(새 논제 주축)",
            "hypothesis": "Split-consistent outcome distillation(분할 일관 결과 증류)이 Stage294(294단계)의 OOS 양수/validation 음수 비대칭을 줄일 수 있다.",
            "broad_sweep": "train-only outcome labels, validation damage veto, OOS preserve gate, direction flip/skip/distill(학습 전용 결과 라벨/검증 손상 거부/표본외 보존 관문/반전·회피·증류)",
            "aggressive_sweep": "distill flip winners into dense payoff bands(반전 승자 구간을 고밀도 보상 구간으로 증류)",
            "defensive_sweep": "hard reject validation-negative states and deep local pockets(검증 음수 상태와 깊은 국소 포켓 강한 거부)",
            "success_gate": "validation and OOS both positive, 4-10 trades/day, smooth zoomed curve(검증/표본외 양수, 일 4-10거래, 확대 곡선 매끄러움)",
            "discard_condition": "validation remains negative or OOS edge disappears(검증이 계속 음수거나 표본외 우위가 사라짐)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage295_validation_damage_veto_router",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_defensive(새 논제 방어형)",
            "hypothesis": "Validation damage veto router(검증 손상 거부 라우터)가 Stage294(294단계)의 OOS 양수 단서를 보존하면서 검증 손실을 제거할 수 있다.",
            "broad_sweep": "month/session/time-underwater veto, cost-aware acceptance, reduced-risk state(月/세션/수중시간 거부, 비용 인식 수락, 축소위험 상태)",
            "aggressive_sweep": "only re-expand when validation damage clears(검증 손상이 사라질 때만 재확장)",
            "defensive_sweep": "minimum density guard and curve pocket cap(최소 밀도 보호와 곡선 포켓 상한)",
            "success_gate": "density remains 4-10 while validation net becomes positive(밀도 4-10 유지와 검증 순수익 양수)",
            "discard_condition": "veto becomes thin trade-count repair(거부가 얇은 거래수 수리로 변함)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage295_oos_edge_preserve_aggressive_rescale",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_aggressive(새 논제 공격형)",
            "hypothesis": "OOS edge preserve aggressive rescale(표본외 우위 보존 공격형 재스케일)가 OOS 양수 단서를 순수익 규모로 키울 수 있다.",
            "broad_sweep": "OOS-positive source bands, validation damage countercheck, payoff/risk asymmetric sizing(표본외 양수 원천 구간/검증 손상 대조/손익·위험 비대칭 크기)",
            "aggressive_sweep": "selectively widen OOS-positive bands up to 10 trades/day(표본외 양수 구간을 일 10거래까지 선택 확장)",
            "defensive_sweep": "validation veto and rolling drawdown cap(검증 거부와 롤링 손실 상한)",
            "success_gate": "profit scale and smoothness improve together(수익 규모와 매끄러움 동시 개선)",
            "discard_condition": "scale comes only from validation loss or concentration(규모가 검증 손실이나 집중에서만 나옴)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
    ]


def status_pack(selected: Mapping[str, Any] | None) -> tuple[str, str, str, str]:
    if selected:
        return (
            "completed_mt5_outcome_relabel_directional_flip_review_candidate_gate_ready_stage295_adapter_opened",
            "mt5_outcome_relabel_directional_flip_candidate_package_gate_ready_adapter_required_no_onnx",
            "run295A_design_adapter_package_for_stage294_candidate",
            NEXT_ADAPTER_STAGE_ID,
        )
    return (
        "completed_mt5_outcome_relabel_directional_flip_review_no_candidate_stage295_opened",
        "mt5_outcome_relabel_directional_flip_runtime_probe_negative_no_adapter_no_onnx",
        "run295A_design_split_consistent_outcome_distillation_rebuild_packet",
        NEXT_REBUILD_STAGE_ID,
    )


def result_rows(
    selected: Mapping[str, Any] | None,
    scoreboard_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    next_action: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    b = r293.base
    candidate_gate = "passed" if selected else "failed"
    rows = [
        {
            "result_subject": "Stage294 outcome relabel directional flip MT5 review(294단계 결과 재라벨 방향 반전 MT5 검토)",
            "evidence_available": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)};source_kpi={b.rel(SOURCE_KPI)}",
            "evidence_missing": "Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성), MT5 runtime reproduction(MT5 런타임 재현)",
            "judgment_label": "exploratory" if selected else "negative",
            "judgment_class": judgment,
            "claim_boundary": BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": "OOS(표본외) 양수 단서는 보존하지만 validation(검증)이 전부 음수라 ONNX(온엑스) 후보로 넘기지 않는다.",
        }
    ]
    gates = [
        {
            "gate_name": "mt5_runtime_probe(MT5 런타임 탐침)",
            "status": "passed",
            "evidence_path": b.rel(SOURCE_KPI),
            "effect": "actual routed total(실제 라우팅 전체) 기준으로 후보를 판정했다.",
        },
        {
            "gate_name": "minimum_trade_and_density(최소 거래수와 밀도)",
            "status": candidate_gate,
            "evidence_path": b.rel(SCOREBOARD),
            "effect": "최소 거래수와 일 4-10거래 조건을 동시에 보았다.",
        },
        {
            "gate_name": "profit_efficiency_curve(순수익/효율/곡선)",
            "status": candidate_gate,
            "evidence_path": b.rel(SCOREBOARD),
            "effect": "순수익 규모, PF(수익 팩터), 회복, 기대값, 확대 곡선 포켓을 함께 보았다.",
        },
        {
            "gate_name": "adapter_package(어댑터 패키지)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "후보 게이트 전이므로 Adapter(어댑터)를 만들지 않는다.",
        },
        {
            "gate_name": "onnx_readiness(ONNX 준비)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "Adapter(어댑터)와 parity(동등성) 전이므로 ONNX(온엑스)를 시작하지 않는다.",
        },
    ]
    return rows, gates


def report_markdown(
    scoreboard_rows: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any] | None,
    status: str,
    judgment: str,
    next_action: str,
    next_stage_id: str,
) -> str:
    lines = [
        "# run294C MT5 Outcome Relabel Directional Flip Review(294C MT5 결과 재라벨 방향 반전 검토)",
        "",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- selected_candidate(선택 후보): `{selected['package_id'] if selected else 'none'}`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(ONNX 준비): `not_started`",
        f"- next_action(다음 행동): `{next_action}`",
        f"- next_stage(다음 단계): `{next_stage_id}`",
        "",
        "Effect(효과): Stage294(294단계)는 OOS(표본외) 일부 양수 단서를 만들었지만 validation(검증)이 전부 음수라서 ONNX(온엑스) 후보로 넘기지 않는다.",
        "",
        "| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | val/day(검증 일거래) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | OOS/day(표본외 일거래) | gate(게이트) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {pkg} | {vn:.2f} | {vpf:.2f} | {vtd:.2f} | {on:.2f} | {opf:.2f} | {otd:.2f} | {gate} |".format(
                pkg=row["package_id"],
                vn=r293.base.safe_float(row["validation_net_profit"]),
                vpf=r293.base.safe_float(row["validation_pf"]),
                vtd=r293.base.safe_float(row["validation_trades_per_day"]),
                on=r293.base.safe_float(row["oos_net_profit"]),
                opf=r293.base.safe_float(row["oos_pf"]),
                otd=r293.base.safe_float(row["oos_trades_per_day"]),
                gate=row["review_label"],
            )
        )
    lines.extend(
        [
            "",
            "## Stage295 Thesis(295단계 논제)",
            "",
            "Stage295(295단계)는 flip(반전) 자체를 반복하지 않는다. OOS(표본외) 양수 단서가 validation(검증)에서 왜 깨지는지 split-consistent outcome distillation(분할 일관 결과 증류)과 validation damage veto(검증 손상 거부)로 새 decision surface(판단 표면)를 만든다.",
            "",
            f"Claim boundary(주장 경계): `{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def decision_markdown(selected: Mapping[str, Any] | None, status: str, judgment: str, next_stage_id: str) -> str:
    if selected:
        decision = f"{selected['package_id']} passes the candidate package gate(후보 패키지 게이트) and moves to Adapter package(어댑터 패키지) work."
    else:
        decision = "No Stage294 package passes the ONNX-worthy candidate gate(ONNX화 가치 후보 게이트), so Stage295 opens split-consistent outcome distillation(분할 일관 결과 증류)."
    return f"""# Stage294 Decision(294단계 결정)

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): {decision}
- next_stage(다음 단계): `{next_stage_id}`

Effect(효과): OOS(표본외) 양수만으로 ONNX(온엑스)에 넘기지 않고, validation(검증) 손상을 직접 다루는 새 구조로 넘어간다.
"""


def write_next_stage_scaffold(
    queue_rows: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any] | None,
    next_stage_id: str,
    next_action: str,
) -> None:
    b = r293.base
    stage_root = ROOT / "stages" / next_stage_id
    for subdir in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        b.io_path(stage_root / subdir).mkdir(parents=True, exist_ok=True)
    input_name = "adapter_seed_queue.csv" if selected else "stage295_seed_queue.csv"
    status = "opened_adapter_package_for_stage294_candidate" if selected else "opened_split_consistent_outcome_distillation_rebuild"
    target = selected["package_id"] if selected else "none"
    b.write_csv(stage_root / "01_inputs" / input_name, b.QUEUE_COLUMNS, queue_rows)
    b.write_md(
        stage_root / "00_spec" / "stage_brief.md",
        f"""# Stage295 Brief(295단계 개요)

- stage_id(단계 ID): `{next_stage_id}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- question(질문): Can split-consistent outcome distillation(분할 일관 결과 증류) preserve Stage294 OOS upside(Stage294 표본외 상방) while removing validation damage(검증 손상)?
- boundary(경계): `{BOUNDARY}`

Effect(효과): Stage294(294단계)의 OOS 양수/validation 음수 비대칭을 좁은 flip repair(반전 수리)가 아니라 새 label/decision/risk surface(라벨/판단/위험 표면) 질문으로 바꾼다.
""",
    )
    b.write_md(
        stage_root / "01_inputs" / "input_refs.md",
        f"""# Stage295 Input Refs(295단계 입력 참조)

- source_report(원천 보고): `{b.rel(REPORT)}`
- source_scoreboard(원천 점수표): `{b.rel(SCOREBOARD)}`
- source_failure_memory(원천 실패 기억): `{b.rel(FAILURE_MEMORY)}`
- source_queue(원천 대기열): `{b.rel(stage_root / "01_inputs" / input_name)}`

Effect(효과): Stage294(294단계)의 결과를 다음 질문의 입력 근거로만 사용한다.
""",
    )
    b.write_md(stage_root / "03_reviews" / "review_index.md", "# Stage295 Review Index(295단계 검토 색인)\n")
    b.write_csv(
        stage_root / "03_reviews" / "stage_run_ledger.csv",
        b.STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage295_opened_from_run294C",
                "stage_id": next_stage_id,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage294_review",
                "status": status,
                "judgment": "opened_from_stage294_runtime_review",
                "evidence_boundary": "planning_from_stage294_evidence",
                "report_path": b.rel(REPORT),
                "notes": f"queue_rows={len(queue_rows)};next_action={next_action}",
            }
        ],
    )
    b.write_md(
        stage_root / "04_selected" / "selection_status.md",
        f"""# Stage295 Selection Status(295단계 선택 상태)

- stage_status(단계 상태): `{status}`
- current_packet(현재 작업 묶음): `{next_stage_id}_v1`
- current_run(현재 실행): `not_started`
- source_stage(원천 단계): `{STAGE_ID}`
- target_candidate(목표 후보): `{target}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- input_refs(입력 참조): `{b.rel(stage_root / "01_inputs" / "input_refs.md")}`
""",
    )


def replace_first_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def update_registers(selected: Mapping[str, Any] | None, next_stage_id: str) -> None:
    b = r293.base
    idea = b.io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if b.path_exists(IDEA_REGISTER) else "Register ideas when they become durable work.\n"
    if not selected and "IDEA-ST295-SPLIT-CONSISTENT-OUTCOME-DISTILLATION" not in idea:
        idea = (
            idea.rstrip()
            + f"\n\n| `IDEA-ST295-SPLIT-CONSISTENT-OUTCOME-DISTILLATION` | `{next_stage_id}` | split-consistent outcome distillation(분할 일관 결과 증류) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_no_candidate` | Stage294(294단계)의 OOS 양수/validation 음수 비대칭을 새 label/decision/risk surface(라벨/판단/위험 표면)로 재구성 |\n"
        )
        b.write_md(IDEA_REGISTER, idea)
    if not selected:
        negative = b.io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if b.path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
        if "NEG-ST294-MT5-OUTCOME-RELABEL-DIRECTIONAL-FLIP" not in negative:
            negative = (
                negative.rstrip()
                + "\n\n| `NEG-ST294-MT5-OUTCOME-RELABEL-DIRECTIONAL-FLIP` | `IDEA-ST294-MT5-OUTCOME-RELABEL-DIRECTIONAL-FLIP` | MT5 outcome relabel directional flip(MT5 결과 재라벨 방향 반전)이 ONNX-worthy candidate(ONNX화 가치 후보)로 닫히지 않음 | run294C(294C 실행)에서 OOS(표본외)는 일부 양수였지만 모든 validation(검증)이 음수라 후보 게이트를 통과하지 못함 | flip(반전)이 OOS 단서를 만들 수 있다는 점은 보존하되, validation damage(검증 손상)를 새 구조로 다뤄야 함 | split-consistent outcome distillation(분할 일관 결과 증류) 또는 validation damage veto(검증 손상 거부)일 때만 재개 |\n"
            )
            b.write_md(NEGATIVE_REGISTER, negative)


def update_docs(
    created_at: str,
    artifacts: Sequence[Path],
    scoreboard_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any] | None,
    status: str,
    judgment: str,
    next_action: str,
    next_stage_id: str,
) -> None:
    b = r293.base
    selected_text = selected["package_id"] if selected else "none"
    b.upsert_csv(
        RUN_REGISTRY,
        b.RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "mt5_outcome_relabel_directional_flip_review",
                "status": status,
                "judgment": judgment,
                "path": b.rel(REPORT),
                "notes": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)};selected_candidate={selected_text};target_stage={next_stage_id};next_action={next_action}",
            }
        ],
        key="run_id",
    )
    b.upsert_csv(
        ALPHA_LEDGER,
        b.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "mt5_outcome_relabel_directional_flip_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "candidate_selection_review",
                "scoreboard_lane": "mt5_outcome_relabel_directional_flip",
                "status": status,
                "judgment": judgment,
                "path": b.rel(REPORT),
                "primary_kpi": f"scoreboard_rows={len(scoreboard_rows)};selected_candidate={selected_text}",
                "guardrail_kpi": "adapter_package=none;onnx_readiness=not_started",
                "external_verification_status": "completed_run294B_mt5_probe",
                "notes": f"target_stage={next_stage_id};next_action={next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    b.upsert_csv(
        STAGE_LEDGER,
        b.STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "mt5_outcome_relabel_directional_flip_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "mt5_outcome_relabel_directional_flip_review_scoreboard",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "candidate_gate_review_no_adapter_no_onnx",
                "report_path": b.rel(REPORT),
                "notes": f"target_stage={next_stage_id};selected_candidate={selected_text}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(b.rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage294_mt5_outcome_relabel_directional_flip_review_artifact",
            "path": b.rel(path),
            "sha256": b.sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run294C MT5 outcome relabel directional flip review and Stage295 handoff",
        }
        for path in artifacts
        if b.path_exists(path)
    ]
    b.upsert_csv(ARTIFACT_REGISTRY, b.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    write_next_stage_scaffold(queue_rows, selected, next_stage_id, next_action)

    b.write_md(
        SELECTED,
        f"""# Stage294 Selection Status(294단계 선택 상태)

- stage_status(단계 상태): `{status}`
- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `Stage293`
- selected_candidate(선택 후보): `{selected_text}`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- report(보고): `{b.rel(REPORT)}`
- scoreboard(점수표): `{b.rel(SCOREBOARD)}`
""",
    )
    review_index = b.io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if b.path_exists(REVIEW_INDEX) else "# Stage294 Review Index(294단계 검토 색인)\n"
    review_index = b.append_once(
        review_index,
        "run294C_report",
        f"- run294C_report(294C 보고): `{b.rel(REPORT)}`\n- run294C_scoreboard(294C 점수표): `{b.rel(SCOREBOARD)}`\n- run294C_failure_memory(294C 실패 기억): `{b.rel(FAILURE_MEMORY)}`",
    )
    b.write_md(REVIEW_INDEX, review_index)

    current = b.io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if b.path_exists(CURRENT_STATE) else ""
    current = replace_first_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{next_stage_id}_v1`")
    current = replace_first_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_first_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{next_stage_id}`")
    current = replace_first_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{STAGE_ID}`")
    current = replace_first_prefix(current, "- target_surface(", "- target_surface(목표 표면): `none`")
    current = replace_first_prefix(current, "- status(", f"- status(상태): `{status}`")
    current = replace_first_prefix(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    current = b.append_once(
        current,
        "run294C_summary",
        f"- run294C_summary(294C 요약): Stage294(294단계) MT5 actual routed total(MT5 실제 라우팅 전체)을 검토했다. Effect(효과): OOS(표본외) 양수 단서는 있었지만 validation(검증)이 모두 음수라 selected_candidate(선택 후보)는 `{selected_text}`이고 Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않으며 `{next_stage_id}`를 새 논제로 열었다.",
    )
    b.write_md(CURRENT_STATE, current)

    workspace = b.io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if b.path_exists(WORKSPACE_STATE) else ""
    workspace = b.replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = b.replace_line_prefix(workspace, "active_stage:", f"active_stage: {next_stage_id}")
    workspace = b.replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage294(294단계) run294C(294C 실행) MT5 outcome relabel directional flip review(MT5 결과 재라벨 방향 반전 검토) `{RUN_ID}`. "
        f"Effect(효과): scoreboard(점수표) `{len(scoreboard_rows)}`행과 failure memory(실패 기억) `{len(failure_rows)}`행을 만들고 selected candidate(선택 후보) `{selected_text}`로 `{next_stage_id}`를 열었다.\n"
    )
    workspace = b.prepend_focus(workspace, focus, RUN_ID)
    b.write_md(WORKSPACE_STATE, workspace)

    changelog = b.io_path(CHANGELOG).read_text(encoding="utf-8-sig") if b.path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = b.append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run294C MT5 outcome relabel directional flip review(294C MT5 결과 재라벨 방향 반전 검토)\n\n"
        f"- status(상태): `{status}`\n"
        f"- judgment(판정): `{judgment}`\n"
        f"- effect(효과): Stage294(294단계)를 `{selected_text}` 선택 상태로 판정하고 `{next_stage_id}`를 열었다.\n"
        f"- boundary(경계): Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 아직 `not_started/not_claimed`다.\n",
    )
    b.write_md(CHANGELOG, changelog)
    update_registers(selected, next_stage_id)


def main() -> None:
    patch_review293_constants()
    r293.stage294_queue_rows = stage295_queue_rows
    r293.status_pack = status_pack
    r293.result_rows = result_rows
    r293.report_markdown = report_markdown
    r293.decision_markdown = decision_markdown
    r293.update_docs = update_docs
    r293.main()


if __name__ == "__main__":
    main()
