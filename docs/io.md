# Input/Output

All the switches, LEDs, buttons are connected directly to the Raspberry Pi, the [AVR](ATtiny.md) micro-controller or through the [TM1638](TM1638.md) and [TM1637](TM1637.md)boards.
More precisely, the push-buttons are connected to the Raspberry Pi, the switches and the potentiometer to the the AVR. All the displays (TM1638 and TM1637) are driven by the AVR. 

## Signal naming convention

The following tables regroup all the IO connectiviy. I have choose to name signals as following `xxx_yyyzz` where:
- `xxx` is the board name or panel number, like `RPi` (raspberry Pi), `8TM` (TM1638), `7TM` (TM1637) or `P9` (`P` for *panel*)
- `yyy` is the button/signal/io name (like `GPIO12` or `LED`)
- `zz` is the number (may be empty if not necessary)

For buttons and displays, the common valyes for `yyy` are (some are possible):
- `SW2`: 2-position switch (toggle switch)
- `SW3`: 3-position switch (toggle)
- `ROT`: rotary switch
- `POT`: potentiometer
- `PB`: push button
- `LED`: led (classical one-color led)
- `RGB`: RGB LED
- `BAR`: bargraph
- `SSD`: Seven-segment display (block of four)

## Raspberry Pi

### IOs

| RPi Pin number                | Name       | IO  | Connected to  |   | Connected to  | IO  | Name       | RPi Pin number                |
|:------------------------------|:----------:|:---:|:-------------:|:-:|:-------------:|:---:|:----------:|------------------------------:|
| 01 (3.3v)                     |            |     |               |   |               |     |            |                       (5v) 02 |
| 03 (**GPIO02**, SDA1, I2C)    | `RPi_IO2`  | In  | `P8_PB_`      |   |               |     |            |                       (5v) 04 |
| 05 (**GPIO03**, SCL1, I2C)    | `RPi_IO3`  | In  | `P8_PB_`      |   |               |     |            |                      (GND) 06 |
| 07 (**GPIO04**, GPIO_GCLK)    | `RPi_IO4`  | In  | `P8_PB_`      |   | `P8_PB_`      | In  | `RPi_IO14` |         (TXD0, **GPIO14**) 08 |
| 09 (GND)                      |            |     |               |   | `P8_PB_`      |     | `RPi_IO15` |         (RXD0, **GPIO15**) 10 |
| 11 (**GPIO17**, GPIO_GEN0)    | `RPi_IO17` | In  | `P8_PB_`      |   | `P8_PB_`      | In  | `RPi_IO18` |    (GPIO_GEN1, **GPIO18**) 12 |
| 13 (**GPIO27**, GPIO_GEN2)    | `RPi_IO27` | In  | `P8_PB_`      |   |               |     |            |                      (GND) 14 |
| 15 (**GPIO22**, GPIO_GEN3)    | `RPi_IO22` | In  | `P8_PB_`      |   |   x           |     | `RPi_IO23` |    (GPIO_GEN4, **GPIO23**) 16 |
| 17 (3.3v)                     |            |     |               |   |   x           |     | `RPi_IO24` |    (GPIO_GEN5, **GPIO24**) 18 |
| 19 (**GPIO10**, SPI_MOSI)     | `RPi_MOSI` | Out | `AT_MOSI`     |   |               |     |            |                      (GND) 20 |
| 21 (**GPIO09**, SPI_MISO)     | `RPi_MISO` | In  | `AT_MISO`     |   | `AT_RESET`    | Out | `RPi_IO25` |    (GPIO_GEN6, **GPIO25**) 22 |
| 23 (**GPIO11**, SPI_CLK)      | `RPi_SCK`  | Out | `AT_SCK`      |   |   x (SPI?)    |  ?  | `RPi_IO8`  |    (SPI_CE0_N, **GPIO08**) 24 |
| 25 (GND)                      |            |     |               |   | `P7_PB_UP`    | In  | `RPi_IO7`  |    (SPI_CE1_N, **GPIO07**) 26 |
| 27 (**ID_SD**, I2C ID EEPROM) |            |     |               |   |               |     |            | (I2C ID EEPROM, **ID_SC**) 28 |
| 29 (**GPIO05**)               | `RPi_IO5`  | In  | `P7_PB_DOWN`  |   |               |     |            |                      (GND) 30 |
| 31 (**GPIO06**)               | `RPi_IO6`  | In  | `P7_PB_RIGHT` |   | `P7_PB_LEFT`  | In  | `RPi_IO12` |               (**GPIO12**) 32 |
| 33 (**GPIO13**)               | `RPi_IO13` |     |               |   |               |     |            |                      (GND) 34 |
| 35 (**GPIO19**)               | `RPi_IO19` |     |   x           |   |   x           |     | `RPi_IO16` |               (**GPIO16**) 36 |
| 37 (**GPIO26**)               | `RPi_IO26` |     |   x           |   |   x           |     | `RPi_IO20` |               (**GPIO20**) 38 |
| 39 (GND)                      |            |     |   x           |   |   x           |     | `RPi_IO21` |               (**GPIO21**) 40 |

x: still available

*[Here](datasheet/RPi3-GPIO.png) is the official Raspberry GPIO table*

### other devices

- USB connectivity:

| RPi USB | Connected to                  |
|:-------:|:-----------------------------:|
| #1      | LCD touchscreen `P14_LCD_USB` |
| #2      |                               |
| #3      | USB connector `P9_USB_0`      |
| #4      | USB connector `P9_USB_1`      |

- HDMI: to the LCD touchscreen `P14_LCD_USB`
- 3.5 Jack sound:  


## ATtiny


| ATtiny88   Pin number    | Name       | IO  | Connected to   |   | Connected to  | IO  | Name       |  ATtiny88   Pin number    |
|:-------------------------|:----------:|:---:|:--------------:|:-:|:-------------:|:---:|:----------:|--------------------------:|
| 01 (**PC6**, RESET)      | `AT_RESET` | In  | `RPi_IO25`     |   | `P4_POT_2`    | Out | `AT_ADC5`  |   (ADC5, SCL, **PC5**) 28 |
| 02 (**PD0**)             | `AT_PD0`   | In  |  I_KB0         |   | `P4_POT_1`    | Out | `AT_ADC4`  |   (ADC4, SDA, **PC4**) 27 |
| 03 (**PD1**)             | `AT_PD1`   | In  |  I_KB1         |   | `P4_POT_0`    | Out | `AT_ADC3`  |   (ADC3, SCL, **PC3**) 26 |
| 04 (**PD2**, INT0)       | `AT_PD2`   | In  |  I_KB2         |   | `7TM3_CLK`    | In  | `AT_PC2`   |        (ADC2, **PC2**) 25 |
| 05 (**PD3**, INT1)       | `AT_PD3`   | In  |  I_KB3         |   | `7TM2_CLK`    | In  | `AT_PC1`   |        (ADC1, **PC1**) 24 |
| 06 (**PD4**, T0)         | `AT_PD4`   | Out |  O_KB0         |   | `7TM1_CLK`    | In  | `AT_PC0`   |        (ADC0, **PC0**) 23 |
| 07 (VCC)                 |            |     |    3.3V        |   |     GND       |     |            |                  (GND) 22 |
| 08 (GND)                 |            |     |     GND        |   | `AT_LED`, OKB2| Out | `AT_PC7`   |              (**PC7**) 21 |
| 09 (**PB6**, CLKI)       | `AT_PB6`   | I/O | `8TM_DIO`      |   |    +3.3V      |     |            |                 (AVCC) 20 |
| 10 (**PB7**)             | `AT_PB7`   | Out | `8TM_CLK`,O_KB3|   |  `Rpi_SCK`    | In  | `AT_SCK`   |         (SCK, **PB5**) 19 |
| 11 (**PD5**  T1)         | `AT_PD5`   | Out | `8TM1_STB`     |   |  `Rpi_MISO`   | Out | `AT_MISO`  |        (MISO, **PB4**) 18 |
| 12 (**PD6**, AIN0)       | `AT_PD6`   | Out | `8TM2_STB`     |   |  `Rpi_MOSI`   | In  | `AT_MOSI`  |        (MOSI, **PB3**) 17 |
| 13 (**PD7**  AIN1)       | `AT_PD7`   | Out | `8TM3_STB`     |   |     GND       | In  | `AT_SS`    |          (SS, **PB2**) 16 |
| 14 (**PB0**, CLK0,ICP1)  | `AT_PB0`   | Out | `7TM_DATA`     |   |  `P2_RGB`     | Out | `AT_PB1`   |        (OC1A, **PB1**) 15 |

                                              
For debug purpose only, a simple LED is connected to `AT_PB6`.
The I_KBx and O_KBy corresponds to a possible matrix 4*4 keyboard (don't know yet if I will put it or not).

Note that the ATtiny is powered by 3.3V (and not 5V).
There are some 100k resistor between the ATtiny and the RPi for the lines `SCK`, `MISO`, `MOSI`, `RESET` and `SS`.


## TM1638 boards
The three TM1638s are "chained" (to save some GPIO), so it means they share the same clock (`8TM_CLK`) and data I/O (`8TM_DIO`). Only the STB (`8TM1_STB`, `8TM2_STB` and `8TM3_STB`) is different:
- the TM Board #1 is used for the IOs of the bottom panels (toggle switch buttons, leds and counter)
- TM Board #2 is used for
- TM Board #3 is used for


| Pin description   | Name       | Connected to |
|:------------------|:----------:|:------------:|
| STB (TM board #1) | `8TM1_STB` | `AT_PD5`     |
| STB (TM board #2) | `8TM2_STB` | `AT_PD6`     |
| STB (TM board #3) | `8TM3_STB` | `AT_PD7`     |
| CLK (Clock input) | `8TM_CLK`  | `AT_PB7`     |
| DIO (Data I/O)    | `8TM_DIO`  | `AT_PB6`     |




### Outputs

| TM Board | Output | Connected to |
|:--------:|:------:|:------------:|
| #1       | 8      | `P4_LED`     |



### Inputs

The TM1638 IC has three input lines, named K1, K2 and K3.
K3 is the original line on the board, and K1 was added. K1 is only used on the first TM board (bottom)   


#### TM Board #1

| Line | Input   | Connected to | Functionality   |
|:----:|:-------:|:------------:|:---------------:|
| K1   | 0       |              |                 |  
| K1   | 1       |              |                 |
| K1   | 2       |              |                 |
| K1   | 3       |  `P6_SW2_0`  |  Phase 1        |
| K1   | 4       |  `P6_SW2_1`  |  Phase 2        |
| K1   | 5       |  `P6_SW2_2`  |  Phase 3        |
| K1   | 6       |  `P3_SW2_0`  |  Laser armement |
| K1   | 7       |  `P3_SW2_1`  |  Laser color    |
| K3   | 0       |              |                 |
| K3   | 1       |  `P1_SW3:2`  |  Game mode      | ok
| K3   | 2       |  `P1_SW3:1`  |  Game mode      | ok
| K3   | 3       |  `P5_SW3:2`  | flight mode     | ok
| K3   | 4       |  `P5_SW3:1`  | flight mode     | ok
| K3   | 5       |  `P5_SW2`    |  autopilot      | ok
| K3   | 6       |  `P9_SW3:2`  |  COM2           | ok
| K3   | 7       |  `P9_SW3:1`  |  COM1           | ok



#### TM Board #2


| Input   | Connected to |
|:-------:|:------------:|
| 1       |              |
| 2       |              |
| 3       |              |
| 4       |              |
| 5       |              |
| 6       |              |
| 7       |              |
| 8       |              |


## TM1637 boards
The three TM1637 have common data (`7TM_DATA`), but separated clocks (`7TM1_CLK`, `7TM2_CLK`, `7TM2_CLK`).

| TM Board | Pin  | Name        | Connected to |
|:--------:|:-----|:-----------:|:------------:| 
| #1, 2, 3 | DATA | `7TM_DATA`  | `AT_PB0`     |
| #1       | CLK  | `7TM1_CLK`  | `AT_PC0`     |
| #2       | CLK  | `7TM2_CLK`  | `AT_PC1`     |
| #3       | CLK  | `7TM3_CLK`  | `AT_PC2`     |

