# Security Policy

## Supported Versions

Security fixes are handled on the latest released version.

## Reporting a Vulnerability

If you find a vulnerability, avoid posting secrets, exploit details, private screenshots, credentials, customer material, or proprietary design references in a public issue.

Use GitHub private vulnerability reporting when available, or contact the maintainer through the repository owner profile. If the concern is not sensitive, open a GitHub issue with enough detail to reproduce the problem.

Reports should include:

- Affected files or commands.
- Expected and actual behavior.
- Reproduction steps.
- Relevant environment details.

## Scope

Security-sensitive areas include:

- Script behavior in `scripts/`.
- Eval validation bypasses.
- Instructions that could encourage disclosure of private design references or credentials.
- Installability and package metadata that could mislead users about what the skill does.
