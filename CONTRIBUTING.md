# Contributing

Thanks for helping improve Design Orchestrator.

## Development Setup

Clone the repository, then validate the skill package from the repository root:

```bash
skills-ref validate "$PWD/skills/design-orchestrator"
python3 -m py_compile skills/design-orchestrator/scripts/validate-evals.py
skills/design-orchestrator/scripts/validate-evals.py --help
skills/design-orchestrator/scripts/validate-evals.py skills/design-orchestrator/evals/routing-and-quality-evals.json
npx skills add "$PWD" --list
```

If `skills-ref` is not installed, run the official reference implementation:

```bash
git clone --depth 1 https://github.com/agentskills/agentskills /tmp/agentskills
uv run --project /tmp/agentskills/skills-ref skills-ref validate "$PWD/skills/design-orchestrator"
```

## Contribution Guidelines

- Keep the repository installable with `npx skills add srinitude/design-orchestrator`.
- Keep `skills/design-orchestrator/SKILL.md` focused on core routing behavior and non-obvious quality gates.
- Put long-form design guidance in `skills/design-orchestrator/references/`.
- Put deterministic repeated logic in `scripts/`.
- Keep eval cases realistic and tied to stable route IDs, artifact IDs, and phase IDs.
- Preserve the standalone fallback behavior when companion capabilities are unavailable.
- Avoid committing private screenshots, credentials, API keys, generated caches, customer material, or proprietary references.

## Pull Requests

Before opening a pull request:

1. Run the validation commands above.
2. Update README, examples, references, or evals when behavior changes.
3. Keep commits focused and use clear commit messages.
4. Explain what changed, why it changed, and how it was validated.
