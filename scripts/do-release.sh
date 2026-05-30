#!/usr/bin/env bash
set -eu

RELEASE_REPO="pdomain/pdomain-index-pip"
RELEASE_PREFLIGHT="make ci"

# shellcheck source=scripts/release-common.sh
. "$(dirname "$0")/release-common.sh"
pd_release_main "$@"
