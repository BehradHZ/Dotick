# AI Contribution Guidelines (Notion Integration)

This repository can be modified by an AI assistant (Notion AI) acting on behalf of the repo owner (Behrad). These rules apply to any AI agent (Notion AI, Claude Code, Codex, or others) making changes here.

## Core rules

1. **Never commit directly to `main`.** All AI-driven changes must go through a feature branch and a Pull Request.
2. **Branch naming**: use `ai/<short-description>`, e.g. `ai/add-login-page`, `ai/fix-typo-readme`.
3. **One logical change per PR.** Keep PRs small and focused so they are easy to review.
4. **Always open a Pull Request** targeting `main` (or the relevant base branch) instead of pushing directly. Do not merge the PR yourself — the human owner reviews and merges.
5. **Write a clear PR description**: what changed, why, and how it was tested (if applicable).
6. **Do not change repository settings**, visibility, branch protection rules, collaborators, or secrets. Only the human owner manages these.
7. **Do not delete branches, tags, or releases** unless explicitly instructed by the human owner in the request.
8. **Respect existing code style and structure.** Match conventions already used in the repo rather than introducing new patterns without reason.
9. **Never commit secrets, API keys, tokens, or credentials.** Run a secret scan on new/changed content before committing if such a tool is available.
10. **If a task is ambiguous or risky** (e.g. deleting files, large refactors, changing CI/CD), pause and ask the human owner for confirmation before proceeding.

## Workflow summary

1. Create a new branch from the latest `main`.
2. Make the requested changes on that branch.
3. Open a Pull Request describing the change.
4. Wait for the human owner to review, request changes, or merge.

This keeps the human owner in full control of what actually lands in `main`, while still letting AI assistants do the implementation work.
