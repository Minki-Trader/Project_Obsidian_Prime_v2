from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from foundation.control_plane.ledger import io_path


DEFAULT_GROK_EXECUTABLE = os.environ.get("GROK_EXECUTABLE", r"C:\Users\awdse\.grok\bin\grok.exe")
REVIEW_SIZE_LIMITS = {
    "small": 4_000,
    "medium": 12_000,
    "large": 24_000,
}
KNOWN_NOISE_MARKERS = (
    "mcp server",
    "disallowedtools entry matched nothing",
    "git repo discovery failed",
    "plugin warning",
    "global config",
)
TOP_LEVEL_ARTIFACT_DENYLIST = frozenset({"mcps"})
SNAPSHOT_ONLY_RULE = (
    "You are an external second-opinion reviewer for a bounded evidence snapshot. "
    "Answer only from the prompt. Do not inspect files, run tools, browse, spawn "
    "subagents, or perform local verification. If evidence is insufficient, say "
    "needs_local_verification."
)


@dataclass(frozen=True)
class GrokReviewResult:
    review_size: str
    prompt_hash: str
    command: tuple[str, ...]
    returncode: int | None
    timed_out: bool
    duration_seconds: float
    clean_stdout: str
    raw_stdout: str
    raw_stderr: str
    stripped_noise_lines: tuple[str, ...] = ()
    preflight_warnings: tuple[str, ...] = ()
    unexpected_top_level_artifacts: tuple[str, ...] = ()
    packet_paths: dict[str, str] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        return not self.timed_out and self.returncode == 0 and bool(self.clean_stdout.strip())

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_size": self.review_size,
            "prompt_hash": self.prompt_hash,
            "command": list(self.command),
            "returncode": self.returncode,
            "timed_out": self.timed_out,
            "success": self.success,
            "duration_seconds": self.duration_seconds,
            "clean_stdout": self.clean_stdout,
            "raw_stdout": self.raw_stdout,
            "raw_stderr": self.raw_stderr,
            "stripped_noise_lines": list(self.stripped_noise_lines),
            "preflight_warnings": list(self.preflight_warnings),
            "unexpected_top_level_artifacts": list(self.unexpected_top_level_artifacts),
            "packet_paths": dict(self.packet_paths),
        }

    def to_summary_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "review_size": self.review_size,
            "prompt_hash": self.prompt_hash,
            "command": list(_redact_prompt_payload(self.command)),
            "returncode": self.returncode,
            "timed_out": self.timed_out,
            "success": self.success,
            "duration_seconds": self.duration_seconds,
            "stripped_noise_line_count": len(self.stripped_noise_lines),
            "preflight_warnings": list(self.preflight_warnings),
            "unexpected_top_level_artifacts": list(self.unexpected_top_level_artifacts),
            "packet_paths": dict(self.packet_paths),
        }
        if not self.packet_paths:
            payload["clean_stdout"] = self.clean_stdout
        return payload


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def run_grok_review(
    prompt: str,
    *,
    executable: str | Path = DEFAULT_GROK_EXECUTABLE,
    cwd: str | Path | None = None,
    timeout_seconds: float = 300,
    review_size: str = "small",
    extra_args: Sequence[str] = (),
    output_dir: str | Path | None = None,
    repo_root: str | Path | None = None,
    prompt_file_path: str | Path | None = None,
) -> GrokReviewResult:
    normalized_size = _normalize_review_size(review_size)
    warnings = tuple(_preflight_warnings(prompt, normalized_size))
    if not prompt.strip():
        raise ValueError("prompt must not be empty")

    cwd_path = Path(cwd) if cwd is not None else None
    repo_root_path = Path(repo_root) if repo_root is not None else None
    before_top_level = _top_level_snapshot(repo_root_path)
    command_args = [*list(extra_args), *snapshot_only_args()]
    if prompt_file_path is not None:
        command = tuple([str(executable), *command_args, "--prompt-file", str(prompt_file_path)])
    else:
        command = tuple([str(executable), *command_args, "-p", prompt])

    started = time.monotonic()
    raw_stdout = ""
    raw_stderr = ""
    returncode: int | None = None
    timed_out = False

    try:
        completed = subprocess.run(
            list(command),
            cwd=str(cwd_path) if cwd_path else None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
        raw_stdout = completed.stdout or ""
        raw_stderr = completed.stderr or ""
        returncode = completed.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        raw_stdout = _coerce_timeout_payload(exc.stdout)
        raw_stderr = _coerce_timeout_payload(exc.stderr)

    duration = time.monotonic() - started
    clean_stdout, stripped = strip_known_noise(raw_stdout)
    unexpected_artifacts = tuple(sorted(_top_level_snapshot(repo_root_path) - before_top_level))
    unexpected_artifacts = tuple(name for name in unexpected_artifacts if name.lower() in TOP_LEVEL_ARTIFACT_DENYLIST)

    result = GrokReviewResult(
        review_size=normalized_size,
        prompt_hash=prompt_hash(prompt),
        command=command,
        returncode=returncode,
        timed_out=timed_out,
        duration_seconds=round(duration, 6),
        clean_stdout=clean_stdout,
        raw_stdout=raw_stdout,
        raw_stderr=raw_stderr,
        stripped_noise_lines=tuple(stripped),
        preflight_warnings=warnings,
        unexpected_top_level_artifacts=unexpected_artifacts,
    )
    if output_dir is not None:
        result = _with_packet_record(result, prompt=prompt, output_dir=Path(output_dir))
    return result


def strip_known_noise(text: str) -> tuple[str, list[str]]:
    clean_lines: list[str] = []
    stripped: list[str] = []
    for line in text.splitlines():
        normalized = line.strip().lower()
        if normalized and any(marker in normalized for marker in KNOWN_NOISE_MARKERS):
            stripped.append(line)
            continue
        clean_lines.append(line)
    return "\n".join(clean_lines).strip(), stripped


def _redact_prompt_payload(command: Sequence[str]) -> tuple[str, ...]:
    redacted: list[str] = []
    skip_next = False
    for arg in command:
        if skip_next:
            redacted.append("<prompt-redacted>")
            skip_next = False
            continue
        redacted.append(arg)
        if arg in {"-p", "--prompt"}:
            skip_next = True
    return tuple(redacted)


def snapshot_only_args() -> tuple[str, ...]:
    return (
        "--rules",
        SNAPSHOT_ONLY_RULE,
        "--no-plan",
        "--no-subagents",
        "--disable-web-search",
    )


def _normalize_review_size(value: str) -> str:
    normalized = str(value).strip().lower()
    if normalized not in REVIEW_SIZE_LIMITS:
        raise ValueError(f"review_size must be one of {sorted(REVIEW_SIZE_LIMITS)}")
    return normalized


def _preflight_warnings(prompt: str, review_size: str) -> list[str]:
    warnings: list[str] = []
    limit = REVIEW_SIZE_LIMITS[review_size]
    if len(prompt) > limit:
        warnings.append(f"prompt_length_exceeds_{review_size}_limit")
    if "\x00" in prompt:
        warnings.append("prompt_contains_nul")
    return warnings


def _coerce_timeout_payload(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _top_level_snapshot(repo_root: Path | None) -> set[str]:
    if repo_root is None:
        return set()
    root = Path(repo_root)
    if not root.exists():
        return set()
    return {path.name for path in root.iterdir()}


def _with_packet_record(result: GrokReviewResult, *, prompt: str, output_dir: Path) -> GrokReviewResult:
    io_path(output_dir).mkdir(parents=True, exist_ok=True)
    prompt_path = output_dir / "prompt.md"
    clean_output_path = output_dir / "clean_output.md"
    raw_diagnostics_path = output_dir / "raw_diagnostics.json"
    metadata_path = output_dir / "metadata.json"

    io_path(prompt_path).write_text(prompt.rstrip("\n") + "\n", encoding="utf-8-sig")
    io_path(clean_output_path).write_text(result.clean_stdout.rstrip("\n") + "\n", encoding="utf-8-sig")
    raw_diagnostics = {
        "raw_stdout": result.raw_stdout,
        "raw_stderr": result.raw_stderr,
        "stripped_noise_lines": list(result.stripped_noise_lines),
    }
    io_path(raw_diagnostics_path).write_text(json.dumps(raw_diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    metadata = result.to_dict()
    metadata.pop("clean_stdout", None)
    metadata.pop("raw_stdout", None)
    metadata.pop("raw_stderr", None)
    metadata["packet_paths"] = {
        "prompt": prompt_path.as_posix(),
        "clean_output": clean_output_path.as_posix(),
        "raw_diagnostics": raw_diagnostics_path.as_posix(),
        "metadata": metadata_path.as_posix(),
    }
    io_path(metadata_path).write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return GrokReviewResult(
        review_size=result.review_size,
        prompt_hash=result.prompt_hash,
        command=result.command,
        returncode=result.returncode,
        timed_out=result.timed_out,
        duration_seconds=result.duration_seconds,
        clean_stdout=result.clean_stdout,
        raw_stdout=result.raw_stdout,
        raw_stderr=result.raw_stderr,
        stripped_noise_lines=result.stripped_noise_lines,
        preflight_warnings=result.preflight_warnings,
        unexpected_top_level_artifacts=result.unexpected_top_level_artifacts,
        packet_paths=metadata["packet_paths"],
    )


def _read_prompt(args: argparse.Namespace) -> str:
    if args.prompt and args.prompt_file:
        raise ValueError("use either --prompt or --prompt-file, not both")
    if args.prompt_file:
        return io_path(Path(args.prompt_file)).read_text(encoding="utf-8-sig")
    if args.prompt:
        return args.prompt
    return sys.stdin.read()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a bounded Grok review and capture transport diagnostics.")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--executable", default=DEFAULT_GROK_EXECUTABLE)
    parser.add_argument("--cwd")
    parser.add_argument("--timeout-seconds", type=float, default=300)
    parser.add_argument("--review-size", choices=tuple(REVIEW_SIZE_LIMITS), default="small")
    parser.add_argument("--output-dir")
    parser.add_argument("--repo-root")
    parser.add_argument("--extra-arg", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--full-json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        prompt = _read_prompt(args)
        result = run_grok_review(
            prompt,
            executable=args.executable,
            cwd=args.cwd,
            timeout_seconds=args.timeout_seconds,
            review_size=args.review_size,
            extra_args=args.extra_arg,
            output_dir=args.output_dir,
            repo_root=args.repo_root,
            prompt_file_path=args.prompt_file,
        )
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

    if args.full_json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    elif args.json:
        print(json.dumps(result.to_summary_dict(), ensure_ascii=False, indent=2))
    else:
        print(result.clean_stdout)
        if result.preflight_warnings:
            print(json.dumps({"preflight_warnings": list(result.preflight_warnings)}, ensure_ascii=False), file=sys.stderr)
        if result.unexpected_top_level_artifacts:
            print(
                json.dumps({"unexpected_top_level_artifacts": list(result.unexpected_top_level_artifacts)}, ensure_ascii=False),
                file=sys.stderr,
            )
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
