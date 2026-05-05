"""Reusable adapter contracts for runtime-facing exploration artifacts."""

from foundation.adapters.contracts import (
    ADAPTER_ROLE_NAMES,
    AdapterCandidateContract,
    AdapterInputContract,
    AdapterOutputContract,
    SignalCard,
    feature_order_hash,
    normalize_roles,
)
from foundation.adapters.onnx_signal_adapter import OnnxSignalAdapter, summarize_signal_cards
from foundation.adapters.score_table_signal_adapter import ScoreTableSignalAdapter

__all__ = [
    "ADAPTER_ROLE_NAMES",
    "AdapterCandidateContract",
    "AdapterInputContract",
    "AdapterOutputContract",
    "OnnxSignalAdapter",
    "ScoreTableSignalAdapter",
    "SignalCard",
    "feature_order_hash",
    "normalize_roles",
    "summarize_signal_cards",
]
