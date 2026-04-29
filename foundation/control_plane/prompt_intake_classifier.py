from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


INFORMATION_TERMS = (
    "설명",
    "파악",
    "평가",
    "검토",
    "어때",
    "왜",
    "보고",
    "확인",
    "explain",
    "review",
    "inspect",
)
STATE_SYNC_TERMS = ("상태", "싱크", "동기화", "current truth", "selection_status", "stage_brief", "sync")
POLICY_TERMS = ("agents.md", "policy", "정책", "스킬", "skill", "운영 시스템", "control plane", "agent_control")
CODE_TERMS = ("코드", "python", "mql5", "테스트", "test", "구현", "수정", "고쳐", "추가")
REFACTOR_TERMS = ("리팩터", "refactor", "모듈", "분산", "비대증", "구조", "pipeline", "owner module")
EXPERIMENT_TERMS = ("가설", "variant", "run", "실험", "모델", "학습", "threshold", "scout")
RUNTIME_TERMS = ("mt5", "strategy tester", "백테스트", "ea", "onnx", "런타임", "runtime", "테스터")
KPI_TERMS = ("kpi", "지표", "장부", "ledger", "normalized", "row grain", "source authority")
ARTIFACT_TERMS = ("산출물", "artifact", "hash", "manifest", "계보", "lineage")
CLEANUP_TERMS = ("삭제", "아카이브", "archive", "cleanup", "보관", "이동")
PUBLISH_TERMS = ("push", "푸시", "commit", "커밋", "github", "깃허브", "merge", "pr", "handoff", "인계")
MUTATION_TERMS = (
    "수정",
    "고쳐",
    "추가",
    "구현",
    "통일",
    "맞춰",
    "바꿔",
    "넣어",
    "채워",
    "보강",
    "넣어",
    "동기화",
    "싱크",
    "반영",
    "정리",
    "삭제",
    "아카이브",
    "push",
    "commit",
)
EXECUTION_TERMS = ("실행", "돌려", "run", "mt5", "백테스트", "test", "테스트", "push", "푸시")
CLAIM_TERMS = ("완료", "검증", "reviewed", "verified", "completed", "승격", "promotion", "runtime_authority")


@dataclass(frozen=True)
class PromptClassification:
    prompt: str
    primary_family: str
    detected_families: tuple[str, ...]
    secondary_families: tuple[str, ...]
    touched_surfaces: tuple[str, ...]
    mutation_intent: bool
    execution_intent: bool
    requested_claims: tuple[str, ...]
    confidence: str
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "prompt": self.prompt,
            "primary_family": self.primary_family,
            "detected_families": list(self.detected_families),
            "secondary_families": list(self.secondary_families),
            "touched_surfaces": list(self.touched_surfaces),
            "mutation_intent": self.mutation_intent,
            "execution_intent": self.execution_intent,
            "requested_claims": list(self.requested_claims),
            "confidence": self.confidence,
            "reasons": list(self.reasons),
        }


def classify_prompt(prompt: str, *, context: Mapping[str, object] | None = None) -> PromptClassification:
    context = context or {}
    text = " ".join(prompt.strip().split())
    lowered = text.lower()
    families: list[str] = []
    surfaces: list[str] = []
    reasons: list[str] = []

    def add_family(family: str, reason: str) -> None:
        if family not in families:
            families.append(family)
        reasons.append(reason)

    if _contains_any(lowered, STATE_SYNC_TERMS):
        add_family("state_sync", "prompt_mentions_current_state_or_sync")
        _add(surfaces, "docs_current_truth")
    if _contains_any(lowered, POLICY_TERMS):
        add_family("policy_skill_governance", "prompt_mentions_policy_skill_or_control_plane")
        _add(surfaces, "policies_and_skills")
    if _contains_any(lowered, REFACTOR_TERMS):
        add_family("code_refactor", "prompt_mentions_refactor_or_module_structure")
        _add(surfaces, "foundation_code")
        _add(surfaces, "pipelines")
    elif _contains_any(lowered, CODE_TERMS):
        add_family("code_edit", "prompt_mentions_code_or_tests")
        _add(surfaces, "foundation_code")
    if _contains_any(lowered, RUNTIME_TERMS):
        add_family("runtime_backtest", "prompt_mentions_mt5_runtime_or_backtest")
        _add(surfaces, "mt5_runtime")
        _add(surfaces, "run_artifacts")
    if _contains_any(lowered, KPI_TERMS):
        add_family("kpi_evidence", "prompt_mentions_kpi_or_ledger")
        _add(surfaces, "kpi_ledgers")
    if _contains_any(lowered, ARTIFACT_TERMS):
        add_family("artifact_lineage", "prompt_mentions_artifacts_or_hashes")
        _add(surfaces, "run_artifacts")
    if _contains_any(lowered, CLEANUP_TERMS):
        add_family("cleanup_archive", "prompt_mentions_cleanup_archive_or_delete")
        _add(surfaces, "run_artifacts")
    if _contains_any(lowered, PUBLISH_TERMS):
        add_family("publish_handoff", "prompt_mentions_publish_git_or_handoff")
    if _contains_any(lowered, EXPERIMENT_TERMS) and "runtime_backtest" not in families:
        add_family("experiment_execution", "prompt_mentions_experiment_run_or_model")
        _add(surfaces, "run_artifacts")

    mutation_intent = _contains_any(lowered, MUTATION_TERMS)
    execution_intent = _contains_any(lowered, EXECUTION_TERMS)
    requested_claims = _requested_claims(lowered)

    if not families:
        add_family("information_only", "no_mutation_or_execution_family_detected")
    elif _contains_any(lowered, INFORMATION_TERMS) and not mutation_intent and not execution_intent:
        add_family("information_only", "prompt_asks_for_explanation_or_review_only")

    priority = (
        "publish_handoff",
        "state_sync",
        "policy_skill_governance",
        "code_refactor",
        "code_edit",
        "runtime_backtest",
        "kpi_evidence",
        "cleanup_archive",
        "experiment_execution",
        "experiment_design",
        "artifact_lineage",
        "information_only",
    )
    primary = next((family for family in priority if family in families), families[0])
    confidence = "high" if len(families) <= 2 else "medium"

    if primary == "information_only" and not surfaces:
        _add(surfaces, "docs_current_truth")
    if bool(context.get("touches_agent_control")):
        _add(surfaces, "policies_and_skills")

    detected = tuple(_unique(families))
    return PromptClassification(
        prompt=prompt,
        primary_family=primary,
        detected_families=detected,
        secondary_families=tuple(family for family in detected if family != primary),
        touched_surfaces=tuple(_unique(surfaces)),
        mutation_intent=mutation_intent,
        execution_intent=execution_intent,
        requested_claims=requested_claims,
        confidence=confidence,
        reasons=tuple(_unique(reasons)),
    )


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term.lower() in text for term in terms)


def _requested_claims(text: str) -> tuple[str, ...]:
    claims: list[str] = []
    if _contains_any(text, ("완료", "completed", "complete")):
        claims.append("completed")
    if _contains_any(text, ("검증", "verified", "verification")):
        claims.append("verified")
    if _contains_any(text, ("reviewed", "검토")):
        claims.append("reviewed")
    if _contains_any(text, ("runtime_authority", "런타임 권위")):
        claims.append("runtime_authority")
    return tuple(_unique(claims))


def _add(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def _unique(values: list[str] | tuple[str, ...]) -> list[str]:
    return list(dict.fromkeys(values))
