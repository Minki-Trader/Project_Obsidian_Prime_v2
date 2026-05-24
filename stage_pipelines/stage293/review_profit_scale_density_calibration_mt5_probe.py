from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage292 import review_anti_direction_meta_label_trade_simulator_mt5_probe as base  # noqa: E402

STAGE_ID = "293_onnx_candidate_campaign__profit_scale_density_calibration_rebuild"
NEXT_REBUILD_STAGE_ID = "294_onnx_candidate_campaign__mt5_outcome_relabel_directional_flip_rebuild"
NEXT_ADAPTER_STAGE_ID = "294_onnx_candidate_campaign__adapter_package_for_stage293_candidate"
RUN_ID = "run293C_review_profit_scale_density_calibration_mt5_probe_v1"
RUN_NUMBER = "run293C"
SOURCE_RUN_ID = "run293B_profit_scale_density_calibration_mt5_probe_v1"
PARENT_RUN_ID = "run293A_design_profit_scale_density_calibration_rebuild_v1"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN293A = STAGE_ROOT / "02_runs" / "run293A"
RUN293B = STAGE_ROOT / "02_runs" / "run293B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_MANIFEST = RUN293A / "candidate_payload_manifest.csv"
SOURCE_KPI = RUN293B / "mt5_kpi_summary.csv"
SOURCE_EXECUTION = RUN293B / "execution_result.json"
PRODUCER = Path("stage_pipelines/stage293/review_profit_scale_density_calibration_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "profit_scale_density_calibration_review_scoreboard.csv"
MONTHLY = RUN_ROOT / "monthly_attribution.csv"
SESSION = RUN_ROOT / "session_attribution.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
LOCAL_POCKETS = RUN_ROOT / "local_curve_pocket_diagnostics.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage294_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run293C_profit_scale_density_calibration_review_stage294_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage293_profit_scale_density_calibration_review_stage294_open.md"

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
        "RUN292A": RUN293A,
        "RUN292B": RUN293B,
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


def stage294_queue_rows(selected: Mapping[str, Any] | None) -> list[dict[str, Any]]:
    refs = ";".join(
        [
            "stage267_reference_evidence",
            "stage286_density_curve_quality",
            "stage287_density_scale_curve_pocket",
            "stage290_payoff_weighted_edge",
            "stage291_walk_forward_payoff_generalization",
            "stage292_anti_direction_meta_trade_sim",
            "stage293_profit_scale_density_calibration",
        ]
    )
    if selected:
        return [
            {
                "seed_id": "stage294_adapter_package_for_stage293_candidate",
                "source_stage_id": STAGE_ID,
                "source_run_id": RUN_ID,
                "seed_role": "adapter_package_build(어댑터 패키지 구성)",
                "hypothesis": f"{selected['package_id']} can be formalized as an Adapter package(어댑터 패키지) with traceable feature order(피처 순서), decision surface(판단 표면), risk logic(위험 로직), and runtime handoff(런타임 인계).",
                "broad_sweep": "feature order receipt, decision surface receipt, risk logic receipt, runtime handoff receipt(피처 순서/판단 표면/위험 로직/런타임 인계 영수증)",
                "aggressive_sweep": "none; adapter packaging only(없음; 어댑터 패키징만)",
                "defensive_sweep": "parity pressure before ONNX export(ONNX 내보내기 전 동등성 압박)",
                "success_gate": "Adapter package complete, feature order fixed, runtime handoff reproducible(어댑터 패키지 완료/피처 순서 고정/런타임 인계 재현)",
                "discard_condition": "feature order or runtime handoff cannot be traced(피처 순서 또는 런타임 인계를 추적할 수 없음)",
                "prior_stage_refs": refs,
                "claim_boundary": BOUNDARY,
            }
        ]
    return [
        {
            "seed_id": "stage294_mt5_outcome_relabel_directional_flip",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_primary(새 논제 주축)",
            "hypothesis": "MT5 outcome relabeling(메타트레이더5 결과 재라벨) can turn near-breakeven dense losers(고밀도 근본전 손실 표면) into a direction-aware edge(방향 인식 우위) by learning from filled trade outcomes rather than proxy labels(대리 라벨).",
            "broad_sweep": "filled-trade win/loss, adverse excursion, hold-path PnL, direction flip, flat veto(체결 거래 승패/불리 이동/보유 경로 손익/방향 반전/관망 거부)",
            "aggressive_sweep": "flip negative expectancy bands, widen only high-payoff dense windows(음의 기대값 구간 반전, 높은 보상 고밀도 창만 확장)",
            "defensive_sweep": "reject bands with deep rolling loss pockets and weak-session damage(깊은 롤링 손실 포켓과 약한 세션 손상 구간 거부)",
            "success_gate": "validation and OOS both positive, 4-10 trades/day, PF/recovery/expectancy positive, no deep zoomed curve hollow(검증/표본외 양수, 일 4-10거래, 수익 팩터/회복/기대값 양수, 확대 곡선 깊은 패임 없음)",
            "discard_condition": "direction flip remains negative or creates curve holes(방향 반전이 계속 음수거나 곡선 구멍을 만듦)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage294_cost_aware_trade_acceptance",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_defensive_profit_quality(새 논제 방어형 수익 품질)",
            "hypothesis": "Cost-aware trade acceptance(비용 인식 거래 수락) can keep Stage293 density(밀도) while removing fills whose MT5 spread/skip/path cost(스프레드/스킵/경로 비용) turns proxy edge(대리 우위) negative.",
            "broad_sweep": "spread-normalized edge, realized cost bands, session cost veto, hold-time cost decay(스프레드 정규화 우위/실현 비용 구간/세션 비용 거부/보유시간 비용 감쇠)",
            "aggressive_sweep": "keep dense bands only when cost-adjusted payoff is convex(비용 조정 보상이 볼록할 때만 고밀도 구간 유지)",
            "defensive_sweep": "hard veto on negative expectancy sessions and large adverse path(음의 기대값 세션과 큰 불리 경로 강한 거부)",
            "success_gate": "profit scale improves without falling below 4 trades/day(일 4거래 아래로 떨어지지 않고 순수익 규모 개선)",
            "discard_condition": "cost filter becomes a thin trade-count repair(비용 필터가 얇은 거래수 수리로 변함)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage294_near_breakeven_flip_smoother",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_curve_smoother(새 논제 곡선 완화)",
            "hypothesis": "Near-breakeven flip smoothing(근본전 반전 완화) can transform cp293A/cp293F-like losses(293A/293F형 손실) into a smoother rising account path(완만한 우상향 계좌 경로) by alternating flip, skip, and reduced-risk states(반전/회피/축소위험 상태).",
            "broad_sweep": "rolling expectancy state, recent drawdown state, side-specific flip probability, reduced-risk route(롤링 기대값 상태/최근 손실폭 상태/방향별 반전 확률/축소위험 경로)",
            "aggressive_sweep": "increase exposure after fresh equity highs only(새 평가금 고점 이후에만 노출 확대)",
            "defensive_sweep": "decrease exposure after local pocket detection(국소 포켓 감지 뒤 노출 축소)",
            "success_gate": "zoomed balance/equity keeps upward slope across validation and OOS(검증과 표본외 확대 잔액/평가금이 우상향 유지)",
            "discard_condition": "smoother removes profit scale or stays net negative(완화가 수익 규모를 제거하거나 순손실 유지)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage294_aggressive_density_payoff_rescale",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_aggressive_profit_scale(새 논제 공격형 수익 규모)",
            "hypothesis": "Aggressive density/payoff rescale(공격형 밀도/보상 재스케일) can retain 4-10 trades/day(일 4-10거래) while pushing net profit(순수익) above the ONNX-worthy scale(ONNX화 가치 규모).",
            "broad_sweep": "per-session density quota, payoff-ranked entry expansion, tail capture, max-hold variation(세션별 밀도 할당/보상 순위 진입 확장/꼬리 수익 포착/최대 보유 변형)",
            "aggressive_sweep": "controlled over-density bands up to 10 trades/day(일 10거래까지 통제된 과밀 구간)",
            "defensive_sweep": "monthly loss cap, rolling pocket stop, concentration cap(월 손실 상한/롤링 포켓 중지/집중도 상한)",
            "success_gate": "net profit, PF, recovery, expectancy, and smoothness all improve together(순수익/수익 팩터/회복/기대값/매끄러움 동시 개선)",
            "discard_condition": "higher scale only appears through top-trade concentration or drawdown pocket(수익 규모가 상위 거래 집중이나 손실 포켓으로만 나타남)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
    ]


def status_pack(selected: Mapping[str, Any] | None) -> tuple[str, str, str, str]:
    if selected:
        return (
            "completed_profit_scale_density_calibration_review_candidate_gate_ready_stage294_adapter_opened",
            "profit_scale_density_calibration_candidate_package_gate_ready_adapter_required_no_onnx",
            "run294A_design_adapter_package_for_stage293_candidate",
            NEXT_ADAPTER_STAGE_ID,
        )
    return (
        "completed_profit_scale_density_calibration_review_no_candidate_stage294_opened",
        "profit_scale_density_calibration_runtime_probe_negative_no_adapter_no_onnx",
        "run294A_design_mt5_outcome_relabel_directional_flip_rebuild_packet",
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
            "result_subject": "Stage293 profit-scale density calibration MT5 review(293단계 순수익 규모/거래 밀도 보정 MT5 검토)",
            "evidence_available": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)};source_kpi={base.rel(SOURCE_KPI)}",
            "evidence_missing": "Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성), MT5 runtime reproduction(MT5 런타임 재현)",
            "judgment_label": "exploratory" if selected else "negative",
            "judgment_class": judgment,
            "claim_boundary": BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": "순수익이 음수라서 ONNX(온엑스)로 넘기지 않고, 실제 MT5 결과 재라벨과 방향 반전을 새 Stage294 논제로 연다.",
        }
    ]
    gates = [
        {
            "gate_name": "mt5_runtime_probe(MT5 런타임 탐침)",
            "status": "passed",
            "evidence_path": base.rel(SOURCE_KPI),
            "effect": "actual routed total(실제 라우팅 전체) 기준으로 후보를 판정한다.",
        },
        {
            "gate_name": "minimum_trade_and_density(최소 거래수와 밀도)",
            "status": candidate_gate,
            "evidence_path": base.rel(SCOREBOARD),
            "effect": "최소 거래수와 일 4-10거래 조건을 동시에 본다.",
        },
        {
            "gate_name": "profit_efficiency_curve(순수익/효율/곡선)",
            "status": candidate_gate,
            "evidence_path": base.rel(SCOREBOARD),
            "effect": "순수익 규모, PF(수익 팩터), 회복, 기대값, 확대 곡선 포켓을 함께 본다.",
        },
        {
            "gate_name": "adapter_package(어댑터 패키지)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "후보 게이트 전에는 Adapter(어댑터)를 만들지 않는다.",
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
        "# run293C Profit-Scale Density Calibration Review(293C 순수익 규모/거래 밀도 보정 검토)",
        "",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- selected_candidate(선택 후보): `{selected['package_id'] if selected else 'none'}`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(ONNX 준비): `not_started`",
        f"- next_action(다음 행동): `{next_action}`",
        f"- next_stage(다음 단계): `{next_stage_id}`",
        "",
        "Effect(효과): Stage293(293단계)는 trade density(거래 밀도)는 일부 맞췄지만 net profit(순수익), PF(수익 팩터), recovery(회복), expectancy(기대값), curve pocket(곡선 포켓)을 함께 통과한 package(패키지)가 없어 Adapter/ONNX(어댑터/온엑스)를 진행하지 않는다.",
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
            "## Stage294 Thesis(294단계 논제)",
            "",
            "Stage294(294단계)는 Stage293(293단계)의 좁은 repair(수리)가 아니다. 실제 MT5 outcome relabeling(MT5 결과 재라벨), direction flip(방향 반전), cost-aware acceptance(비용 인식 수락), curve smoother(곡선 완화)를 새 decision surface(판단 표면)로 만든다.",
            "",
            f"Claim boundary(주장 경계): `{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def decision_markdown(selected: Mapping[str, Any] | None, status: str, judgment: str, next_stage_id: str) -> str:
    if selected:
        decision = f"{selected['package_id']} passes the candidate package gate(후보 패키지 게이트) and moves to Adapter package(어댑터 패키지) work."
    else:
        decision = "No Stage293 package passes the ONNX-worthy candidate gate(ONNX화 가치 후보 게이트), so Stage294 opens MT5 outcome relabeling and directional flip rebuild(MT5 결과 재라벨/방향 반전 재구성)."
    return f"""# Stage293 Decision(293단계 결정)

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): {decision}
- next_stage(다음 단계): `{next_stage_id}`

Effect(효과): 순수익이 음수인 후보를 ONNX(온엑스)로 밀지 않고, 실제 런타임 손익에서 다시 label/decision surface(라벨/판단 표면)를 만든다.
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
    if selected:
        input_name = "adapter_seed_queue.csv"
        status = "opened_adapter_package_for_stage293_candidate"
        target = selected["package_id"]
    else:
        input_name = "stage294_seed_queue.csv"
        status = "opened_mt5_outcome_relabel_directional_flip_rebuild"
        target = "none"
    base.write_csv(stage_root / "01_inputs" / input_name, base.QUEUE_COLUMNS, queue_rows)
    base.write_md(
        stage_root / "00_spec" / "stage_brief.md",
        f"""# Stage294 Brief(294단계 개요)

- stage_id(단계 ID): `{next_stage_id}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- question(질문): Can MT5 outcome relabeling and directional flip(메타트레이더5 결과 재라벨과 방향 반전) turn dense near-breakeven losers(고밀도 근본전 손실 표면) into an ONNX-worthy candidate(ONNX화 가치 후보)?
- boundary(경계): `{BOUNDARY}`

Effect(효과): Stage293(293단계)의 음수 순수익을 좁게 고치지 않고, 실제 체결 손익을 새 label/decision/risk surface(라벨/판단/위험 표면)로 재구성한다.
""",
    )
    base.write_md(
        stage_root / "01_inputs" / "input_refs.md",
        f"""# Stage294 Input Refs(294단계 입력 참조)

- source_report(원천 보고): `{base.rel(REPORT)}`
- source_scoreboard(원천 점수표): `{base.rel(SCOREBOARD)}`
- source_failure_memory(원천 실패 기억): `{base.rel(FAILURE_MEMORY)}`
- source_queue(원천 대기열): `{base.rel(stage_root / "01_inputs" / input_name)}`

Effect(효과): Stage293(293단계)의 결과를 후보 보존이 아니라 Stage294(294단계)의 새 질문 입력 근거로만 사용한다.
""",
    )
    base.write_md(stage_root / "03_reviews" / "review_index.md", "# Stage294 Review Index(294단계 검토 색인)\n")
    base.write_csv(
        stage_root / "03_reviews" / "stage_run_ledger.csv",
        base.STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage294_opened_from_run293C",
                "stage_id": next_stage_id,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage293_review",
                "status": status,
                "judgment": "opened_from_stage293_runtime_review",
                "evidence_boundary": "planning_from_stage293_evidence",
                "report_path": base.rel(REPORT),
                "notes": f"queue_rows={len(queue_rows)};next_action={next_action}",
            }
        ],
    )
    base.write_md(
        stage_root / "04_selected" / "selection_status.md",
        f"""# Stage294 Selection Status(294단계 선택 상태)

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
    if selected and "IDEA-ST294-ADAPTER-FOR-STAGE293-CANDIDATE" not in idea:
        idea = (
            idea.rstrip()
            + f"\n\n| `IDEA-ST294-ADAPTER-FOR-STAGE293-CANDIDATE` | `{next_stage_id}` | Adapter package(어댑터 패키지) for Stage293 candidate(293단계 후보) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_after_candidate_gate` | 후보 게이트 통과 뒤 Adapter(어댑터)와 parity(동등성)만 진행 |\n"
        )
        base.write_md(IDEA_REGISTER, idea)
    if not selected and "IDEA-ST294-MT5-OUTCOME-RELABEL-DIRECTIONAL-FLIP" not in idea:
        idea = (
            idea.rstrip()
            + f"\n\n| `IDEA-ST294-MT5-OUTCOME-RELABEL-DIRECTIONAL-FLIP` | `{next_stage_id}` | MT5 outcome relabel and directional flip rebuild(MT5 결과 재라벨/방향 반전 재구성) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_no_candidate` | Stage293(293단계)의 near-breakeven dense losers(고밀도 근본전 손실)를 실제 체결 손익 label(라벨)로 재구성 |\n"
        )
        base.write_md(IDEA_REGISTER, idea)

    if not selected:
        negative = base.io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if base.path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
        if "NEG-ST293-PROFIT-SCALE-DENSITY-CALIBRATION" not in negative:
            negative = (
                negative.rstrip()
                + "\n\n| `NEG-ST293-PROFIT-SCALE-DENSITY-CALIBRATION` | `IDEA-ST293-PROFIT-SCALE-DENSITY-CALIBRATION` | profit-scale density calibration(순수익 규모/거래 밀도 보정)이 ONNX-worthy candidate(ONNX화 가치 후보)로 닫히지 않음 | run293C(293C 실행)에서 모든 actual routed total(실제 라우팅 전체)이 검증 또는 표본외 순손실이고 PF(수익 팩터), 회복, 기대값, 곡선 포켓을 함께 통과한 패키지가 없음 | cp293A/cp293F의 근본전 고밀도 손실은 outcome relabel(결과 재라벨)과 direction flip(방향 반전) 입력으로 보존 | MT5 filled trade outcome(체결 거래 결과) 기반 새 label/decision/risk surface(라벨/판단/위험 표면)일 때만 재개 |\n"
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
                "lane": "profit_scale_density_calibration_review",
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
                "record_view": "profit_scale_density_calibration_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "candidate_selection_review",
                "scoreboard_lane": "profit_scale_density_calibration",
                "status": status,
                "judgment": judgment,
                "path": base.rel(REPORT),
                "primary_kpi": f"scoreboard_rows={len(scoreboard_rows)};selected_candidate={selected_text}",
                "guardrail_kpi": "adapter_package=none;onnx_readiness=not_started",
                "external_verification_status": "completed_run293B_mt5_probe",
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
                "view": "profit_scale_density_calibration_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "profit_scale_density_calibration_review_scoreboard",
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
            "artifact_type": "stage293_profit_scale_density_calibration_review_artifact",
            "path": base.rel(path),
            "sha256": base.sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run293C profit-scale density calibration review and Stage294 handoff",
        }
        for path in artifacts
        if base.path_exists(path)
    ]
    base.upsert_csv(ARTIFACT_REGISTRY, base.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    write_next_stage_scaffold(queue_rows, selected, next_stage_id, next_action)

    base.write_md(
        SELECTED,
        f"""# Stage293 Selection Status(293단계 선택 상태)

- stage_status(단계 상태): `{status}`
- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `Stage292`
- selected_candidate(선택 후보): `{selected_text}`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- report(보고): `{base.rel(REPORT)}`
- scoreboard(점수표): `{base.rel(SCOREBOARD)}`
""",
    )
    review_index = base.io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if base.path_exists(REVIEW_INDEX) else "# Stage293 Review Index(293단계 검토 색인)\n"
    review_index = base.append_once(
        review_index,
        "run293C_report",
        f"- run293C_report(293C 보고): `{base.rel(REPORT)}`\n- run293C_scoreboard(293C 점수표): `{base.rel(SCOREBOARD)}`\n- run293C_failure_memory(293C 실패 기억): `{base.rel(FAILURE_MEMORY)}`",
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
        "run293C_summary",
        f"- run293C_summary(293C 요약): Stage293(293단계) MT5 actual routed total(MT5 실제 라우팅 전체)을 검토했다. Effect(효과): selected_candidate(선택 후보)는 `{selected_text}`이고 Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않으며 `{next_stage_id}`를 새 논제로 열었다.",
    )
    base.write_md(CURRENT_STATE, current)

    workspace = base.io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if base.path_exists(WORKSPACE_STATE) else ""
    workspace = base.replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = base.replace_line_prefix(workspace, "active_stage:", f"active_stage: {next_stage_id}")
    workspace = base.replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage293(293단계) run293C(293C 실행) profit-scale density calibration review(순수익 규모/거래 밀도 보정 검토) `{RUN_ID}`. "
        f"Effect(효과): scoreboard(점수표) `{len(scoreboard_rows)}`행과 failure memory(실패 기억) `{len(failure_rows)}`행을 만들고 selected candidate(선택 후보) `{selected_text}`로 `{next_stage_id}`를 열었다.\n"
    )
    workspace = base.prepend_focus(workspace, focus, RUN_ID)
    base.write_md(WORKSPACE_STATE, workspace)

    changelog = base.io_path(CHANGELOG).read_text(encoding="utf-8-sig") if base.path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = base.append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run293C Profit-scale density calibration review(293C 순수익 규모/거래 밀도 보정 검토)\n\n"
        f"- status(상태): `{status}`\n"
        f"- judgment(판정): `{judgment}`\n"
        f"- effect(효과): Stage293(293단계)를 `{selected_text}` 선택 상태로 판정하고 `{next_stage_id}`를 열었다.\n"
        f"- boundary(경계): Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 아직 `not_started/not_claimed`다.\n",
    )
    base.write_md(CHANGELOG, changelog)
    update_registers(selected, next_stage_id)


def main() -> None:
    configure_base()
    base.stage293_queue_rows = stage294_queue_rows
    base.status_pack = status_pack
    base.result_rows = result_rows
    base.report_markdown = report_markdown
    base.decision_markdown = decision_markdown
    base.update_docs = update_docs
    base.main()


if __name__ == "__main__":
    main()
