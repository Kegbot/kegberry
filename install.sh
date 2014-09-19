#!/bin/bash
# Kegberry install script.
# Source: https://github.com/Kegbot/kegberry

set -e
set -x

sudo bash -c "DEBIAN_FRONTEND=noninteractive apt-get -yq install python-setuptools"
sudo easy_install pip
sudo pip install -U virtualenv
sudo pip install -U --pre kegberry
kegberry $INSTALLFLAGS install
