# Kegberry: Kegbot for Raspberry Pi

## Overview

Kegberry turns your Raspberry Pi into a Kegbot Kegerator Server.

Using the [Kegbot Server](https://github.com/Kegbot/kegbot) software,
your RPi can manage your beer taps, record drinks, control access, and more.
For more information about Kegbot, see the
[Kegbot home page](https://kegbot.org).

Since [Kegbot Server](https://github.com/Kegbot/kegbot) is a Python/Django
application, most of the work here is simply glue to automate
and simplify running it on Raspbian.

**Main Repository:** https://github.com/Kegbot/kegberry


## Instructions

### 0. Prerequisites

If you have a freshly installed Raspbian device, you're probably
good to go.

#### Dedicated Raspberry Pi

Obviously, you need a Rasberry Pi.

The installer script assumes you'll be dedicating this device to Kegberry;
for example, it replaces the default nginx configuration with Kegbot's.
(If you need to install Kegbot Server on a shared RPi for some reason,
follow the normal [installation guide](https://kegbot.org/docs/server/).)

#### Raspbian 2014-01-07

These instructions assume you've installed a fresh copy of
[Raspbian](http://www.raspbian.org/) on your RPi.  These instructions have
been tested with version **2014-01-07**.

Consult the [installation instructions](http://elinux.org/RPi_Easy_SD_Card_Setup)
if you haven't already installed Raspbian.

#### `pi` User

Configuration files assume we'll be running Kegbot as the `pi` user.
If you'd prefer to use a different account, you'll need to make these
adjustments after installing Kegberry.


### 1. Install Kegberry

Connect to your pi and run the following script:

```
$ bash -c "$(curl -fsSL https://raw.github.com/Kegbot/kegberry/master/src/install.sh)"
```

Sit back and relax as [kegbot-server](https://github.com/Kegbot/kegbot-server),
MySQL, and all related dependencies are installed and configured for you.


### 2. Configure Kegbot Server

Once Kegberry has finished installing your system, you're ready to sign in
and configure your shiny new Kegbot Server.

Navigate to your RPi's IP address in your browser and you should see the
setup wizard.


## Troubleshooting

To report a problem, please use the
[Kegberry issue tracker](https://github.com/Kegbot/kegberry/issues).


## Upgrading

### Upgrading Kegbot Server

Upgrading `kegbot-server` on a Kegberry device follows the same steps as on
any other Linux server.  See the
[official upgrade docs](https://kegbot.org/docs/server/upgrade-kegbot/) for more
details.

### Upgrading the entire Kegberry image

Kegberry does not (yet) include a full-system updater.  To upgrade a device, we
advise you to backup all data, install a new system image, and re-run the
kegberry installer from scratch.


## Caveats

The RPi is an amazing device, but Kegbot Server was written to target machines
with much greater computing resources.  You may find the server to be
substantially slower than on a "real" machine.

Kegberry currently does not provide any extra tools for backing up or restoring
your server data.  You should make regular backups of your MySQL database and
uploaded media (`~pi/kegbot-data/media`).

Since Kegbot runs as the `pi` user, and since the `pi` user has `sudo` access
in Raspbian, a vulnerability in the Kegbot server could lead to a compromise
of the entire device.  You should run Kegbot as another user or remove
`sudo` access if this is a concern for you.


## License and Copyright

All code is offered under the GPLv2 license, unless otherwise noted. Please see
LICENSE.txt for the full license.

All code and documentation are Copyright 2014 Bevbot LLC, unless
otherwise noted.

"Kegberry", "Kegbot", and the Kegbot logo are trademarks of Bevbot LLC;
please don't reuse them without our permission.

