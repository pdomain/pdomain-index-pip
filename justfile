set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
set positional-arguments

# Copy this wrapper and install-hooks with the shell setting to sibling justfiles.
[private]
_ai +args:
    #!/usr/bin/env bash
    set -euo pipefail
    if env AI= just --quiet "$@" > .ci-ai.log 2>&1; then
        printf 'PASS: %s\n' "$*"
    else
        result=$?
        printf 'FAIL: %s (exit %s)\n' "$*" "$result"
        if [[ -f scripts/ai_filter_log.py ]]; then
            uv run python scripts/ai_filter_log.py .ci-ai.log
        else
            tail -50 .ci-ai.log
        fi
        exit "$result"
    fi

install-hooks:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai install-hooks; fi
    if [[ -f .git ]]; then
        echo "hooks: worktree checkout - the canonical repo owns them, skipping"
    elif [[ -n "$(git config --get core.hooksPath || true)" ]]; then
        echo "hooks: core.hooksPath is set - leaving it alone, skipping"
    else
        uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
    fi

help:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai help; fi
    just --list

setup:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai setup; fi
    uv sync --locked --group dev
    just --quiet install-hooks

install:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai install; fi
    just --quiet setup

remove-venv:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai remove-venv; fi
    rm -rf "${UV_PROJECT_ENVIRONMENT:-.venv}"

reset:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai reset; fi
    just --quiet clean remove-venv setup

reset-venv:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai reset-venv; fi
    just --quiet reset

reset-full:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai reset-full; fi
    just --quiet clean remove-venv
    uv cache clean
    just --quiet setup

update-hooks:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai update-hooks; fi
    uv run pre-commit autoupdate --freeze

lint:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai lint; fi
    uv run ruff check --select I --fix scripts tests
    uv run ruff check --fix scripts tests

lint-check:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai lint-check; fi
    uv run ruff format --check scripts tests
    uv run ruff check scripts tests

format:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai format; fi
    uv run ruff format scripts tests
    uv run mdformat README.md CONVENTIONS.md docs

format-check:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai format-check; fi
    uv run ruff format --check scripts tests

typecheck:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai typecheck; fi
    uv run basedpyright scripts tests

test:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai test; fi
    uv run pytest -n auto tests -q

test-single:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai test-single; fi
    if [[ -z "${TEST:-}" ]]; then
        echo "ERROR: missing TEST parameter" >&2
        exit 2
    fi
    uv run pytest "$TEST" -q

test-k:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai test-k; fi
    if [[ -z "${K:-}" ]]; then
        echo "ERROR: missing K parameter" >&2
        exit 2
    fi
    uv run pytest tests -q -k "$K"

actionlint:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai actionlint; fi
    if compgen -G '.github/workflows/*.yml' >/dev/null; then
        uv run actionlint .github/workflows/*.yml
    else
        echo "  [actionlint] no workflows present - skipping."
    fi

shell-check:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai shell-check; fi
    uv run shellcheck -x scripts/*.sh

docs-check:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai docs-check; fi
    uv run mdformat --check README.md CONVENTIONS.md $(find docs -name "*.md" ! -path "docs/issues/TEMPLATE.md")

static-check:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai static-check; fi
    just --quiet lint-check typecheck actionlint shell-check docs-check

pre-commit-check:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai pre-commit-check; fi
    uv run pre-commit run --all-files

[default]
ci:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai ci; fi
    just --quiet setup pre-commit-check lint-check typecheck actionlint shell-check docs-check test build
    docgraph check --strict

ci-slow:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai ci-slow; fi
    just --quiet ci

regen:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai regen; fi
    uv run python scripts/regen_index.py --out "${OUT:-_site/simple}"

build:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai build; fi
    just --quiet regen

smoke:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai smoke; fi
    just --quiet smoke-regen

smoke-regen:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai smoke-regen; fi
    tmpdir=$(mktemp -d)
    trap 'rm -rf "$tmpdir"' EXIT
    OUT="$tmpdir/simple" just --quiet regen
    test -f "$tmpdir/simple/index.html"
    echo "smoke regen wrote $tmpdir/simple/index.html"

clean:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai clean; fi
    # Keep the log while the AI wrapper has stdout open on it.
    if [[ ! .ci-ai.log -ef /dev/stdout ]]; then rm -f .ci-ai.log; fi
    rm -rf _site .pytest_cache .ruff_cache .basedpyright
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

upgrade-deps:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai upgrade-deps; fi
    for marker in "${UV_PROJECT_ENVIRONMENT:-.venv}/.pdomain-local-mode" "${UV_PROJECT_ENVIRONMENT:-.venv}/.pdomain-dev-local"; do
        if [[ -f "$marker" ]]; then
            echo "Refusing dependency upgrades while $marker exists" >&2
            exit 1
        fi
    done
    uv lock --upgrade
    uv sync --group dev

release-patch:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai release-patch; fi
    BUMP=patch ./scripts/do-release.sh

release-minor:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai release-minor; fi
    BUMP=minor ./scripts/do-release.sh

release-major:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai release-major; fi
    BUMP=major ./scripts/do-release.sh

_do-release:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${AI:-}" ]]; then exec just --quiet _ai _do-release; fi
    BUMP="${BUMP:-minor}" ./scripts/do-release.sh
