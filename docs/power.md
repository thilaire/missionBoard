# Smart switch for the raspberry Pi

First, the [micro-controller](ATtiny.md) and the [Raspberry Pi](RPi.md) were powered through the key-switch B1-SW2 (5V came from the transformer to the micro-USB of the Raspberry via the switch, and then the ATtiny was powered by the 3.3V of the Raspberry).

But, I was not safe to turn off directly the Raspberry Pi without shut it down (with commands like `shutdown`).
So, now, the ATtiny is always on (powered by a dedicated 5v-to-3.3v converter), and command a mecanical relay ()