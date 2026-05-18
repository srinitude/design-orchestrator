# Design Quality Rubric

Use this rubric for subjective review after deterministic validation passes. It is intentionally separate from `scripts/validate-evals.py` because design quality requires judgment.

Score each dimension from 0-3:

- 0: missing or harmful.
- 1: present but vague, generic, or incomplete.
- 2: usable with minor gaps.
- 3: specific, coherent, and ready for handoff.

## Dimensions

| Dimension | What Good Looks Like |
| --- | --- |
| Intent and audience | The output names the platform, audience, goal, constraints, and success criteria early. |
| Research grounding | Reference Notes include 3-5 concise signals and the visual direction responds to them. |
| Journey or viewer path | Product UI has user flow and states; static artifacts have message hierarchy and attention path. |
| Visual specificity | Type, color, layout, imagery, surface, density, and hierarchy are concrete enough to recreate. |
| Platform fit | Web and mobile conventions are explicit; mobile safe areas and touch targets are handled when relevant. |
| Accessibility | Contrast, type size, focus, keyboard or touch behavior, reduced motion, semantics, and error states are addressed. |
| Interaction and motion | Motion has purpose, timing, restraint, and reduced-motion fallback. Interactions include states and feedback. |
| Responsive behavior | Breakpoints, layout shifts, truncation, density changes, and content priority are clear. |
| Non-genericity | The output avoids category reflexes, vague "modern clean" language, decorative defaults, and one-note palettes. |
| Handoff readiness | Acceptance criteria, component states, token notes, QA steps, and implementation risks are testable. |

## Interpretation

- 24-30: strong output. Deliver after a brief self-revision pass.
- 16-23: usable but needs targeted revision before delivery.
- 0-15: revise substantially before delivery.

Accessibility is not averaged away. A serious accessibility miss fails the output even when the total score is high.
