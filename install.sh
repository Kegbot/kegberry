#!/bin/bash
# Kegberry install script.
# Source: https://github.com/Kegbot/kegberry

set -e
set -x

sudo easy_install-pypy pip
sudo pip install -U kegberry
kegberry install