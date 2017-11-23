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
  reset = 8;
  sck   = 11;
  mosi  = 10;
  miso  = 9;
;
```

3. test if everything works with

```Shell
sudo avrdude -c linuxgpio -p attiny861 -v
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
         AVR Part                      : ATtiny861
         Chip Erase delay              : 4000 us
         PAGEL                         : PB3
         BS2                           : PB2
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
           eeprom        65    10     4    0 no        512    4    128  4000  4000 0xff 0xff
           flash         65     6    64    0 yes      8192   64    128  4500  4500 0xff 0xff
           signature      0     0     0    0 no          3    0      0     0     0 0x00 0x00
           lock           0     0     0    0 no          1    0      0  4500  4500 0x00 0x00
           lfuse          0     0     0    0 no          1    0      0  4500  4500 0x00 0x00
           hfuse          0     0     0    0 no          1    0      0  4500  4500 0x00 0x00
           efuse          0     0     0    0 no          1    0      0  4500  4500 0x00 0x00
           calibration    0     0     0    0 no          1    0      0     0     0 0x00 0x00

         Programmer Type : linuxgpio
         Description     : Use the Linux sysfs interface to bitbang GPIO lines
         Pin assignment  : /sys/class/gpio/gpio{n}
           RESET   =  8
           SCK     =  11
           MOSI    =  10
           MISO    =  9

avrdude: AVR device initialized and ready to accept instructions

Reading | ################################################## | 100% 0.00s

avrdude: Device signature = 0x1e930d
avrdude: safemode: lfuse reads as 62
avrdude: safemode: hfuse reads as DF
avrdude: safemode: efuse reads as 1

avrdude: safemode: lfuse reads as 62
avrdude: safemode: hfuse reads as DF
avrdude: safemode: efuse reads as 1
avrdude: safemode: Fuses OK (E:01, H:DF, L:62)

avrdude done.  Thank you.
```
(I had to check with another IO conf to be sure that it was working because I couldn't believe it worked on the 1st attempt !)

4. Configure the fuses of the ATTiny
(in my case, I want to use the 8MHz intern oscillator, without scaling, so the fuses are `0xE2DFFF`)
Go to [http://www.engbedded.com/fusecalc/](http://www.engbedded.com/fusecalc/) (or equivalent) to compute your fuses, and use `avrdude`:
```Shell
avrdude -c linuxgpio -p attiny861 -U lfuse:w:0xe2:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m 
```

Eventually, if you have the error 
```
Can't export GPIO 8, already exported/busy?: Device or resource busy
avrdude done.  Thank you.
```
You can add 8 in the file `/sys/class/gpio/unexport` with:
```shell
echo 8 > /sys/class/gpio/unexport
```


5. write the code, compile it and send it with `avrdude` to the ATtiny !!

```
avr-gcc -c -mmcu=attiny861 toto.c -DF_CPU=8000000UL -Os
avr-gcc -mmcu=attiny861 -o toto.elf toto.o
avr-objcopy -j .text -j .data -O ihex toto.elf toto.hex
```

(there is a dedicated Makefile for this)