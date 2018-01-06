# Secondary micro-controller

First, the micro-controller was used to second the Raspberry Pi as piloting the WS2812-like LEDs and acquiring some analog values (potentiometer).
Finally I decided to give him all the polling tasks (pilot the TM1638s, pilot the RGB Leds, the TM1637s, and probably a matrix keyboard) the Raspberry cannot perform (ok, I know the raspberry can control the LED through the SPI, if programing is well done, since the timing are very tight).

## Choice of the micro-controller

I just needed a SPI connection with the Raspberry Pi, few ADCs (to "read" the potentiometer), and a lot of IOs.

I have listed all the micro-controllers I had in stock, and I've chose the  **ATtiny88**, because, among all the micro-controllers I have in stock, this one has enough IOs, run fast enough (8MHz without external quartz, up to 10MHz) and has enough RAM/Flash (I am sure that 1Kb is enough, but I wanted some extra space, "just in case").

Of course, any AVR or PIC (or any other micro-controller) you have in stock, or any Arduino-based board would be ok (At first, I choosed a **ATtiny631**, but finally, I moved the connection to the TM1638 and TM1637 boards from the RPi to the micro-controller, and the 631 did not have enough IOs).

As a bonus, I can directly program it through the Raspberry Pi, through the SPI.

## Program it through the Raspberry Pi

This is done following these two tutorials ([here](https://www.rototron.info/raspberry-pi-avr-programmer-spi-tutorial/) and [here](http://ozzmaker.com/program-avr-using-raspberry-pi-gpio/)).

The idea is to use the SPI (`SPI_MISO`, `SPI_MOSI` and `SPI_CLK`) of the raspberry Pi, plus one IO (for the reset) to program the AVR using its In-System Programmable feature. And the SPI will also be used to connect the two devices.

1. install [`avrdure`](http://www.nongnu.org/avrdude/) on the Raspberry 
    
```Shell
sudo apt-get install avrdude
```
    
2. configure it according to our IO setting. Add (or uncomment) the file `/etc/avrdude.conf` as:

```INI
programmer
  id    = "linuxgpio";
  desc  = "Use the Linux sysfs interface to bitbang GPIO lines";
  type  = "linuxgpio";
  reset = 25;
  sck   = 11;
  mosi  = 10;
  miso  = 9;
;
```
You can choose any other IO for the reset (#25 was arbitrary choice).

3. test if everything works with

```Shell
sudo avrdude -c linuxgpio -p attiny88 -v
```
And you should have something like this
```
avrdude: Version 6.1, compiled on Jul  7 2015 at 10:29:47
         Copyright (c) 2000-2005 Brian Dean, http://www.bdmicro.com/
         Copyright (c) 2007-2014 Joerg Wunsch

         System wide configuration file is "/etc/avrdude.conf"
         User configuration file is "/root/.avrduderc"
         User configuration file does not exist or is not a regular file, skipping

         Using Port                    : unknown
         Using Programmer              : linuxgpio
         AVR Part                      : ATtiny88
         Chip Erase delay              : 9000 us
         PAGEL                         : PD7
         BS2                           : PC2
         RESET disposition             : dedicated
         RETRY pulse                   : SCK
         serial program mode           : yes
         parallel program mode         : yes
         Timeout                       : 200
         StabDelay                     : 100
         CmdexeDelay                   : 25
         SyncLoops                     : 32
         ByteDelay                     : 0
         PollIndex                     : 3
         PollValue                     : 0x53
         Memory Detail                 :

                                  Block Poll               Page                       Polled
           Memory Type Mode Delay Size  Indx Paged  Size   Size #Pages MinW  MaxW   ReadBack
           ----------- ---- ----- ----- ---- ------ ------ ---- ------ ----- ----- ---------
           eeprom        65    20     4    0 no         64    4      0  3600  3600 0xff 0xff
           flash         65     6    64    0 yes      8192   64    128  4500  4500 0xff 0xff
           lfuse          0     0     0    0 no          1    0      0  4500  4500 0x00 0x00
           hfuse          0     0     0    0 no          1    0      0  4500  4500 0x00 0x00
           efuse          0     0     0    0 no          1    0      0  4500  4500 0x00 0x00
           lock           0     0     0    0 no          1    0      0  4500  4500 0x00 0x00
           calibration    0     0     0    0 no          1    0      0     0     0 0x00 0x00
           signature      0     0     0    0 no          3    0      0     0     0 0x00 0x00

         Programmer Type : linuxgpio
         Description     : Use the Linux sysfs interface to bitbang GPIO lines
         Pin assignment  : /sys/class/gpio/gpio{n}
           RESET   =  25
           SCK     =  11
           MOSI    =  10
           MISO    =  9

avrdude: AVR device initialized and ready to accept instructions

Reading | ################################################## | 100% 0.00s

avrdude: Device signature = 0x1e9311
avrdude: safemode: lfuse reads as 6E
avrdude: safemode: hfuse reads as DF
avrdude: safemode: efuse reads as 7

avrdude: safemode: lfuse reads as 6E
avrdude: safemode: hfuse reads as DF
avrdude: safemode: efuse reads as 7
avrdude: safemode: Fuses OK (E:07, H:DF, L:6E)

avrdude done.  Thank you.

```
(I had to check with another IO conf to be sure that it was working because I couldn't believe it worked on the 1st attempt !)

4. Configure the fuses of the ATTiny
(in my case, I want to use the 8MHz intern oscillator, without scaling, so the fuses are `0xE2DFFF`)
Go to [http://eleccelerator.com/fusecalc/fusecalc.php?chip=attiny88](http://eleccelerator.com/fusecalc/fusecalc.php) (or equivalent) to compute your fuses, and use `avrdude`:
```Shell
avrdude -c linuxgpio -p attiny88 -U lfuse:w:0xEE:m 	-U hfuse:w:0xDF:m   
```

Eventually, if you have the error 
```
Can't export GPIO 25, already exported/busy?: Device or resource busy
avrdude done.  Thank you.
```
You can add 25 (or the corresponding GPIO pin)in the file `/sys/class/gpio/unexport` with:
```shell
echo 25 > /sys/class/gpio/unexport
```


5. write the code, compile it and send it with `avrdude` to the ATtiny !!

```
avr-gcc -c -mmcu=attiny88 toto.c -DF_CPU=8000000UL -Os
avr-gcc -mmcu=attiny88 -o toto.elf toto.o
avr-objcopy -j .text -j .data -O ihex toto.elf toto.hex
```

(there is a dedicated `Makefile` for this in the `src/AVR/` folder)

6. *Warning* !
After each use of avrdude (of the SPI bus), I need to reinitalize the SPI with
```
sudo rmmod spi_bcm2835
sudo modprobe spi_bcm2835
```
this is already included in the Makefile provided.


## Polling and timing

The ATtiny need to do some polling to detect some changes in the switches/potentiometers, through the TM1638 boards. I also wanted to make the RGB LEDs (and the LCD displays?) blinking.

For that purpose, I need to prepare some periodic tasks:
- polling of the analog inputs (potentiometers)
- polling to get data from the TM1638
- make the RGB LED blink
- polling to get data from the matrix keyboard (if I add it, one day)
- update the display (TM1637 and TM1638) if needed

I need to read the inputs (switches, not push button) at leat 10 times a second (rought approximation), and each "task" take between few cycles (read the matrix keyboard or run the ADC) and less than a millisecond (pilot the RGB leds or talk with the TMs). So I have decided to set a period of 15.625ms (1/64 of a second), and to count in which cycle we are (with the 8-bit variable `ncycle`):
- when `(ncycle&3) == 0`: (every 62.5ms) run ADC0, read `8TM1` (1st TM1638), update `8TM1` and `7TM1` displays if necessary
- when `(ncycle&3) == 1`: (every 62.5ms) run ADC1, read `8TM2` (2nd TM1638), update `8TM2` and `7TM2` displays if necessary
- when `(ncycle&3) == 2`: (every 62.5ms) run ADC2, read `8TM3` (2nd TM1638), update `8TM3` and `7TM3` displays if necessary
- when `(ncyccle&15) == 15`: (every 250ms) update the RGB leds if necessary (according to blinking)

So TIME1 is configured to generate interruption every 15625 ticks, with a prescaler of 1/8 (Frequency of the ATtiny: 8MHz, see this [AVR timer calculator](http://eleccelerator.com/avr-timer-calculator/)):

```C
	TCCR1B = (1U<<CS11) | (1U<<WGM12);     /* prescaler = 1/8 and Clear Timer on Compare match (CTC) T*/
	TCCR1C = (1U<<FOC1A);    /* channel A */
	OCR1A = 15625;              /* 15625 ticks @ 1MHz -> 15.625ms */
	TIMSK1 = (1U<<OCIE1A);      /* set interrupt on Compare channel A */
```

For the RGB Leds, the 4 MSB of `ncycle` (so `ncycle>>4`) indicates in which blinking cycle we are. So, for each RGB Led, a 16-bit word encodes the blinking scheme (each bit indicates if the LED is on/off in the corresponding blinking cycle). 
See the [APA106 documentation](APA106.md) for the blinking details (how to encode blink pattern, how to compute when to send data, and when it is not necessary, etc.)


## Communication between RPi and micro-controller (protocol)

The communication between the Raspberry Pi is "simple". The RPi send a first byte, that indicates the command. This command may be followed by some data (up to 8 bytes).
The following table sums up the commands:

|7|6|5|4|3|2|1|0|Details|Extra bytes|
|-|-|-|-|-|-|-|-|:-|:-|
|`0`|`0`|`0`|`0`|`0`|`0`|`0`|`0`| No Operation |0|
|-|-|-|-|-|-|-|-|-|-|
|`0`|`0`|`0`|`x`|`x`|`x`|`x`|`x`| Set RGB Led | 5 bytes |
| | | | | | | | | `xxxxx` is the number of the Led |(blinkH, blinkL, Red, Green, Blue)
|-|-|-|-|-|-|-|-|-|-|
|`0`|`1`|`s`|`l`|`l`|`l`|`t`|`t`| Set/clear a led | 0 |
| | | | | | | | | `s` is 1 to set a led, 0 to clear | |
| | | | | | | | | `lll` is the number of the led | |
| | | | | | | | | `tt` is the number of the TM1638 considered | |
|-|-|-|-|-|-|-|-|-|-|
|`1`|`0`|`b`|`b`|`b`|`x`|`t`|`t`| Set the brightness of the TM163x | 0 |
| | | | | | | | | `bbb` is the brightness | |
| | | | | | | | | `x` is 1 for the TM1637, 0 for the TM1638 | |
| | | | | | | | | `tt` is the number of the TM163x considered | |
|-|-|-|-|-|-|-|-|-|-|
|`1`|`1`|`0`|`a`|`d`|`x`|`t`|`t`| Set the 7+segment display of the TM163x | 4 or 8 bytes |
| | | | | | | | | `a` is 0 to set 4 digits, 1 to set 8 digits | |
| | | | | | | | | `d` is 0 for the 1st display, 1 for the 2nd display | |
| | | | | | | | | `x` is 1 for the TM1637, 0 for the TM1638 | |
| | | | | | | | | `tt` is the number of the TM163x considered | |
|-|-|-|-|-|-|-|-|-|-|
|`1`|`1`|`1`|`0`|`o`|`x`|`t`|`t`| Turn on/off the display of the TM163x | 0 |
| | | | | | | | | `o` is 0 to set 4 digits, 1 to set 8 digits | |
| | | | | | | | | `d` is 0 for the 1st display, 1 for the 2nd display | |
| | | | | | | | | `x` is 1 for the TM1637, 0 for the TM1638 | |
| | | | | | | | | `tt` is the number of the TM163x considered | |
|-|-|-|-|-|-|-|-|-|-|
|`1`|`1`|`1`|`1`|`0`|`x`|`t`|`t`| Clear the display of the TM163x | 0 |
| | | | | | | | | `x` is 1 for the TM1637, 0 for the TM1638 | |
| | | | | | | | | `tt` is the number of the TM163x considered | |
|-|-|-|-|-|-|-|-|-|-|
|`1`|`1`|`1`|`1`|`1`|`x`|`x`|`x`| not used | 0 |
|`0`|`0`|`1`|`x`|`x`|`x`|`x`|`x`| not used | 0 |
|`0`|`0`|`0`|`1`|`1`|`x`|`x`|`x`| not used | 0 |
|-|-|-|-|-|-|-|-|-|-|

