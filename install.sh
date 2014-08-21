#!/bin/bash
# Kegberry install script.
# Source: https://github.com/Kegbot/kegberry

set -e
set -x

sudo easy_install-2.7 pip
sudo pip install -U kegberry
kegberry install