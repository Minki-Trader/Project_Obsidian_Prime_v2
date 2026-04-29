from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from foundation.control_plane.prompt_intake_classifier import PromptClassification
from foundation.control_plane.risk_vector_scan import RiskVectorScan


@dataclass(frozen=True)
class DecisionQuestion:
    question_id: str
    prompt: str
    options: tuple[Mapping[str, str], ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "question_id": self.question_id,
            "prompt": self.prompt,
            "options": [dict(option) for option in self.options],
        }


@dataclass(frozen=True)
class DecisionLock:
    mode: str
    assumptions: Mapping[str, object] = field(default_factory=dict)
    questions: tuple[DecisionQuestion, ...] = ()
    required_user_decisions: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "mode": self.mode,
            "assumptions": dict(self.assumptions),
            "questions": [question.to_dict() for question in self.questions],
            "required_user_decisions": list(self.required_user_decisions),
        }


def build_decision_lock(classification: PromptClassification, risk_scan: RiskVectorScan) -> DecisionLock:
    if classification.primary_family == "information_only" and not classification.mutation_intent and not classification.execution_intent:
        return DecisionLock(
            mode="assume_safe_default",
            assumptions={
                "file_edit_allowed": False,
                "execution_allowed": False,
                "ledger_write_allowed": False,
                "new_claim_allowed": False,
                "report_only": True,
            },
        )

    decision_ids = tuple(risk_scan.required_decision_locks)
    if risk_scan.hard_stop_risks or decision_ids:
        return DecisionLock(
            mode="ask_user",
            questions=_questions_for(decision_ids or ("edit_policy",)),
            required_user_decisions=decision_ids or ("edit_policy",),
        )

    return DecisionLock(
        mode="assume_safe_default",
        assumptions={
            "file_edit_allowed": classification.mutation_intent,
            "execution_allowed": classification.execution_intent,
            "ledger_write_allowed": "kpi_evidence" in classification.detected_families,
            "new_claim_allowed": False,
            "report_only": not classification.mutation_intent and not classification.execution_intent,
        },
    )


def _questions_for(decision_ids: tuple[str, ...]) -> tuple[DecisionQuestion, ...]:
    questions: list[DecisionQuestion] = []
    if "edit_policy" in decision_ids:
        questions.append(
            DecisionQuestion(
                question_id="edit_policy",
                prompt="파일을 실제로 수정할지 고정해야 합니다.",
                options=(
                    {
                        "option_id": "report_only",
                        "label": "Report only",
                        "effect": "No file edits; current_truth_synced/completed claims are forbidden.",
                    },
                    {
                        "option_id": "edit_with_gates",
                        "label": "Edit with gates",
                        "effect": "File edits allowed only with required audits and final claim guard.",
                    },
                ),
            )
        )
    if "canonical_current_truth" in decision_ids:
        questions.append(
            DecisionQuestion(
                question_id="canonical_current_truth",
                prompt="충돌한 현재 진실의 기준값을 고정해야 합니다.",
                options=(
                    {
                        "option_id": "use_workspace_state",
                        "label": "Use workspace_state",
                        "effect": "workspace_state.yaml becomes the canonical current truth source.",
                    },
                    {
                        "option_id": "block_for_review",
                        "label": "Block for review",
                        "effect": "No sync or completion claim until a human picks the canonical state.",
                    },
                ),
            )
        )
    if "destructive_change_permission" in decision_ids:
        questions.append(
            DecisionQuestion(
                question_id="destructive_change_permission",
                prompt="삭제/보관/덮어쓰기 권한을 명시해야 합니다.",
                options=(
                    {
                        "option_id": "forbid_destructive",
                        "label": "Forbid destructive",
                        "effect": "No delete/archive/reset actions are allowed.",
                    },
                    {
                        "option_id": "allow_with_manifest",
                        "label": "Allow with manifest",
                        "effect": "Destructive work requires a manifest and explicit user quote.",
                    },
                ),
            )
        )
    if "execution_scope" in decision_ids:
        questions.append(
            DecisionQuestion(
                question_id="execution_scope",
                prompt="실행 범위와 완료 조건을 고정해야 합니다.",
                options=(
                    {
                        "option_id": "full_scope",
                        "label": "Full scope",
                        "effect": "All requested units must complete or the task is partial/blocked.",
                    },
                    {
                        "option_id": "approved_reduced_scope",
                        "label": "Reduced scope",
                        "effect": "Reduced completion is allowed only with a user quote.",
                    },
                ),
            )
        )
    return tuple(questions)
