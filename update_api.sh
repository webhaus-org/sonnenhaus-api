#! /usr/bin/env bash

own_dir="$(dirname "${BASH_SOURCE[0]}")"

# usage:
# update_api.sh <systemd-unit-name>

set -euo pipefail

git \
  -C "${own_dir}" \
  pull origin master --rebase

sudo systemctl restart "${1}"
