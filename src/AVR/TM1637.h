/*----------------------------------------------------------------------------

                          *========================*
                          |                        |
                          | Project MissionBoard   |
                          |                        |
                          *========================*


 Authors: T. HILAIRE
 Licence: GPL v3

 File: TM1637.h
       low-level driver for the TM1637 chip
       - basic function to driver the TM1637 chip
       - used by the high-level driver (see TMx.c)


Copyright 2017-2018 T. Hilaire

----------------------------------------------------------------------------*/

#ifndef _TM1637_H_
#define _TM1637_H_

#include <avr/io.h>

#define BIT(x) (0x01 << (x))

/* Constants to define the Ports for DIO (Data IO) and the three CLK (Clock) (one per TM) */
#define TM1637_DIO_PORT      PORTB
#define TM1637_DIO_DDR       DDRB
#define TM1637_DIO_PINR      PINB
#define TM1637_DIO_PIN       0

#define TM1637_CLK_PORT      PORTD
#define TM1637_CLK_DDR       DDRD
#define TM1637_CLK_PIN0      0
#define TM1637_CLK_PIN1      1
#define TM1637_CLK_PIN2      2


/* intern bit manipulation macros */
/* check if they correspond to asm set_bit / clear_bit ? */
inline __attribute__((always_inline)) static void setTM1637_Clk( uint8_t mask) { TM1637_CLK_PORT |= mask; }
inline __attribute__((always_inline)) static void clearTM1637_Clk(uint8_t mask) { TM1637_CLK_PORT &= ~mask; }

inline __attribute__((always_inline)) static void setTM1637_Dio() { TM1637_DIO_PORT |= BIT(TM1637_DIO_PIN); }
inline __attribute__((always_inline)) static void clearTM1637_Dio() { TM1637_DIO_PORT &= ~BIT(TM1637_DIO_PIN); }
inline __attribute__((always_inline)) static void writeTM1637_Dio(uint8_t b) { b ? setTM1637_Dio() : clearTM1637_Dio(); }


/* some constants (cf manual)*/
#define READ_MODE 0x02
#define WRITE_MODE 0x00
#define INCR_ADDR 0x00
#define FIXED_ADDR 0x04


/* functions */
/*
void TM1637_setup(uint8_t brightness);
void TM1637_clearDisplay(uint8_t StbMask);
void TM1637_turnOff(uint8_t StbMask);
void TM1637_turnOn(uint8_t brightness, uint8_t StbMask);
void TM1637_sendCommand(uint8_t cmd, uint8_t StbMask);
void TM1637_sendData(uint8_t addr, uint8_t data, uint8_t StbMask);
void TM1637_setDataMode(uint8_t wr_mode, uint8_t addr_mode);
void TM1637_sendByte(uint8_t data);
*/

void TM1637_setup(uint8_t clkMask);
void TM1637_write(uint8_t first, uint8_t second, uint8_t third, uint8_t fourth, uint8_t clkMask);
void TM1637_start(uint8_t clkMask);
void TM1637_stop(uint8_t clkMask);
uint8_t TM1637_writeValue(uint8_t value, uint8_t ClkMask);

#endif