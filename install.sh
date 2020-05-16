#!/bin/bash
# Kegberry install script.
# Source: https://github.com/Kegbot/kegberry

set -e

COMPOSE_TEMPLATE="version: '3.0'

services:
  kegbot:
    image: kegbot/server:latest
    restart: always
    ports:
      - '8000:8000'
    volumes:
      - _kegbot_data_dir_:/kegbot-data
    tmpfs:
      - /tmp
      - /var/tmp
    environment:
      KEGBOT_REDIS_URL: 'redis://redis:6379/0'
      KEGBOT_DATABASE_URL: 'mysql://kegbot_dev:changeme@mysql/kegbot_dev'
      KEGBOT_SETUP_ENABLED: 'true'
      KEGBOT_DEBUG: 'true'
      KEGBOT_SECRET_KEY: '_kegbot_secret_key_'
      KEGBOT_INSECURE_SHARED_API_KEY: '_kegbot_insecure_shared_api_key_'

  workers:
    image: kegbot/server:latest
    restart: always
    command: bin/kegbot run_workers
    volumes:
      - _kegbot_data_dir_:/kegbot-data
    tmpfs:
      - /tmp
      - /var/tmp
    environment:
      KEGBOT_REDIS_URL: redis://redis:6379/0
      KEGBOT_DATABASE_URL: mysql://kegbot_dev:changeme@mysql/kegbot_dev
      KEGBOT_SETUP_ENABLED: 'true'
      KEGBOT_DEBUG: 'true'
      KEGBOT_SECRET_KEY: '_kegbot_secret_key_'

  mysql:
    image: kegbot/mariadb:latest
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: 'changeme'
      MYSQL_USER: 'kegbot_dev'
      MYSQL_PASSWORD: 'changeme'
      MYSQL_DATABASE: 'kegbot_dev'
    tmpfs:
      - /tmp
      - /var/tmp
    volumes:
      - _mysql_data_dir_:/var/lib/mysql

  redis:
    image: redis:latest
    restart: always

  pycore:
    image: kegbot/pycore:latest
    restart: always
    tmpfs:
      - /tmp
      - /var/tmp
    environment:
      KEGBOT_REDIS_URL: redis://redis:6379/0
      KEGBOT_API_KEY: '_kegbot_insecure_shared_api_key_'
      KEGBOT_API_URL: 'http://kegbot:8000/api/'

  kegboard:
    image: kegbot/pycore:latest
    restart: always
    command: bin/kegboard_daemon.py --kegboard_device=/dev/ttyACM0
    tmpfs:
      - /tmp
      - /var/tmp
    environment:
      KEGBOT_REDIS_URL: redis://redis:6379/0
    devices:
      - /dev/ttyACM0:/dev/ttyACM0
      - /dev/bus/usb:/dev/bus/usb

volumes:
  mysql-data:
  kegbot-data:
"

log() {
    echo "--- $@"
}

warning() {
    echo "WARNING: $@"
}

ensure_docker() {
    log "Checking for docker ..."
    docker_status=`which docker`
    if [ $? -ne 0 ]; then
        log "Docker not installed, installing ..."
        curl -sSL https://get.docker.com | sh
        sudo usermod -aG docker $USER
    fi

    docker_version=`docker --version`
    if [ $? -ne 0 ]; then
        log "Docker version could not be determined"
    else
        log "Docker version ${docker_version} - great!"
    fi

    log "Testing docker ..."
    docker run hello-world 2>&1 > /dev/null
    log "Docker works!"
}

ensure_python() {
    log "Checking for python ..."
    python_status=`which python3`
    if [ $? -ne 0 ]; then
        log "Python not installed, installing ..."
        sudo apt-get install -y libffi-dev libssl-dev
        sudo apt-get install -y python3 python3-pip
        sudo apt-get remove python-configparser || true
    fi

    python_version=`python3 --version 2>&1`
    if [ $? -ne 0 ]; then
        log "Python3 version could not be determined"
        exit 1
    fi
    log "Python version ${python_version} - great!"
}

ensure_docker_compose() {
    log "Checking for docker-compose ..."
    docker_compose_status=`which docker-compose`
    if [ $? -ne 0 ]; then
        log "docker-compose not installed, installing ..."
        sudo pip3 install docker-compose
    fi

    docker_compose=`docker-compose --version`
    if [ $? -ne 0 ]; then
        log "docker-compose version could not be determined"
    else
        log "docker-compose version ${docker_compose} - great!"
    fi
}

ensure_all_dependencies() {
    ensure_docker
    ensure_python
    ensure_docker_compose
}

setup_vars() {
    DISTRO_NAME=$(lsb_release -s -i 2>/dev/null || echo -n "Unknown")

    if [ "${DISTRO_NAME}" != "Raspbian" ]; then
        warning "Kegberry is meant to be run on Raspbian, but your distro is '${DISTRO_NAME}'"
        read -p "Proceed anyway? [y/N]: " proceed_str
        proceed_str=${proceed_str:-No}
        case "${proceed_str}" in
            [yY][eE][sS]|[yY])
                true
                ;;
            *)
                log "Exiting."
                exit 1
                ;;
        esac
    fi

    KEGBERRY_DIR="$HOME/kegberry"
    if [[ -d "${KEGBERRY_DIR}" ]]; then
        echo "Found a Kegbot directory at ${KEGBERRY_DIR}"
        read -p "Use this as the kegberry dir? [n/Y]: " proceed_str
        proceed_str=${proceed_str:-Yes}
        case "${proceed_str}" in
            [yY][eE][sS]|[yY])
                ;;
            *)
                log "Exiting."
                exit 1
                ;;
        esac
    fi

    KEGBOT_DATA_DIR="${KEGBERRY_DIR}/data"
    if [[ -d "${KEGBOT_DATA_DIR}" ]]; then
        echo "Found a Kegbot data directory at ${KEGBOT_DATA_DIR}"
        read -p "Proceed and use this as data dir? [n/Y]: " proceed_str
        proceed_str=${proceed_str:-Yes}
        case "${proceed_str}" in
            [yY][eE][sS]|[yY])
                ;;
            *)
                log "Exiting."
                exit 1
                ;;
        esac
    fi

    MYSQL_DATA_DIR="${KEGBERRY_DIR}/mysql"
    if [[ -d "${MYSQL_DATA_DIR}" ]]; then
        echo "Found a mysql data directory at ${MYSQL_DATA_DIR}"
        read -p "Proceed and use this as mysql dir? [n/Y]: " proceed_str
        proceed_str=${proceed_str:-Yes}
        case "${proceed_str}" in
            [yY][eE][sS]|[yY])
                ;;
            *)
                log "Exiting."
                exit 1
                ;;
        esac
    fi

    DOCKER_COMPOSE_FILE="${KEGBERRY_DIR}/docker-compose.yml"
    if [[ -e "${DOCKER_COMPOSE_FILE}" ]]; then
        warning "Docker compose config already exists at ${DOCKER_COMPOSE_FILE}."
        read -p "Proceed anyway and overwrite? [y/N]: " proceed_str
        proceed_str=${proceed_str:-No}
        case "${proceed_str}" in
            [yY][eE][sS]|[yY])
                true
                ;;
            *)
                log "Exiting."
                exit 1
                ;;
        esac
    fi

    KEGBOT_SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
    KEGBOT_INSECURE_SHARED_API_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
}

do_install() {
    setup_vars
    ensure_all_dependencies

    log "Installing ..."

    log "Setting up directories ..."
    mkdir -p ${KEGBOT_DATA_DIR}
    mkdir -p ${KEGBERRY_DIR}
    mkdir -p ${MYSQL_DATA_DIR}

    log "Installing docker compose file at ${DOCKER_COMPOSE_FILE} ..."
    echo -e "${COMPOSE_TEMPLATE}" > ${DOCKER_COMPOSE_FILE}
    sed -i -e "s%_kegbot_data_dir_%${KEGBOT_DATA_DIR}%" ${DOCKER_COMPOSE_FILE}
    sed -i -e "s%_mysql_data_dir_%${MYSQL_DATA_DIR}%" ${DOCKER_COMPOSE_FILE}
    sed -i -e "s%_kegbot_secret_key_%${KEGBOT_SECRET_KEY}%" ${DOCKER_COMPOSE_FILE}
    sed -i -e "s%_kegbot_insecure_shared_api_key_%${KEGBOT_INSECURE_SHARED_API_KEY}%" ${DOCKER_COMPOSE_FILE}

    log "Fetching images ..."
    docker-compose -f ${DOCKER_COMPOSE_FILE} pull

    log "Done!"
    echo ""
    echo "To run, do the following: "
    echo ""
    echo "    $ cd ${KEGBERRY_DIR}"
    echo "    $ docker-compose up"
    echo ""
    echo "To run in the background, use:"
    echo ""
    echo "    $ docker-compose up -d"
    echo ""
    echo "Enjoy!"

}

do_install