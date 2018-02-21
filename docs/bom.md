# Bill of material


From the [functionalities](functionalities.md), we can deduce the bill of materials

# What I need

### Electronic devices
- 4 Bargraphs (for the oxygen, rocket fuel and spaceship levels)
- 7 blocks of four 7-segment displays  (2 for the countdown, speed, position, altitude, pitch and roll). See [doc on the TM1637 and TM1638](TM163x.md) for details.
- some leds (start (green), manual command (green), lights (green x2), electricity (green x2), turbo (blue x2)). 
- 20 multicolor (RGB) leds (1 per push button + leds in panel display (oxygen, doors x2, electricity, automatic pilot, alarm, takeoff, orbit, landing, overspeed). See [this](APA106.md) for details.
- 4 10k\omega potentiometers (one online for the engine power, and 3 rotary for the audio, pitch and roll)

### (micro) computers
- 1 raspberry pi (I have Pi3, but Pi2 should be ok. Pi Zero is ok, but cannot be used in game mode IMHO)
- 1 micro-controllers for the WS812b-like leds and other IOs: I choose an AVR ATtiny88 (because I had it in stock). See [this](ATtiny.md) to understand why this one, and how I program it directly with the Raspberry Pi.

### switchs/buttons
- 10 2-position switches (laser, automatic pilot, lights (x2), electricity (x3), turbo (x2), computer)
- 4 3-position switches (doors, pumps (x2), audio)
- 8 push buttons with led (brake, parachute, landing gear, laser, engines x2, unhook spaceship)
- 1 big red push button with led (go button)
- 1 on/off switch with key (start)
- 2 rotary switch band selector, 4 Poles 3 Positions (start mode, flight mode)
- 4 rocket-switch (takeoff phases x3, laser)
- joystick

## misc
- 2 small speakers
- 2 USB-a female plug
- 2 female audio 3.5mm jack
- 1 jack power plugs (male/female



# What I bought (and where)

I do not specially recommand these shops, the links are just here to give you full description of what I bought.

- a 7-inch touch screen LCD (7-inch 800x480 HDMI LCD (B) from [waveshare](https://www.waveshare.com/wiki/7inch_HDMI_LCD_(B))): 52€ at [amazon](https://www.amazon.fr/gp/product/B01HPV6RUS/ref=oh_aui_detailpage_o07_s00)
- 5 rocket switches: [9.66€ for 5 of them](http://www.priceminister.com/offer/buy/1740523176/5pcs-dc-12v-20a-cover-led-light-rocker-toggle-switch-spst-on-off-car-truck-bi582.html)
- 4 boards with 8 7-segment displays (with a TM1638 led-and-buttons driver): [2.50€ each](http://www.gearbest.com/lcd-led-display-module/pp_354750.html)
- 1 giant push-button with led (60mm): [1.6€](https://fr.aliexpress.com/item/5-Colors-LED-Light-Lamp-60MM-Big-Round-Arcade-Video-Game-Player-Push-Button-Switch/32794775928.html)
- 10 toggle switches: [2.6€](https://fr.aliexpress.com/item/10Pcs-Blue-Mini-MTS-203-6-Pin-SPDT-ON-OFF-ON-6A-125VAC-Toggle-Switches/32792308755.html)
- 10 square push-button (32mm, transparent): around [1€ each](https://fr.aliexpress.com/item/10pcs-32mm-LED-Illuminated-Arcade-Button-12V-Square-Push-Button-with-Micro-Switch-for-Coin-Operated/32792126188.html) or [here](https://fr.aliexpress.com/item/2pcs-lot-33-33mm-square-LED-lighted-Illuminated-push-button-MANE-Jamma-arcade-game-machine-accessories/32710197272.html) (same price, but it took time to send the command)
- some green/red/yellow/white/blue [leds](https://fr.aliexpress.com/item/200PC-Lot-3MM-5MM-Led-Kit-With-Box-Mixed-Color-Red-Green-Yellow-Blue-White-Light/32626322055.html) (2.5€)
- A game arcade [joystick](https://fr.aliexpress.com/item/DIY-Game-Arcade-Joystick-Red-Ball-4-8-Way-Replacement-Parts-For-Fighting-Stick-Parts-Game/32741227545.html) (numeric, not analogic): 5.3€
- some LED holders to mount them: [1.3€](https://fr.aliexpress.com/item/CNIM-Hot-20-Pcs-Copper-5mm-Light-Emitting-Diode-LED-Holder-Mount-Panel-Display/32715039086.html)
- a 10k\Omega slide [potentiometer](https://fr.aliexpress.com/item/Free-shipping-1pcs-Slide-Potentiometer-10K-Linear-Module-Dual-Output-for-Arduino-AVR-Electronic-Block/32742799309.html): 1.4€
- Some [bargraphs](https://fr.aliexpress.com/item/2PCS-New-10-Segment-Led-Bargraph-Light-Display-Red-Yellow-Green-Blue/32767236126.html) (0.85€ each)
- A ["hat" board ](https://fr.aliexpress.com/item/Free-Shipping-DIY-Prototyping-Hat-Shield-Hole-Plate-Kit-Prototype-Expansion-Board-3V-5V-for-Raspberry/32788948092.html) for the raspberry (it will not be a real hat, because I will not put any eeprom): 2.86€
- some [screw connectors](https://fr.aliexpress.com/item/20PCS-KF301-2P-5-08mm-2-Pin-Connect-Terminal-Screw-Terminal-Connector/32438229697.html): 1.80€ for 20
- [gaming headphone](https://www.aliexpress.com/item/Over-ear-Wired-earphone-headphones-gaming-headset-for-pc-video-game-gamer-For-Playstation-for-PS4/32579786730.html): 2€ (low quality, but very cheap... the right price for how it will be used)
- [key switch](https://www.aliexpress.com/item/KS02-Key-Switch-ON-OFF-Lock-Switch-KS-02/32606053670.html): 0.85€
- pack of 50 RGB leds APA106 (a clone of the NeoPixels WS2812b), [5mm LEDs](https://fr.aliexpress.com/item/10pcs-1000pcs-DC5V-APA106-F5-5mm-F8-8mm-Round-RGB-LED-APA106-chipset-inside-RGB-Full/32792759587.html): 11.5€
- 10 3-position [toggle switches](https://fr.aliexpress.com/item/10Pcs-3-Pin-3-Position-ON-OFF-ON-SPDT-Mini-Latching-Toggle-Switch-AC-125V-6A/32712692663.html): 1.9€ for 10
- 5 [rotary potentiometers](https://fr.aliexpress.com/item/5pcs-1K-1M-OHM-3-Terminal-Single-Linear-Taper-Rotary-Volume-B-Type-Potentiometer-Pot-W/32725338190.html) (with colored button): 2.33€ for 5
- flat 50cm HDMI cable
- smal [audio amplifier](https://fr.aliexpress.com/item/3W-2-Mini-Digital-Power-Audio-Amplifier-Board-DIY-Stereo-USB-DC-5V-Power-Supply-PAM8403/32778625137.html): 0.5€
- some screw connector with 2.54mm
- some resistors

- a cheap wallet like [this one](https://www.cdiscount.com/bricolage/amenagement-atelier/valise-avec-bords-en-alu/f-1660404-auc5411257029136.html): 43cmx30cmx15cm (I bought a used one for 1€!). Please check that the height is around 15cm (12 or 13 is not enough)
