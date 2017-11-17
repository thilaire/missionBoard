# Secondary micro-controller

This micro-controller is used to pilot the WS2812-like LEDs, acquire some analog values (potentiometer), and maybe pilot few leds or switches.
Some secondary tasks (but that need to be fast) the Raspberry cannot perform (ok, I know the raspberry can control the LED through the SPI, if programing is well done, since the timing are very tight).

## Choice of the micro-controller

I just needed a SPI connection with the Raspberry Pi, few ADCs (to "read" the potentiometer), few IOs.


I have listed all the micro-controllers I had in stock, and I've chose the  **ATtiny861V**, because, among all the micro-controllers I have in stock, this one has enough IOs (more than the ATtiny84 that would have been perfect, but I wanted some extra IOs, just in case), run fast enough (8MHz without external quartz, up to 10MHz) and has enough RAM/Flash (I am sure that 1Kb is enough, but I wanted some extra space, "just in case").

Of course, any AVR or PIC (or any other micro-controller) you have in stock, or any Arduino-based board would be ok.

As a bonus, I can directly program it through the Raspberry Pi

## Program it through the Raspberry Pi

This is done following these two tutorials ([here](https://www.rototron.info/raspberry-pi-avr-programmer-spi-tutorial/) and [here](http://ozzmaker.com/program-avr-using-raspberry-pi-gpio/)).

The idea is to use the SPI (`SPI_MISO`, `SPI_MOSI` and `SPI_CLK`) of the raspberry Pi, but any other IO (for the reset) to program the AVR using its In-System Programmable feature. And the SPI will also be used to connect the two devices.
The program (`avrdure`)[] can be configured for this purpose.