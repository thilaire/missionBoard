/*----------------------------------------------------------------------------

                          *========================*
                          |                        |
                          | Project MissionBoard   |
                          |                        |
                          *========================*


 Authors: T. HILAIRE
 Licence: GPL v3

 File: TM1638.c
       low-level driver for the TM1638 chip
       - basic function to driver the TM1638 chip
       - used by the high-level driver (see TMx8.c)


Copyright 2017-2018 T. Hilaire

----------------------------------------------------------------------------*/

#ifndef _TM1638_H_
#define _TM1638_H_

#define BIT(x) (0x01 << (x))
/* TODO: use it everywhere in the code ? */

/* Constants to define the Ports for DIO (Data IO), CLK (Clock) and STBs (Enable pins) */
#define TM1638_DIO_PORT      PORTB
#define TM1638_DIO_DDR       DDRB
#define TM1638_DIO_PINR      PINB
#define TM1638_DIO_PIN       6

#define TM1638_CLK_PORT      PORTB
#define TM1638_CLK_DDR       DDRB
#define TM1638_CLK_PIN       7

#define TM1638_STB_PORT      PORTD
#define TM1638_STB_DDR       DDRD
#define TM1638_STB_MASK_PIN  0b11100000
#define TM1638_STB_PIN0      5
#define TM1638_STB_PIN1      6
#define TM1638_STB_PIN2      7


/* intern bit manipulation macros */
/* check if they correspond to asm set_bit / clear_bit ? */
inline __attribute__((always_inline)) static void setTM1638_Clk() { TM1638_CLK_PORT |= BIT(TM1638_CLK_PIN); }
inline __attribute__((always_inline)) static void clearTM1638_Clk() { TM1638_CLK_PORT &= ~BIT(TM1638_CLK_PIN); }
inline __attribute__((always_inline)) static void setTM1638_Dio() { TM1638_DIO_PORT |= BIT(TM1638_DIO_PIN); }
inline __attribute__((always_inline)) static void clearTM1638_Dio() { TM1638_DIO_PORT &= ~BIT(TM1638_DIO_PIN); }
inline __attribute__((always_inline)) static void writeTM1638_Dio(uint8_t b) { b ? setTM1638_Dio() : clearTM1638_Dio(); }
inline __attribute__((always_inline)) static void setTM1638_Dio_Input() { TM1638_DIO_DDR &= ~BIT(TM1638_DIO_PIN); }
inline __attribute__((always_inline)) static void setTM1638_Dio_Output() { TM1638_DIO_DDR |= BIT(TM1638_DIO_PIN); }
inline __attribute__((always_inline)) static void clearTM1638_Stb( uint8_t mask) { TM1638_STB_PORT &= ~mask; }
inline __attribute__((always_inline)) static void setTM1638_Stb() { TM1638_STB_PORT |= TM1638_STB_MASK_PIN ; }


/* some constants (cf manual)*/
#define READ_MODE 0x02
#define WRITE_MODE 0x00
#define INCR_ADDR 0x00
#define FIXED_ADDR 0x04


/* functions */
void TM1638_setup(uint8_t brightness);
void TM1638_clearDisplay(uint8_t StbMask);
void TM1638_turnOff(uint8_t StbMask);
void TM1638_turnOn(uint8_t brightness, uint8_t StbMask);
void TM1638_sendCommand(uint8_t cmd, uint8_t StbMask);
void TM1638_sendData(uint8_t addr, uint8_t data, uint8_t StbMask);
void TM1638_setDataMode(uint8_t wr_mode, uint8_t addr_mode);
void TM1638_sendByte(uint8_t data);
void TM1638_getData(uint8_t* data, uint8_t StbMask);
uint8_t TM1638_getByte();


#endif