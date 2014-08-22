---
layout: page
permalink: /
title: "Kegberry: Raspberry Pi Beer Keg Monitor and Digital Taplist"
description: Kegberry is a free system that a Raspberry Pi into a digital tap list and beer keg monitor.
tags: [Kegberry, Kegbot]
image:
  feature: abstract-1.jpg
---

# Say Hello to Kegberry

You've got a Raspberry Pi and you love beer on tap.  Now what? *Make it a
Kegberry*.

## What can it do?

* **Keg Volume Monitor.** Want to know what's left?  With a little extra
  hardware, your Kegberry becomes a powerful and battle-tested keg monitor.
* **Digital Tap List.**  Give your taps an internet presence.  Kegberry's
  server lets everyone know what's on tap.
* **Twitter, Untappd, and more.** Links to [Untappd](https://untappd.com/)
  for beverage information; posts to your site's Twitter account when you
  add and remove kegs.
* **Notification System.** Want to be alerted when the keg is running low,
  or when someone has started pouring?  No problem; Kegberry does it all.
* **Account System.** Give your friends and family access to your data, and
  enable privacy modes to keep others out.

<!-- <figure class="half">
  <img src="/images/image-filename-1.jpg" alt="">
  <img src="/images/image-filename-2.jpg" alt="">
</figure>
 -->

## What does it cost?

**It's free!** You provide the Raspberry Pi and optional HDMI display,
we give you the software for free.


## Installation

It's easy to install Kegberry! You can flash our pre-installed system
image, or install within Raspbian.


### Option 1: Flash New Image

Download our
[customized Raspbian image](https://github.com/Kegbot/kegberry/releases),
install it to an new SD card as usual, and navigate to your Pi in your web browser.
Kegberry is running and ready to go!


### Option 2: Install Within Raspbian

Run our simple install script on your Raspbian system:

```
bash -c "$(curl -fsSL https://raw.github.com/Kegbot/kegberry/master/install.sh)"
```

The installer is fully automatic, and should take about 10-15 minutes to complete
depending on your connection speed. Once finished, your system will be online at
**http://your-ip/**

*Problems? We recommend starting with a fresh image.*


## Help and Support

* Join the [kegberry-announce](https://groups.google.com/forum/#!forum/kegberry-announce)
  mailing list to be informed of new releases. 
* Check out the [Kegberry Forum](http://forum.kegbot.org/discussions/kegbot-kegberry),
  where you can talk to other users for help and support.
* IRC user? Join us in `#kegbot` on `irc.freenode.net`.
* Think you've found a software bug? Submit it to the
  [Kegberry issue tracker](https://github.com/Kegbot/kegberry/issues).


## License and Credit

Kegberry is brought to you by Bevbot LLC, the same team that
invented [Kegbot](https://kegbot.org/).

Kegberry is licensed under the
[Apache 2 License](https://github.com/Kegbot/kegberry/blob/master/LICENSE.txt).

Please note, unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
