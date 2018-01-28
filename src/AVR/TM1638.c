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

#include <avr/io.h>
#include <util/delay.h>
#include "TM1638.h"



void TM1638_setup(uint8_t brightness)
{
	/* configure the pins (CLK, DIO and STBs are output) */
	TM1638_DIO_DDR |= (1U<<TM1638_DIO_PIN);
	TM1638_CLK_DDR |= (1U<<TM1638_CLK_PIN);
	TM1638_STB_DDR |= TM1638_STB_MASK_PIN;

	/* STBs and CLK high */
	setTM1638_Stb();
	setTM1638_Clk();

	/* set brightness and clear all the displays */
	TM1638_turnOn(brightness, TM1638_STB_MASK_PIN);
	TM1638_clearDisplay(TM1638_STB_MASK_PIN);
}


/* Turn off every led / display
- StbMask: bitmask indicating which TM is concerned
*/
void TM1638_clearDisplay(uint8_t StbMask)
{
	clearTM1638_Stb(StbMask);
	/* set data read mode (automatic address increased) */
	TM1638_setDataMode(WRITE_MODE, INCR_ADDR);
	TM1638_sendByte(0xC0);   /* address command set to the 1st address */
	for(uint8_t i=0; i<16; i++)
		TM1638_sendByte(0x00);   /* set to zero all the addresses */

	setTM1638_Stb();
}


/* Turn off (physically) the leds */
void TM1638_turnOff(uint8_t StbMask)
{
		TM1638_sendCommand(0x80, StbMask);
}


/* Turn on the display and set the brightness
The pulse width used is set to:
0 => 1/16       4 => 11/16
1 => 2/16       5 => 12/16
2 => 4/16       6 => 13/16
3 => 10/16      7 => 14/16
- brightness: between 0 and 7
- StbMask: bitmask indicating which TM is concerned
*/
void TM1638_turnOn(uint8_t brightness, uint8_t StbMask)
{
	TM1638_sendCommand(0x88 | (brightness & 7), StbMask);
}




/*===============================
  Communication with the TM163x
=================================*/
/* 		Send a command
- cmd: cmd to send
- StbMask: bitmask indicating which TM is concerned
*/
void TM1638_sendCommand(uint8_t cmd, uint8_t StbMask)
{
		clearTM1638_Stb(StbMask); /* enable the corresponding TM (for receiving data) */
		TM1638_sendByte(cmd);     /* send the byte */
		setTM1638_Stb();          /* disable all the TM */
}


/* Send a data at address addr
- addr: adress of the data
- data: value of the data
- StbMask: bitmask indicating which TM is concerned
*/
void TM1638_sendData(uint8_t addr, uint8_t data, uint8_t StbMask)
{
	/* set mode */
	clearTM1638_Stb(StbMask);
	TM1638_setDataMode(WRITE_MODE, FIXED_ADDR);
	setTM1638_Stb();
	/* set address and send byte (stb must go high and low before sending address) */
	clearTM1638_Stb(StbMask);
	TM1638_sendByte(0xC0 | addr);
	TM1638_sendByte(data);
	setTM1638_Stb();
}


/* Get the data (buttons) of the TM
- StbMask: bitmask indicating which TM is concerned
- data: array to fill
Fills the four octets read
*/
void TM1638_getData(uint8_t* data, uint8_t StbMask)
{
	/* set in read mode */
	clearTM1638_Stb(StbMask);
	TM1638_setDataMode(READ_MODE, INCR_ADDR);
	_delay_us(20);  /* wait at least 10µs ? */
	/* read four bytes */
	for(uint8_t i=0; i<4; i++)
		*data++ = TM1638_getByte();
	setTM1638_Stb();
}


/* Set the data modes
- wr_mode: READ_MODE (read the key scan) or WRITE_MODE (write data)
- addr_mode: INCR_ADDR (automatic address increased) or FIXED_ADDR
*/
void TM1638_setDataMode(uint8_t wr_mode, uint8_t addr_mode)
{
	TM1638_sendByte(0x40 | wr_mode | addr_mode);
}

/* Send a byte using bit-bang (Stb must be Low)
- data: a byte to send
*/
void TM1638_sendByte(uint8_t data)
{
	for( uint8_t i=0; i<8; i++)
	{
		clearTM1638_Clk();
		writeTM1638_Dio((data & 1));
		data >>= 1;
		setTM1638_Clk();
	}
}


/* Receive a byte (from the TM previously configured)
Returns the byte received
*/
uint8_t TM1638_getByte()
{
	/* configure DIO in input with pull-up */
	TM1638_DIO_DDR &= ~(1U<<TM1638_DIO_PIN);
	TM1638_DIO_PORT |= (1U<<TM1638_DIO_PIN);
	/* read 8 bits */
	uint8_t temp = 0;
	for( uint8_t i=0; i<8; i++)
	{
		temp >>= 1;
		clearTM1638_Clk();
		if (TM1638_DIO_PINR & (1U<<TM1638_DIO_PIN))
			temp |= 0x80;
		setTM1638_Clk();
	}
	/* put back DIO in output mode */
	TM1638_DIO_DDR |= (1U<<TM1638_DIO_PIN);
	return temp;
}

