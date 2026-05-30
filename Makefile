# pdomain-index-pip -- static pip simple-index tooling
# Usage: make <target>

AI ?=
LOG := .ci-ai.log

ifdef AI
_goals := $(or $(MAKECMDGOALS),ci)
.PHONY: $(_goals)
$(_goals):
	@rm -f $(LOG)
	@$(MAKE) --no-print-directory AI= $@ > $(LOG) 2>&1 \
		&& echo "PASS $@ (log: $(LOG))" \
		|| (echo "FAIL $@:"; tail -50 $(LOG); echo "(full log: $(LOG))"; exit 1)

else

.PHONY: help setup install remove-venv reset reset-venv reset-full upgrade-deps format format-check lint lint-check typecheck test test-single test-k actionlint shell-check docs-check static-check pre-commit-check ci ci-slow regen build smoke smoke-regen clean release-patch release-minor release-major _do-release

OUT ?= _site/simple

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install locked development dependencies
	uv sync --group dev

install: setup ## Alias for setup

remove-venv: ## Remove the virtual environment
	rm -rf .venv

reset-venv: reset ## Alias for reset

reset: ## Rebuild virtual environment after cleaning generated local state
	@$(MAKE) --no-print-directory clean
	@$(MAKE) --no-print-directory remove-venv
	@$(MAKE) --no-print-directory setup

reset-full: ## Rebuild environment after clearing the uv cache
	@$(MAKE) --no-print-directory clean
	@$(MAKE) --no-print-directory remove-venv
	uv cache clean
	@$(MAKE) --no-print-directory setup

upgrade-deps: ## Upgrade locked development dependencies and sync
	uv lock --upgrade
	uv sync --group dev

format: ## Format Python and Markdown files
	uv run ruff format scripts tests
	uv run ruff check --select I --fix scripts tests
	uv run ruff check --fix scripts tests
	uv run mdformat README.md CONVENTIONS.md docs

lint-check: ## Read-only ruff format+check (no auto-fix; matches CI exactly)
	uv run ruff format --check scripts tests
	uv run ruff check scripts tests

format-check: lint-check ## Alias for lint-check

lint: ## Run Python linting and import sorting with auto-fix
	uv run ruff check --select I --fix scripts tests
	uv run ruff check --fix scripts tests

typecheck: ## Run basedpyright
	uv run basedpyright scripts tests

test: ## Run the pytest suite
	uv run pytest tests -q

test-single: ## Run one pytest node id (usage: make test-single TEST='tests/...::test_name')
	@if [ -z "$(TEST)" ]; then \
		echo "ERROR: missing TEST parameter"; \
		echo "Example: make test-single TEST='tests/test_regen_index.py::test_repo_allowlist_uses_current_pdomain_names'"; \
		exit 2; \
	fi
	uv run pytest "$(TEST)" -q

test-k: ## Run tests by pytest -k expression (usage: make test-k K='pattern')
	@if [ -z "$(K)" ]; then \
		echo "ERROR: missing K parameter"; \
		echo "Example: make test-k K='repo_allowlist'"; \
		exit 2; \
	fi
	uv run pytest tests -q -k "$(K)"

actionlint: ## Lint GitHub Actions workflows
	uv run actionlint .github/workflows/*.yml

shell-check: ## Check shell scripts with ShellCheck
	uv run shellcheck -x scripts/*.sh

docs-check: ## Check Markdown formatting
	uv run mdformat --check README.md CONVENTIONS.md docs

static-check: lint-check typecheck actionlint shell-check docs-check ## Run all read-only static checks

pre-commit-check: static-check ## Workspace-compatible alias for static checks

ci: setup static-check test ## Run complete local CI

ci-slow: ci ## Full pre-flight alias; no extra slow checks exist today

regen: ## Regenerate the simple index; override OUT=path as needed
	uv run python scripts/regen_index.py --out "$(OUT)"

build: regen ## Build the static simple index under OUT (default: _site/simple)

smoke: smoke-regen ## Alias for smoke-regen

smoke-regen: ## Safely regenerate the simple index into a temporary directory
	@tmpdir=$$(mktemp -d); \
	trap 'rm -rf "$$tmpdir"' EXIT; \
	$(MAKE) --no-print-directory regen OUT="$$tmpdir/simple"; \
	test -f "$$tmpdir/simple/index.html"; \
	echo "smoke regen wrote $$tmpdir/simple/index.html"

clean: ## Remove local caches and generated site output
	rm -rf _site .pytest_cache .ruff_cache .basedpyright .ci-ai.log
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

release-patch: ## Release: bump patch, run ci, tag, push, trigger release workflow
	@$(MAKE) --no-print-directory _do-release BUMP=patch

release-minor: ## Release: bump minor, run ci, tag, push, trigger release workflow
	@$(MAKE) --no-print-directory _do-release BUMP=minor

release-major: ## Release: bump major, run ci, tag, push, trigger release workflow
	@$(MAKE) --no-print-directory _do-release BUMP=major

# scripts/do-release.sh handles repo-state guards, runs the make ci pre-flight,
# creates the three-component tag, pushes main + exact tag, then dispatches
# .github/workflows/release.yml with that tag.
# Pass FORCE=1 to skip repo-state guards (pre-flight still runs).
# Pass SKIP_PUSH=1 to create the tag locally without pushing.
_do-release:
	@BUMP=$(or $(BUMP),minor) ./scripts/do-release.sh

endif
