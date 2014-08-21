# Kegberry: Complete Beer Tap Monitoring for Raspberry Pi

Kegberry turns your Raspberry Pi into an complete beer tap monitoring
system!

**Main Repository:** https://github.com/Kegbot/kegberry

## Quickstart

Impatient? Try this!

```
$ bash -c "$(curl -fsSL https://raw.github.com/Kegbot/kegberry/master/src/install.sh)"
```

Read on for more detail.


## Background

Kegberry is based on and includes several opensource projects:

* [Kegbot Server](https://github.com/Kegbot/kegbot-server): Web user interface,
  database backend, API.
* [Kegbot Pycore](https://github.com/Kegbot/kegbot-pycore): Flow monitoring
  and sensing loop.
* [Kegboard](https://github.com/Kegbot/kegboard): Arduino-based firmware and
  schematics for flow sensing, temperature sensing (DS18B20), and
  RFID or OneWire-based authentication tokens.

For more information about Kegbot, see the
[Kegbot home page](https://kegbot.org).

## Install Guide

### Prerequisites

If you have a freshly installed Raspbian device, you're probably
good to go.

* **Kegbot Hardware**: You'll need the Kegbot hardware -- a flow meter and a
  controller board -- in order to collect and report data.  Support for using
  the Pi's GPIOs instead of a kegboard is [coming soon](https://github.com/Kegbot/kegberry/issues/6).
  See [Get Kegbot](https://kegbot.org/get-kegbot) for an overview of the hardware.
* **Dedicated Raspberry Pi**: The installer script assumes you'll be dedicating
  the target RPi to Kegberry; for example, it replaces the default nginx
  configuration with Kegbot's.
* **Raspbian**: These instructions assume you've installed a fresh copy of
  [Raspbian](http://www.raspbian.org/) on your RPi.  These instructions have
  been tested with version **2014-01-07**
  ([installation instructions](http://elinux.org/RPi_Easy_SD_Card_Setup)).

If your setup doesn't quite match these requirements, don't worry; at
the moment, Kegberry is just a shortcut.  Consult the
[full installation guide](https://kegbot.org/docs/server/) instead.


### Install Kegberry

Connect to your pi and run the following script:

```
$ bash -c "$(curl -fsSL https://raw.github.com/Kegbot/kegberry/master/src/install.sh)"
```

Sit back and relax as [kegbot-server](https://github.com/Kegbot/kegbot-server),
MySQL, and all related dependencies are installed and configured for you.


### Configure Kegbot Server

Once Kegberry has finished installing your system, you're ready to sign in
and configure your shiny new Kegbot Server.

Navigate to your RPi's IP address in your browser and you should see the
setup wizard.

Once you complete setup, reboot.


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


## News and Updates

Join the [kegberry-announce](https://groups.google.com/forum/#!forum/kegberry-announce)
mailing list to be informed of new releases.

For release notes, see `CHANGELOG.md`.


## License and Copyright

All code and documentation are Copyright 2014 Bevbot LLC, unless
otherwise noted.

Code is licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0),
or in the file `LICENSE.txt`.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"Kegberry", "Kegbot", and the Kegbot logo are trademarks of Bevbot LLC;
please don't reuse them without our permission.
