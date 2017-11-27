# Input/Output

All the switches, LEDs, buttons are connected directly to the Raspberry Pi, the AVR micro-controller or through the [TM1638](TM1638.md) boards.

## Signal naming convention

The following tables regroup all the IO connectiviy. I have choose to name signals as following `xxx_yyyzz` where:
- `xxx` is the board name or panel number, like `RPi`, `TM1` or `P9` (`P` for *panel*)
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
| 09 (GND)                      |            |     |               |   |               |     | `RPi_IO15` |         (RXD0, **GPIO15**) 10 |
| 11 (**GPIO17**, GPIO_GEN0)    | `RPi_IO17` | In  | `P8_PB_`      |   | `P8_PB_`      | In  | `RPi_IO18` |    (GPIO_GEN1, **GPIO18**) 12 |
| 13 (**GPIO27**, GPIO_GEN2)    | `RPi_IO27` | In  | `P8_PB_`      |   |               |     |            |                      (GND) 14 |
| 15 (**GPIO22**, GPIO_GEN3)    | `RPi_IO22` | In  | `P8_PB_`      |   |   x           | In  | `RPi_IO23` |    (GPIO_GEN4, **GPIO23**) 16 |
| 17 (3.3v)                     |            |     |               |   |   x           | In  | `RPi_IO24` |    (GPIO_GEN5, **GPIO24**) 18 |
| 19 (**GPIO10**, SPI_MOSI)     | `RPi_MOSI` | Out |  `AT_MOSI`    |   |               |     |            |                      (GND) 20 |
| 21 (**GPIO09**, SPI_MISO)     | `RPi_MISO` | In  |  `AT_MISO`    |   |   x           | In  | `RPi_IO25` |    (GPIO_GEN6, **GPIO25**) 22 |
| 23 (**GPIO11**, SPI_CLK)      | `RPi_SCK`  | Out |  `AT_SCK`     |   | `AT_RESET`    | Out | `RPi_IO8`  |    (SPI_CE0_N, **GPIO08**) 24 |
| 25 (GND)                      |            |     |               |   | `P7_JOY_`     | In  | `RPi_IO7`  |    (SPI_CE1_N, **GPIO07**) 26 |
| 27 (**ID_SD**, I2C ID EEPROM) |            |     |               |   |               |     |            | (I2C ID EEPROM, **ID_SC**) 28 |
| 29 (**GPIO05**)               | `RPi_IO5`  | In  | `P7_JOY_`     |   |               |     |            |                      (GND) 30 |
| 31 (**GPIO06**)               | `RPi_IO6`  | In  | `P7_JOY_`     |   | `P7_JOY_`     | In  | `RPi_IO12` |               (**GPIO12**) 32 |
| 33 (**GPIO13**)               | `RPi_IO13` | In  | `TM3_STB`??   |   |               |     |            |                      (GND) 34 |
| 35 (**GPIO19**)               | `RPi_IO19` | In  | `TM1_STB`     |   | `TM2_STB`??   | Out | `RPi_IO16` |               (**GPIO16**) 36 |
| 37 (**GPIO26**)               | `RPi_IO26` | In  |  ???          |   | `TM_CLK`      | Out | `RPi_IO20` |               (**GPIO20**) 38 |
| 39 (GND)                      |            |     |               |   | `TM_DIO`      | I/O | `RPi_IO21` |               (**GPIO21**) 40 |

To add (in the `x`):
- 4 Inputs for the Joystick
- 9 Inputs for the push-buttons
- 5 Inputs for the TMs (at least 3)

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


| ATtiny861V Pin number         | Name       | IO  | Connected to  |   | Connected to  | IO  | Name       | ATtiny861V Pin number                |
|:------------------------------|:----------:|:---:|:-------------:|:-:|:-------------:|:---:|:----------:|-------------------------------------:|
| 01 (**PB0**, MOSI, SDA, ...)  | `AT_MOSI`  | In  | `RPi_MOSI`    |   |               |     |            |              (ADC0, SDA, **PA0**) 20 |
| 02 (**PB1**, MISO, DO, ...)   | `AT_MISO`  | Out | `RPi_MISO`    |   | `P2_RGB_DIN`  | Out | `AT_PA1`   |               (ADC1, DO, **PA1**) 19 |
| 03 (**PB2**, SCK, SCL, ...)   | `AT_SCK`   | In  | `RPi_SCK`     |   | `P8_LED`      | Out | `AT_PA2`   |              (ADC2, SCL, **PA2**) 18 |
| 04 (**PB3**, OC1B, ...)       |            |     |               |   |               |     |            |                   (AREF, **PA3**) 17 |
| 05 (VCC)                      |            |     |     +5V       |   |     GND       |     |            |                            (AGND) 16 |
| 06 (GND)                      |            |     |     GND       |   |     +5V       |     |            |                            (AVCC) 15 |
| 07 (**PB4**, XTAL1, ...)      |            |     |               |   |               |     |            |             (ADC3, ICP0, **PA4**) 14 |
| 08 (**PB5**, XTAL2, ...)      |            |     |               |   |  `P4_POT_2`   | In  | `AT_ADC4`  |             (ADC4, AIN2, **PA5**) 13 |
| 09 (**PB6**  ADC9, T0, ...)   | `AT_PB6`   | Out | `AT_LED`      |   |  `P4_POT_1`   | In  | `AT_ADC5`  |             (ADC5, AIN0, **PA6**) 12 |
| 10 (**PB7**, RESET, ...)      | `AT_RESET` | In  | `RPi_IO8`     |   |  `P4_POT_0`   | In  | `AT_ADC6`  |             (ADC6, AIN1, **PA7**) 11 |
                                              
For debug purpose only, a simple LED is connected to `AT_PB6`.


## TM1638 boards

The four TM1638s are chained (to save some GPIO), so it means they share the same clock and data I/O. Only the STB (Chip select) is different:
- the TM Board #1 is used for the IOs of the bottom panels (toggle switch buttons, leds and counter)
- TM Board #2 is used for
- TM Board #3 is used for
- TM Board #4 is used for


| Pin description   | Name      | Connected to |
|:------------------|:---------:|:------------:|
| STB (TM board #1) | `TM1_STB` | `RPi_IO19`   |
| STB (TM board #2) | `TM2_STB` |              |
| STB (TM board #3) | `TM3_STB` |              |
| STB (TM board #4) | `TM4_STB` |              |
| STB (TM board #5) | `TM5_STB` |              |
| CLK (Clock input) | `TM_CLK`  | `RPi_IO20`   |
| DIO (Data I/O)    | `TM_DIO`  | `RPi_IO21`   |


### Outputs

| TM Board | Output       | Connected to |
|:--------:|:------------:|:------------:|
| #1       | `TM1_LED_7`  |              |
| #1       | 8  | `P4_LED`     |



### Inputs

#### TM Board #1
| Input Line | Input   | Connected to |
|:----------:|:-------:|:------------:|
| 1          | 1       | `P9_SW3:1`   |
| 1          | 2       | `P9_SW3:2`   |
| 1          | 3       | `P5_SW2`     |
| 1          | 4       | `P5_SW3:1`   |
| 1          | 5       | `P5_SW3:2`   |
| 1          | 6       | `P1_SW3:1`   |
| 1          | 7       | `P1_SW3:2`   |
| 1          | 8       |              |
| 2          | 1       |  `P3_SW2_0`  |
| 2          | 2       |  `P3_SW2_1`  |
| 2          | 3       |  `P6_SW2_0`  |
| 2          | 4       |  `P6_SW2_1`  |
| 2          | 5       |  `P6_SW2_2`  |
| 2          | 6       |              |
| 2          | 7       |              |
| 2          | 8       |              |


#### TM Board #2
All the inputs use the input line #1 (denoted `K1` in the datasheet)

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