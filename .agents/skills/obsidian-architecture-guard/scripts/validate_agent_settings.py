from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


UTF8_BOM = b"\xef\xbb\xbf"
HANGUL_RE = re.compile(r"[\uac00-\ud7a3]")
SUSPICIOUS_CJK_RE = re.compile(r"[\u4e00-\u9fff\uf900-\ufaff]")
MOJIBAKE_RE = re.compile(
    r"(?:\?ㅽ|\?묒|\?섎|\?댁|\?⑦|"
    r"\u91ce|\u4e80|\uc3ed|\u904a|\ub179|\ubb7c|\u907a|\ub2f8|\ub2e9)"
)
REQUIRED_PATHS = [
    "AGENTS.md",
    "docs/policies/architecture_invariants.md",
    "docs/policies/exploration_mandate.md",
    "docs/policies/kpi_measurement_standard.md",
    "docs/policies/run_result_management.md",
    "docs/policies/result_judgment_policy.md",
    "docs/registers/architecture_debt_register.md",
    "docs/registers/run_registry.csv",
    "docs/registers/idea_registry.md",
    "docs/registers/negative_result_register.md",
    "docs/registers/legacy_lesson_register.md",
    "docs/templates/run_manifest_template.json",
    "docs/templates/kpi_record_template.json",
    "docs/templates/result_summary_template.md",
    "docs/policies/agent_trigger_policy.md",
    "docs/policies/reentry_order.md",
    ".agents/skills/obsidian-architecture-guard/SKILL.md",
    ".agents/skills/obsidian-architecture-guard/agents/openai.yaml",
    ".agents/skills/obsidian-session-intake/SKILL.md",
    ".agents/skills/obsidian-session-intake/agents/openai.yaml",
    ".agents/skills/obsidian-reentry-read/SKILL.md",
    ".agents/skills/obsidian-reentry-read/agents/openai.yaml",
    ".agents/skills/obsidian-claim-discipline/SKILL.md",
    ".agents/skills/obsidian-claim-discipline/agents/openai.yaml",
    ".agents/skills/obsidian-stage-transition/SKILL.md",
    ".agents/skills/obsidian-stage-transition/agents/openai.yaml",
    ".agents/skills/obsidian-answer-clarity/SKILL.md",
    ".agents/skills/obsidian-answer-clarity/agents/openai.yaml",
    ".agents/skills/obsidian-code-quality/SKILL.md",
    ".agents/skills/obsidian-code-quality/agents/openai.yaml",
    ".agents/skills/obsidian-lane-classifier/SKILL.md",
    ".agents/skills/obsidian-lane-classifier/agents/openai.yaml",
    ".agents/skills/obsidian-exploration-mandate/SKILL.md",
    ".agents/skills/obsidian-exploration-mandate/agents/openai.yaml",
    ".agents/skills/obsidian-work-packet-router/SKILL.md",
    ".agents/skills/obsidian-work-packet-router/agents/openai.yaml",
    ".agents/skills/obsidian-experiment-design/SKILL.md",
    ".agents/skills/obsidian-experiment-design/agents/openai.yaml",
    ".agents/skills/obsidian-data-integrity/SKILL.md",
    ".agents/skills/obsidian-data-integrity/agents/openai.yaml",
    ".agents/skills/obsidian-model-validation/SKILL.md",
    ".agents/skills/obsidian-model-validation/agents/openai.yaml",
    ".agents/skills/obsidian-runtime-parity/SKILL.md",
    ".agents/skills/obsidian-runtime-parity/agents/openai.yaml",
    ".agents/skills/obsidian-backtest-forensics/SKILL.md",
    ".agents/skills/obsidian-backtest-forensics/agents/openai.yaml",
    ".agents/skills/obsidian-performance-attribution/SKILL.md",
    ".agents/skills/obsidian-performance-attribution/agents/openai.yaml",
    ".agents/skills/obsidian-environment-reproducibility/SKILL.md",
    ".agents/skills/obsidian-environment-reproducibility/agents/openai.yaml",
    ".agents/skills/obsidian-artifact-lineage/SKILL.md",
    ".agents/skills/obsidian-artifact-lineage/agents/openai.yaml",
    ".agents/skills/obsidian-result-judgment/SKILL.md",
    ".agents/skills/obsidian-result-judgment/agents/openai.yaml",
    ".agents/skills/obsidian-code-surface-guard/SKILL.md",
    ".agents/skills/obsidian-code-surface-guard/agents/openai.yaml",
    ".agents/skills/obsidian-workflow-drift-guard/SKILL.md",
    ".agents/skills/obsidian-workflow-drift-guard/agents/openai.yaml",
    ".agents/skills/obsidian-reference-scout/SKILL.md",
    ".agents/skills/obsidian-reference-scout/agents/openai.yaml",
    ".agents/skills/obsidian-run-evidence-system/SKILL.md",
    ".agents/skills/obsidian-run-evidence-system/agents/openai.yaml",
]
REQUIRED_AGENT_INTERFACE_KEYS = ("display_name", "short_description", "default_prompt")
AGENT_PROMPT_REQUIRED_CONCEPTS = {
    ".agents/skills/obsidian-session-intake/agents/openai.yaml": (
        "current truth",
        "cold",
        "warm",
        "work packet lifecycle",
        "skill routing",
        "final answer",
    ),
    ".agents/skills/obsidian-reentry-read/agents/openai.yaml": (
        "starting",
        "resuming",
        "workspace state",
        "active stage",
        "policy",
        "register",
    ),
    ".agents/skills/obsidian-architecture-guard/agents/openai.yaml": (
        "architecture",
        "agent settings",
        "repo-scoped skills",
        "policy",
        "artifact",
        "path",
        "encoding",
    ),
    ".agents/skills/obsidian-code-surface-guard/agents/openai.yaml": (
        "code writing",
        "owner module",
        "caller",
        "contract",
        "artifact",
        "monolith",
        "reference_scout_pairing",
    ),
    ".agents/skills/obsidian-exploration-mandate/agents/openai.yaml": (
        "exploration",
        "idea variants",
        "tier",
        "wfo",
        "operating promotion",
        "runtime authority",
    ),
    ".agents/skills/obsidian-work-packet-router/agents/openai.yaml": (
        "work packet lifecycle",
        "skill selection",
        "phase plan",
        "stop conditions",
        "final answer filter",
    ),
    ".agents/skills/obsidian-experiment-design/agents/openai.yaml": (
        "hypothesis",
        "baseline",
        "controls",
        "sample scope",
        "criteria",
        "evidence plan",
    ),
    ".agents/skills/obsidian-data-integrity/agents/openai.yaml": (
        "data source",
        "time axis",
        "sample scope",
        "feature-label boundary",
        "split boundary",
        "leakage risk",
    ),
    ".agents/skills/obsidian-model-validation/agents/openai.yaml": (
        "model",
        "threshold",
        "calibration",
        "split",
        "wfo",
        "overfit",
    ),
    ".agents/skills/obsidian-runtime-parity/agents/openai.yaml": (
        "python",
        "mt5",
        "runtime",
        "shared contract",
        "parity check",
        "claim boundary",
    ),
    ".agents/skills/obsidian-backtest-forensics/agents/openai.yaml": (
        "strategy tester",
        "tester identity",
        "ea identity",
        "trade evidence",
        "spread",
        "commission",
    ),
    ".agents/skills/obsidian-performance-attribution/agents/openai.yaml": (
        "kpi",
        "baseline",
        "drivers",
        "segment checks",
        "trade shape",
        "confidence",
    ),
    ".agents/skills/obsidian-environment-reproducibility/agents/openai.yaml": (
        "clean checkout",
        "dependency",
        "environment",
        "entry command",
        "local assumptions",
        "reproducibility judgment",
    ),
    ".agents/skills/obsidian-artifact-lineage/agents/openai.yaml": (
        "source inputs",
        "producer",
        "consumer",
        "artifact paths",
        "hashes",
        "lineage judgment",
    ),
    ".agents/skills/obsidian-result-judgment/agents/openai.yaml": (
        "evidence",
        "missing",
        "judgment label",
        "claim boundary",
        "next condition",
        "answer-clarity",
    ),
    ".agents/skills/obsidian-reference-scout/agents/openai.yaml": (
        "code writing",
        "official docs",
        "maintained source",
        "api",
        "mql5",
        "library behavior",
        "not_required",
    ),
    ".agents/skills/obsidian-run-evidence-system/agents/openai.yaml": (
        "run evidence",
        "measurement",
        "identity",
        "judgment",
        "run registry",
        "external verification",
    ),
    ".agents/skills/obsidian-claim-discipline/agents/openai.yaml": (
        "claim",
        "boundary",
        "runtime authority",
        "operating promotion",
        "positive",
        "blocked",
    ),
    ".agents/skills/obsidian-stage-transition/agents/openai.yaml": (
        "stage transition",
        "active_stage",
        "handoff",
        "workspace_state",
        "selection status",
        "registry",
    ),
    ".agents/skills/obsidian-answer-clarity/agents/openai.yaml": (
        "user-facing",
        "status summary",
        "result report",
        "completion report",
        "current meaning",
        "next action",
    ),
    ".agents/skills/obsidian-lane-classifier/agents/openai.yaml": (
        "lane",
        "exploration",
        "evidence",
        "promotion",
        "runtime",
        "hard gate",
    ),
    ".agents/skills/obsidian-workflow-drift-guard/agents/openai.yaml": (
        "blocker",
        "source material",
        "tool",
        "environment",
        "recovery",
        "retry",
        "external verification",
        "terminal action",
        "pre-block evidence",
    ),
    ".agents/skills/obsidian-code-quality/agents/openai.yaml": (
        "code quality",
        "responsibility",
        "flow",
        "contract",
        "test intent",
    ),
}


def has_utf8_bom(data: bytes) -> bool:
    return data.startswith(UTF8_BOM)


def leading_utf8_bom_count(data: bytes) -> int:
    count = 0
    offset = 0
    while data.startswith(UTF8_BOM, offset):
        count += 1
        offset += len(UTF8_BOM)
    return count


def iter_text_docs(repo_root: Path) -> list[Path]:
    roots = [
        repo_root / "AGENTS.md",
        repo_root / "docs",
        repo_root / ".agents",
        repo_root / "stages",
        repo_root / "foundation",
    ]
    paths: list[Path] = []
    for root in roots:
        if root.is_file():
            paths.append(root)
        elif root.exists():
            paths.extend(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".txt"})
    return sorted(set(paths))


def check_required_paths(repo_root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_PATHS:
        if not (repo_root / rel).exists():
            errors.append(f"missing required path: {rel}")
    return errors


def check_docs(repo_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for path in iter_text_docs(repo_root):
        rel = path.relative_to(repo_root).as_posix()
        data = path.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{rel}: not valid UTF-8: {exc}")
            continue

        bom_count = leading_utf8_bom_count(data)
        if bom_count > 1:
            errors.append(f"{rel}: contains repeated UTF-8 BOM markers")
        has_hangul = bool(HANGUL_RE.search(text))
        if has_hangul and not has_utf8_bom(data):
            errors.append(f"{rel}: Korean text requires UTF-8 with BOM")
        if "\ufffd" in text:
            errors.append(f"{rel}: contains Unicode replacement character")
        if MOJIBAKE_RE.search(text):
            errors.append(f"{rel}: contains likely mojibake")
        if SUSPICIOUS_CJK_RE.search(text) and not has_hangul:
            warnings.append(f"{rel}: contains CJK text without Hangul; inspect if unexpected")
    return errors, warnings


def check_policy_links(repo_root: Path) -> list[str]:
    errors: list[str] = []
    trigger_policy = (repo_root / "docs/policies/agent_trigger_policy.md").read_text(encoding="utf-8-sig")
    reentry = (repo_root / "docs/policies/reentry_order.md").read_text(encoding="utf-8-sig")
    agents = (repo_root / "AGENTS.md").read_text(encoding="utf-8-sig")
    debt = (repo_root / "docs/registers/architecture_debt_register.md").read_text(encoding="utf-8-sig")
    exploration = (repo_root / "docs/policies/exploration_mandate.md").read_text(encoding="utf-8-sig")
    kpi = (repo_root / "docs/policies/kpi_measurement_standard.md").read_text(encoding="utf-8-sig")
    run_management = (repo_root / "docs/policies/run_result_management.md").read_text(encoding="utf-8-sig")
    judgment = (repo_root / "docs/policies/result_judgment_policy.md").read_text(encoding="utf-8-sig")
    promotion = (repo_root / "docs/policies/promotion_policy.md").read_text(encoding="utf-8-sig")

    required_pairs = [
        ("agent_trigger_policy.md", trigger_policy, "obsidian-architecture-guard"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-session-intake"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-reentry-read"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-work-packet-router"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-answer-clarity"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-claim-discipline"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-code-quality"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-lane-classifier"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-exploration-mandate"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-experiment-design"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-data-integrity"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-model-validation"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-runtime-parity"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-backtest-forensics"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-performance-attribution"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-environment-reproducibility"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-artifact-lineage"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-result-judgment"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-code-surface-guard"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-workflow-drift-guard"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-reference-scout"),
        ("agent_trigger_policy.md", trigger_policy, "obsidian-run-evidence-system"),
        ("agent_trigger_policy.md", trigger_policy, "architecture_invariants.md"),
        ("agent_trigger_policy.md", trigger_policy, "exploration_mandate.md"),
        ("agent_trigger_policy.md", trigger_policy, "kpi_measurement_standard.md"),
        ("agent_trigger_policy.md", trigger_policy, "run_result_management.md"),
        ("agent_trigger_policy.md", trigger_policy, "result_judgment_policy.md"),
        ("reentry_order.md", reentry, "architecture_invariants.md"),
        ("reentry_order.md", reentry, "exploration_mandate.md"),
        ("reentry_order.md", reentry, "kpi_measurement_standard.md"),
        ("reentry_order.md", reentry, "run_result_management.md"),
        ("reentry_order.md", reentry, "result_judgment_policy.md"),
        ("reentry_order.md", reentry, "obsidian-work-packet-router"),
        ("AGENTS.md", agents, "Architecture Invariants"),
        ("AGENTS.md", agents, "Exploration Mandate"),
        ("AGENTS.md", agents, "Run Evidence System"),
        ("AGENTS.md", agents, "Progressive Hardening"),
        ("AGENTS.md", agents, "Codex Work Lifecycle"),
        ("AGENTS.md", agents, "obsidian-work-packet-router"),
        ("architecture_debt_register.md", debt, "AD-001"),
        ("architecture_debt_register.md", debt, "AD-002"),
        ("architecture_debt_register.md", debt, "AD-003"),
        ("architecture_debt_register.md", debt, "AD-004"),
        ("architecture_debt_register.md", debt, "AD-005"),
        ("architecture_debt_register.md", debt, "AD-006"),
        ("architecture_debt_register.md", debt, "AD-007"),
        ("exploration_mandate.md", exploration, "promotion-ineligible"),
        ("exploration_mandate.md", exploration, "tier_c_local_research"),
        ("exploration_mandate.md", exploration, "WFO"),
        ("kpi_measurement_standard.md", kpi, "structural_scout"),
        ("kpi_measurement_standard.md", kpi, "regular_risk_execution"),
        ("kpi_measurement_standard.md", kpi, "trade_shape"),
        ("run_result_management.md", run_management, "run_registry.csv"),
        ("run_result_management.md", run_management, "run_manifest.json"),
        ("result_judgment_policy.md", judgment, "positive"),
        ("result_judgment_policy.md", judgment, "negative"),
        ("result_judgment_policy.md", judgment, "invalid"),
        ("promotion_policy.md", promotion, "promotion_candidate"),
        ("promotion_policy.md", promotion, "operating_promotion"),
        ("promotion_policy.md", promotion, "runtime_probe"),
        ("promotion_policy.md", promotion, "runtime_authority"),
    ]
    for label, text, needle in required_pairs:
        if needle not in text:
            errors.append(f"{label}: missing required reference `{needle}`")
    return errors


def check_progressive_hardening_warnings(repo_root: Path) -> list[str]:
    warnings: list[str] = []
    checks = [
        ("AGENTS.md", repo_root / "AGENTS.md"),
        ("exploration_mandate.md", repo_root / "docs/policies/exploration_mandate.md"),
        ("result_judgment_policy.md", repo_root / "docs/policies/result_judgment_policy.md"),
        ("obsidian-lane-classifier/SKILL.md", repo_root / ".agents/skills/obsidian-lane-classifier/SKILL.md"),
        ("obsidian-run-evidence-system/SKILL.md", repo_root / ".agents/skills/obsidian-run-evidence-system/SKILL.md"),
    ]
    required_terms = ("promotion_candidate", "operating_promotion", "runtime_probe", "runtime_authority")
    for label, path in checks:
        text = path.read_text(encoding="utf-8-sig")
        for term in required_terms:
            if term not in text:
                warnings.append(f"{label}: progressive hardening warning: missing `{term}`")
    return warnings


def read_simple_agent_interface(path: Path) -> dict[str, str]:
    interface: dict[str, str] = {}
    in_interface = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if raw_line.strip() == "interface:":
            in_interface = True
            continue
        if not in_interface:
            continue
        if raw_line and not raw_line.startswith((" ", "\t")):
            break
        match = re.match(r"^\s+([A-Za-z0-9_]+):\s*(.*)\s*$", raw_line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        interface[key] = value.strip()
    return interface


def check_agent_settings(repo_root: Path) -> list[str]:
    errors: list[str] = []
    for rel_path, required_concepts in AGENT_PROMPT_REQUIRED_CONCEPTS.items():
        path = repo_root / rel_path
        if not path.exists():
            errors.append(f"{rel_path}: missing agent settings file")
            continue
        interface = read_simple_agent_interface(path)
        if not interface:
            errors.append(f"{rel_path}: missing interface section")
            continue
        for key in REQUIRED_AGENT_INTERFACE_KEYS:
            if not interface.get(key):
                errors.append(f"{rel_path}: missing or empty interface.{key}")
        prompt_text = " ".join(
            interface.get(key, "") for key in ("short_description", "default_prompt")
        ).lower()
        for concept in required_concepts:
            if concept.lower() not in prompt_text:
                errors.append(f"{rel_path}: agent prompt missing required concept `{concept}`")
    return errors


def check_skill_frontmatter(repo_root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = repo_root / ".agents" / "skills"
    if not skills_root.exists():
        errors.append("missing repo-scoped skills root: .agents/skills")
        return errors

    for skill_file in sorted(skills_root.glob("*/SKILL.md")):
        rel = skill_file.relative_to(repo_root).as_posix()
        text = skill_file.read_text(encoding="utf-8-sig")
        lines = text.splitlines()
        if not lines or lines[0].strip().lstrip("\ufeff") != "---":
            errors.append(f"{rel}: missing YAML frontmatter opener")
            continue
        try:
            end_index = lines[1:].index("---") + 1
        except ValueError:
            errors.append(f"{rel}: missing YAML frontmatter closer")
            continue
        frontmatter = "\n".join(lines[1:end_index])
        if not re.search(r"^name:\s*\S+", frontmatter, flags=re.MULTILINE):
            errors.append(f"{rel}: missing frontmatter name")
        if not re.search(r"^description:\s*\S+", frontmatter, flags=re.MULTILINE):
            errors.append(f"{rel}: missing frontmatter description")
        if "TODO" in frontmatter:
            errors.append(f"{rel}: frontmatter still contains TODO")
    return errors


def frontmatter_name(skill_file: Path) -> str | None:
    text = skill_file.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0].strip().lstrip("\ufeff") != "---":
        return None
    try:
        end_index = lines[1:].index("---") + 1
    except ValueError:
        return None
    frontmatter = "\n".join(lines[1:end_index])
    match = re.search(r"^name:\s*(\S+)", frontmatter, flags=re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip()


def check_skill_routing_completeness(repo_root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = repo_root / ".agents" / "skills"
    trigger_policy_path = repo_root / "docs/policies/agent_trigger_policy.md"
    if not skills_root.exists() or not trigger_policy_path.exists():
        return errors

    trigger_policy = trigger_policy_path.read_text(encoding="utf-8-sig")
    for skill_file in sorted(skills_root.glob("*/SKILL.md")):
        skill_dir = skill_file.parent
        rel_dir = skill_dir.relative_to(repo_root).as_posix()
        skill_name = frontmatter_name(skill_file) or skill_dir.name

        if skill_name not in trigger_policy:
            errors.append(f"{rel_dir}: skill `{skill_name}` is not routed in agent_trigger_policy.md")

        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if not openai_yaml.exists():
            errors.append(f"{rel_dir}: missing agents/openai.yaml; every repo skill must expose routing metadata")
            continue

        interface = read_simple_agent_interface(openai_yaml)
        for key in REQUIRED_AGENT_INTERFACE_KEYS:
            if not interface.get(key):
                rel_yaml = openai_yaml.relative_to(repo_root).as_posix()
                errors.append(f"{rel_yaml}: missing or empty interface.{key}")
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        if not re.search(r"allow_implicit_invocation:\s*true\b", yaml_text):
            rel_yaml = openai_yaml.relative_to(repo_root).as_posix()
            errors.append(f"{rel_yaml}: policy.allow_implicit_invocation must be true for repo-scoped skills")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Obsidian agent settings, skill routing, architecture guard links, and Korean encoding.")
    parser.add_argument("--repo-root", default=".", help="Repository root to validate.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(check_required_paths(repo_root))
    doc_errors, doc_warnings = check_docs(repo_root)
    errors.extend(doc_errors)
    warnings.extend(doc_warnings)
    if not errors:
        errors.extend(check_policy_links(repo_root))
        warnings.extend(check_progressive_hardening_warnings(repo_root))
    errors.extend(check_agent_settings(repo_root))
    errors.extend(check_skill_frontmatter(repo_root))
    errors.extend(check_skill_routing_completeness(repo_root))

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("OK: agent settings, skill routing, architecture guard links, and Korean encoding checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
