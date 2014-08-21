#!/bin/bash
# Kegberry install script.
# Source: https://github.com/Kegbot/kegberry

set -e
set -x

export PATH="$PATH:/usr/lib/pypy-upstream/bin"

sudo PATH=$PATH easy_install-pypy pip
sudo PATH=$PATH pip install -U virtualenv kegberry
kegberry install

