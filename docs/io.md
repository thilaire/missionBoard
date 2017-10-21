# Input/Output

All the switches, LEDs, buttons are connected directly to the Raspberry Pi or through the [TM1638](TM1638.md) boards.

## Signal naming convention

The following tables regroup all the IO connectiviy. I have choose to name signals as following `xxx-yyyzz` where:
- `xxx` is the board name (or panel number), like `RPi`, `TM1` or `9`
- `yyy` is the function/signal/io name (like `GPIO12` or `LED`)
- `zz` is the number (may be empty if not necessary)


## Raspberry Pi

| RPi Pin number                | Name       | Connected to  |   | Connected to  | Name       | RPi Pin number                       |
|:------------------------------|:----------:|:-------------:|:-:|:-------------:|:----------:|-------------------------------------:|
| 01 (3.3v)                     |            |               |   |               |            | (5v) 02                              |
| 03 (**GPIO02**, SDA1, I2C)    | `RPi-IO2`  |               |   |               |            | (5v) 04                              |
| 05 (**GPIO03**, SCL1, I2C)    | `RPi-IO3`  |               |   |               |            | (GND) 06                             |
| 07 (**GPIO04**, GPIO_GCLK)    | `RPi-IO4`  |               |   |               | `RPi-IO14` | (TXD0, **GPIO14**) 08                |
| 09 (GND)                      |            |               |   |               | `RPi-IO15` | (RXD0, **GPIO15**) 10                |
| 11 (**GPIO17**, GPIO_GEN0)    | `RPi-IO17` |               |   |               | `RPi-IO18` | (GPIO_GEN1, **GPIO18**) 12           |
| 13 (**GPIO27**, GPIO_GEN2)    | `RPi-IO27` |               |   |               |            | (GND) 14                             |
| 15 (**GPIO22**, GPIO_GEN3)    | `RPi-IO22` |               |   |               | `RPi-IO23` | (GPIO_GEN4, **GPIO23**) 16           |
| 17 (3.3v)                     |            |               |   |               | `RPi-IO24` | (GPIO_GEN5, **GPIO24**) 18           |
| 19 (**GPIO10**, SPI_MOSI)     | `RPi-IO10` |               |   |               |            | (GND) 20                             |
| 21 (**GPIO09**, SPI_MISO)     | `RPi-IO9`  |               |   |               | `RPi-IO25` | (GPIO_GEN6, **GPIO25**) 22           |
| 23 (**GPIO11**, SPI_CLK)      | `RPi-IO11` |               |   |               | `RPi-IO8`  | (SPI_CE0_N, **GPIO08**) 24           |
| 25 (GND)                      |            |               |   |               | `RPi-IO7`  | (SPI_CE1_N, **GPIO07**) 26           |
| 27 (**ID_SD**, I2C ID EEPROM) |            |               |   |               |            | (I2C ID EEPROM, **ID_SC**) 28        |
| 29 (**GPIO05**)               | `RPi-IO5`  |               |   |               |            | (GND) 30                             |
| 31 (**GPIO06**)               | `RPi-IO6`  |               |   |               | `RPi-IO12` | (**GPIO12**) 32                      |
| 33 (**GPIO13**)               | `RPi-IO13` |               |   |               |            | (GND) 34                             |
| 35 (**GPIO19**)               | `RPi-IO19` |               |   |               | `RPi-IO16` | (**GPIO16**) 36                      |
| 37 (**GPIO26**)               | `RPi-IO26` |               |   | `TM-CLK`      | `RPi-IO20` | (**GPIO20**) 38                      |
| 39 (GND)                      |            |               |   | `TM-DIO`      | `RPi-IO21` | (**GPIO21**) 40                      |


*[Here](datasheet/RPi3-GPIO.png) is the official Raspberry GPIO table*

## TM1638 boards

The four TM1638s are chained (to save some GPIO), so it means they share the same clock and data I/O. Only the STB (Chip select) is different:
- the TM Board #1 is used for the IOs of the bottom panels (toggle switch buttons, leds and counter)
- TM Board #2 is used for
- TM Board #3 is used for
- TM Board #4 is used for


| Pin description   | Name      | Connected to |
|:------------------|:---------:|:------------:|
| STB (TM board #1) | `TM1-STB` | `RPi-IO19`   |
| STB (TM board #2) | `TM2-STB` |              |
| STB (TM board #3) | `TM3-STB` |              |
| STB (TM board #4) | `TM4-STB` |              |
| CLK (Clock input) | `TM-CLK`  | `RPi-IO20`   |
| DIO (Data I/O)    | `TM_DIO`  | `RPi-IO21`   |


### Outputs

| TM Board | Output   | Connected to |
|:--------:|:--------:|:------------:|
| #1       | `LED_7`  |              |
| #1       | `LED_8`  |              |



### Inputs

#### #1 TM Board
| Input Line | Input   | Connected to |
|:----------:|:-------:|:------------:|
| 1          | 1       |              |
| 1          | 2       |              |
| 1          | 3       |              |
| 1          | 4       |              |
| 1          | 5       |              |
| 1          | 6       |              |
| 1          | 7       |              |
| 1          | 8       |              |
| 2          | 1       |              |
| 2          | 2       |              |
| 2          | 3       |              |
| 2          | 4       |              |
| 2          | 5       |              |
| 2          | 6       |              |
| 2          | 7       |              |
| 2          | 8       |              |


#### #2 TM Board
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