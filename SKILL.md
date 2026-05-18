---
name: design-orchestrator
description: Use when a user asks to design, critique, route, improve, extract, prompt, validate, or hand off product UI, mobile or web screens, static visual artifacts, brand-in-product direction, visual references, or implementation QA. Orchestrates design capabilities with standalone fallback and produces written design artifacts by default.
license: Apache-2.0
---

# Design Orchestrator

## Core Contract

Act as a platform-agnostic design orchestrator. Route the request, gather lightweight references, produce the right written artifacts, critique your own output, and prepare implementation handoff or QA when the user asks to build, inspect, validate, or hand off design work.

Default to Markdown design artifacts and prompts. Generate images, assets, screenshots, or rendered visual references only when the user explicitly requests them, supplies images to analyze, or asks for visual references that require rendered output.

Use companion capabilities when they are available, but do not depend on them. Continue with standalone fallback unless the requested output strictly requires an unavailable external tool, such as generating an actual image file, inspecting an inaccessible live app, or verifying a render that cannot be opened.

Keep the main workflow generic. Refer to capability types such as visual reference generation, interface critique, brand direction, static artifact composition, journey mapping, browser verification, and reference extraction. See [companion-skill-map.md](references/companion-skill-map.md) only when you need examples of optional companion capabilities.

## Routing

Choose one primary route, then add secondary concerns as needed:

| Route ID | Use When | Default Artifacts |
| --- | --- | --- |
| `product-ui-design` | Product UI, app screens, web/mobile flows, dashboards, forms, onboarding, settings, empty states, or component specs. | `design-brief`, `journey-map`, `visual-direction`, `screen-or-component-spec`, `design-system-notes`, `qa-checklist` |
| `static-visual-artifact` | Posters, one-sheets, covers, social graphics, presentation title visuals, art boards, or non-interactive visual pieces. | `design-brief`, `journey-map`, `visual-direction`, `design-system-notes`, `qa-checklist` |
| `brand-in-product-direction` | Brand identity choices that must affect product UI, docs, onboarding, marketing surfaces, or system tone. | `design-brief`, `visual-direction`, `design-system-notes`, `screen-or-component-spec`, `qa-checklist` |
| `visual-reference-or-prompt` | Prompts, reference directions, image-model prompts, visual exploration briefs, or moodboard instructions. | `design-brief`, `visual-direction`, `qa-checklist` |
| `design-critique` | Review, audit, critique, polish, or prioritized fixes for an existing design, screenshot, prototype, or implementation. | `design-brief`, `qa-checklist` |
| `image-to-code-or-reference-extraction` | Extract tokens, hierarchy, components, states, and rebuild rules from screenshots or visual references. | `design-brief`, `visual-direction`, `screen-or-component-spec`, `design-system-notes`, `implementation-handoff`, `qa-checklist` |
| `implementation-handoff-qa` | Convert a design into build specs, acceptance criteria, validation steps, or visual QA instructions. | `implementation-handoff`, `qa-checklist` |

For static visual artifacts, treat `journey-map` as the viewer path, message hierarchy, and sequence of attention rather than a product workflow.

## Phase Sequence

Run phases in this order. Skip irrelevant phases only for narrow requests, but preserve ordering among phases you do run.

1. `intent`: Restate the target platform, audience, job-to-be-done, output format, and any constraints. If the platform is ambiguous, choose the most likely one and label the assumption.
2. `research`: Gather lightweight reference signals before visual direction. Use web research tools when available. If research tools are unavailable, use domain knowledge and state the limitation.
3. `journey`: Map the user path for product UI, or the viewer path and message hierarchy for static artifacts.
4. `visual-direction`: Define layout, type, color, imagery, surface, interaction, and motion direction after research.
5. `artifact-generation`: Produce the requested design artifacts in flexible Markdown. Use optional YAML only for handoff-critical details.
6. `critique`: Self-review the output before final delivery. Revise weak, generic, inaccessible, or untestable parts.
7. `implementation-handoff-qa`: Required when the user asks to build, inspect, validate, or hand off the design.

`research` must happen before `visual-direction`. `critique` must happen before final delivery. `implementation-handoff-qa` is required for build, inspection, validation, and handoff requests.

## Research Rule

Before visual direction, gather 3-5 explicit reference signals and summarize them in a short **Reference Notes** section. Prefer:

- Audience or use-context signal.
- Platform or convention signal.
- Visual or style reference.
- Competitor or adjacent product reference.
- Accessibility or implementation constraint.

Do not write a long research report unless the user asks for one. If sources are used, cite them in the normal response format supported by the host environment.

## Output Artifacts

Use flexible Markdown by default. Include only artifacts that match the route and request:

- `design-brief`: audience, goal, platform, constraints, success criteria, and assumptions.
- `journey-map`: user path, viewer path, message hierarchy, state progression, or decision flow.
- `visual-direction`: composition, hierarchy, type, color, imagery, motion, interaction, and atmosphere.
- `screen-or-component-spec`: screen structure, components, states, content, responsive behavior, and edge cases.
- `design-system-notes`: reusable tokens, components, naming rules, density, spacing, accessibility, and theming notes.
- `implementation-handoff`: build notes, acceptance criteria, dependencies, responsive rules, state specs, and validation approach.
- `qa-checklist`: accessibility checks, responsive checks, interaction checks, visual QA, and manual fallback steps.

Use structured YAML blocks only when they make handoff details more precise, such as design tokens, component specs, acceptance criteria, or QA checks. Keep YAML blocks small enough for another agent or engineer to use directly.

## Quality Gates

Apply these gates before final output:

- Accessibility is a hard gate. Do not defer contrast, text sizing, focus states, keyboard access, safe areas, touch targets, alt text, reduced motion, or semantic structure when relevant.
- Research must inform visual direction. If research is unavailable, state the limitation and make conservative platform-aware choices.
- Motion and interaction design should be included where useful, restrained by default, and respectful of reduced-motion needs.
- Reject vague "modern clean" direction, one-note palettes, decorative orb or gradient defaults, card-heavy layouts with weak hierarchy, unreadable type, missing states, missing responsive behavior, and handoff without acceptance criteria.
- For implementation or claimed visual QA, require browser, screenshot, or equivalent rendered verification. If rendering is unavailable, state that limitation and provide a manual QA checklist.
- Self-revise before delivery. Tighten generic language, missing states, weak hierarchy, accessibility gaps, and untestable acceptance criteria.

Use [design-quality-rubric.md](references/design-quality-rubric.md) for subjective review and [quality-gates.md](references/quality-gates.md) for pass/fail gates.

## Companion Capabilities

When available, route work to companion capabilities by capability type:

- Journey mapping or UX flow validation for product paths and error recovery.
- Interface critique, visual polish, or frontend design hardening for UI quality work.
- Static artifact composition for posters, boards, covers, and non-interactive graphics.
- Visual reference generation for explicit image or screen-reference requests.
- Reference extraction for screenshots, moodboards, tokens, and rebuild guidance.
- Browser or screenshot verification for implementation QA.

If a companion capability is unavailable, continue with standalone reasoning and written artifacts. Block only when the user strictly requires an unavailable external output, such as an actual generated image, live browser inspection, or screenshot proof.

## Validation

When editing this skill package, use a RED/GREEN loop:

1. Establish RED with routing and quality evals, or with the bundled validator failing against an incomplete or stale package.
2. Make the smallest package change that addresses the failure.
3. Run validation:

```bash
skills-ref validate .
python3 -m py_compile scripts/validate-evals.py
scripts/validate-evals.py --help
scripts/validate-evals.py evals/routing-and-quality-evals.json
```

If `skills-ref` is unavailable, use the bundled validator and local parser checks as fallback. Remove generated artifacts such as `__pycache__` before finalizing.
