/*
* Author: T. HILAIRE
*
* Licence: GPL v3
*/

#include <avr/io.h>
#include <util/delay.h>
#include "TM1638.h"



void TMx8_setup(uint8_t brightness)
{
	/* configure the pins (CLK, DIO and STBs are output) */
	TMx8_DIO_DDR |= (1U<<TMx8_DIO_PIN);
	TMx8_CLK_DDR |= (1U<<TMx8_CLK_PIN);
	TMx8_STB_DDR |= TMx8_STB_MASK_PIN;

	/* STBs and CLK high */
	setTMx8_Stb();
	setTMx8_Clk();

	/* set brightness and clear the displays */
	TMx8_turnOn(brightness, TMx8_STB_MASK_PIN);
	TMx8_clearDisplay(TMx8_STB_MASK_PIN);
}


/* Turn off every led / display
- StbMask: bitmask indicating which TM is concerned
*/
void TMx8_clearDisplay(uint8_t StbMask)
{
	clearTMx8_Stb(StbMask);
	/* set data read mode (automatic address increased) */
	TMx8_setDataMode(WRITE_MODE, INCR_ADDR);
	TMx8_sendByte(0xC0);   /* address command set to the 1st address */
	for(uint8_t i=0; i<16; i++)
		TMx8_sendByte(0x00);   /* set to zero all the addresses */

	setTMx8_Stb();
}


/* Turn off (physically) the leds */
void TMx8_turnOff(uint8_t StbMask)
{
		TMx8_sendCommand(0x80, StbMask);
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
void TMx8_turnOn(uint8_t brightness, uint8_t StbMask)
{
	TMx8_sendCommand(0x88 | (brightness & 7), StbMask);
}




/*===============================
  Communication with the TM163x
=================================*/
/* 		Send a command
- cmd: cmd to send
- StbMask: bitmask indicating which TM is concerned
*/
void TMx8_sendCommand(uint8_t cmd, uint8_t StbMask)
{
		clearTMx8_Stb(StbMask); /* enable the corresponding TM (for receiving data) */
		TMx8_sendByte(cmd);     /* send the byte */
		setTMx8_Stb();          /* disable all the TM */
}


/* Send a data at address addr
- addr: adress of the data
- data: value of the data
- StbMask: bitmask indicating which TM is concerned
*/
void TMx8_sendData(uint8_t addr, uint8_t data, uint8_t StbMask)
{
	/* set mode */
	clearTMx8_Stb(StbMask);
	TMx8_setDataMode(WRITE_MODE, FIXED_ADDR);
	setTMx8_Stb();
	/* set address and send byte (stb must go high and low before sending address) */
	clearTMx8_Stb(StbMask);
	TMx8_sendByte(0xC0 | addr);
	TMx8_sendByte(data);
	setTMx8_Stb();
}


/* Get the data (buttons) of the TM
- StbMask: bitmask indicating which TM is concerned
- data: array to fill
Fills the four octets read
*/
void getData(uint8_t* data, uint8_t StbMask)
{
	/* set in read mode */
	clearTMx8_Stb(StbMask);
	TMx8_setDataMode(READ_MODE, INCR_ADDR);
	_delay_us(20);  /* wait at least 10µs ? */
	/* read four bytes */
	for(uint8_t i=0; i<4; i++)
		*data++ = TMx8_getByte();
	setTMx8_Stb();
}


/* Set the data modes
- wr_mode: READ_MODE (read the key scan) or WRITE_MODE (write data)
- addr_mode: INCR_ADDR (automatic address increased) or FIXED_ADDR
*/
void TMx8_setDataMode(uint8_t wr_mode, uint8_t addr_mode)
{
	TMx8_sendByte(0x40 | wr_mode | addr_mode);
}

/* Send a byte using bit-bang (Stb must be Low)
- data: a byte to send
*/
void TMx8_sendByte(uint8_t data)
{
	for( uint8_t i=0; i<8; i++)
	{
		clearTMx8_Clk();
		writeTMx8_Dio((data & 1));
		data >>= 1;
		setTMx8_Clk();
	}
}


/* Receive a byte (from the TM previously configured)
Returns the byte received
*/
uint8_t TMx8_getByte()
{
	/* configure DIO in input with pull-up */
	TMx8_DIO_DDR &= ~(1U<<TMx8_DIO_PIN);
	TMx8_DIO_PORT |= (1U<<TMx8_DIO_PIN);
	/* read 8 bits */
	uint8_t temp = 0;
	for( uint8_t i=0; i<8; i++)
	{
		temp >>= 1;
		clearTMx8_Clk();
		if (TMx8_DIO_PINR & (1U<<TMx8_DIO_PIN))
			temp |= 0x80;
		setTMx8_Clk();
	}
	/* put back DIO in output mode */
	TMx8_DIO_DDR |= (1U<<TMx8_DIO_PIN);
	return temp;
}

