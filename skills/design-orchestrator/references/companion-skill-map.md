# Companion Skill Map

This skill is designed to work without companion skills. Use this map only when the runtime exposes related capabilities. Treat all names below as optional examples, not dependencies or public requirements.

## Routing To Capabilities

| Route ID | Generic Capability To Prefer | Optional Local Examples |
| --- | --- | --- |
| `product-ui-design` | Product UI design, frontend design, interface hardening, journey mapping. | `impeccable`, `high-end-visual-design`, `user-journeys` |
| `static-visual-artifact` | Static visual artifact composition, poster or board creation, graphic design output. | `canvas-design` |
| `brand-in-product-direction` | Brand system direction, logo and identity exploration, product-surface translation. | `brandkit`, `impeccable` |
| `visual-reference-or-prompt` | Visual reference generation, web or mobile screen prompt direction, image-model prompt writing. | `imagegen-frontend-web`, `imagegen-frontend-mobile`, `brandkit` |
| `design-critique` | Interface critique, accessibility review, hierarchy audit, design polish. | `impeccable`, `user-journeys` |
| `image-to-code-or-reference-extraction` | Screenshot analysis, design-system extraction, visual-to-code planning, token extraction. | `image-to-code`, `visual-design-system-extractor` |
| `implementation-handoff-qa` | Browser verification, screenshot QA, acceptance criteria, design-to-implementation handoff. | `image-to-code`, `impeccable`, `user-journeys` |

## Fallback Rules

- If companion capabilities are available, use them for the part of the task they are best suited to handle.
- If they are unavailable, continue with the core `design-orchestrator` workflow and produce written artifacts.
- Do not name optional local skills in user-facing output unless the user asks which companion capability was used.
- Do not block because a companion capability is missing unless the user specifically required the unavailable external output.
- Keep generated repo content license-clean: use the local skills as routing and quality inspiration only, not as copied source text.
