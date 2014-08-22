# Copyright (C) 2014 Bevbot LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Config file templates for the kegberry tool."""

from string import Template

# Required variables:
#  DATA_DIR: Kegbot data directory.
#  SERVER_VENV: Kegbot-server virtualenv base directory
#  PYCORE_VENV: Pycore virtualenv base directory.
#  HOME_DIR: Kegbot user home dir.
#  USER: Kegbot user.

NGINX_CONF = Template("""
### Kegbot nginx.conf file -- Kegberry edition.

upstream kegbot {
  server 127.0.0.1:8000;
}

server {
  listen 80;
  tcp_nopush on;
  tcp_nodelay on;

  gzip on;
  gzip_disable "msie6";
  gzip_types text/plain text/css application/x-javascript text/xml application/xml application/xml+rss text/javascript;
  gzip_vary on;

  keepalive_timeout 0;
  client_max_body_size 10m;

  location / {
    proxy_redirect      off;
    proxy_set_header    Host                    $$host;
    proxy_set_header    X-Real-IP               $$remote_addr;
    proxy_set_header    X-Forwarded-For         $$proxy_add_x_forwarded_for;
    proxy_set_header    X-Forwarded-Protocol    $$scheme;
    proxy_pass          http://kegbot;
    proxy_connect_timeout 60s;
    proxy_read_timeout 120s;

  }

  location /media/ {
    alias           $DATA_DIR/media/;
    access_log      off;
    log_not_found   off;
    expires         7d;
    add_header      pragma public;
    add_header      cache-control "public";
  }

  location /static/ {
    alias           $DATA_DIR/static/;
    access_log      off;
    log_not_found   off;
    expires         7d;
    add_header      pragma public;
    add_header      cache-control "public";
  }

  location /robots.txt {
    root            $DATA_DIR/static/;
    access_log      off;
    log_not_found   off;
  }

  location /favicon.ico {
    root            $DATA_DIR/static/;
    access_log      off;
    log_not_found   off;
  }
}
""")

SUPERVISOR_CONF = Template("""
### Supervisor.conf for Kegbot -- Kegberry edition.

[group:kegbot]
programs=gunicorn,celery,kegbot_core,kegboard_daemon

[program:gunicorn]
command=su -l $USER -c '$SERVER_VENV/bin/kegbot run_gunicorn --settings=pykeg.settings --timeout=120 -w 2'
directory=$HOME_DIR
autostart=true
autorestart=true
redirect_stderr=true
startsecs=30

[program:celery]
command=su -l $USER -c 'sleep 10; $SERVER_VENV/bin/kegbot run_workers'
directory=$HOME_DIR
autostart=true
autorestart=true
redirect_stderr=true
startsecs=40

[program:kegbot_core]
command=su -l $USER -c 'sleep 15; $PYCORE_VENV/bin/kegbot_core.py --flagfile=$HOME_DIR/.kegbot/pycore-flags.txt'
directory=$HOME_DIR
autostart=true
autorestart=true
redirect_stderr=true
startsecs=45

[program:kegboard_daemon]
command=su -l $USER -c 'sleep 20; $PYCORE_VENV/bin/kegboard_daemon.py'
directory=$HOME_DIR
autostart=true
autorestart=true
redirect_stderr=true
startsecs=50

""")