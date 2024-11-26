#!/usr/bin/env bash

set -euo pipefail

function main() {
  if [ "$(whoami)" = "root" ]; then
    echo "WARNING: user is root"
    SUDO=
  else
    SUDO=sudo
  fi
  VENV_NAME='astro_pi_orbit-venv'
  
  DEPENDENCIES=(
    python3-pip
    python3-venv
  )
  echo "***************************"
  echo "Astro Pi Orbit (astro_pi_orbit)"
  echo "***************************"
  echo "I will need to use sudo to install some dependencies"
  echo "-------------------------------------------------------------"
  $SUDO apt-get update
  $SUDO apt-get install -y "${DEPENDENCIES[@]}"
  (cd "$HOME" && python3 -m venv --system-site-packages "$VENV_NAME")
  source "${HOME}/${VENV_NAME}/bin/activate"
  pip install astro_pi_orbit
  
  echo "-------------------------------------------------------------"
  echo "All done!"
  echo "Created virtual environment \"${VENV_NAME}\""
  echo "To use picamzero with Thonny, follow the instructions here:"
  echo "https://rpf.io/thonny-install"
}

main
