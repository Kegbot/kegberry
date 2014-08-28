---
layout: page
permalink: /install/
title: Install Kegberry
image:
  feature: bevbot-bubbles-2.jpg
share: true
---

We've worked hard to make Kegberry painless to install.
You can flash our pre-installed system image, or install on a working
Raspbian system.

## Option 1: Flash New Image

Download our
[customized Raspbian image](https://github.com/Kegbot/kegberry/releases/tag/2.0.0b3),
install it to an new SD card as usual, and navigate to your Pi in your web browser.
Kegberry is running and ready to go.


## Option 2: Install Within Raspbian

Run our simple install script on your Raspbian system:

```
bash -c "$(curl -fsSL https://raw.github.com/Kegbot/kegberry/master/install.sh)"
```

The installer is fully automatic, and should take about 10-15 minutes to complete
depending on your connection speed. Once finished, your system will be online at
**http://your-ip/**

*Problems? We recommend starting with a fresh image.*

## Next Steps

Once your system is installed, the Kegbot Server will be running on
`http://your-ip`.  Navigate this page to complete the setup wizard and
access the admin console.

## Adding Flow Monitoring

Adding keg level and flow monitoring to your Kegberry system is easy, and
requires some extra hardware.

### What You Need

To monitor your kegs and taps, the fastest and *easiest* option is to grab a
[Single Tap Kegbot Kit](https://kegbot.org/get-kegbot/kegbot-hardware), which
includes all the hardware to monitor a single tap. (It also directly helps support
the project.)

You can get the kit from The Kegbot Store, or on Amazon:

* [Single Tap Kegbot Kit on The Kegbot Store](http://store.kegbot.org/products/kegbot-kit) ($135.99)
* [Single Tap Kegbot Kit on Amazon](http://amzn.to/1zXDbyO) ($139.99)

If you're technically savvy or just want more of an adventure, you can also
roll your own board using an Arduino; just
[flash the Kegboard firmware](https://github.com/Kegbot/kegboard) and add any meter you like.  

(We'll soon support monitoring via the Pi GPIO, too;
[follow GitHub issue #6](https://github.com/Kegbot/kegberry/issues/6) for progress, and see the
[FAQ](/faq/) for more recommendations.)


### Installing the Kits

First, follow the
[Kegbot Getting Started Guide](https://kegbot.org/docs/getting-started/hardware-installation/)
to connect your flow meters to your beer lines.

Next, connect the controller board(s) to the Raspberry Pi via USB.  Within a few
seconds, you should see a new Controller listed in the Kegbot Admin console.

### Linking Controllers to Taps

Once you have added a controller, you must tell the system which tap it 
is connected to.

In the web interface, select **Admin -> Taps** and click on a tap to edit.
In the **Flow Meter** section, select **kegboard-01234567.flow0**, substituting
`01234567` for the last 8 digits of your controller's serial number, which
you should see in the list.
