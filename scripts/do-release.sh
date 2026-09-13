#!/usr/bin/env bash
set -eu

RELEASE_REPO="pdomain/pdomain-index-pip"
# This repo publishes tooling, not a distributable: `make build` here
# regenerates the static index rather than producing a wheel. Release the
# tag alone.
RELEASE_BUILD=":"
RELEASE_PREFLIGHT="make ci"

# shellcheck source=scripts/release-common.sh
. "$(dirname "$0")/release-common.sh"
pd_release_main "$@"
