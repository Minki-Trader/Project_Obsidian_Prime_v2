from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from foundation.control_plane.ledger import io_path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(io_path(path).read_bytes()).hexdigest()


@dataclass(frozen=True)
class TesterMaterializationConfig:
    expert: str = "Project_Obsidian_Prime_v2\\foundation\\mt5\\ObsidianPrimeV2_RuntimeProbeEA.ex5"
    symbol: str = "US100"
    period: str = "M5"
    model: int = 4
    deposit: float = 500.0
    leverage: str = "1:100"
    optimization: int = 0
    execution_mode: int = 0
    forward_mode: int = 0
    use_local: int = 1
    use_remote: int = 0
    use_cloud: int = 0
    replace_report: int = 1
    shutdown_terminal: int = 0
    from_date: str | None = None
    to_date: str | None = None
    report: str | None = None


def format_mt5_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def materialize_tester_set_file(
    parameters: Mapping[str, Any],
    output_path: Path,
    *,
    generated_by: str = "foundation.mt5.tester_files",
) -> dict[str, Any]:
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    lines = [f"; generated_by={generated_by}"]
    for key, value in parameters.items():
        lines.append(f"{key}={format_mt5_value(value)}")
    io_path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "format": "mt5_set",
        "parameter_count": int(len(parameters)),
    }


def materialize_tester_ini_file(
    config: TesterMaterializationConfig,
    output_path: Path,
    *,
    set_file_path: Path | None = None,
) -> dict[str, Any]:
    tester_values: dict[str, Any] = {
        "Expert": config.expert,
        "Symbol": config.symbol,
        "Period": config.period,
        "Model": config.model,
        "Deposit": config.deposit,
        "Leverage": config.leverage,
        "Optimization": config.optimization,
        "ExecutionMode": config.execution_mode,
        "ForwardMode": config.forward_mode,
        "UseLocal": config.use_local,
        "UseRemote": config.use_remote,
        "UseCloud": config.use_cloud,
        "ReplaceReport": config.replace_report,
        "ShutdownTerminal": config.shutdown_terminal,
    }
    if config.from_date is not None:
        tester_values["FromDate"] = config.from_date
    if config.to_date is not None:
        tester_values["ToDate"] = config.to_date
    if config.report is not None:
        tester_values["Report"] = config.report
    if set_file_path is not None:
        tester_values["ExpertParameters"] = set_file_path.as_posix()

    lines = ["[Tester]"]
    for key, value in tester_values.items():
        lines.append(f"{key}={format_mt5_value(value)}")
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    io_path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "format": "mt5_tester_ini",
        "tester": tester_values,
    }
