# design-orchestrator

[![skills.sh](https://skills.sh/b/srinitude/design-orchestrator)](https://skills.sh/s/srinitude/design-orchestrator)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Validate](https://github.com/srinitude/design-orchestrator/actions/workflows/validate.yml/badge.svg)](https://github.com/srinitude/design-orchestrator/actions/workflows/validate.yml)

`design-orchestrator` is a public, portable Agent Skill for routing design requests into written design artifacts, critique, and implementation-ready handoff.

It works as an orchestrator when companion design capabilities are available and as a standalone workflow when they are not. The skill supports product UI, static visual artifacts, brand-in-product direction, visual reference prompts, design critique, reference extraction, and implementation handoff QA.

The skill defaults to Markdown artifacts and prompts. It generates assets or images only when the user explicitly asks for visual references or rendered output.

## Install

```bash
npx skills add srinitude/design-orchestrator
```

To preview the skills exposed by this repository:

```bash
npx skills add srinitude/design-orchestrator --list
```

## Use Cases

- Route vague design requests into a stable design workflow.
- Produce concise design briefs, journey maps, visual direction, component specs, handoff notes, and QA checklists.
- Keep web and mobile platform assumptions explicit.
- Apply lightweight research before visual direction.
- Critique and self-revise before final delivery.
- Preserve accessibility, responsive behavior, interaction states, and acceptance criteria as hard gates.

## Package Structure

```text
design-orchestrator/
|-- skills/
|   `-- design-orchestrator/
|       |-- agents/
|       |   `-- openai.yaml
|       |-- evals/
|       |   `-- routing-and-quality-evals.json
|       |-- examples/
|       |   |-- product-ui-output.md
|       |   `-- static-artifact-output.md
|       |-- references/
|       |   |-- companion-skill-map.md
|       |   |-- design-quality-rubric.md
|       |   `-- quality-gates.md
|       |-- scripts/
|       |   `-- validate-evals.py
|       `-- SKILL.md
|-- skills-lock.json
|-- package.json
|-- README.md
|-- LICENSE
`-- NOTICE
```

## Repository Files

- [SKILL.md](SKILL.md): core skill instructions.
- [agents/openai.yaml](agents/openai.yaml): optional OpenAI-facing skill metadata.
- [skills/design-orchestrator/references/companion-skill-map.md](skills/design-orchestrator/references/companion-skill-map.md): optional companion capability routing examples.
- [skills/design-orchestrator/references/design-quality-rubric.md](skills/design-orchestrator/references/design-quality-rubric.md): subjective design review rubric.
- [skills/design-orchestrator/references/quality-gates.md](skills/design-orchestrator/references/quality-gates.md): hard gates and manual QA fallback.
- [skills/design-orchestrator/evals/routing-and-quality-evals.json](skills/design-orchestrator/evals/routing-and-quality-evals.json): routing and quality eval cases.
- [skills/design-orchestrator/scripts/validate-evals.py](skills/design-orchestrator/scripts/validate-evals.py): standard-library validation script.
- [examples/product-ui-output.md](examples/product-ui-output.md): product UI example output.
- [examples/static-artifact-output.md](examples/static-artifact-output.md): static artifact example output.

## Validation

Validate the skill package:

```bash
skills-ref validate .
```

If `skills-ref` is not installed, run the official reference implementation:

```bash
git clone --depth 1 https://github.com/agentskills/agentskills /tmp/agentskills
uv run --project /tmp/agentskills/skills-ref skills-ref validate "$PWD/skills/design-orchestrator"
```

Validate the bundled script and eval contract:

```bash
python3 -m py_compile skills/design-orchestrator/scripts/validate-evals.py
skills/design-orchestrator/scripts/validate-evals.py --help
skills/design-orchestrator/scripts/validate-evals.py skills/design-orchestrator/evals/routing-and-quality-evals.json
```

Validate skills CLI discovery:

```bash
npx skills add "$PWD" --list
```

The same checks run in GitHub Actions for pushes and pull requests.

## Requirements

- Python 3.9 or newer.
- Node.js and `npx` only for optional skills CLI discovery.
- `uv` only when running the official `skills-ref` fallback from source.

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

Keep changes focused on the portable Agent Skill package: `skills/design-orchestrator/SKILL.md` for core behavior, `skills/design-orchestrator/references/` for longer guidance, `skills/design-orchestrator/evals/` for routing and quality cases, and `skills/design-orchestrator/scripts/` for deterministic validation.

## Security

Report security concerns using [SECURITY.md](SECURITY.md). Do not include secrets, private screenshots, credentials, proprietary design references, or customer material in public issues.

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
