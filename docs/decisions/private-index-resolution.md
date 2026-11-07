---
Status: active
Owner: CT
Created: 2026-07-13
Last verified: 2026-11-07
Kind: decision
---

# Resolve pdomain packages through an explicit index

## Agent Index

- **Status:** active
- **Owner:** CT
- **Created:** 2026-07-13
- **Last verified:** 2026-11-07
- **Kind:** decision

## Context

Using a pdomain URL as an unrestricted extra index lets a resolver choose a
same-named package from the public default index. That creates a dependency
confusion risk for packages intended to come from the pdomain release-asset
index.

## Decision

Project configurations must declare the pdomain index as `explicit = true` and
map each private pdomain distribution to it with `[tool.uv.sources]`. This is the
repeatable package-to-index mechanism.

One-off commands must pin the target distribution to a direct wheel or artifact
URL instead of adding the private index as an unrestricted `--index`. Configure
authentication for the artifact host when access is private, and retain the generated
`#sha256=` fragment when one is available. A direct requirement fixes the target
package's source while leaving PyPI available for public transitive
dependencies.

Public dependencies continue to resolve from PyPI. A pdomain package moves to
PyPI only through a deliberate publishing and migration decision.

## Consequences

- A project mapping or direct artifact requirement fails when its pdomain source
  is unavailable instead of selecting a public package with the same name.
- Each consumer must list its pdomain package-to-index mappings.
- Adding the private index with `--index` alone is not a safe one-off pin because
  a missing project can still fall through by package name.
- Direct local wheel installs do not need an index option.

## Supersedes / Superseded-by

This supersedes README examples that used unrestricted `--index`,
`--extra-index-url`, or `explicit = false`. It has no superseding decision.
