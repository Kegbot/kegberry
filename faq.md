---
layout: page
permalink: /faq/
title: Kegberry FAQ
image:
  feature: bevbot-bubbles-2.jpg
share: true
---


## General

### Can I use Kegberry without flow sensing / extra hardware?

Yes.

Though Kegberry and Kegbot were designed to actively monitor kegs,
most features (including tap listing and keg management) work just as well
without it.


### Will Kegberry interfere with other programs on my Raspberry Pi?

No, most likely not.

We've taken care to install Kegberry in a special, isolated environment.
The Kegbot programs run as a special `kegberry` user, and all data
(aside from the database and two kegberry-specific configuration files)
is stored in this user's home directory.


### How is Kegberry different from Kegbot?

Kegberry *is* Kegbot, in a special package optimized for
Raspberry Pi.

Kegberry includes and is built atop the open source
[Kegbot Server](https://github.com/Kegbot/kegbot-server) and
[Kegbot Pycore](https://github.com/Kegbot/kegbot-pycore) packages,
but unless you're a developer this detail isn't very important.


### How is Kegberry different from the Kegbot Android App?

They both perform the same jobs, just in different ways.

In an Android-powered Kegbot, controllers attach directly to a tablet
and in turn the app reports data to a server (or saves it internally).
[Watch our Kickstarter video](https://www.youtube.com/watch?v=vR0pqkPFUsw)
for a 3 minute overview of how the Android system works.

Kegberry runs the same server, but uses a special sensor daemon
([pycore](https://github.com/Kegbot/kegbot-pycore)) instead of the Android
app.


## Flow Sensing

### How many taps can I monitor?

There isn't a hard limit.

Kegberry scales as you add more controllers via the USB port. So scaling
up is a simple matter of plugging in another USB device.

The Raspberry Pi is a small device in terms of available
memory and CPU, so bear in mind these resource limits when planning your
system.


### Why not use the Raspberry Pi GPIO?

We [will support this soon](https://github.com/Kegbot/kegberry/issues/6),
but using a [Kegbot Kit](http://store.kegbot.org/products/kegbot-kit) is superior.

We've been doing this for over 10 years and have built Kegbot-style systems
in almost every way imaginable.  The [Kegbot Kit](http://store.kegbot.org/products/kegbot-kit)
is the culmination of those many years of research: it's by far the easiest
way to get started and "just works".

Second, the Kegbot Kit is portable because Kegbot works on lots of systems,
not just Raspberry Pi.  If you find yourself wanting more horsepower one day,
you can simply plug your Kegboard into any workstation with USB support.
That's impossible with a Raspberry Pi board.

Finally, we know many of our users are tinkerers, so although we do recommend
a standard configuration, we've designed the system to be open at *all* levels.
Using a non-standard controller is only a matter of sending meter data to the 
[Kegbot API](https://kegbot.org/docs/api).

