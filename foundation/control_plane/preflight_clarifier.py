from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any, Mapping


_COUNT_RE = re.compile(r"(?P<count>\d+)\s*(?:개|가지|회|번|runs?|variants?)?", re.IGNORECASE)
_APPROX_TERMS = ("정도", "쯤", "대략", "약 ", "around", "about", "roughly", "~")
_BATCH_TERMS = ("가설", "run", "variant", "변형", "실행", "돌려", "패키지", "일괄", "배치", "batch")
_VERIFICATION_TERMS = (
    "검증",
    "확인",
    "테스트",
    "성능",
    "검사",
    "validation",
    "verify",
    "verification",
    "oos",
    "표본외",
    "mt5",
    "전략 테스터",
    "백테스트",
    "runtime",
    "런타임",
)
_UNATTENDED_TERMS = ("자는 동안", "자고", "overnight", "unattended", "알아서", "크게 돌려")
_MT5_EXCLUSION_TERMS = ("mt5는 하지마", "mt5 하지마", "mt5 제외", "mt5는 제외", "mt5 안", "mt5 없이")
_PYTHON_TERMS = ("python", "파이썬", "structural", "구조")
_ONLY_TERMS = ("만", "only")
_ALL_MT5_TERMS = ("mt5까지", "mt5 전부", "mt5 전체", "mt5 모두", "mt5 validation", "mt5 oos")
_ALL_SCOPE_TERMS = ("전부", "전체", "모두", "all")
_RISK_FLAG_LABELS = {
    "approximate_batch_count": "수량이 대략적임(approximate batch count, 대략 수량)",
    "execution_layer_ambiguous": "무엇을 실행할지 애매함(execution layer ambiguous, 실행 층 애매함)",
    "ambiguous_verification_layer": "검증 범위가 애매함(verification layer ambiguous, 검증 층 애매함)",
    "mt5_possible_but_not_confirmed": "MT5(메타트레이더5) 필요 여부가 확정되지 않음",
    "scope_reduction_not_authorized": "축소 작업(scope reduction, 범위 축소)이 승인되지 않음",
    "unattended_batch_work": "자는 동안 실행 같은 무인 배치(unattended batch, 무인 배치) 위험",
    "context_requires_mt5_confirmation": "현재 문맥상 MT5(메타트레이더5) 확인이 필요할 수 있음",
}


@dataclass(frozen=True)
class ClarificationOption:
    option_id: str
    label: str
    description: str
    effect: str
    scope_delta: Mapping[str, Any] = field(default_factory=dict)
    recommended: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "option_id": self.option_id,
            "label": self.label,
            "description": self.description,
            "effect": self.effect,
            "scope_delta": dict(self.scope_delta),
            "recommended": self.recommended,
        }


@dataclass(frozen=True)
class ClarificationQuestion:
    question_id: str
    prompt: str
    options: tuple[ClarificationOption, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "question_id": self.question_id,
            "prompt": self.prompt,
            "options": [option.to_dict() for option in self.options],
        }


@dataclass(frozen=True)
class PreflightClarificationResult:
    prompt: str
    needs_clarification: bool
    blocked_until_answer: bool
    risk_flags: tuple[str, ...] = ()
    inferred_counts: Mapping[str, int] = field(default_factory=dict)
    questions: tuple[ClarificationQuestion, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "prompt": self.prompt,
            "needs_clarification": self.needs_clarification,
            "blocked_until_answer": self.blocked_until_answer,
            "risk_flags": list(self.risk_flags),
            "inferred_counts": dict(self.inferred_counts),
            "questions": [question.to_dict() for question in self.questions],
        }


def analyze_prompt_for_clarification(
    prompt: str,
    *,
    context: Mapping[str, Any] | None = None,
) -> PreflightClarificationResult:
    context = context or {}
    text = " ".join(prompt.strip().split())
    lowered = text.lower()
    count = _infer_requested_count(lowered)
    inferred_counts = {"requested_variants": count} if count is not None else {}

    has_batch = _contains_any(lowered, _BATCH_TERMS)
    has_verification = _contains_any(lowered, _VERIFICATION_TERMS)
    approximate_count = count is not None and _contains_any(lowered, _APPROX_TERMS)
    unattended = _contains_any(lowered, _UNATTENDED_TERMS)
    explicit_python_only = _is_explicit_python_only(lowered)
    explicit_full_mt5 = _is_explicit_full_mt5(lowered)

    risk_flags: list[str] = []
    if approximate_count:
        risk_flags.append("approximate_batch_count")
    if has_batch and count is not None and not explicit_python_only and not explicit_full_mt5:
        risk_flags.append("execution_layer_ambiguous")
    if has_verification and not explicit_python_only and not explicit_full_mt5:
        risk_flags.append("ambiguous_verification_layer")
        risk_flags.append("mt5_possible_but_not_confirmed")
        risk_flags.append("scope_reduction_not_authorized")
    if unattended:
        risk_flags.append("unattended_batch_work")
    if bool(context.get("requires_mt5")) and not explicit_python_only and not explicit_full_mt5:
        risk_flags.append("context_requires_mt5_confirmation")

    needs_clarification = bool(risk_flags) and not (explicit_python_only or explicit_full_mt5)
    questions = _build_questions(count=count, has_verification=has_verification) if needs_clarification else ()

    return PreflightClarificationResult(
        prompt=prompt,
        needs_clarification=needs_clarification,
        blocked_until_answer=needs_clarification,
        risk_flags=tuple(dict.fromkeys(risk_flags)),
        inferred_counts=inferred_counts,
        questions=questions,
    )


def format_clarification_for_user(result: PreflightClarificationResult) -> str:
    if not result.needs_clarification:
        return (
            "사전 확인(preflight clarification, 사전 확인) 필요 없음. "
            "효과(effect, 효과): 요청 범위가 이미 충분히 고정되어 바로 진행할 수 있습니다."
        )

    lines = [
        "실행 전에 확인이 필요합니다.",
        "효과(effect, 효과): 제가 Python(파이썬)만 돌리고 검증 완료라고 말하거나, 상위 후보만 몰래 줄이는 일을 막습니다.",
    ]
    if result.risk_flags:
        lines.append("감지된 위험(risk flags, 위험 표시): " + ", ".join(_format_risk_flags(result.risk_flags)))

    for question in result.questions:
        lines.append("")
        lines.append(question.prompt)
        for option in question.options:
            suffix = " [추천(recommended, 추천)]" if option.recommended else ""
            lines.append(f"- {option.label}{suffix}: {option.description}")
            lines.append(f"  효과(effect, 효과): {option.effect}")

    lines.append("")
    lines.append("위 선택지 중 하나를 골라주면 그 범위가 work packet(작업 묶음)의 acceptance criteria(완료 조건)로 고정됩니다.")
    return "\n".join(lines)


def _infer_requested_count(lowered_prompt: str) -> int | None:
    for match in _COUNT_RE.finditer(lowered_prompt):
        value = int(match.group("count"))
        if value > 1:
            return value
    return None


def _build_questions(*, count: int | None, has_verification: bool) -> tuple[ClarificationQuestion, ...]:
    display_count = count if count is not None else 1
    full_recommended = has_verification

    scope_question = ClarificationQuestion(
        question_id="execution_and_verification_scope",
        prompt="이 작업의 실행 범위(scope, 범위)를 어떻게 고정할까요?",
        options=(
            ClarificationOption(
                option_id="python_mt5_all",
                label="A. Python(파이썬)+MT5(메타트레이더5) 전체 검증",
                description=(
                    f"{display_count}개 모두 Python structural(파이썬 구조 탐색), "
                    "MT5 validation(메타트레이더5 검증), MT5 OOS(표본외 검증)를 남깁니다."
                ),
                effect="하나라도 빠지면 completed(완료) 금지이고 status(상태)는 partial(부분) 또는 blocked(차단)입니다.",
                scope_delta={
                    "expected_python_structural_count": display_count,
                    "expected_mt5_validation_count": display_count,
                    "expected_mt5_oos_count": display_count,
                    "top_k_reduction_allowed": False,
                },
                recommended=full_recommended,
            ),
            ClarificationOption(
                option_id="python_structural_only",
                label="B. Python(파이썬) 구조 탐색만",
                description=f"{display_count}개 모두 Python structural(파이썬 구조 탐색)까지만 실행합니다.",
                effect="MT5(메타트레이더5) 검증 완료 주장은 금지되고, 보고도 Python-only(파이썬 한정)로만 씁니다.",
                scope_delta={
                    "expected_python_structural_count": display_count,
                    "expected_mt5_validation_count": 0,
                    "expected_mt5_oos_count": 0,
                    "mt5_claims_forbidden": True,
                },
                recommended=not full_recommended,
            ),
            ClarificationOption(
                option_id="python_all_mt5_top_k",
                label="C. Python(파이썬) 전체 + MT5(메타트레이더5) 상위 후보만",
                description=(
                    f"{display_count}개 Python structural(파이썬 구조 탐색) 후 "
                    "선정된 top-K(상위 후보)만 MT5(메타트레이더5)로 확인합니다."
                ),
                effect=(
                    "사용자가 고른 축소 범위로 기록되어야 하며, final claim(최종 주장)은 "
                    "completed_reduced_scope(축소 범위 완료)만 허용됩니다."
                ),
                scope_delta={
                    "expected_python_structural_count": display_count,
                    "expected_mt5_validation_count": "selected_top_k",
                    "expected_mt5_oos_count": "selected_top_k",
                    "requires_user_scope_reduction_quote": True,
                },
            ),
        ),
    )

    questions = [scope_question]
    if count is not None:
        questions.append(
            ClarificationQuestion(
                question_id="batch_count_lock",
                prompt=f"{count}개라는 수량(count, 수량)을 어떻게 해석할까요?",
                options=(
                    ClarificationOption(
                        option_id="exact_count",
                        label=f"A. 정확히 {count}개 고정",
                        description=f"{count}개보다 적으면 완료로 말하지 않습니다.",
                        effect="실제 산출물이 부족하면 scope gate(범위 게이트)가 막습니다.",
                        scope_delta={"requested_variants_exact": count},
                        recommended=True,
                    ),
                    ClarificationOption(
                        option_id="around_count_requires_plan",
                        label=f"B. {count}개 전후 허용",
                        description="먼저 실제 실행 수량을 제안하고, 사용자가 승인한 뒤 실행합니다.",
                        effect="승인 없는 자동 축소가 금지됩니다.",
                        scope_delta={"requested_variants_approximate": count, "requires_count_approval": True},
                    ),
                    ClarificationOption(
                        option_id="time_boxed",
                        label="C. 시간 기준으로 가능한 만큼",
                        description="정해진 시간 안에서 가능한 수량만 실행합니다.",
                        effect="처음부터 partial(부분) 또는 timeboxed(시간 제한) 결과로만 보고합니다.",
                        scope_delta={"timeboxed": True, "completion_claims_forbidden": True},
                    ),
                ),
            )
        )

    return tuple(questions)


def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(needle in text for needle in needles)


def _format_risk_flags(risk_flags: tuple[str, ...]) -> list[str]:
    return [_RISK_FLAG_LABELS.get(flag, flag) for flag in risk_flags]


def _is_explicit_python_only(text: str) -> bool:
    return _contains_any(text, _PYTHON_TERMS) and _contains_any(text, _ONLY_TERMS) and _contains_any(text, _MT5_EXCLUSION_TERMS)


def _is_explicit_full_mt5(text: str) -> bool:
    return _contains_any(text, _ALL_MT5_TERMS) and _contains_any(text, _ALL_SCOPE_TERMS)
