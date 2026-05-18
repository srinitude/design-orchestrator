#!/usr/bin/env python3
"""Validate the design-orchestrator skill package and eval contract.

This script intentionally uses only the Python standard library so it can run in
minimal agent environments.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/companion-skill-map.md",
    "references/design-quality-rubric.md",
    "references/quality-gates.md",
    "evals/routing-and-quality-evals.json",
    "scripts/validate-evals.py",
    "examples/product-ui-output.md",
    "examples/static-artifact-output.md",
    "README.md",
    "LICENSE",
]

ROUTE_IDS = {
    "product-ui-design",
    "static-visual-artifact",
    "brand-in-product-direction",
    "visual-reference-or-prompt",
    "design-critique",
    "image-to-code-or-reference-extraction",
    "implementation-handoff-qa",
}

ARTIFACT_IDS = {
    "design-brief",
    "journey-map",
    "visual-direction",
    "screen-or-component-spec",
    "design-system-notes",
    "implementation-handoff",
    "qa-checklist",
}

PHASE_IDS = {
    "intent",
    "research",
    "journey",
    "visual-direction",
    "artifact-generation",
    "critique",
    "implementation-handoff-qa",
}

FALLBACK_BEHAVIORS = {
    "continue_with_standalone_fallback",
    "block_only_if_generation_is_strictly_required",
    "state_rendering_limitation_and_continue_with_manual_qa",
}

REQUIRED_SKILL_SECTIONS = [
    "Core Contract",
    "Routing",
    "Phase Sequence",
    "Research Rule",
    "Output Artifacts",
    "Quality Gates",
    "Companion Capabilities",
    "Validation",
]

EXAMPLE_SECTIONS = {
    "examples/product-ui-output.md": [
        "Reference Notes",
        "Design Brief",
        "Journey Map",
        "Visual Direction",
        "Screen or Component Spec",
        "Design System Notes",
        "Critique",
        "QA Checklist",
    ],
    "examples/static-artifact-output.md": [
        "Reference Notes",
        "Design Brief",
        "Viewer Path",
        "Visual Direction",
        "Message Hierarchy",
        "Critique",
        "QA Checklist",
    ],
}


class ValidationError(Exception):
    """Raised when validation finds one or more package problems."""


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{path}: expected UTF-8 text") from exc


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc


def parse_frontmatter(skill_path: Path) -> dict[str, str]:
    text = read_text(skill_path)
    if not text.startswith("---\n"):
        raise ValidationError("SKILL.md: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValidationError("SKILL.md: unterminated YAML frontmatter")
    frontmatter = text[4:end]
    parsed: dict[str, str] = {}
    for raw_line in frontmatter.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValidationError(f"SKILL.md frontmatter: invalid line {raw_line!r}")
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip().strip('"')
    return parsed


def parse_simple_openai_yaml(path: Path) -> dict[str, str]:
    text = read_text(path)
    parsed: dict[str, str] = {}
    in_interface = False
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith("interface:"):
            in_interface = True
            continue
        if raw_line and not raw_line.startswith(" "):
            in_interface = False
        if in_interface:
            match = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*\"(.*)\"\s*$", raw_line)
            if match:
                parsed[match.group(1)] = match.group(2)
    required = {"display_name", "short_description", "default_prompt"}
    missing = sorted(required - parsed.keys())
    if missing:
        raise ValidationError(f"{path}: missing interface keys: {', '.join(missing)}")
    return parsed


def validate_required_files(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.exists():
            errors.append(f"missing required file: {rel}")
        elif path.is_file() and path.stat().st_size == 0:
            errors.append(f"empty required file: {rel}")
    return errors


def validate_skill(root: Path) -> list[str]:
    errors: list[str] = []
    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        return ["SKILL.md: missing"]
    try:
        frontmatter = parse_frontmatter(skill_path)
    except ValidationError as exc:
        return [str(exc)]
    name = frontmatter.get("name")
    description = frontmatter.get("description", "")
    if name != "design-orchestrator":
        errors.append("SKILL.md: name must be design-orchestrator")
    if not (1 <= len(description) <= 1024):
        errors.append("SKILL.md: description must be 1-1024 characters")
    if frontmatter.get("license") != "Apache-2.0":
        errors.append("SKILL.md: license must be Apache-2.0")
    text = read_text(skill_path)
    for section in REQUIRED_SKILL_SECTIONS:
        if f"## {section}" not in text:
            errors.append(f"SKILL.md: missing section {section!r}")
    for phase_id in PHASE_IDS:
        if f"`{phase_id}`" not in text:
            errors.append(f"SKILL.md: missing phase id `{phase_id}`")
    for route_id in ROUTE_IDS:
        if f"`{route_id}`" not in text:
            errors.append(f"SKILL.md: missing route id `{route_id}`")
    for artifact_id in ARTIFACT_IDS:
        if f"`{artifact_id}`" not in text:
            errors.append(f"SKILL.md: missing artifact id `{artifact_id}`")
    return errors


def validate_openai_yaml(root: Path) -> list[str]:
    path = root / "agents/openai.yaml"
    if not path.exists():
        return ["agents/openai.yaml: missing"]
    try:
        parsed = parse_simple_openai_yaml(path)
    except ValidationError as exc:
        return [str(exc)]
    errors: list[str] = []
    if "$design-orchestrator" not in parsed["default_prompt"]:
        errors.append("agents/openai.yaml: default_prompt must mention $design-orchestrator")
    if len(parsed["short_description"]) > 64:
        errors.append("agents/openai.yaml: short_description must be <= 64 characters")
    return errors


def validate_eval_file(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)
    if data.get("skill_name") != "design-orchestrator":
        errors.append("evals: skill_name must be design-orchestrator")
    if set(data.get("canonical_route_ids", [])) != ROUTE_IDS:
        errors.append("evals: canonical_route_ids must match required route IDs")
    if set(data.get("canonical_artifacts", [])) != ARTIFACT_IDS:
        errors.append("evals: canonical_artifacts must match required artifacts")
    if set(data.get("phase_ids", [])) != PHASE_IDS:
        errors.append("evals: phase_ids must match required phase IDs")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append("evals: evals must be a non-empty list")
        return errors
    seen: set[str] = set()
    types: set[str] = set()
    for index, case in enumerate(evals):
        prefix = f"evals[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        eval_id = case.get("id")
        if not isinstance(eval_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", eval_id):
            errors.append(f"{prefix}: id must be lowercase kebab-case")
        elif eval_id in seen:
            errors.append(f"{prefix}: duplicate id {eval_id}")
        else:
            seen.add(eval_id)
        case_type = case.get("type")
        if case_type not in {"routing", "quality"}:
            errors.append(f"{prefix}: type must be routing or quality")
        else:
            types.add(case_type)
        prompt = case.get("prompt")
        if not isinstance(prompt, str) or len(prompt.strip()) < 20:
            errors.append(f"{prefix}: prompt must be a realistic non-empty user prompt")
        route_id = case.get("expected_route_id")
        if route_id not in ROUTE_IDS:
            errors.append(f"{prefix}: expected_route_id is invalid")
        artifacts = case.get("expected_artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            errors.append(f"{prefix}: expected_artifacts must be a non-empty list")
        else:
            invalid = sorted(set(artifacts) - ARTIFACT_IDS)
            if invalid:
                errors.append(f"{prefix}: invalid expected_artifacts: {', '.join(invalid)}")
        phases = case.get("required_phases")
        if not isinstance(phases, list) or not phases:
            errors.append(f"{prefix}: required_phases must be a non-empty list")
        else:
            invalid = sorted(set(phases) - PHASE_IDS)
            if invalid:
                errors.append(f"{prefix}: invalid required_phases: {', '.join(invalid)}")
            if "visual-direction" in phases and "research" not in phases:
                errors.append(f"{prefix}: research is required before visual-direction")
            if "critique" not in phases:
                errors.append(f"{prefix}: critique phase is required")
        sections = case.get("required_sections")
        if not isinstance(sections, list) or not all(isinstance(item, str) and item for item in sections):
            errors.append(f"{prefix}: required_sections must be a non-empty string list")
        fallback = case.get("fallback_behavior")
        if fallback not in FALLBACK_BEHAVIORS:
            errors.append(f"{prefix}: fallback_behavior is invalid")
        quality_checks = case.get("quality_checks")
        if not isinstance(quality_checks, list) or not quality_checks:
            errors.append(f"{prefix}: quality_checks must be a non-empty list")
    if "routing" not in types:
        errors.append("evals: must include routing evals")
    if "quality" not in types:
        errors.append("evals: must include quality evals")
    return errors


def validate_examples(root: Path) -> list[str]:
    errors: list[str] = []
    for rel, sections in EXAMPLE_SECTIONS.items():
        path = root / rel
        if not path.exists():
            errors.append(f"{rel}: missing")
            continue
        text = read_text(path)
        for section in sections:
            if section not in text:
                errors.append(f"{rel}: missing example section {section!r}")
    return errors


def validate_license(root: Path) -> list[str]:
    path = root / "LICENSE"
    if not path.exists():
        return ["LICENSE: missing"]
    text = read_text(path)
    if "Apache License" not in text or "Version 2.0" not in text:
        return ["LICENSE: expected Apache License Version 2.0 text"]
    return []


def validate_links(root: Path) -> list[str]:
    errors: list[str] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in sorted(root.rglob("*.md")):
        text = read_text(path)
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip()
            if (
                not target
                or target.startswith("#")
                or "://" in target
                or target.startswith("mailto:")
            ):
                continue
            target_path = target.split("#", 1)[0]
            resolved = (path.parent / target_path).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(root)}: link escapes repo: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(root)}: broken relative link: {target}")
    return errors


def validate_repo(eval_path: Path) -> list[str]:
    root = eval_path.resolve().parents[1]
    errors: list[str] = []
    errors.extend(validate_required_files(root))
    try:
        errors.extend(validate_eval_file(eval_path))
    except ValidationError as exc:
        errors.append(str(exc))
    errors.extend(validate_skill(root))
    errors.extend(validate_openai_yaml(root))
    errors.extend(validate_examples(root))
    errors.extend(validate_license(root))
    errors.extend(validate_links(root))
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the design-orchestrator eval file and required skill repo files."
    )
    parser.add_argument(
        "eval_file",
        nargs="?",
        default="evals/routing-and-quality-evals.json",
        help="Path to the routing and quality eval JSON file.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    eval_path = Path(args.eval_file)
    if not eval_path.exists():
        print(f"ERROR: eval file not found: {eval_path}", file=sys.stderr)
        return 2
    errors = validate_repo(eval_path)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed: design-orchestrator package and eval contract are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
