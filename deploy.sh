#!/usr/bin/env bash
set -euo pipefail

# june.kim now builds from the unified Astro project.
# This script delegates to junekim-migrates/deploy.sh.

MIGRATE_DIR="$HOME/Documents/junekim-migrates"

if [[ ! -d "$MIGRATE_DIR" ]]; then
  echo "ERROR: $MIGRATE_DIR not found."
  echo "       The site now builds from the Astro project, not Jekyll."
  exit 1
fi

cd "$MIGRATE_DIR"
exec bash deploy.sh "$@"
