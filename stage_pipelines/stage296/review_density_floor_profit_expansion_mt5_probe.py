from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage292 import review_anti_direction_meta_label_trade_simulator_mt5_probe as base  # noqa: E402


STAGE_ID = "296_onnx_candidate_campaign__density_floor_profit_expansion_rebuild"
NEXT_REBUILD_STAGE_ID = "297_onnx_candidate_campaign__bilevel_curve_monotonic_profit_rebuild"
NEXT_ADAPTER_STAGE_ID = "297_onnx_candidate_campaign__adapter_package_for_stage296_candidate"
RUN_ID = "run296C_review_density_floor_profit_expansion_mt5_probe_v1"
RUN_NUMBER = "run296C"
SOURCE_RUN_ID = "run296B_density_floor_profit_expansion_mt5_probe_v1"
PARENT_RUN_ID = "run296A_design_density_floor_profit_expansion_rebuild_v1"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN296A = STAGE_ROOT / "02_runs" / "run296A"
RUN296B = STAGE_ROOT / "02_runs" / "run296B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_MANIFEST = RUN296A / "candidate_payload_manifest.csv"
SOURCE_KPI = RUN296B / "mt5_kpi_summary.csv"
SOURCE_EXECUTION = RUN296B / "execution_result.json"
PRODUCER = Path("stage_pipelines/stage296/review_density_floor_profit_expansion_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "density_floor_profit_expansion_review_scoreboard.csv"
MONTHLY = RUN_ROOT / "monthly_attribution.csv"
SESSION = RUN_ROOT / "session_attribution.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
LOCAL_POCKETS = RUN_ROOT / "local_curve_pocket_diagnostics.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage297_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run296C_density_floor_profit_expansion_review_stage297_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage296_density_floor_profit_expansion_review_stage297_open.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def configure_base() -> None:
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
        "RUN292A": RUN296A,
        "RUN292B": RUN296B,
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
        setattr(base, name, value)


def stage297_queue_rows(selected: Mapping[str, Any] | None) -> list[dict[str, Any]]:
    refs = ";".join(
        [
            "stage267_reference_evidence",
            "stage286_density_curve_quality_failure",
            "stage287_density_scale_curve_pocket_failure",
            "stage293_profit_scale_density_calibration_failure",
            "stage294_outcome_flip_oos_clue",
            "stage295_split_consistent_outcome_distillation_failure",
            "stage296_density_floor_profit_expansion_review",
        ]
    )
    if selected:
        return [
            {
                "seed_id": "stage297_adapter_package_for_stage296_candidate",
                "source_stage_id": STAGE_ID,
                "source_run_id": RUN_ID,
                "seed_role": "adapter_package_build(어댑터 패키지 구성)",
                "hypothesis": f"{selected['package_id']} can be formalized as an Adapter package(어댑터 패키지) with fixed feature order(고정 피처 순서), decision surface(판단 표면), risk logic(위험 로직), and runtime handoff(런타임 인계).",
                "broad_sweep": "feature order receipt, decision surface receipt, risk logic receipt, runtime handoff receipt(피처 순서/판단 표면/위험 로직/런타임 인계 영수증)",
                "aggressive_sweep": "none; adapter packaging only(없음; 어댑터 패키징만)",
                "defensive_sweep": "ONNX parity pressure and MT5 reproduction planning(온엑스 동등성 압박과 MT5 재현 계획)",
                "success_gate": "Adapter package complete and ONNX-go pressure ready(어댑터 패키지 완료와 온엑스 진행 압박 준비)",
                "discard_condition": "feature order or runtime handoff cannot be traced(피처 순서나 런타임 인계를 추적할 수 없음)",
                "prior_stage_refs": refs,
                "claim_boundary": BOUNDARY,
            }
        ]
    return [
        {
            "seed_id": "stage297_bilevel_curve_monotonic_profit_primary",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_primary(새 논제 주축)",
            "hypothesis": "Bi-level curve-monotonic profit rebuild(이중 단계 곡선 단조 수익 재구성)가 entry creation(진입 생성)과 curve veto(곡선 거부)를 한 표면 안에서 같이 학습하면 순수익 규모와 매끈한 우상향을 동시에 만들 수 있다.",
            "broad_sweep": "trade-level outcome labels, rolling pocket penalty, month/session monotonicity, density floor router(거래 단위 결과 라벨/롤링 포켓 벌점/월세션 단조성/거래 밀도 하한 라우터)",
            "aggressive_sweep": "payoff-tail widening up to 10 trades/day only where rolling curve stays positive(롤링 곡선이 양수로 버티는 곳에서만 일 10거래까지 보상 꼬리 확장)",
            "defensive_sweep": "hard reject negative validation pockets, weak sessions, top-trade concentration, and long underwater zones(검증 음수 포켓/약한 세션/상위 거래 집중/긴 수중 구간 강한 거부)",
            "success_gate": "validation/OOS both positive with >=300 net each, combined >=800, PF/recovery/expectancy positive, 4-10 trades/day, and no deep zoomed curve hollow(검증/표본외 각각 순수익 300 이상, 합산 800 이상, PF/회복/기대값 양수, 일 4-10거래, 깊은 확대 곡선 패임 없음)",
            "discard_condition": "profit scale appears only through one month, one session, or deep rolling drawdown pocket(수익 규모가 한 달/한 세션/깊은 롤링 손실 포켓으로만 나타남)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage297_aggressive_payoff_density_surface",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_aggressive(새 논제 공격형)",
            "hypothesis": "Aggressive payoff-density surface(공격형 보상-밀도 표면)가 cp296A/E proxy(대리) 상방을 실제 MT5(메타트레이더5) 수익 규모로 전환할 수 있다.",
            "broad_sweep": "payoff-ranked entry expansion, side-aware direction remap, asymmetric hold/exit(보상 순위 진입 확장/방향 인식 재매핑/비대칭 보유와 청산)",
            "aggressive_sweep": "density bands 6/8/10 trades/day with tail capture(일 6/8/10거래 밀도 구간과 꼬리 수익 포착)",
            "defensive_sweep": "validation damage veto and rolling drawdown cap(검증 손상 거부와 롤링 손실폭 상한)",
            "success_gate": "profit scale and curve smoothness improve together without falling below 4 trades/day(일 4거래 아래로 떨어지지 않고 수익 규모와 곡선 매끄러움이 함께 개선)",
            "discard_condition": "higher density lowers PF below 1.12 or creates local curve holes(높은 밀도가 PF 1.12 아래로 내리거나 국소 곡선 구멍을 만듦)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage297_defensive_curve_veto_countermodel",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_defensive(새 논제 방어형)",
            "hypothesis": "Curve veto countermodel(곡선 거부 반대모델)이 validation damage(검증 손상)를 먼저 제거한 뒤 밀도와 수익을 확장해야 한다.",
            "broad_sweep": "train-only pocket labels, weak-month/session features, underwater state, top-contribution cap(학습 전용 포켓 라벨/약한 월세션 피처/수중 상태/상위 기여 상한)",
            "aggressive_sweep": "only re-expand after pocket labels clear(포켓 라벨이 사라진 뒤에만 재확장)",
            "defensive_sweep": "reject negative expectancy bands and drawdown-to-net outliers(음의 기대값 구간과 손실폭 대비 순수익 이상치 거부)",
            "success_gate": "validation and OOS curves pass pocket gates before Adapter(어댑터 전 검증/표본외 곡선 포켓 관문 통과)",
            "discard_condition": "veto becomes thin trade-count repair below 4 trades/day(거부가 일 4거래 미만 얇은 거래수 수리가 됨)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
    ]


def status_pack(selected: Mapping[str, Any] | None) -> tuple[str, str, str, str]:
    if selected:
        return (
            "completed_density_floor_profit_expansion_review_candidate_gate_ready_stage297_adapter_opened",
            "density_floor_profit_expansion_candidate_package_gate_ready_adapter_required_no_onnx",
            "run297A_design_adapter_package_for_stage296_candidate",
            NEXT_ADAPTER_STAGE_ID,
        )
    return (
        "completed_density_floor_profit_expansion_review_no_candidate_stage297_opened",
        "density_floor_profit_expansion_runtime_probe_negative_no_adapter_no_onnx",
        "run297A_design_bilevel_curve_monotonic_profit_rebuild_packet",
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
    candidate_gate = "passed" if selected else "failed"
    rows = [
        {
            "result_subject": "Stage296 density-floor profit expansion MT5 review(296단계 거래 밀도 하한 수익 확장 MT5 검토)",
            "evidence_available": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)};source_kpi={base.rel(SOURCE_KPI)}",
            "evidence_missing": "Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성), MT5 runtime reproduction(MT5 런타임 재현)",
            "judgment_label": "exploratory" if selected else "negative",
            "judgment_class": judgment,
            "claim_boundary": BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": "최소 거래수, 일 4-10거래, 순수익 규모, PF(수익 팩터), 회복, 기대값, 확대 곡선 포켓을 actual routed total(실제 라우팅 전체) 기준으로 같이 판정했다.",
        }
    ]
    gates = [
        {
            "gate_name": "mt5_runtime_probe(MT5 런타임 탐침)",
            "status": "passed",
            "evidence_path": base.rel(SOURCE_KPI),
            "effect": "actual routed total(실제 라우팅 전체) 기준으로 후보를 판정했다.",
        },
        {
            "gate_name": "minimum_trade_and_density(최소 거래수와 밀도)",
            "status": candidate_gate,
            "evidence_path": base.rel(SCOREBOARD),
            "effect": "검증과 표본외 모두 최소 거래수와 일 4-10거래 조건을 동시에 보았다.",
        },
        {
            "gate_name": "profit_efficiency_curve(순수익/효율/곡선)",
            "status": candidate_gate,
            "evidence_path": base.rel(SCOREBOARD),
            "effect": "순수익 규모, PF(수익 팩터), 회복, 기대값, 월/세션/롤링 포켓을 함께 보았다.",
        },
        {
            "gate_name": "adapter_package(어댑터 패키지)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "후보 게이트 통과 전에는 Adapter(어댑터)를 만들지 않는다.",
        },
        {
            "gate_name": "onnx_readiness(ONNX 준비)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "Adapter(어댑터)와 parity(동등성) 전에는 ONNX(온엑스)를 시작하지 않는다.",
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
        "# run296C Density-Floor Profit Expansion Review(296C 거래 밀도 하한 수익 확장 검토)",
        "",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- selected_candidate(선택 후보): `{selected['package_id'] if selected else 'none'}`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(ONNX 준비): `not_started`",
        f"- next_action(다음 행동): `{next_action}`",
        f"- next_stage(다음 단계): `{next_stage_id}`",
        "",
        "Effect(효과): Stage296(296단계)는 proxy(대리) 상방을 그대로 믿지 않고 MT5 actual routed total(MT5 실제 라우팅 전체)에서 최소 거래수, 일 4-10거래, 순수익 규모, PF(수익 팩터), 회복, 기대값, 월/세션/롤링 포켓을 같이 판정한다.",
        "",
        "| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | val/day(검증 일거래) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | OOS/day(표본외 일거래) | gate(게이트) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {pkg} | {vn:.2f} | {vpf:.2f} | {vtd:.2f} | {on:.2f} | {opf:.2f} | {otd:.2f} | {gate} |".format(
                pkg=row["package_id"],
                vn=base.safe_float(row["validation_net_profit"]),
                vpf=base.safe_float(row["validation_pf"]),
                vtd=base.safe_float(row["validation_trades_per_day"]),
                on=base.safe_float(row["oos_net_profit"]),
                opf=base.safe_float(row["oos_pf"]),
                otd=base.safe_float(row["oos_trades_per_day"]),
                gate=row["review_label"],
            )
        )
    lines.extend(
        [
            "",
            "## Stage297 Thesis(297단계 논제)",
            "",
            "조건을 통과한 패키지가 있으면 Stage297(297단계)은 Adapter package(어댑터 패키지)로 넘어간다. 없으면 Stage297(297단계)은 좁은 repair(수리)가 아니라 bi-level curve-monotonic profit rebuild(이중 단계 곡선 단조 수익 재구성)로 entry creation(진입 생성), profit scale(순수익 규모), curve veto(곡선 거부)를 한 번에 다시 설계한다.",
            "",
            f"Claim boundary(주장 경계): `{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def decision_markdown(selected: Mapping[str, Any] | None, status: str, judgment: str, next_stage_id: str) -> str:
    if selected:
        decision = f"{selected['package_id']} passes the candidate package gate(후보 패키지 게이트) and moves to Adapter package(어댑터 패키지) work."
    else:
        decision = "No Stage296 package passes the ONNX-worthy candidate gate(ONNX화 가치 후보 게이트), so Stage297 opens bi-level curve-monotonic profit rebuild(이중 단계 곡선 단조 수익 재구성)."
    return f"""# Stage296 Decision(296단계 결정)

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): {decision}
- next_stage(다음 단계): `{next_stage_id}`

Effect(효과): 순수익 규모와 매끈한 곡선 조건을 동시에 통과하지 못한 패키지를 ONNX(온엑스)로 밀지 않고, 조건 통과 전에는 Adapter(어댑터)를 시작하지 않는다.
"""


def write_next_stage_scaffold(
    queue_rows: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any] | None,
    next_stage_id: str,
    next_action: str,
) -> None:
    stage_root = ROOT / "stages" / next_stage_id
    for subdir in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        base.io_path(stage_root / subdir).mkdir(parents=True, exist_ok=True)
    input_name = "adapter_seed_queue.csv" if selected else "stage297_seed_queue.csv"
    stage_status = "opened_adapter_package_for_stage296_candidate" if selected else "opened_bilevel_curve_monotonic_profit_rebuild"
    target = selected["package_id"] if selected else "none"
    base.write_csv(stage_root / "01_inputs" / input_name, base.QUEUE_COLUMNS, queue_rows)
    question = (
        "Can the selected Stage296 candidate package be formalized into a traceable Adapter package(어댑터 패키지)?"
        if selected
        else "Can bi-level curve-monotonic profit rebuild(이중 단계 곡선 단조 수익 재구성) deliver minimum trade count(최소 거래수), 4-10 trades/day(일 4-10거래), profit scale(순수익 규모), and smooth zoomed curves(매끈한 확대 곡선) together?"
    )
    base.write_md(
        stage_root / "00_spec" / "stage_brief.md",
        f"""# Stage297 Brief(297단계 개요)

- stage_id(단계 ID): `{next_stage_id}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- question(질문): {question}
- boundary(경계): `{BOUNDARY}`

Effect(효과): Stage296(296단계)의 결과를 후보 보존 압력으로 쓰지 않고, 조건을 통과했을 때만 Adapter(어댑터)로 넘기며 실패 시에는 새 decision/risk/model surface(판단/위험/모델 표면) 질문으로 바꾼다.
""",
    )
    base.write_md(
        stage_root / "01_inputs" / "input_refs.md",
        f"""# Stage297 Input Refs(297단계 입력 참조)

- source_report(원천 보고): `{base.rel(REPORT)}`
- source_scoreboard(원천 점수표): `{base.rel(SCOREBOARD)}`
- source_failure_memory(원천 실패 기억): `{base.rel(FAILURE_MEMORY)}`
- source_queue(원천 대기열): `{base.rel(stage_root / "01_inputs" / input_name)}`

Effect(효과): Stage297(297단계)은 Stage296(296단계)의 MT5(메타트레이더5) 결과를 근거로 쓰되, 같은 threshold repair(임계값 수리)를 반복하지 않는다.
""",
    )
    base.write_md(stage_root / "03_reviews" / "review_index.md", "# Stage297 Review Index(297단계 검토 색인)\n")
    base.write_csv(
        stage_root / "03_reviews" / "stage_run_ledger.csv",
        base.STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage297_opened_from_run296C",
                "stage_id": next_stage_id,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage296_review",
                "status": stage_status,
                "judgment": "opened_from_stage296_runtime_review",
                "evidence_boundary": "planning_from_stage296_evidence",
                "report_path": base.rel(REPORT),
                "notes": f"queue_rows={len(queue_rows)};next_action={next_action}",
            }
        ],
    )
    base.write_md(
        stage_root / "04_selected" / "selection_status.md",
        f"""# Stage297 Selection Status(297단계 선택 상태)

- stage_status(단계 상태): `{stage_status}`
- current_packet(현재 작업 묶음): `{next_stage_id}_v1`
- current_run(현재 실행): `not_started`
- source_stage(원천 단계): `{STAGE_ID}`
- target_candidate(목표 후보): `{target}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- input_refs(입력 참조): `{base.rel(stage_root / "01_inputs" / "input_refs.md")}`
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
    idea = base.io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if base.path_exists(IDEA_REGISTER) else "Register ideas when they become durable work.\n"
    if selected and "IDEA-ST297-ADAPTER-FOR-STAGE296-CANDIDATE" not in idea:
        idea = (
            idea.rstrip()
            + f"\n\n| `IDEA-ST297-ADAPTER-FOR-STAGE296-CANDIDATE` | `{next_stage_id}` | Adapter package(어댑터 패키지) for Stage296 candidate(296단계 후보) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_after_candidate_gate` | 후보 게이트 통과 뒤 Adapter(어댑터), parity(동등성), ONNX(온엑스) 압박만 진행 |\n"
        )
        base.write_md(IDEA_REGISTER, idea)
    if not selected and "IDEA-ST297-BILEVEL-CURVE-MONOTONIC-PROFIT" not in idea:
        idea = (
            idea.rstrip()
            + f"\n\n| `IDEA-ST297-BILEVEL-CURVE-MONOTONIC-PROFIT` | `{next_stage_id}` | bi-level curve-monotonic profit rebuild(이중 단계 곡선 단조 수익 재구성) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_no_candidate` | Stage296(296단계)의 proxy-positive/runtime-gated(대리 양수/런타임 관문) 공백을 entry creation(진입 생성), profit scale(순수익 규모), curve veto(곡선 거부) 공동 목적함수로 재구성 |\n"
        )
        base.write_md(IDEA_REGISTER, idea)
    if not selected:
        negative = base.io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if base.path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
        if "NEG-ST296-DENSITY-FLOOR-PROFIT-EXPANSION" not in negative:
            negative = (
                negative.rstrip()
                + "\n\n| `NEG-ST296-DENSITY-FLOOR-PROFIT-EXPANSION` | `IDEA-ST296-DENSITY-FLOOR-PROFIT-EXPANSION` | density-floor profit expansion(거래 밀도 하한 수익 확장)이 ONNX-worthy candidate(ONNX화 가치 후보)로 닫히지 않음 | run296C(296C 실행)에서 최소 거래수, 일 4-10거래, 순수익 규모, PF(수익 팩터), 회복, 기대값, 곡선 포켓을 함께 통과한 패키지가 없음 | cp296 proxy(대리) 상방은 보존하되 MT5 runtime(메타트레이더5 런타임)에서 수익 규모와 곡선 품질을 같이 만족해야 함 | 새 curve-monotonic profit objective(곡선 단조 수익 목적함수) 또는 entry/risk surface(진입/위험 표면)일 때만 재개 |\n"
            )
            base.write_md(NEGATIVE_REGISTER, negative)


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
    selected_text = selected["package_id"] if selected else "none"
    base.upsert_csv(
        RUN_REGISTRY,
        base.RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "density_floor_profit_expansion_review",
                "status": status,
                "judgment": judgment,
                "path": base.rel(REPORT),
                "notes": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)};selected_candidate={selected_text};target_stage={next_stage_id};next_action={next_action}",
            }
        ],
        key="run_id",
    )
    base.upsert_csv(
        ALPHA_LEDGER,
        base.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "density_floor_profit_expansion_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "candidate_selection_review",
                "scoreboard_lane": "density_floor_profit_expansion",
                "status": status,
                "judgment": judgment,
                "path": base.rel(REPORT),
                "primary_kpi": f"scoreboard_rows={len(scoreboard_rows)};selected_candidate={selected_text}",
                "guardrail_kpi": "adapter_package=none;onnx_readiness=not_started;goal_achieve=not_claimed",
                "external_verification_status": "completed_run296B_mt5_probe",
                "notes": f"target_stage={next_stage_id};next_action={next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    base.upsert_csv(
        STAGE_LEDGER,
        base.STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "density_floor_profit_expansion_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "density_floor_profit_expansion_review_scoreboard",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "candidate_gate_review_no_adapter_no_onnx",
                "report_path": base.rel(REPORT),
                "notes": f"target_stage={next_stage_id};selected_candidate={selected_text}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(base.rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage296_density_floor_profit_expansion_review_artifact",
            "path": base.rel(path),
            "sha256": base.sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run296C density-floor profit expansion review and Stage297 handoff",
        }
        for path in artifacts
        if base.path_exists(path)
    ]
    base.upsert_csv(ARTIFACT_REGISTRY, base.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    write_next_stage_scaffold(queue_rows, selected, next_stage_id, next_action)
    base.write_md(
        SELECTED,
        f"""# Stage296 Selection Status(296단계 선택 상태)

- stage_status(단계 상태): `{status}`
- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `Stage295`
- selected_candidate(선택 후보): `{selected_text}`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- next_stage(다음 단계): `{next_stage_id}`
- report(보고): `{base.rel(REPORT)}`
- scoreboard(점수표): `{base.rel(SCOREBOARD)}`
""",
    )
    review_index = base.io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if base.path_exists(REVIEW_INDEX) else "# Stage296 Review Index(296단계 검토 색인)\n"
    review_index = base.append_once(
        review_index,
        "run296C_report",
        f"- run296C_report(296C 보고): `{base.rel(REPORT)}`\n- run296C_scoreboard(296C 점수표): `{base.rel(SCOREBOARD)}`\n- run296C_failure_memory(296C 실패 기억): `{base.rel(FAILURE_MEMORY)}`\n- run296C_local_pockets(296C 국소 포켓): `{base.rel(LOCAL_POCKETS)}`",
    )
    base.write_md(REVIEW_INDEX, review_index)
    current = base.io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if base.path_exists(CURRENT_STATE) else ""
    current = replace_first_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{next_stage_id}_v1`")
    current = replace_first_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_first_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{next_stage_id}`")
    current = replace_first_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{STAGE_ID}`")
    current = replace_first_prefix(current, "- target_surface(", "- target_surface(목표 표면): `none`")
    current = replace_first_prefix(current, "- status(", f"- status(상태): `{status}`")
    current = replace_first_prefix(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    current = base.append_once(
        current,
        "run296C_summary",
        f"- run296C_summary(296C 요약): Stage296(296단계) MT5 actual routed total(MT5 실제 라우팅 전체)을 검토했다. Effect(효과): selected_candidate(선택 후보)는 `{selected_text}`이고 Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않으며 `{next_stage_id}`를 열었다.",
    )
    base.write_md(CURRENT_STATE, current)
    workspace = base.io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if base.path_exists(WORKSPACE_STATE) else ""
    workspace = base.replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = base.replace_line_prefix(workspace, "active_stage:", f"active_stage: {next_stage_id}")
    workspace = base.replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage296(296단계) run296C(296C 실행) density-floor profit expansion review(거래 밀도 하한 수익 확장 검토) `{RUN_ID}`. "
        f"Effect(효과): scoreboard(점수표) `{len(scoreboard_rows)}`행과 failure memory(실패 기억) `{len(failure_rows)}`행을 만들고 selected candidate(선택 후보) `{selected_text}`로 `{next_stage_id}`를 열었다.\n"
    )
    workspace = base.prepend_focus(workspace, focus, RUN_ID)
    base.write_md(WORKSPACE_STATE, workspace)
    changelog = base.io_path(CHANGELOG).read_text(encoding="utf-8-sig") if base.path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = base.append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run296C Density-floor profit expansion review(296C 거래 밀도 하한 수익 확장 검토)\n\n"
        f"- status(상태): `{status}`\n"
        f"- judgment(판정): `{judgment}`\n"
        f"- effect(효과): Stage296(296단계)를 `{selected_text}` 선택 상태로 판정하고 `{next_stage_id}`를 열었다.\n"
        f"- boundary(경계): Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 아직 `not_started/not_claimed`다.\n",
    )
    base.write_md(CHANGELOG, changelog)
    update_registers(selected, next_stage_id)


def main() -> None:
    configure_base()
    base.stage293_queue_rows = stage297_queue_rows
    base.status_pack = status_pack
    base.result_rows = result_rows
    base.report_markdown = report_markdown
    base.decision_markdown = decision_markdown
    base.write_next_stage_scaffold = write_next_stage_scaffold
    base.update_docs = update_docs
    base.main()


if __name__ == "__main__":
    main()
