---
Status: active
Owner: CT
Created: 2026-05-21
Last verified: 2026-11-07
Kind: process
---

# AGENTS.md — pdomain-index-pip

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-05-21
- **Last verified:** 2026-11-07
- **Kind:** process
- **Read when:** planning, implementing, reviewing, or verifying repository work.
- **Search terms:** development workflow, worktree, CI, delegation, verification.

Canonical agent context for the `pdomain-index-pip` repo. [CLAUDE.md](CLAUDE.md)
is a symlink to this file; Codex and other assistants read this file directly.

## Before coding

These steps are workspace defaults for any coding task. **User-level settings
override them** — a user's own `~/.claude/CLAUDE.md`, `settings.json`, or a
direct instruction in the conversation takes precedence and may waive or
change any step below.

### Working principles

- **Use skills.** Invoke the relevant superpowers skill before starting —
  process skills first (`brainstorming`, `systematic-debugging`,
  `writing-plans`, `test-driven-development`), then implementation skills.
  If a skill applies, using it is not optional.
- **Write clearly.** Follow `docs/process/writing-style.md` for direct user
  updates, handoffs, final summaries, docs, reports, issue text, PR text, and
  user-facing copy. Keep agent communication short, clear, and easy to scan.
- **Delegate by default.** Dispatch subagents for non-trivial work: per-repo
  agents for repo changes, `Explore` for code searches. This keeps large tool
  output out of the parent context.
- **Parallelize.** Run independent tasks as concurrent subagents — multiple
  agent calls in a single message. Set `model: sonnet` on implementers and
  reviewers.

### Steps

1. **Check the working tree.** `git status --short`. Surface or resolve stray
   uncommitted work before starting — don't build on it.
1. **Read repo guidance.** This repo's `AGENTS.md` and [CONVENTIONS.md](CONVENTIONS.md) for
   repo-specific rules. `CLAUDE.md` is a symlink to `AGENTS.md`.
1. **Consult repository context.** Read [DOCGRAPH.md](DOCGRAPH.md) when present,
   then use its retrieval workflow and authored `docs/context/` ground truth.
   Also consult the relevant folders under `docs/`:
   `plans/` (the work plan), `specs/` (design specs — follow any `Spec:`
   pointer from the issue), `research/` (prior investigations), `decisions/`
   (ADRs / constraints), `architecture/` (shipped design).
1. **Check live issue status.** Read the governed record in
   [docs/issues/](docs/issues/README.md) and its linked plan. GitHub Issues is
   disabled; the [roadmap](docs/roadmap.md) lists remaining work.
1. **Check for in-flight work.** Open PRs and existing branches touching the
   same area, to avoid colliding with work-in-progress.
1. **Consult agent memory.** `.claude/agent-memory/<repo>/feedback_*.md` for
   corrections not yet promoted to `CONVENTIONS.md`.
1. **Locate code with `Explore` first.** Use an `Explore` subagent to find
   relevant files before broad `Read`/grep.
1. **Isolate in a worktree.** Never work directly in the interactive checkout.
   Use the `using-git-worktrees` skill
   to set up an isolated worktree. When delegating to a full-power
   implementation agent, pass `isolation: "worktree"` on the `Agent` call
   (skip for `-docs` agents and the `driver` agent). When an agent returns a
   worktree path + branch, use the `finishing-a-development-branch` skill to
   decide how to integrate.
1. **TDD.** Write the failing test first where the plan calls for it.
1. **Verify before committing.** Focused verification plus `just ci`.
1. **Commit locally; do not push** without explicit say-so.

<!-- workspace-process:end -->

## Agent-specific notes

### Claude

Skills are routed through the plugins listed in the detection report. Follow
`DOCGRAPH.md` for retrieval, lifecycle, and write-safety rules.

### Codex

Read [DOCGRAPH.md](DOCGRAPH.md) before docgraph work; its rules are
authoritative for retrieval, lifecycle, context, and write safety. This
subsection replaces the former standalone `CODEX.md`.

<!-- >>> repo-setup:repo-facts sha256:bdf6550b3e125b7dca57587d2b2714398c173fb8e0d46b8d1427664d8a33e0b6 -->

## Repository facts

`pdomain-index-pip` generates a PEP 503 "simple" Python package index from
GitHub release assets and publishes it as a static site.

- **Language:** Python, managed with `uv` (`uv.lock` present).
- **Source:** `scripts/` — `regen_index.py` (index generator),
  `publish-index.sh` (local publication), `do-release.sh`, `release-common.sh`.
- **Tests:** `tests/`, pytest.
- **Docs:** `docs/`, governed by docgraph (`docgraph.toml`, `DOCGRAPH.md`,
  authored ground truth under `docs/context/`).
- **Build output:** the generated index, written under `_site/simple` by
  default.
- **Toolchain:** ruff, basedpyright, pytest, mdformat, actionlint, shellcheck.

<!-- <<< repo-setup:repo-facts -->

<!-- >>> repo-setup:commands-and-gates sha256:6dfca4642352ea266a5032c325cdf7b338bb9aa1ea25408a264666709523ef00 -->

## Commands and gates

`just ci` is the full local gate. Run it before committing. The GitHub Actions
workflows were removed on 2026-09-13.

- `just ci` — complete local CI.
- `just static-check` — read-only checks: lint, typecheck, actionlint,
  shellcheck, docs.
- `just test` — pytest suite.
- `just docs-check` — Markdown formatting.
- `just regen` — regenerate the simple index.

Underlying tools, when a narrower run is needed:

- `uv run pytest`
- `uv run ruff check`
- `uv run ruff format`
- `uv run basedpyright`

Repository scripts: `scripts/regen_index.py`, `scripts/publish-index.sh`,
`scripts/do-release.sh`, and `scripts/release-common.sh`.

<!-- <<< repo-setup:commands-and-gates -->

<!-- >>> repo-setup:writing-and-review sha256:c4d04ecf9e9b9ece93d141ddc484d132e1e72449671a84c8abc179925a0bc0d6 -->

## Writing and review

- Route new durable reader-facing documents through `write-readably`.
- Route edits of existing prose through `edit-for-readability`.
- Adversarial review follows the consuming plugin's own policy.
- Python work follows the `writing-python` mandatory gate.

<!-- <<< repo-setup:writing-and-review -->
