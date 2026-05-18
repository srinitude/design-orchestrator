# Quality Gates

Use these gates before final delivery. Hard gates must pass or be explicitly reported as blocked with a concrete limitation.

## Hard Gates

- **Accessibility:** Contrast, type size, focus, keyboard access, touch targets, semantics, error states, safe areas, and reduced motion are addressed when relevant.
- **Research before visual direction:** Visual direction follows Reference Notes. If research tools are unavailable, the limitation is stated.
- **Critique before delivery:** The output includes a self-review and visible corrections or prioritized gaps.
- **Implementation QA:** Build, inspect, validate, and handoff requests include acceptance criteria and QA checks.
- **Rendered verification when claimed:** Browser, screenshot, or equivalent rendered checks are required when implementation happens or visual QA is claimed.

## Anti-Generic Gate

Revise before delivery if the output relies on:

- Vague "modern clean" or "sleek premium" language without concrete choices.
- One-note palettes or category reflexes.
- Decorative orb, blob, bokeh, or gradient backgrounds as the default visual idea.
- Card-heavy layouts with weak hierarchy.
- Unreadable type, tiny labels, or unspecified typography.
- Missing states, empty states, errors, loading, focus, disabled, hover, pressed, and responsive behavior.
- Handoff without acceptance criteria.

## Manual QA Fallback

If rendering or browser verification is unavailable, state that limitation and provide a manual checklist that covers:

- Desktop and mobile viewport checks.
- Text wrapping and truncation.
- Keyboard, focus, and touch behavior.
- Contrast and reduced-motion preference.
- Loading, empty, error, disabled, and success states.
- Screenshot comparison or design review steps the user can run later.
