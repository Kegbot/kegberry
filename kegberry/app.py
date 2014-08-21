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

"""Kegberry tool: Kegbot installer for Raspberry Pi."""

import logging
import os
import sys
import gflags
import pkg_resources
import pwd
import random
import subprocess
import tempfile
from contextlib import closing

from kegberry import templates

FLAGS = gflags.FLAGS

gflags.DEFINE_string('kegberry_user', 'kegberry',
    'The user account which will be used for kegberry files.')

gflags.DEFINE_string('kegberry_home', '/home/kegberry',
    'Path to the data directory for Kegberry.')

gflags.DEFINE_boolean('verbose', False,
    'Log extra stuff.')

gflags.DEFINE_string('mysql_database', 'kegbot',
    'Database for the MySQL server.')

gflags.DEFINE_string('mysql_user', 'root',
    'User for the MySQL server.')

gflags.DEFINE_string('mysql_password', '',
    'Password for the MySQL user, if any.')

gflags.DEFINE_boolean('skip_package_update', False,
    'If set, skips "apt-get update/upgrade" during install/upgrade.')

gflags.DEFINE_string('kegbot_server_package', 'kegbot==1.0.1',
    '(Advanced use only.) Version of Kegbot Server to install.')

gflags.DEFINE_string('kegbot_pycore_package', 'kegbot-pycore==1.1.3',
    '(Advanced use only.) Version of Kegbot Pycore to install.')

gflags.DEFINE_boolean('fake', False,
    '(Advanced use only.) If true, external commands are not run.')

BANNER = r"""
     oOOOOOo
    ,|    oO  Kegberry v{} - http://kegberry.com
   //|     |
   \\|     |  "{}"
    `|     |      -- {}
     `-----`
"""

QUOTES = (
    ('He was a wise man who invented beer.', 'Plato'),
    ('Beer is made by men, wine by God.', 'Martin Luther'),
    ('Who cares how time advances? I am drinking ale today.', 'Edgar Allen Poe'),
    ('It takes beer to make thirst worthwhile.', 'German proverb'),
    ('Beer: So much more than just a breakfast drink.', 'Homer Simpson'),
    ('History flows forward on a river of beer.', 'Anonymous'),
    ('Work is the curse of the drinking classes.', 'Oscar Wilde'),
    ('For a quart of ale is a dish for a king.', 'William Shakespeare, "A Winter\'s Tale"'),
    ('Beer. Now there\'s a temporary solution.', 'Homer Simpson'),
)

STATUS_FILENAME = '.kegberry-info.json'

REQUIRED_PACKAGES = (
    'nginx-light',
    'libjpeg-dev',
    'supervisor',
    'python-setuptools',
    'python-dev',
    'libmysqlclient-dev',
    'mysql-server',
    'redis-server',
)

KEGBOT_VERSION = '1.0.1'

logger = logging.getLogger(__name__)

class KegberryError(Exception): pass
class CommandError(KegberryError): pass

def get_version():
    try:
        return pkg_resources.get_distribution('kegberry').version
    except pkg_resources.DistributionNotFound:
        return '0.0.0'


def run_command(cmd, fail_silently=False):
    logger.debug('Running command: {}'.format(cmd))
    if FLAGS.fake:
        return 0
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        if not fail_silently:
            print e.output
            print ''
            logger.error('Command returned error:')
            logger.error('  Command: {}'.format(cmd))
            logger.error('  Return code: {}'.format(e.returncode))
        raise e


def run_as_kegberry(cmd, **kwargs):
    cmd = cmd.replace('"', '\\"')
    wrapped = 'sudo su -l {} -c "{}"'.format(FLAGS.kegberry_user, cmd)
    return run_command(wrapped, kwargs)

def run_in_virtualenv(cmd, **kwargs):
    virtualenv = os.path.join(FLAGS.kegberry_home, 'kb')
    cmd = '. {}/bin/activate && {}'.format(virtualenv, cmd)
    return run_as_kegberry(cmd, **kwargs)

def run_mysql(subcommand, command='mysql', **kwargs):
    cmd = '{} -u {} '.format(command, FLAGS.mysql_user)
    if FLAGS.mysql_password:
        cmd += '-p="{}" '.format(FLAGS.mysql_password)
    cmd += subcommand
    return run_command(cmd, **kwargs)

def print_banner():
    version = get_version()
    quote, author = random.choice(QUOTES)
    print BANNER.format(version, quote, author)

def write_tempfile(data):
    fd, path = tempfile.mkstemp()
    with closing(os.fdopen(fd, 'w')) as tmp:
        tmp.write(data)
    return path


class KegberryApp(object):
    """Main command-line application."""
    def run(self):
        try:
            extra_argv = FLAGS(sys.argv)[1:]
        except gflags.FlagsError, e:
            self.help(error=e, exit=1)
        if FLAGS.verbose:
            level = logging.DEBUG
        else:
            level = logging.INFO
        # logging.basicConfig(level=level,
        #     format='%(asctime)s %(levelname)-8s (%(name)s) %(message)s')
        logging.basicConfig(level=level,
            format='%(levelname)-8s: %(message)s')

        if not extra_argv:
            self.help('Must give at least one command.', exit=1)

        command = extra_argv[0]
        args = extra_argv[1:]

        command_fn = getattr(self, command)
        if not command_fn:
            self.help('Error: command does not exist', exit=1)

        print_banner()
        command_fn(args=args)

    def help(self, error=None, exit=None):
        """Prints help information."""
        print 'Usage: {} ARGS\n{}\n\n'.format(sys.argv[0], FLAGS)
        if error:
            print 'Error: %s' % (error,)
        if exit is not None:
            print 'Exiting ...'
            sys.exit(exit)

    def status(self, args=None):
        status_file = os.path.join(FLAGS.kegberry_home, STATUS_FILENAME)
        print 'App version: {}'.format(get_version())
        if not os.path.exists(status_file):
            print 'Error: Kegberry does not seem to be installed.',
            print ' (Tried {})'.format(status_file)

    def _update_packages(self):
        if not FLAGS.skip_package_update:
            logger.info('Updating package list ...')
            run_command('sudo bash -c "DEBIAN_FRONTEND=noninteractive apt-get -yq update"')

            logger.info('Upgrading packages ...')
            run_command('sudo bash -c "DEBIAN_FRONTEND=noninteractive apt-get -yq upgrade"')

        logger.info('Installing required packages ...')
        run_command('sudo bash -c "DEBIAN_FRONTEND=noninteractive apt-get -yq install {}"'.format(
            ' '.join(REQUIRED_PACKAGES)))

    def install(self, args=None):
        """Performs an initial Kegberry install."""
        self._update_packages()

        logger.info('Checking if database exists ...')
        try:
            run_mysql(command='mysqlshow', subcommand=FLAGS.mysql_database, fail_silently=True)
        except subprocess.CalledProcessError:
            logger.info('Creating database ...')
            run_mysql('-e "create database {}"'.format(FLAGS.mysql_database))

        logger.info('Installing MySQL timezones ...')
        cmd = 'mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u {}'.format(FLAGS.mysql_user)
        if FLAGS.mysql_password:
            cmd += ' -p={}'.format(FLAGS.mysql_password)
        cmd += ' mysql'
        run_command(cmd)

        user = FLAGS.kegberry_user
        try:
            pwd.getpwnam(user)
        except KeyError:
            logger.info('User "{}" does not exist, creating ...'.format(user))
            run_command('sudo useradd -m {}'.format(user))

        logger.info('Checking/installing virtualenv ...')
        virtualenv = os.path.join(FLAGS.kegberry_home, 'kb')
        run_as_kegberry('if [ ! -e {} ]; then virtualenv {}; fi'.format(virtualenv, virtualenv))

        logger.info('Installing python packages ...')
        run_in_virtualenv('pip install {} {}'.format(
            FLAGS.kegbot_server_package, FLAGS.kegbot_pycore_package))

        logger.info('Installing Kegbot ...')
        cmd = 'setup-kegbot.py --interactive=false --db_type=mysql --db_database="{}"'.format(FLAGS.mysql_database)
        data_root = os.path.join(FLAGS.kegberry_home, 'kegbot-data')
        cmd += ' --data_root={}'.format(data_root)
        if FLAGS.mysql_password:
            cmd += ' --db_password="{}"'.format(FLAGS.mysql_password)
        run_in_virtualenv(cmd)

        logger.info('Generating API key ...')
        api_key = run_in_virtualenv('kegbot create_api_key Kegberry')

        api_cfg = "--api_url=http://localhost/api\\n--api_key={}\\n".format(api_key)
        run_as_kegberry('echo -e "{}" > ~/.kegbot/pycore-flags.txt'.format(api_cfg))
        run_as_kegberry('chmod 600 ~/.kegbot/pycore-flags.txt'.format(api_cfg))

        logger.info('Installing config files ...')
        template_vars = {
            'USER': FLAGS.kegberry_user,
            'HOME_DIR': FLAGS.kegberry_home,
            'DATA_DIR': data_root,
        }

        nginx_conf = write_tempfile(templates.NGINX_CONF.substitute(**template_vars))
        run_command('sudo bash -c "mv {} /etc/nginx/sites-available/default"'.format(nginx_conf))

        supervisor_conf = write_tempfile(templates.SUPERVISOR_CONF.substitute(**template_vars))
        run_command('sudo bash -c "mv {} /etc/supervisor/conf.d/kegbot.conf"'.format(supervisor_conf))

        logger.info('Reloading daemons ...')
        run_command('sudo bash -c "supervisorctl reload"')
        run_command('sudo bash -c "service nginx restart"')

    def upgrade(self, args=None):
        logger.info('Checking for `kegberry` command update')
        output = run_command('sudo bash -c "pip install -U kegberry"')
        if 'already up-to-date' in output[0]:
            logger.info('Command is already up-to-date.')
        else:
            logger.info('Kegberry command upgraded.')
            logger.info('Please run "kegberry upgrade" again.')
            return

    def delete(self, args=None):
        confirm = raw_input('REALLY delete all kegberry data? This is irreversible. Type YES: ')
        if confirm.strip() != 'YES':
            print 'Delete aborted.'
            sys.exit(1)

        logger.info('Stopping services ...')
        run_command('sudo supervisorctl stop all')

        logger.info('Deleting user "{}" ...'.format(FLAGS.kegberry_user))
        run_command('sudo userdel -r -f {}; true'.format(FLAGS.kegberry_user))

        logger.info('Dropping database "{}"'.format(FLAGS.mysql_database))
        run_mysql('-e "drop database {}"'.format(FLAGS.mysql_database))
