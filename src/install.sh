#!/bin/bash
# Kegberry install script.
# Source: https://github.com/Kegbot/kegberry

set -e
set -x

### Configuration section

REQUIRED_PACKAGES="nginx-light libjpeg-dev supervisor python-setuptools python-dev libsqlite3-dev libmysqlclient-dev mysql-server memcached redis-server"
KEGBERRY_DIR="/etc/kegberry"

KEGBOT_PIP_NAME="kegbot"
PYCORE_PIP_NAME="kegbot-pycore"

NGINX_CONF_URL="https://raw.github.com/Kegbot/kegberry/master/system-files/kegbot-nginx.conf"
SUPERVISOR_CONF_URL="https://raw.github.com/Kegbot/kegberry/master/system-files/kegbot-supervisor.conf"

### Functions

error() {
  echo "Error: $@"
  exit 1
}

info() {
  echo "---" $@
}

do_apt_get() {
  sudo bash -c "DEBIAN_FRONTEND=noninteractive apt-get -yq $*"
}

install_kegberry() {
  sudo mkdir -p ${KEGBERRY_DIR}

  info "Updating distro ..."
  do_apt_get update
  do_apt_get upgrade

  info "Installing required packages ..."
  do_apt_get install ${REQUIRED_PACKAGES}

  info "Installing pip ..."
  sudo easy_install-2.7 pip

  info "Installing Kegbot Server ..."
  sudo pip install -U ${KEGBOT_PIP_NAME}

  info "Installing Kegbot Pycore ..."
  sudo pip install -U ${PYCORE_PIP_NAME}

  info "Loading MySQL timezones ..."
  mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql

  info "Configuring Kegbot Server ..."
  mysqladmin -u root create kegbot || true
  setup-kegbot.py --db_type=mysql --interactive=false

  info "Generating API key ..."
  api_key=$(kegbot create_api_key "Kegberry")
  mkdir -p /home/pi/.kegbot/
  echo "--api_url=http://localhost/api/" > /home/pi/.kegbot/pycore-flags.txt
  echo "--api_key=${api_key}" >> /home/pi/.kegbot/pycore-flags.txt

  info "Installing configs ..."
  sudo bash -c "curl -o /etc/nginx/sites-available/default ${NGINX_CONF_URL}"
  sudo bash -c "curl -o /etc/supervisor/conf.d/kegbot.conf ${SUPERVISOR_CONF_URL}"

  info "Restarting daemons ..."
  sudo supervisorctl reload
  sudo /etc/init.d/nginx restart

  info "Done! Kegbot has been installed."
}

### Main program
install_kegberry
