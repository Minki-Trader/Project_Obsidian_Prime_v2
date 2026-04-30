from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class DatasetSpec:
    dataset_id: str
    feature_set_id: str
    path: Path
    feature_order_path: Path | None = None
    feature_order_hash: str | None = None
    label_id: str | None = None
    split_id: str | None = None


@dataclass(frozen=True)
class ThresholdPolicySpec:
    policy_id: str
    method: str
    selection_scope: str
    params: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModelFamilySpec:
    model_family: str
    training_method: str
    params: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Mt5RuntimeSpec:
    common_run_root: str
    ea_source_path: Path = Path("foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5")
    ea_expert_path: str = "Project_Obsidian_Prime_v2\\foundation\\mt5\\ObsidianPrimeV2_RuntimeProbeEA.ex5"
    tester_set_name: str = "ObsidianPrimeV2_RuntimeProbeEA.set"
    max_hold_bars: int = 12
    route_mode: str | None = None


@dataclass(frozen=True)
class AlphaRunSpec:
    stage_id: str
    stage_number: int
    run_number: str
    run_id: str
    exploration_label: str
    model: ModelFamilySpec
    primary_dataset: DatasetSpec
    threshold_policy: ThresholdPolicySpec
    output_root: Path
    mt5: Mt5RuntimeSpec | None = None
    fallback_dataset: DatasetSpec | None = None
    source_run_id: str | None = None
    parent_run_id: str | None = None
    tags: Sequence[str] = ()


STAGE10_ID = "10_alpha_scout__default_split_model_threshold_scan"
STAGE11_ID = "11_alpha_robustness__wfo_label_horizon_sensitivity"
STAGE12_ID = "12_model_family_challenge__extratrees_training_effect"

DEFAULT_FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"


def default_common_run_root(stage_number: int | str, run_id: str) -> str:
    stage_text = str(stage_number).strip()
    if stage_text.lower().startswith("stage"):
        stage_label = stage_text.lower()
    else:
        stage_label = f"stage{int(stage_text):02d}"
    return f"Project_Obsidian_Prime_v2/{stage_label}/{run_id}"


def stage_number_from_id(stage_id: str) -> int:
    prefix = str(stage_id).split("_", 1)[0]
    return int(prefix)


def run_output_root(stage_id: str, run_id: str) -> Path:
    return Path("stages") / stage_id / "02_runs" / run_id


def stage_review_ledger_path(stage_id: str) -> Path:
    return Path("stages") / stage_id / "03_reviews" / "stage_run_ledger.csv"

