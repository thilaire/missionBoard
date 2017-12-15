/*
* Author: T. HILAIRE
*
* Licence: GPL v3
*/

#ifndef _TM163x_H_
#define _TM163x_H_

#define BIT(x) (0x01 << (x))

/* Constants to define the Ports for DIO (Data IO), CLK (Clock) and STBs (Enable pins) */
#define TMx8_DIO_PORT      PORTB
#define TMx8_DIO_DDR       DDRB
#define TMx8_DIO_PINR      PINB
#define TMx8_DIO_PIN       6

#define TMx8_CLK_PORT      PORTB
#define TMx8_CLK_DDR       DDRB
#define TMx8_CLK_PIN       7

#define TMx8_STB_PORT      PORTD
#define TMx8_STB_DDR       DDRD
#define TMx8_STB_MASK_PIN  0b11100000
#define TMx8_STB_PIN0      5
#define TMx8_STB_PIN1      6
#define TMx8_STB_PIN2      7


/* intern bit manipulation macros */
/* check if they correspond to asm set_bit / clear_bit ? */
inline __attribute__((always_inline)) static void setTMx8_Clk() { TMx8_CLK_PORT |= BIT(TMx8_CLK_PIN); }
inline __attribute__((always_inline)) static void clearTMx8_Clk() { TMx8_CLK_PORT &= ~BIT(TMx8_CLK_PIN); }
inline __attribute__((always_inline)) static void setTMx8_Dio() { TMx8_DIO_PORT |= BIT(TMx8_DIO_PIN); }
inline __attribute__((always_inline)) static void clearTMx8_Dio() { TMx8_DIO_PORT &= ~BIT(TMx8_DIO_PIN); }
inline __attribute__((always_inline)) static void writeTMx8_Dio(uint8_t b) { b ? setTMx8_Dio() : clearTMx8_Dio(); }
inline __attribute__((always_inline)) static void setTMx8_Dio_Input() { TMx8_DIO_DDR &= ~BIT(TMx8_DIO_PIN); }
inline __attribute__((always_inline)) static void setTMx8_Dio_Output() { TMx8_DIO_DDR |= BIT(TMx8_DIO_PIN); }
inline __attribute__((always_inline)) static void clearTMx8_Stb( uint8_t mask) { TMx8_STB_PORT &= ~mask; }
inline __attribute__((always_inline)) static void setTMx8_Stb() { TMx8_STB_PORT |= TMx8_STB_MASK_PIN ; }


/* some constants (cf manual)*/
#define READ_MODE 0x02
#define WRITE_MODE 0x00
#define INCR_ADDR 0x00
#define FIXED_ADDR 0x04


/* functions */
void TMx8_setup(uint8_t brightness);
void TMx8_clearDisplay(uint8_t StbMask);
void TMx8_turnOff(uint8_t StbMask);
void TMx8_turnOn(uint8_t brightness, uint8_t StbMask);
void TMx8_sendCommand(uint8_t cmd, uint8_t StbMask);
void TMx8_sendData(uint8_t addr, uint8_t data, uint8_t StbMask);
void TMx8_setDataMode(uint8_t wr_mode, uint8_t addr_mode);
void TMx8_sendByte(uint8_t data);
uint8_t TMx8_getByte();


#endif