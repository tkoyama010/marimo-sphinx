# AGENTS.md

Instructions for AI agents when working in this repository.

## Git Commits

- Do not add `Co-Authored-By: <AI agent>` trailers to commit messages.

## Creating GitHub Issues

Always use the provided issue templates when opening GitHub issues for this project.

### Bug Reports

Use `gh issue create` with the bug report template:

```bash
gh issue create \
  --title "<short description of the bug>" \
  --label "bug" \
  --body "$(cat <<'EOF'
## Description

<clear and concise description of the bug>

## Steps to Reproduce

1.
2.
3.

## Expected Behavior

<what you expected to happen>

## Actual Behavior

<what actually happened; include error messages and tracebacks>

## Environment

- marimo-sphinx version:
- Sphinx version:
- Python version:
- OS:

## Additional Context

<any other context, screenshots, or configuration snippets>
EOF
)"
```

### Feature Requests

Use `gh issue create` with the feature request template:

```bash
gh issue create \
  --title "<short description of the feature>" \
  --label "enhancement" \
  --body "$(cat <<'EOF'
## Problem / Motivation

<what problem does this feature solve and why is it needed>

## Proposed Solution

<describe the feature you would like to see>

## Alternatives Considered

<any alternative solutions or workarounds you have considered>

## Additional Context

<any other context, examples, or references>
EOF
)"
```

### Rules

- Never use `--body` with a plain string that skips these sections.
- Always include all required sections (Description/Steps/Expected/Actual/Environment for bugs; Problem/Solution for features).
- Pick exactly one label: `bug` or `enhancement`.
- Keep the title short (under 72 characters) and in imperative mood.
